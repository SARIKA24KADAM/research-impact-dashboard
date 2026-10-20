# Build the interactive report in Power BI Desktop

This repository contains source data, Power Query examples and measure definitions. It does not contain a `.pbix`/`.pbip` because Power BI Desktop was not available while this repository was assembled.

1. Run the data generator and validation commands from the root README.
2. In Desktop, import each CSV in `data/synthetic/`. Import the public CSV separately if you use the context page.
3. Apply the matching query in `powerbi/queries/`, or use it as a template. Set date, integer, decimal and currency types deliberately.
4. Create relationships from `docs/data_model.md`. Keep fact tables separate to prevent fan-out and double counting.
5. Add measures from `powerbi/measures/portfolio_measures.dax` and compare them with filtered source examples.
6. Create the four pages in `docs/report_pages.md`.
7. Add source, fictional-data and caveat labels. Check keyboard navigation, contrast, titles, units and alt text.
8. Save as Power BI Project (`.pbip`) if your Desktop version supports it, then commit the project folder. Otherwise save `.pbix` and consider adding a PDF or screenshots.
9. Record the Desktop version, refresh date and checks in `docs/validation_log.md`.

Official Microsoft documentation: [Power BI Projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview), [report definition](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report), [semantic model definition](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset/).
