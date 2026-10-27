# Usability Testing Tool

A Streamlit application for collecting consent, demographic information, usability task results, and an exit questionnaire, with aggregated reports.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app1.py
```

On Windows, use `python` instead of `python3` if needed.

## Deploy on Streamlit Community Cloud

1. Push these files to GitHub.
2. Visit https://share.streamlit.io and sign in with GitHub.
3. Create an app using branch `main` and main file `app1.py`.

## Data notes

The app stores user responses in local CSV files in `data/`, excluded from Git. Streamlit Community Cloud local storage is not permanent. Secure the Report tab (which displays participant responses and allows data deletion), and configure durable storage before collecting real participant data.
