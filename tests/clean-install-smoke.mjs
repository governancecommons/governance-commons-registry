import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const fixtures = join(dirname(fileURLToPath(import.meta.url)), "fixtures");
const command = process.platform === "win32" ? "gc-validate.cmd" : "gc-validate";

function windowsQuote(value) {
  return `"${value.replaceAll('"', '""')}"`;
}

function expect(code, args) {
  const result = process.platform === "win32"
    ? spawnSync(process.env.ComSpec || "cmd.exe", ["/d", "/s", "/c", [command, ...args.map(windowsQuote)].join(" ")], { encoding: "utf8" })
    : spawnSync(command, args, { encoding: "utf8", shell: false });
  if (result.error) throw result.error;
  if (result.status !== code) {
    throw new Error(`expected exit ${code}, got ${result.status}\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`);
  }
}

expect(0, ["--spec", "ons", "--output", "json", join(fixtures, "valid checks ünicode.json")]);
expect(1, ["--spec", "ons", join(fixtures, "invalid checks ünicode.json")]);
expect(2, ["--spec", "ons", join(fixtures, "missing file.json")]);
