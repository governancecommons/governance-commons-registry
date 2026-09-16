/** Specification/package compatibility policy for the Governance Commons SDK. */

export type CompatibilityStatus = "supported" | "compatible" | "unsupported" | "invalid";

export interface CompatibilityResult {
  readonly spec: string;
  readonly requested_version: string;
  readonly current_version: string;
  readonly minimum_compatible_version: string;
  readonly status: CompatibilityStatus;
  readonly message: string;
}

type ParsedVersion = { major: number; minor: number; patch: number };

const VERSION_PATTERN = /^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))?(?:[-+][0-9A-Za-z.-]+)?$/;

function parseVersion(value: string): ParsedVersion | null {
  const match = VERSION_PATTERN.exec(value);
  if (match === null) return null;
  return { major: Number(match[1]), minor: Number(match[2]), patch: Number(match[3] ?? 0) };
}

function compare(a: ParsedVersion, b: ParsedVersion): number {
  return a.major - b.major || a.minor - b.minor || a.patch - b.patch;
}

export function checkSpecCompatibility(
  spec: string,
  requestedVersion: string,
  options: { current_version: string; minimum_compatible_version?: string },
): CompatibilityResult {
  const current = parseVersion(options.current_version);
  const minimum = parseVersion(options.minimum_compatible_version ?? options.current_version);
  const requested = parseVersion(requestedVersion);
  const minimumText = options.minimum_compatible_version ?? options.current_version;
  if (current === null || minimum === null) throw new Error("current_version and minimum_compatible_version must be valid versions");
  if (requested === null) return { spec, requested_version: requestedVersion, current_version: options.current_version, minimum_compatible_version: minimumText, status: "invalid", message: "specification version is not a valid GC version" };
  if (compare(requested, current) === 0) return { spec, requested_version: requestedVersion, current_version: options.current_version, minimum_compatible_version: minimumText, status: "supported", message: "requested specification version is exactly supported" };
  if (requested.major === current.major && compare(requested, minimum) >= 0 && compare(requested, current) < 0) return { spec, requested_version: requestedVersion, current_version: options.current_version, minimum_compatible_version: minimumText, status: "compatible", message: "requested older specification version is within the explicitly declared compatibility range" };
  return { spec, requested_version: requestedVersion, current_version: options.current_version, minimum_compatible_version: minimumText, status: "unsupported", message: "requested specification version is outside the explicitly supported compatibility range" };
}

export const SPEC_POLICIES: Readonly<Record<string, readonly [string, string]>> = {
  ons: ["1.4.0", "1.4.0"],
  "agent-dossier": ["1.4.0", "1.4.0"],
  "governance-record": ["1.0.0", "1.0.0"],
  capabilities: ["0.1", "0.1"],
};

export function checkRegisteredSpecCompatibility(spec: string, requestedVersion: string): CompatibilityResult {
  const policy = SPEC_POLICIES[spec];
  if (policy === undefined) return { spec, requested_version: requestedVersion, current_version: "", minimum_compatible_version: "", status: "unsupported", message: "specification is not registered by this SDK" };
  return checkSpecCompatibility(spec, requestedVersion, { current_version: policy[0], minimum_compatible_version: policy[1] });
}
