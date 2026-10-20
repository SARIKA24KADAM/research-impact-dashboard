# Data inventory

## Fictional operational data

Generated with Python's standard `random` module, seed `24062026`, using `scripts/generate_demo_data.py`. The generator creates entirely invented example records; no real university, funder, employee or project data is included.

| File | Rows in generated sample | What it contains |
| --- | ---: | --- |
| `themes.csv` | 4 | Battery, grid, charging and industrial decarbonization themes |
| `owners.csv` | 6 | Fictional role labels and names |
| `projects.csv` | 12 | Fictional demonstration projects, owners, themes, dates and statuses |
| `kpi_definitions.csv` | 4 | Indicator names, units, direction, target and definitions |
| `budgets.csv` | 48 | Project-year fictional approved budget snapshots, 2023–2026 |
| `commitments.csv` | 36 | Fictional funding commitments by project and source |
| `expenditures.csv` | 144 | Quarterly fictional transactions, 2023–2025 |
| `kpi_actuals.csv` | 576 | Project-KPI-quarter illustrative values, 2023–2025 |
| `reporting_obligations.csv` | 144 | Project-quarter expected reporting records with example receipt status |
| `milestones.csv` | 48 | Four fictional milestones per project and example status |
| `research_outputs.csv` | 48 | Fictional publication, dataset and report records |
| `risks.csv` | 12 | Fictional project risk records |
| `corrective_actions.csv` | 12 | Fictional mitigation-action examples |
| `dq_issues.csv` | 16 | Fictional issue-register examples, separate from validation failures |

Rerunning the generator overwrites these tables deterministically. `scripts/validate_data.py` checks keys, project references and numeric finance/KPI fields. The result is written to `data/processed/validation_summary.json`.

## Public context data

`data/public/global-data-on-sustainable-energy.csv` is the attributed Kaggle source described in [`public_data_dictionary.md`](public_data_dictionary.md). This copy has 3,649 records and 21 fields. The public chart script filters Canada and plots the source's renewable share of final energy consumption field for available years. This series is not combined with the fictional program data.

## Derived figures

`scripts/create_charts.py` reads the generated tables and the separately stored public CSV. It writes four PNGs to `reports/figures/`: three fictional portfolio previews and one public country context chart. The figures can be regenerated with the README commands.
