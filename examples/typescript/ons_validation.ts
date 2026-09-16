import { buildReport, validateName } from "governance-commons";

const value = "run_intent";
const validation = validateName("python_identifier", value);

const report = buildReport({
  spec: "ons",
  spec_version: "1.4.0",
  profile: "standard",
  subject: "example",
  rules: [
    {
      rule_id: "ONS-CASING-001",
      description: "Python identifiers must be snake_case",
      result: validation.valid ? "pass" : "fail",
      message: validation.valid ? null : validation.violation ?? null,
    },
  ],
});

console.log(JSON.stringify(report, null, 2));
