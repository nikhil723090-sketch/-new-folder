# Module 5 - Crime Pattern Detection

This module uses Python and pandas to detect crime patterns.

## Detects

- peak crime hours
- crime by season
- crime by district
- repeat offenders
- repeat locations
- hotspot map points

## Visualization

- Matplotlib PNG chart for peak crime hours
- Plotly HTML chart for district-wise crime
- Plotly HTML map for hotspots
- CSV summaries that can be imported into Power BI

## Run

From `karnatakaa pulice`:

```bash
python -m module_5_crime_pattern_detection.demo crime_records.csv --output-dir pattern_report
```

Outputs:

```text
pattern_report/
  peak_crime_hours.csv
  crime_by_season.csv
  crime_by_district.csv
  repeat_offenders.csv
  repeat_locations.csv
  peak_crime_hours.png
  crime_by_district.html
  crime_hotspot_map.html
```

## Power BI

Import the generated CSV files into Power BI and build visuals for district,
season, crime type, repeat offenders, and repeat locations.
