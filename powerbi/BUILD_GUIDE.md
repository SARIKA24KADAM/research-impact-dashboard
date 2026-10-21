# Open the Power BI project

This repository includes a Power BI Project at `ResearchImpact.pbip`, with a semantic model and a four-page report.

## Open and refresh

1. Install Power BI Desktop for Windows.
2. If needed, enable **Power BI Project (.pbip) save option** in **File > Options and settings > Options > Preview features**.
3. Open `ResearchImpact.pbip` from the repository root.
4. Refresh the model. The M queries read the CSV files from the public GitHub `main` branch. Set the web source credential to **Anonymous** if prompted; an internet connection is required.
5. Save as `.pbix` from **File > Save as** if you need a single-file report.

The semantic model is stored in `ResearchImpact.SemanticModel/model.bim` (TMSL), and the report uses the PBIR project structure in `ResearchImpact.Report`. The project uses explicit DAX measures and relationships to keep budget, commitment and expenditure facts separate. Public country-level energy context remains in its own table.

Power BI Desktop is not installed in the environment where this project was assembled, so the PBIP could not be opened and refreshed here. The project follows Microsoft's documented PBIP, PBIR and semantic model folder formats; the first open in Desktop is the final compatibility check.

Microsoft documentation: [Power BI Projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview), [report folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report), [semantic model folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset).
