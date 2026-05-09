# Airbnb Market Structures: Rome vs. Copenhagen
Data Visualisation PW. Group: MESA. Year 2025/2026

---

## How to Access the Project

The project is hosted online and does not require any local setup to view. All visualisations, interactive components, and findings are accessible through the website.

**Website:** [romevscopenhagen.wordpress.com](https://romevscopenhagen.wpcomstaging.com)

---

## Project Structure

The submission contains the following files:

**Website source files**
- `page.html`: the full page content and structure
- `styles.css`: all custom styling
- `script.js`: the JavaScript city explorer and white/black hat toggle

These files are embedded in the live WordPress site through the Custom HTML block functionality. The live site at romevscopenhagen.wordpress.com is the intended way to experience the project, as it includes the embedded Tableau dashboards and hosted images.

**Python notebook and data**

`projectdv.ipynb`: the full analysis notebook covering data cleaning, integration, feature engineering, UPI construction, concentration metrics, and chart generation
- input: `listings_Rome.csv`, `neighbourhoods_Rome.geojson`, `listings_Copenhagen.csv`, `neighbourhoods_Copenhagen.geojson`
- output
    - `listings_clean.csv`: the cleaned and integrated listing-level dataset (46,535 rows)
    - `host_stats.csv`: host-level statistics including category classification
    - `neighbourhood_upi.csv`: neighbourhood-level aggregates and UPI scores
    - `neighbourhoods_combined.geojson`:spatial boundary files for both cities
    - All visualizations as png files for the website

**Report**
- `report.pdf`: the 5-page paper-style report

**AI use appendix**
- `ai_appendix.pdf`: the AI use appendix 

---

## Tableau Dashboards

The five Tableau dashboards are published on Tableau Public and embedded in the website. They can also be accessed directly through the Tableau Public links:

The individual views are:
- [ExplanatoryView](https://public.tableau.com/views/Cartella2_17774709061460/ExplanatoryView)
- [NeighbourhoodRanking](https://public.tableau.com/views/Cartella2_17774709061460/NeighbourhoodRanking)
- [ProfessionalHostConcentrationRomevsCopenhagen](https://public.tableau.com/views/Cartella2_17774709061460/ProfessionalHostConcentrationRomevsCopenhagen)
- [UPIDashboard](https://public.tableau.com/views/Cartella2_17774709061460/UPIDashboard)
- [PricevsUrbanPressurebyNeighbourhood](https://public.tableau.com/views/Cartella2_17774709061460/PricevsUrbanPressurebyNeighbourhood)

---

## Running the Python Notebook

The notebook was written in Python 3. To install all required dependencies, run:

```
pip install pandas numpy matplotlib seaborn geopandas scipy
```

Before running, make sure the input data files are organised in the following folder structure:

```
data/
  rome/
  copenhagen/
  exports/
```

The notebook can then be run top to bottom and will reproduce all cleaning steps, concentration metrics, the Lorenz curve, and the white hat and black hat visualisations.

---

## Data Source

Both listing datasets were obtained from [Inside Airbnb](https://insideairbnb.com), September 2025 snapshots. Neighbourhood boundary files were also sourced from Inside Airbnb.
