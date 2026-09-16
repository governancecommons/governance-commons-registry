/**
 * ONS (Ontic Namespace Structure) — TypeScript reference implementation.
 *
 * Validates names against the casing rules, separator grammar, governance ID grammar,
 * and cluster registration protocol defined in ONS v1.4.0.
 *
 * This module has zero runtime dependencies. All patterns are derived directly from
 * the canonical ONS specification (ons/ons.yaml) and are versioned with this package.
 *
 * @see https://governancecommons.org/ons
 * @spec ONS v1.4.0
 */

// ---------------------------------------------------------------------------
// Separator grammar
// ---------------------------------------------------------------------------

export type SeparatorToken = "." | "-" | "_" | ":";
export type SeparatorSemantic = "hierarchy" | "compound" | "lexical_binding" | "qualification";

export interface SeparatorRule {
  readonly token: SeparatorToken;
  readonly name: "dot" | "hyphen" | "underscore" | "colon";
  readonly semantic: SeparatorSemantic;
  readonly meaning: string;
}

export const SEPARATORS: readonly SeparatorRule[] = [
  { token: ".", name: "dot", semantic: "hierarchy", meaning: "Scope depth or namespace nesting." },
  { token: "-", name: "hyphen", semantic: "compound", meaning: "Human-readable word or segment joining." },
  { token: "_", name: "underscore", semantic: "lexical_binding", meaning: "Words bound inside a language identifier." },
  { token: ":", name: "colon", semantic: "qualification", meaning: "Attribute qualification, level, or key-value boundary." },
] as const;

// ---------------------------------------------------------------------------
// Casing rules
// ---------------------------------------------------------------------------

export type CasingDomain =
  | "python_identifier" | "python_class" | "python_constant" | "css_custom_property"
  | "governance_id" | "governance_cluster" | "python_filename" | "governance_filename"
  | "ts_js_filename" | "directory_name" | "qualification_authority" | "qualification_metadata";

export interface CasingRule {
  readonly domain: CasingDomain;
  readonly rule: string;
  readonly pattern: RegExp;
  readonly description: string;
}

export const CASING_RULES: readonly CasingRule[] = [
  { domain: "python_identifier", rule: "snake_case", pattern: /^[a-z_][a-z0-9_]*$/, description: "Lowercase, underscore-separated Python identifiers." },
  { domain: "python_class", rule: "PascalCase", pattern: /^[A-Z][A-Za-z0-9]*$/, description: "PascalCase Python class names." },
  { domain: "python_constant", rule: "UPPER_SNAKE", pattern: /^[A-Z][A-Z0-9_]*$/, description: "UPPER_SNAKE_CASE Python constants." },
  { domain: "css_custom_property", rule: "--root-kebab", pattern: /^--[a-z][a-z0-9]*(?:-[a-z0-9]+)+$/, description: "CSS custom properties prefixed with -- in kebab-case." },
  { domain: "governance_id", rule: "UPPER.decimal", pattern: /^[A-Z]{2,6}\.[0-9]{2}$/, description: "Governance record IDs: CLUSTER.SEQ (e.g. ONS.00)." },
  { domain: "governance_cluster", rule: "UPPER", pattern: /^[A-Z]{2,6}$/, description: "Registered uppercase cluster identifiers (2–6 chars)." },
  { domain: "python_filename", rule: "snake_case.py", pattern: /^[a-z][a-z0-9_]*\.py$/, description: "snake_case Python filenames ending in .py." },
  { domain: "governance_filename", rule: "UPPER.decimal.md", pattern: /^[A-Z]{2,6}\.[0-9]{2}\.md$/, description: "Governance document filenames: CLUSTER.SEQ.md." },
  { domain: "ts_js_filename", rule: "kebab-case", pattern: /^[a-z0-9][a-z0-9-]*\.(?:ts|js)$/, description: "kebab-case TypeScript and JavaScript filenames." },
  { domain: "directory_name", rule: "lowercase-kebab", pattern: /^[a-z0-9][a-z0-9-]*$/, description: "Lowercase kebab-case directory names." },
  { domain: "qualification_authority", rule: "UPPER:integer", pattern: /^[A-Z]{1,6}:[0-9]+$/, description: "Authority level qualifications (e.g. AL:2)." },
  { domain: "qualification_metadata", rule: "lower:lower", pattern: /^[a-z][a-z0-9.]*:[a-z0-9._-]+$/, description: "Metadata key-value qualifications (e.g. env:production)." },
] as const;

const CLUSTER_PATTERN = /^[A-Z]{2,6}$/;
const SEQ_PATTERN = /^[0-9]{2}$/;
const GOVERNANCE_ID_PATTERN = /^[A-Z]{2,6}\.[0-9]{2}$/;

export interface ValidationResult { readonly valid: boolean; readonly violation?: string; }
export interface GovernanceIdResult { readonly valid: boolean; readonly cluster?: string; readonly seq?: string; readonly violation?: string; }

export function validateName(domain: CasingDomain, name: string): ValidationResult {
  const rule = CASING_RULES.find((r) => r.domain === domain);
  if (rule === undefined) return { valid: false, violation: `Unknown casing domain: "${domain}".` };
  if (rule.pattern.test(name)) return { valid: true };
  return { valid: false, violation: `"${name}" does not conform to ONS domain "${domain}" (rule: ${rule.rule}, pattern: ${rule.pattern.source}).` };
}

export function parseGovernanceId(id: string): GovernanceIdResult {
  if (!GOVERNANCE_ID_PATTERN.test(id)) {
    const dotIdx = id.indexOf(".");
    if (dotIdx === -1) return { valid: false, violation: `"${id}" is missing the dot separator. Expected format: CLUSTER.SEQ (e.g. ONS.00).` };
    const cluster = id.slice(0, dotIdx);
    const seq = id.slice(dotIdx + 1);
    if (!CLUSTER_PATTERN.test(cluster)) return { valid: false, violation: `Cluster "${cluster}" must be 2–6 uppercase ASCII letters (pattern: ${CLUSTER_PATTERN.source}).` };
    if (!SEQ_PATTERN.test(seq)) return { valid: false, violation: `Sequence "${seq}" must be a zero-padded two-digit integer (pattern: ${SEQ_PATTERN.source}).` };
    return { valid: false, violation: `"${id}" does not match the governance ID pattern ${GOVERNANCE_ID_PATTERN.source}.` };
  }
  const dotIdx = id.indexOf(".");
  return { valid: true, cluster: id.slice(0, dotIdx), seq: id.slice(dotIdx + 1) };
}

export function validateCluster(cluster: string): ValidationResult {
  if (CLUSTER_PATTERN.test(cluster)) return { valid: true };
  return { valid: false, violation: `"${cluster}" is not a valid cluster name. Expected 2–6 uppercase ASCII letters (pattern: ${CLUSTER_PATTERN.source}).` };
}

export function detectSeparator(name: string): SeparatorSemantic | null {
  for (const sep of SEPARATORS) if (name.includes(sep.token)) return sep.semantic;
  return null;
}

export function detectSeparators(name: string): Array<{ token: SeparatorToken; semantic: SeparatorSemantic }> {
  return SEPARATORS.filter((sep) => name.includes(sep.token)).map((sep) => ({ token: sep.token, semantic: sep.semantic }));
}

export function getCasingRule(domain: CasingDomain): CasingRule | undefined {
  return CASING_RULES.find((r) => r.domain === domain);
}

export function listDomains(): readonly CasingDomain[] { return CASING_RULES.map((r) => r.domain); }

export const ONS_SPEC_VERSION = "1.4.0" as const;
export const PACKAGE_VERSION = "0.2.0" as const;
