import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const fixtures = join(dirname(fileURLToPath(import.meta.url)), "fixtures");
let command = "gc-validate";
let commandPrefix = [];

if (process.platform === "win32") {
  const shim = spawnSync("where.exe", ["gc-validate.cmd"], { encoding: "utf8" });
  if (shim.status !== 0) throw new Error("global install did not create gc-validate.cmd");
  const npmRoot = spawnSync(process.env.ComSpec || "cmd.exe", ["/d", "/c", "npm root -g"], { encoding: "utf8" });
  if (npmRoot.status !== 0) throw new Error(`cannot resolve npm global root: ${npmRoot.stderr}`);
  command = process.execPath;
  commandPrefix = [join(npmRoot.stdout.trim(), "governance-commons", "dist", "esm", "gc-validate.js")];
}

function expect(code, args) {
  const result = spawnSync(command, [...commandPrefix, ...args], { encoding: "utf8", shell: false });
  if (result.error) throw result.error;
  if (result.status !== code) {
    throw new Error(`expected exit ${code}, got ${result.status}\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`);
  }
}

expect(0, ["--spec", "ons", "--output", "json", join(fixtures, "valid checks ünicode.json")]);
expect(1, ["--spec", "ons", join(fixtures, "invalid checks ünicode.json")]);
expect(2, ["--spec", "ons", join(fixtures, "missing file.json")]);
