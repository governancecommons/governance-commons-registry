# GC–INCIDENT.09 — Independent reviewer evidence contract

This document describes evidence required before a claim of independently verified OECD interoperability can be considered. Passing CI verifies only internal consistency, **not** reviewer independence or correctness.

## Primary-source review

Source: OECD (2025), *Towards a common reporting framework for AI incidents*, DOI 10.1787/f326d4ac-en, Annex B Table B.1.

For **each** of 29 criteria, record an attributed reviewer, date, source page, exact source label (subject to quotation permissions), answer format, vocabulary review, cardinality review, conditional-rule review, and an evidence reference. Discrepancies must be resolved explicitly. The review evidence lives under `source_review_evidence` in the fixture manifest; the per-criterion `independent_human_review` flags alone are insufficient.

## Independent fixtures

An independent author must provide name, affiliation, date, independence statement and evidence reference. Each fixture requires a unique ID, provenance, source file path, criteria covered, positive/negative expected result, criterion-level oracle, and execution evidence. Both positive and negative cases are required. The current assistant-authored examples do **not** count as independent fixtures.

## Semantic round trip

Supply a reviewer, date, test command, test result reference, mapped fields, unmapped fields, explicit loss accounting, and decision. A private envelope restoring the original adapter does not demonstrate GC-native OECD-to-GC-to-OECD equivalence. Do not mark equivalence verified while classification gaps remain unresolved.

## Human release approval

Require named approver, approval date, linked Governance Record reference and approval scope. A boolean approval flag or CI result is not authorization.

## Current decision

**Not independently verified.** Keep `normative=false`, `interoperability_verified=false`, `release_eligible=false`. Independent evidence and human release authorization remain outstanding. Do not describe this work as OECD-certified.
