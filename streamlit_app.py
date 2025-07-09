import streamlit as st
import pandas as pd
from app.lead_utils import clean_data, feature_engineer, score_leads
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Lead Generation Engine", page_icon="📈", layout="wide")

# App Title
st.title("📈 Lead Generation Engine")
st.markdown("Upload **ImportYeti** and **HSN Data** CSV files to discover top potential leads using AI.")

# Sidebar Uploaders
st.sidebar.header("📁 Upload Data Files")
import_file = st.sidebar.file_uploader("Upload ImportYeti CSV", type=["csv"], key="import")
hsn_file = st.sidebar.file_uploader("Upload HSN Code CSV", type=["csv"], key="hsn")

# Process uploaded files
if import_file and hsn_file:
    import_df = pd.read_csv(import_file)
    hsn_df = pd.read_csv(hsn_file)

    st.success("✅ Files uploaded successfully! Processing data...")

    # Clean and feature engineer
    import_df = clean_data(import_df)
    features = feature_engineer(import_df)

    # Score leads
    scored = score_leads(features)

    # Show top leads
    st.subheader("🎯 Top 10 Scored Leads")
    st.dataframe(scored[['company_name', 'lead_score', 'is_good_lead']].sort_values(by='lead_score', ascending=False).head(10))

    # Save and download CSV
    output_path = "outputs/top_leads.csv"
    os.makedirs("outputs", exist_ok=True)
    scored.to_csv(output_path, index=False)

    with open(output_path, 'rb') as f:
        st.download_button("📥 Download Full Lead Report", f, file_name="top_leads.csv", mime="text/csv")

    # Lead Score Chart
    st.subheader("📊 Lead Score Distribution")
    st.bar_chart(scored[['company_name', 'lead_score']].set_index('company_name').sort_values('lead_score', ascending=False).head(10))

    # 🔍 Filter by Company Name
    st.subheader("🔍 Explore a Specific Company")
    unique_companies = scored['company_name'].unique()
    selected_company = st.selectbox("Select a company to view details", unique_companies)

    if selected_company:
        company_info = scored[scored['company_name'] == selected_company]
        st.write("### 🏷️ Company Overview")
        st.write(company_info[['company_name', 'total_shipments', 'unique_suppliers', 'lead_score', 'is_good_lead']])

        st.subheader("📊 Lead Score of Selected Company")
        st.bar_chart(company_info.set_index('company_name')['lead_score'])

else:
    st.warning("⚠️ Please upload both ImportYeti and HSN data files to proceed.")
