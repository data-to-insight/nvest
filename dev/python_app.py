import pandas as pd
import streamlit as st
import warnings
import re
from pandas.errors import SettingWithCopyWarning

# Suppress copy warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# --- Normalised column mapping ---
column_map = {
    "submissiontime": "submission_date",
    "youremail": "email",
    "whichlocalauthoritydoyousupport": "local_authority",
    "yourname": "name",
    "yourjobtitle": "role",
    "whatwouldyoumostlikethenvestnationalforumtoachieve": "desired_outcomes",
    "areyouawareofanylocalworkrelevanttothisforumsaims": "existing_local_work",
    "whichcmsdoesyourlause": "cms",
    "practiceleadname": "lead_name",
    "practiceleademail": "lead_email",
    "performancebileadname": "performance_lead",
    "performancebileademail": "performance_email",
    "techsupportleadname": "support_lead",
    "techsupportleademail": "support_email"
}

# --- App UI ---
st.title("NVEST: Upload Your Data File")

st.markdown("""
Upload a **CSV** file below. Accepted formats: `.csv`.  
The file will be cleaned, renamed, and previewed.
""")

# --- Upload section ---
uploaded_file = st.file_uploader("Upload data file", type=["csv"])  # no xlsx due to pyodide

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df.dropna(axis=0, how="all", inplace=True)
        df.dropna(axis=1, how="all", inplace=True)

        # --- Normalise column names ---
        normalised_cols = df.columns.str.strip().str.lower().str.replace(r"[^\w]", "", regex=True)
        rename_map = {original: column_map[cleaned] for original, cleaned in zip(df.columns, normalised_cols) if cleaned in column_map}
        df.rename(columns=rename_map, inplace=True)

        # --- Create domain from email ---
        if "email" in df.columns:
            df["domain"] = (
                df["email"]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", "", regex=True)
                .str.extract(r"@(.+)$")[0]
            )
        else:
            df["domain"] = pd.NA

        # --- Add default columns ---
        if "steering_grp" not in df.columns:
            df["steering_grp"] = "N"
        if "web_signup" not in df.columns:
            df["web_signup"] = "Y"

        # --- Convert and sort on date ---
        if "submission_date" in df.columns:
            df["submission_date"] = pd.to_datetime(df["submission_date"], errors="coerce")

        sort_keys = [col for col in ["submission_date", "email"] if col in df.columns]
        if sort_keys:
            df.sort_values(by=sort_keys, ascending=[False, True], inplace=True)
            if "email" in df.columns:
                df.drop_duplicates(subset="email", keep="first", inplace=True)

        st.success(f"Loaded and cleaned file: `{uploaded_file.name}`")
        
        st.write("Columns after cleaning:", df.columns.tolist())

        st.dataframe(df)

    except Exception as e:
        st.error(f"Error loading file: {e}")
