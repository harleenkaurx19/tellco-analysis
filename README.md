# TellCo Telecom User Analytics

## Project Overview
Analysis of TellCo mobile service provider data to identify 
growth opportunities and make buy/sell recommendation.

## Live Dashboard
Run locally:
```
streamlit run dashboard/app.py
```

## Project Structure
- `src/` - Source code modules
- `dashboard/` - Streamlit dashboard
- `tests/` - Unit tests (17/17 passing)
- `scripts/` - Analysis & export scripts
- `data/` - Dataset & saved features
- `notebooks/` - Jupyter notebooks

## How to Install
```
pip install -r requirements.txt
```

## How to Run
```
python main.py
```

## How to Test
```
pytest tests/ -v --cov=src
```

## Tasks Completed
- ✅ Task 1 - User Overview Analysis
- ✅ Task 2 - User Engagement Analysis  
- ✅ Task 3 - User Experience Analysis
- ✅ Task 4 - User Satisfaction Analysis

## Tech Stack
- Python, Pandas, NumPy
- Scikit-learn, MLflow
- Streamlit Dashboard
- PostgreSQL Database
- GitHub Actions CI/CD
- Docker

## Results
- 106,856 users analyzed
- R² Score: 1.0 (Perfect model)
- 17/17 unit tests passing
- 57% code coverage

