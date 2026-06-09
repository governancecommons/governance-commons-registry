#!/usr/bin/env node
/// <reference types="node" />
/**
 * gc-report — display a saved GC conformance report.
 *
 * Usage: gc-report [--output text|json] <report-file>
 */

import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { GC_REPORT_VERSION, type ConformanceReport } from "./report.js";
import { printText } from "./cli-util.js";

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    output: { type: "string", default: "text" },
  },
  allowPositionals: true,
});

const output = values.output ?? "text";
const reportFile = positionals[0];

if (!["text", "json"].includes(output)) {
  console.error("gc-report: --output must be text or json");
  process.exit(2);
}
if (!reportFile) {
  console.error("gc-report: report file path is required");
  process.exit(2);
}

let data: unknown;
try {
  data = JSON.parse(readFileSync(reportFile, "utf-8"));
} catch (err) {
  console.error(`gc-report: cannot read ${reportFile}: ${(err as Error).message}`);
  process.exit(2);
}

const d = data as Record<string, unknown>;
if (
  typeof d["gc_report_version"] !== "string" ||
  typeof d["spec"] !== "string" ||
  typeof d["conformant"] !== "boolean"
) {
  console.error(`gc-report: ${reportFile} does not appear to be a valid GC conformance report`);
  process.exit(2);
}

if (d["gc_report_version"] !== GC_REPORT_VERSION) {
  console.error(
    `gc-report: report version '${d["gc_report_version"]}' is not supported by this tool (expected '${GC_REPORT_VERSION}')`
  );
  process.exit(2);
}

const report = data as ConformanceReport;

if (output === "json") {
  console.log(JSON.stringify(report, null, 2));
} else {
  printText(report);
}

process.exit(report.conformant ? 0 : 1);
