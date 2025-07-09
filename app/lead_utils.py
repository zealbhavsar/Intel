import pandas as pd

def clean_data(df):
    df.columns = df.columns.str.strip().str.lower()
    df.dropna(inplace=True)
    return df

def feature_engineer(df):
    df['total_shipments'] = df.groupby('company_name')['shipment_id'].transform('count')
    df['unique_suppliers'] = df.groupby('company_name')['supplier_name'].transform('nunique')
    return df.drop_duplicates(subset='company_name')

def score_leads(df):
    df['lead_score'] = df['total_shipments'] / (df['unique_suppliers'] + 1)
    df['is_good_lead'] = df['lead_score'] > df['lead_score'].median()
    return df
