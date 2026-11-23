# Broiler Farm Performance Analytics

A practical Python, Pandas, SQLite and Streamlit portfolio project for analysing broiler farm daily records.

## Features

- CSV import with basic data-quality validation
- SQLite storage and parameterised SQL queries
- Flock-level performance dashboard
- Daily feed and weight trends
- Cumulative mortality and cost tracking
- Estimated cumulative feed conversion ratio (FCR)
- Downloadable analysed data
- Unit tests for validation and metrics

## Technology

Python, Pandas, SQLite, Streamlit, pytest, Git and GitHub.

## Quick start (Windows)

1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open PowerShell in the project folder.
4. Create and activate a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

5. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

6. Run the dashboard:

```powershell
streamlit run app.py
```

The browser should open the local dashboard. If it does not, use the local URL printed in the terminal.

## Run tests

```powershell
pytest -q
```

## CSV format

The uploaded CSV must contain these columns:

| Column | Meaning | Example |
|---|---|---|
| date | Daily reporting date | 2026-01-01 |
| flock_id | Unique flock label | FLOCK-A |
| birds_placed | Original number placed | 1000 |
| live_birds | Current live count | 990 |
| feed_kg | Feed used that day, kg | 85.5 |
| avg_weight_kg | Average bird weight, kg | 0.85 |
| mortality_count | Deaths recorded that day | 4 |
| feed_cost_kwd | Feed cost for the day, KWD | 22.500 |
| other_cost_kwd | Other recorded costs, KWD | 3.000 |

One row per flock per date. Keep flock IDs consistent.

## Metric definitions and limitations

- Cumulative mortality is the sum of daily mortality counts.
- Cumulative feed is the sum of daily feed records.
- Estimated cumulative FCR = cumulative feed consumed / estimated liveweight gain.
- Estimated liveweight gain = current live biomass - starting chick biomass.
- Starting chick biomass is estimated as birds placed on the first reporting date multiplied by the initial chick weight entered in the app.
- Costs are summed from daily feed and other cost entries.

**Important:** This is a learning and demonstration model, not a certified farm accounting or veterinary system. FCR depends on accurate feed, weighing, placement, mortality, culling, transfer and sale records. Reconcile these before using results for commercial decisions. The sample records are synthetic.

## Suggested next improvements

1. Add multiple houses and production cycles.
2. Add CSV export templates and stronger schema validation.
3. Add PostgreSQL support for multi-user deployment.
4. Add Power BI reporting.
5. Add role-based access, authentication and backups before handling client data.

## Portfolio description

Built a broiler farm analytics dashboard using Python, Pandas, SQLite and Streamlit. The application ingests daily flock records, validates data, stores records in a relational database and calculates operational indicators including cumulative mortality, feed consumption, estimated FCR and production costs. Includes a synthetic dataset, SQL queries, tests and downloadable analysis.
