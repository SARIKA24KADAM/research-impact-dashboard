# Data-quality rules

The validation script checks deterministic structural rules and writes `data/processed/validation_summary.json`.

| Rule | Check | Expected handling |
| --- | --- | --- |
| Unique keys | Identifier is non-empty and unique within each table | Flag duplicates; do not arbitrarily keep one |
| Referential integrity | Project references resolve to a project | Correct at source or flag unresolved records |
| Numeric validity | Finance and KPI values parse as numbers | Flag invalid values and preserve source evidence |
| Non-negative amounts | Budgets, commitments and expenses are zero or positive | Investigate negatives; use reversal type if relevant |
| KPI grain | One value per project, KPI and quarter | Resolve duplicate submissions by an agreed rule |
| Submission completeness | Compare received reports to expected obligations | Missing remains missing, never substitute zero |
| KPI target logic | Value and target share unit and direction | Do not calculate attainment for incompatible definitions |
| Milestone status | A completed milestone has an actual date | Flag conflicting status/date pairs |

The generated source tables satisfy the implemented hard checks. `dq_issues.csv` contains separate fictional tracked issues to demonstrate reporting; they are not failed generator checks. A real implementation should add source row counts, ingestion timestamps, lineage, exception ownership, remediation history and agreed materiality thresholds.
