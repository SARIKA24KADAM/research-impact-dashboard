# Data model

## Table grain

Keep facts at the grains below. Do not join transaction facts directly to milestone or KPI facts, because that can multiply totals.

| Table | Grain | Key fields |
| --- | --- | --- |
| `projects.csv` | One row per project | ProjectID, ThemeID, OwnerID |
| `themes.csv` | One row per theme | ThemeID |
| `owners.csv` | One fictional owner/role | OwnerID |
| `kpi_definitions.csv` | One row per KPI definition | KPIID |
| `kpi_actuals.csv` | One project, KPI and quarter value | ActualID, ProjectID, KPIID, PeriodEnd |
| `budgets.csv` | One project and fiscal-year budget | BudgetID, ProjectID, FiscalYear |
| `commitments.csv` | One funding commitment | CommitmentID, ProjectID |
| `expenditures.csv` | One expense transaction | ExpenditureID, ProjectID, TransactionDate |
| `milestones.csv` | One planned deliverable | MilestoneID, ProjectID |
| `reporting_obligations.csv` | One expected quarterly submission | ObligationID, ProjectID, DueDate |
| `research_outputs.csv` | One research output record | OutputID, ProjectID |
| `risks.csv` | One project risk | RiskID, ProjectID |
| `corrective_actions.csv` | One action linked to a risk | ActionID, RiskID, ProjectID |
| `dq_issues.csv` | One tracked quality issue | IssueID, ProjectID |

Recommended dimensions are Project, Theme, Owner, KPI and Date. Connect dimensions to facts using one-to-many, single-direction relationships. Use separate role-playing date dimensions or inactive relationships for transaction, due, actual and publication dates. Budget is a periodic snapshot, not a transaction table.

```text
Theme 1 ── * Project * ── 1 Owner
                 ├── * KPI Actual * ── 1 KPI Definition
                 ├── * Budget       ├── * Commitment
                 ├── * Expenditure  ├── * Milestone
                 ├── * Reporting Obligation
                 ├── * Research Output
                 ├── * Risk ── * Corrective Action
                 └── * DQ Issue
Date dimensions filter each fact on its relevant date.
```

## Modeling decisions

- Keep approved budget, funding commitment and actual expenditure distinct.
- Compare actual expenditure with its matching project-year budget. Do not sum a yearly budget once per transaction.
- For missing-report rates, use expected obligations as the denominator.
- Respect each KPI's target direction and unit when measuring attainment.
- Keep public energy indicators separate from synthetic project facts.
