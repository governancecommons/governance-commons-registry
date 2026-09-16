import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const validate = join(root, "dist", "esm", "gc-validate.js");
const report = join(root, "dist", "esm", "gc-report.js");

function runNode(script, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [script, ...args], { cwd: root, encoding: "utf8" });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

const temp = await mkdtemp(join(tmpdir(), "gc-sdk-02-cli-"));
const valid = join(temp, "valid.json");
const invalid = join(temp, "invalid.json");
const malformed = join(temp, "malformed.json");
const savedReport = join(temp, "report.json");
const badReport = join(temp, "bad-report.json");

await writeFile(valid, JSON.stringify({ checks: [{ domain: "python_identifier", name: "run_intent" }] }));
await writeFile(invalid, JSON.stringify({ checks: [{ domain: "python_identifier", name: "RunIntent" }] }));
await writeFile(malformed, JSON.stringify({ not_checks: [] }));

const pass = await runNode(validate, ["--spec", "ons", "--output", "json", valid]);
assert.equal(pass.code, 0);
const passReport = JSON.parse(pass.stdout);
assert.equal(passReport.gc_report_version, "1.0.0");
assert.equal(passReport.conformant, true);
assert.equal(passReport.summary.passed, 1);
assert.equal(passReport.summary.failed, 0);

const fail = await runNode(validate, ["--spec", "ons", "--output", "json", invalid]);
assert.equal(fail.code, 1);
const failReport = JSON.parse(fail.stdout);
assert.equal(failReport.conformant, false);
assert.equal(failReport.conformance_level, "none");
assert.equal(failReport.summary.failed, 1);

const text = await runNode(validate, ["--spec", "ons", "--output", "text", valid]);
assert.equal(text.code, 0);
assert.match(text.stdout, /GC Conformance Report/);
assert.match(text.stdout, /ONS-CASING-001/);
assert.match(text.stdout, /Summary: 1 passed, 0 failed, 0 skipped of 1 total/);

const malformedResult = await runNode(validate, ["--spec", "ons", malformed]);
assert.equal(malformedResult.code, 2);
assert.match(malformedResult.stderr, /top-level 'checks' array/);

await writeFile(savedReport, pass.stdout);
const reportJson = await runNode(report, ["--output", "json", savedReport]);
assert.equal(reportJson.code, 0);
assert.deepEqual(JSON.parse(reportJson.stdout), passReport);

const reportText = await runNode(report, ["--output", "text", savedReport]);
assert.equal(reportText.code, 0);
assert.match(reportText.stdout, /GC Conformance Report/);
assert.match(reportText.stdout, /Result:  PASS/);

const nonconformantReport = join(temp, "nonconformant.json");
await writeFile(nonconformantReport, fail.stdout);
const reportFail = await runNode(report, ["--output", "json", nonconformantReport]);
assert.equal(reportFail.code, 1);
assert.equal(JSON.parse(reportFail.stdout).conformant, false);

await writeFile(badReport, JSON.stringify({ ...passReport, gc_report_version: "9.9.9" }));
const unsupported = await runNode(report, ["--output", "json", badReport]);
assert.equal(unsupported.code, 2);
assert.match(unsupported.stderr, /report version '9\.9\.9' is not supported/);

console.log("GC-SDK.02 CLI acceptance OK");
