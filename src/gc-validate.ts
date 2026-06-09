#!/usr/bin/env node
/// <reference types="node" />
/**
 * gc-validate — validate a subject against a Governance Commons spec.
 *
 * Usage: gc-validate --spec ons [--profile standard] [--output text|json] <subject>
 *
 * The subject must be a JSON checks manifest:
 *   { "checks": [{ "domain": "<ons-domain>", "name": "<value>" }, ...] }
 */

import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { ONS_SPEC_VERSION, validateName } from "./ons.js";
import { buildReport, type ConformanceProfile, type RuleResult } from "./report.js";
import { printText } from "./cli-util.js";

const ONS_RULE_IDS: Record<string, [string, string]> = {
  python_identifier:       ["ONS-CASING-001", "Python identifiers must be snake_case"],
  python_class:            ["ONS-CASING-002", "Python class names must be PascalCase"],
  python_constant:         ["ONS-CASING-003", "Python constants must be UPPER_SNAKE_CASE"],
  css_custom_property:     ["ONS-CASING-004", "CSS custom properties must be --root-kebab"],
  governance_id:           ["ONS-CASING-005", "Governance IDs must be CLUSTER.SEQ (e.g. ONS.00)"],
  governance_cluster:      ["ONS-CASING-006", "Cluster names must be 2–6 uppercase ASCII letters"],
  python_filename:         ["ONS-CASING-007", "Python filenames must be snake_case.py"],
  governance_filename:     ["ONS-CASING-008", "Governance filenames must be CLUSTER.SEQ.md"],
  ts_js_filename:          ["ONS-CASING-009", "TypeScript/JS filenames must be kebab-case"],
  directory_name:          ["ONS-CASING-010", "Directory names must be lowercase-kebab"],
  qualification_authority: ["ONS-CASING-011", "Authority qualifications must be UPPER:integer (e.g. AL:2)"],
  qualification_metadata:  ["ONS-CASING-012", "Metadata qualifications must be lower:lower (e.g. env:production)"],
};

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    spec:    { type: "string" },
    profile: { type: "string", default: "standard" },
    output:  { type: "string", default: "text" },
  },
  allowPositionals: true,
});

const spec = values.spec;
const profile = (values.profile ?? "standard") as ConformanceProfile;
const output = values.output ?? "text";
const subject = positionals[0];

if (!spec || !["ons"].includes(spec)) {
  console.error("gc-validate: --spec is required and must be one of: ons");
  process.exit(2);
}
if (!["advisory", "standard", "strict"].includes(profile)) {
  console.error("gc-validate: --profile must be advisory, standard, or strict");
  process.exit(2);
}
if (!["text", "json"].includes(output)) {
  console.error("gc-validate: --output must be text or json");
  process.exit(2);
}
if (!subject) {
  console.error("gc-validate: subject file path is required");
  process.exit(2);
}

let data: unknown;
try {
  data = JSON.parse(readFileSync(subject, "utf-8"));
} catch (err) {
  console.error(`gc-validate: cannot read ${subject}: ${(err as Error).message}`);
  process.exit(2);
}

if (
  typeof data !== "object" || data === null ||
  !Array.isArray((data as Record<string, unknown>)["checks"])
) {
  console.error(`gc-validate: ${subject} must contain a top-level 'checks' array`);
  process.exit(2);
}

const checks = (data as { checks: unknown[] }).checks;
const rules: RuleResult[] = [];

for (let i = 0; i < checks.length; i++) {
  const check = checks[i];
  if (
    typeof check !== "object" || check === null ||
    typeof (check as Record<string, unknown>)["domain"] !== "string" ||
    typeof (check as Record<string, unknown>)["name"] !== "string"
  ) {
    console.error(`gc-validate: checks[${i}] must have string 'domain' and 'name' fields`);
    process.exit(2);
  }
  const domain = (check as { domain: string; name: string }).domain;
  const name = (check as { domain: string; name: string }).name;
  const [ruleId, description] = ONS_RULE_IDS[domain] ?? [`ONS-CASING-???`, `Unknown domain '${domain}'`];
  const result = validateName(domain as Parameters<typeof validateName>[0], name);
  rules.push({
    rule_id: ruleId,
    description,
    result: result.valid ? "pass" : "fail",
    message: result.valid ? null : (result.violation ?? null),
  });
}

const report = buildReport({ spec: "ons", spec_version: ONS_SPEC_VERSION, profile, subject, rules });

if (output === "json") {
  console.log(JSON.stringify(report, null, 2));
} else {
  printText(report);
}

process.exit(report.conformant ? 0 : 1);
