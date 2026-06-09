/// <reference types="node" />
/**
 * Shared CLI utilities — not exported from the library's public API.
 */

import type { ConformanceReport } from "./report.js";

export function printText(report: ConformanceReport): void {
  const status = report.conformant ? "PASS" : "FAIL";
  console.log("GC Conformance Report");
  console.log(`  Spec:    ${report.spec} ${report.spec_version} (${report.profile} profile)`);
  console.log(`  Subject: ${report.subject}`);
  console.log(`  Result:  ${status}`);
  console.log();
  for (const r of report.rules) {
    const marker = r.result === "pass" ? "+" : r.result === "skip" ? "-" : "!";
    console.log(`  ${marker} [${r.rule_id}] ${r.description}`);
    if (r.message) {
      console.log(`      ${r.message}`);
    }
  }
  const s = report.summary;
  console.log(`\n  Summary: ${s.passed} passed, ${s.failed} failed, ${s.skipped} skipped of ${s.total} total`);
}
