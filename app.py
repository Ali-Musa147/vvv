import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Transliteration map
translit_map = {
    'א': 'a', 'ב': 'b', 'ג': 'g', 'ד': 'd', 'ה': 'h',
    'ו': 'v', 'ז': 'z', 'ח': 'ch', 'ט': 't',
    'י': 'y', 'כ': 'k', 'ך': 'k', 'ל': 'l', 'מ': 'm',
    'ם': 'm', 'נ': 'n', 'ן': 'n', 'ס': 's', 'ע': 'a',
    'פ': 'p', 'ף': 'f', 'צ': 'ts', 'ץ': 'ts',
    'ק': 'k', 'ר': 'r', 'ש': 'sh', 'ת': 't'
}

def is_hebrew(text):
    return bool(re.search('[\u0590-\u05FF]', str(text)))

def transliterate(text):
    return ''.join([translit_map.get(c, c) for c in str(text)])

def process_dataframe(df):
    for col in ['First Name', 'Middle Name', 'Last Name']:
        if col in df.columns:
            df[f'{col} (Eng)'] = df[col].apply(lambda x: transliterate(x) if is_hebrew(x) else x)
    return df

def convert_df_to_csv(df):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

# Streamlit UI
st.set_page_config(page_title="Hebrew Name Transliterator", layout="centered")
st.title("🔤 Hebrew Name Transliterator (CSV Tool)")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("Original Data (Preview):")
        st.dataframe(df.head())

        df_processed = process_dataframe(df)

        st.subheader("Processed Data (Preview):")
        st.dataframe(df_processed.head())

        csv_download = convert_df_to_csv(df_processed)
        st.download_button(
            label="📥 Download Transliterated CSV",
            data=csv_download,
            file_name="transliterated_names.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
