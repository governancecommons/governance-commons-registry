/** GC-SDK.05 TypeScript compatibility API smoke test. */
import { checkRegisteredSpecCompatibility, checkSpecCompatibility } from "../src/versioning.js";

const current = checkRegisteredSpecCompatibility("ons", "1.4.0");
if (current.status !== "supported") throw new Error("current ONS version must be supported");

const older = checkSpecCompatibility("example", "1.2.0", {
  current_version: "1.4.0",
  minimum_compatible_version: "1.2.0",
});
if (older.status !== "compatible") throw new Error("explicitly ranged older version must be compatible");

const future = checkRegisteredSpecCompatibility("ons", "2.0.0");
if (future.status !== "unsupported") throw new Error("future major version must be unsupported");

const invalid = checkRegisteredSpecCompatibility("ons", "1.x.0");
if (invalid.status !== "invalid") throw new Error("malformed version must be invalid");
