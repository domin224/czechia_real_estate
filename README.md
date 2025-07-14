# czechia_real_estate

A data analysis project focused on the Czech real estate market. This repository is part of my data portfolio and demonstrates my skills in data acquisition, processing, and visualization.

## Project Overview

- **Data Scraping:** Automated collection of real estate data from publicly available sources, mainly Sreality.cz
- **Data Collection:** Manually gathered publicly accessible data from the Czech Statistical Office (ČSÚ) and the Czech Office for Surveying, Mapping and Cadastre (ČÚZK). The dataset primarily includes information on population size, average wages, and geographical, such as district names and their spatial boundaries.
- **Data Cleaning & Transformation:** The collected data is cleaned and pre-processed using SQL (e.g., removing duplicates, data formatting, etc.), Microsoft Excel, and/or Power Query (during import into Excel or Power BI).
- **Data Storage:** Data is saved to a suitable database and prepared for further analysis.
- **Visualization:** The processed data is visualized in Power BI or Tableau, with final outputs available as interactive dashboards or static reports.

> Disclaimer:
> This project presents average real estate prices and income data across the Czech Republic. Historical data comes from the ČÚZK database, which does not include 2024. Data for 2025 was scraped from Sreality.cz on July 11 and reflects a snapshot, not a full-year average. The project demonstrates the author’s skills in web scraping, data processing, and visualization; 2025 data is included to showcase technical abilities rather than provide a full market overview.

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

This section explains how to reproduce the full workflow, from data acquisition to final dashboards and reports.

### 1. Data Acquisition

- **Scrape real estate listings:**
  - Run the provided Python script to collect current real estate data from [Sreality.cz](https://www.sreality.cz).
  - The output will be saved as a `.csv` file.

- **Collect demographic and geographic data:**
  - Download official datasets manually from:
    - [Czech Statistical Office (ČSÚ)](https://www.czso.cz) – e.g., average wages, population by district.
    - [Czech Office for Surveying, Mapping and Cadastre (ČÚZK)]([https://www.cuzk.cz](https://vdp.cuzk.cz/vdp/ruian/vymennyformat;jsessionid=dm0I_ja6bkGDNPTp87zAFJ7dUhehpb9MKcMkjvosBwfBqrVCGvXa!-369148306)) – e.g., region, district and municipality boundaries.

### 2. Data Cleaning & Transformation

- **Import data into PostgreSQL:**
  - Create a new PostgreSQL database (e.g., `cz_real_estate`) using DBeaver or another client.
  - Import raw CSV files into staging tables.
  - Use the provided SQL scripts. Not all scripts that had been used to alter the tables are provided.

- **Processing in Excel / Power Query:**
  - Files can be further cleaned using Excel or Power Query before import or after SQL processing.
  - Useful for unpivoting, shaping, or quick fixes (e.g., inconsistent column names).

### 3. Data Visualization

- **Power BI:**
  - Connect your PostgreSQL database to the Power BI model.
  - Link the tables using relationships based on shared columns.
  - All tables and the complete model are included in the `powerbi_dashboard.pbix` file.

- **Tableau Public:**
  - Open the Tableau workbook and connect it to your processed data.
  - Unfortunately, the free version of Tableau Public Desktop (which I used) does not support direct connections to PostgreSQL databases.
  - Upload the CSV files and link them in the **Data** panel.
  - All tables and the complete model are included in the `tableau_dashboard.twb` file.

- **Export options:**
  - Export dashboard pages as static PDF reports.
  - Share `.pbix` or Tableau workbook files.
 
### 4. Project Outputs

- Final CSV data tables are provided in [`csv_tables.zip`](csv_tables.zip)
- Example dashboards:
  - Power BI: [`powerbi_dashboard.pbix`](powerbi_dashboard.pbix)
  - Tableau: [Hosted version](https://public.tableau.com/views/Czechia_dashboard/Dashboard1)
- Example static report: [`powerbi_dashboard.pdf`](powerbi_dashboard.pdf)

## Requirements

To fully use and replicate this project, the following software and tools are recommended:

- **[Python 3.10+](https://www.python.org/downloads/)**  
  For running the web scraping and data processing scripts.

- **[PostgreSQL](https://www.postgresql.org/)** (e.g., version 15+)  
  A relational database system used to store and transform the collected data.

- **[DBeaver](https://dbeaver.io/)** (Community Edition is sufficient)  
  A user-friendly database management tool for interacting with the PostgreSQL database and running SQL scripts.

- **[Power BI Desktop](https://powerbi.microsoft.com/en-us/desktop/)** or **[Tableau Public](https://public.tableau.com/)**  
  Used for creating visualizations and dashboards from the processed data.

- **Python packages** (see `requirements.txt`):  
  Includes libraries like `requests`, `pandas`, `beautifulsoup4`, and others.

> Tip: DBeaver is especially useful for managing your PostgreSQL database and executing the included SQL transformation scripts.

## Example Outputs

- [Interactive Tableau Dashboard](https://public.tableau.com/views/Czechia_dashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Power BI dashboard (.pbix)](powerbi_dashboard.pbix)
- [Static PDF report](powerbi_dashboard.pdf)
- [Final CSV data tables (ZIP)](csv_tables.zip)


## Author

- [domin224](https://github.com/domin224)

---

For any questions, feel free to contact me.
