/**
 * Conformance report types — GC-2-C-01.
 *
 * Defines the machine-readable output contract for all Governance Commons validators.
 * Every validator MUST produce a ConformanceReport whose serialised form validates against:
 *   docs/conformance/conformance-report.schema.json  (gc_report_version: "1.0.0")
 */

/** Version of the GC conformance report format schema. */
export const GC_REPORT_VERSION = "1.0.0" as const;

/** Conformance profile evaluated by the validator. */
export type ConformanceProfile = "advisory" | "standard" | "strict";

/** Outcome of evaluating a single rule. */
export type RuleOutcome = "pass" | "fail" | "skip";

/** Highest conformance level achieved by the subject. */
export type ConformanceLevel = "none" | "advisory" | "standard" | "strict";

/** Per-rule evaluation result. */
export interface RuleResult {
  readonly rule_id: string;
  readonly description: string;
  readonly result: RuleOutcome;
  readonly message?: string | null;
}

/** Aggregate counts across all rule results. */
export interface ReportSummary {
  readonly total: number;
  readonly passed: number;
  readonly failed: number;
  readonly skipped: number;
}

/** Machine-readable conformance report. Serialises to the GC conformance report schema v1.0.0. */
export interface ConformanceReport {
  readonly gc_report_version: typeof GC_REPORT_VERSION;
  readonly spec: string;
  readonly spec_version: string;
  readonly profile: ConformanceProfile;
  readonly subject: string;
  readonly generated_at: string;
  readonly rules: readonly RuleResult[];
  readonly summary: ReportSummary;
  readonly conformant: boolean;
  readonly conformance_level: ConformanceLevel;
}

/** Options for {@link buildReport}. */
export interface BuildReportOptions {
  readonly spec: string;
  readonly spec_version: string;
  readonly profile: ConformanceProfile;
  readonly subject: string;
  readonly rules: readonly RuleResult[];
  /** ISO 8601 UTC timestamp; defaults to `new Date().toISOString()`. */
  readonly generated_at?: string;
}

/**
 * Construct a ConformanceReport from a list of RuleResults.
 *
 * Computes summary counts, conformant flag, and conformance_level automatically.
 *
 * @example
 * const report = buildReport({
 *   spec: "ons",
 *   spec_version: "1.4.0",
 *   profile: "standard",
 *   subject: "my-file.yaml",
 *   rules: [{ rule_id: "ONS-CASING-001", description: "snake_case identifiers", result: "pass" }],
 * });
 */
export function buildReport(options: BuildReportOptions): ConformanceReport {
  const { spec, spec_version, profile, subject, rules } = options;
  const generated_at = options.generated_at ?? new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

  const passed = rules.filter((r) => r.result === "pass").length;
  const failed = rules.filter((r) => r.result === "fail").length;
  const skipped = rules.filter((r) => r.result === "skip").length;
  const conformant = failed === 0;
  const conformance_level: ConformanceLevel = conformant ? profile : "none";

  return {
    gc_report_version: GC_REPORT_VERSION,
    spec,
    spec_version,
    profile,
    subject,
    generated_at,
    rules,
    summary: { total: passed + failed + skipped, passed, failed, skipped },
    conformant,
    conformance_level,
  };
}
