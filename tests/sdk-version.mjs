import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const packageJson = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));
const lockJson = JSON.parse(readFileSync(join(root, "package-lock.json"), "utf8"));
const ons = await import(join(root, "dist/esm/ons.js"));

const expected = "0.2.0";
if (packageJson.version !== expected) throw new Error(`package.json version is ${packageJson.version}, expected ${expected}`);
if (lockJson.version !== expected) throw new Error(`package-lock.json version is ${lockJson.version}, expected ${expected}`);
if (lockJson.packages?.[""]?.version !== expected) throw new Error(`lockfile root version is ${lockJson.packages?.[""]?.version}, expected ${expected}`);
if (ons.PACKAGE_VERSION !== expected) throw new Error(`TypeScript PACKAGE_VERSION is ${ons.PACKAGE_VERSION}, expected ${expected}`);
if (ons.ONS_SPEC_VERSION !== "1.4.0") throw new Error(`ONS spec version changed unexpectedly: ${ons.ONS_SPEC_VERSION}`);

console.log(`SDK version metadata OK: ${expected}`);
