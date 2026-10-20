# Research Program Performance & Impact Reporting Dashboard

This portfolio project demonstrates a reporting workflow for a university research program focused on electrification, batteries and decarbonization. It brings finance, delivery, reporting, research outputs and selected public energy indicators into one documented model.

> **Demo data:** Every project, person, budget, expense, milestone, KPI value, submission, risk and research output in the operational files is fictional and generated for this project. It does not represent Volt-Age, a university, funder or real person. The public energy dataset is kept separate from those fictional records.

## What is in the repository

- Reproducible fictional operational CSV tables, generated with a fixed seed.
- An attributed Kaggle sustainable-energy dataset for separate country-level context.
- A field dictionary, KPI register, data model, quality rules, caveats and report design.
- Power Query M examples, DAX measure definitions and Power BI build instructions.
- Three PNG chart previews generated from the fictional tables.

## Questions the dashboard is designed to answer

1. How much approved funding has been spent, committed or left available?
2. Which projects and milestones need attention?
3. Are quarterly reports and KPI updates arriving on time?
4. What research outputs have been recorded, and how do selected public energy indicators vary by country and year?

## Project structure

```text
data/synthetic/       Fictional operational source tables
data/public/          Attributed public energy source
data/processed/       Reproducible validation summary
data/dictionaries/    Field and KPI definitions
docs/                 Model, quality, assumptions and report design
powerbi/              Power Query, DAX and Desktop build guide
reports/figures/      PNG chart previews
scripts/              Data generation, validation and chart scripts
```

## Run it

Requires Python 3.10 or newer. Chart generation uses Matplotlib.

```powershell
python -m pip install -r requirements.txt
python scripts/generate_demo_data.py
python scripts/validate_data.py
python scripts/create_charts.py
```

### PNG charts

![Fictional approved budget, commitments and expenditure by theme](reports/figures/budget_by_theme.png)

![Fictional quarterly KPI progress against target](reports/figures/kpi_trend.png)

![Fictional milestone status counts](reports/figures/milestone_status.png)

These are static previews generated from the fictional operational tables, not screenshots of a live Power BI report.

### Public energy context (separate from the fictional program data)

![Canada renewable share of final energy consumption in the public Kaggle dataset](reports/figures/canada_renewable_share.png)

Source: Ansh Tanwar, *Global Data on Sustainable Energy (2000–2020)*, Kaggle, CC BY 4.0. This country trend is context only and is not attributed to the fictional research program.

## Power BI report

This repository includes Power Query examples, DAX measures, a star-schema proposal and a page-by-page report specification. It does not include a `.pbix` or `.pbip` file because Power BI Desktop was not available in the build environment. Follow [the Power BI build guide](powerbi/BUILD_GUIDE.md) to create and save the interactive report locally.

## Public data and attribution

The separate contextual source is *Global Data on Sustainable Energy (2000–2020)* by Ansh Tanwar, from [Kaggle, version 7](https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy/versions/7). The Kaggle page states CC BY 4.0. See [source attribution and reuse notes](docs/source_attribution.md). Country-level trends are context only; they are not program outcomes and cannot be attributed to a research program.

## Limitations

This is a demonstration model, not an audited finance system, grant-management system, impact evaluation or causal study. The fictional values show reporting logic only. A real deployment needs approved definitions, source reconciliation, privacy and access controls, stakeholder validation and a governed refresh process. Details are in [assumptions and limitations](docs/assumptions_and_limitations.md).

## Portfolio summary

> Built a reproducible research-program performance reporting prototype using fictional operational data, a documented star schema, Power Query transformations, DAX measure definitions, data-quality checks and attributed public energy context.

See [CV and portfolio wording](docs/cv_and_portfolio_summary.md).
