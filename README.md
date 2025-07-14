# czechia_real_estate

A data analysis project focused on the Czech real estate market. This repository is part of my data portfolio and demonstrates my skills in data acquisition, processing, and visualization.

## Project Overview

- **Data Scraping:** Automated collection of real estate data from publicly available sources, mainly Sreality.cz
- **Data Collection:** Manually gathered publicly accessible data from the Czech Statistical Office (ČSÚ) and the Czech Office for Surveying, Mapping and Cadastre (ČÚZK). The dataset primarily includes information on population size, average wages, and geographical, such as district names and their spatial boundaries.
- **Data Cleaning & Transformation:** The collected data is cleaned and pre-processed using SQL (e.g., removing duplicates, data formatting, etc.), Microsoft Excel, and/or Power Query (during import into Excel or Power BI).
- **Data Storage:** Data is saved to a suitable database and prepared for further analysis.
- **Visualization:** The processed data is visualized in Power BI or Tableau, with final outputs available as interactive dashboards or static reports.

> **Note:**  
> Final versions of the data tables were not only processed in SQL, but also in Microsoft Excel and/or using Power Query during import into Excel or Power BI. For this reason, the structure of the final tables (see `csv_tables.zip`) may differ from the original raw tables.

## Technologies Used

- **Python** – for data scraping and initial data manipulation
- **SQL** – for data cleaning and transformation
- **Excel / Power Query** – for additional data processing and shaping
- **Power BI / Tableau** – for visualization and dashboard creation

## Project Outputs

- Interactive dashboards (.pbix for Power BI, Tableau Public)
- Static reports in PDF format
- Final data tables are available as CSV files in a ZIP archive ([csv_tables.zip](csv_tables.zip)) included in this repository

## How to Use the Project

1. **Data Scraping:**  
   Run the provided Python scripts to collect up-to-date real estate data from selected sources.

2. **Data Processing:**  
   Import the data into a SQL database and apply the required transformations using the included SQL scripts. Further data processing and shaping can be done in Excel or Power Query as needed.

3. **Visualization:**  
   Load the processed data into Power BI or Tableau and use the prepared visualizations, or create your own dashboards. Alternatively, export the results as PDF reports or share .pbix files.

## Example Outputs

- [Interactive Tableau Dashboard](https://public.tableau.com/views/Czechia_dashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Power BI dashboard (.pbix)](powerbi_dashboard.pbix)
- [Static PDF report](powerbi_dashboard.pdf)
- [Final CSV data tables (ZIP)](csv_tables.zip)

> **Disclaimer:**  
>This projects presents average real estate prices and income data across the Czech Republic. Historical data comes from the ČÚZK database, which does not include 2024. Income data is from the ČSÚ. Data for 2025 was scraped from Sreality.cz on July 11 and reflects a snapshot, not a full-year average. The dashboard demonstrates the author’s skills in web scraping, data processing, and visualization; 2025 data is included to showcase technical abilities rather than provide a full market overview.

## Author

- [domin224](https://github.com/domin224)

---

For any questions, feel free to contact me.
