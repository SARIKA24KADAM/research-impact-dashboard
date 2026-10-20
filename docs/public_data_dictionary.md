# Public dataset field guide

This describes the included `data/public/global-data-on-sustainable-energy.csv`, sourced from the Kaggle dataset page cited in [`source_attribution.md`](source_attribution.md). The source CSV contains 3,649 data rows and 21 columns in this copy. The original column names are retained, including capitalization, punctuation and the line break in `Density\n(P/Km2)`. Empty cells represent missing values.

| Source column | Meaning / unit |
| --- | --- |
| `Entity` | Country or entity label |
| `Year` | Observation year; the dataset title covers 2000–2020 |
| `Access to electricity (% of population)` | Population share with electricity access, percent |
| `Access to clean fuels for cooking` | Clean-cooking-fuel access indicator; refer to dataset source notes for the precise unit/definition |
| `Renewable-electricity-generating-capacity-per-capita` | Renewable electricity generating capacity per capita; refer to source notes for the unit |
| `Financial flows to developing countries (US $)` | Recorded international financial flows for renewable energy in developing countries, US dollars |
| `Renewable energy share in the total final energy consumption (%)` | Renewable share of total final energy consumption, percent |
| `Electricity from fossil fuels (TWh)` | Electricity generated from fossil fuels, terawatt-hours |
| `Electricity from nuclear (TWh)` | Electricity generated from nuclear energy, terawatt-hours |
| `Electricity from renewables (TWh)` | Electricity generated from renewable sources, terawatt-hours |
| `Low-carbon electricity (% electricity)` | Low-carbon share of electricity generation, percent |
| `Primary energy consumption per capita (kWh/person)` | Primary energy consumption per person, kWh/person |
| `Energy intensity level of primary energy (MJ/$2017 PPP GDP)` | Primary-energy intensity in megajoules per 2017 PPP GDP unit |
| `Value_co2_emissions_kt_by_country` | CO₂ emissions value, kilotonnes, as supplied by the source |
| `Renewables (% equivalent primary energy)` | Renewable energy share as equivalent primary energy, percent |
| `gdp_growth` | GDP growth value as provided by the source |
| `gdp_per_capita` | GDP per capita value as provided by the source |
| `Density\n(P/Km2)` | Population density per square kilometre; source field name includes a line break |
| `Land Area(Km2)` | Land area, square kilometres |
| `Latitude` | Geographic latitude |
| `Longitude` | Geographic longitude |

For indicator definitions and caveats beyond the column labels, consult the Kaggle source and its cited provenance. This project does not infer missing values or join the public rows to the fictional program records.
