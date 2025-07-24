import streamlit as st
import pandas as pd
import numpy as np
import json
import joblib
from sklearn.preprocessing import MinMaxScaler


try:
    scaler = joblib.load(r"D:\aave-credit-scoring\model_training\credit_scaler.pkl")
    model = joblib.load(r"D:\aave-credit-scoring\model_training\rf_credit_model.pkl")
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()


def extract_features_from_df(df):
    df.columns = df.columns.str.lower().str.strip()

    if 'wallet_address' not in df.columns and 'userwallet' in df.columns:
        df['wallet_address'] = df['userwallet']

    if 'actiondata' in df.columns:
        df['amount'] = df['actiondata'].apply(lambda x: x.get('amount') if isinstance(x, dict) else None)
        df['action'] = df['actiondata'].apply(lambda x: x.get('type') if isinstance(x, dict) else None)

    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['action'] = df['action'].str.lower().fillna('unknown')

    grouped = df.groupby(['wallet_address', 'action'])['amount'].sum().unstack(fill_value=0).reset_index()
    grouped['total_deposit_amount'] = grouped.get('deposit', 0)
    grouped['total_borrow_amount'] = grouped.get('borrow', 0)
    grouped['total_repay_amount'] = grouped.get('repay', 0)
    grouped['repay_to_borrow_ratio'] = np.where(
        grouped['total_borrow_amount'] > 0,
        grouped['total_repay_amount'] / grouped['total_borrow_amount'],
        0
    )
    grouped['borrow_to_deposit_ratio'] = np.where(
        grouped['total_deposit_amount'] > 0,
        grouped['total_borrow_amount'] / grouped['total_deposit_amount'],
        0
    )
    liquidation = df[df['action'] == 'liquidationcall'].groupby('wallet_address').size()
    grouped['liquidation_count'] = grouped['wallet_address'].map(liquidation).fillna(0).astype(int)
    tx_count = df.groupby('wallet_address').size()
    grouped['num_transactions'] = grouped['wallet_address'].map(tx_count).fillna(0).astype(int)

    return grouped[['wallet_address', 'total_deposit_amount', 'total_borrow_amount', 'total_repay_amount',
                    'repay_to_borrow_ratio', 'borrow_to_deposit_ratio', 'liquidation_count', 'num_transactions']]


def predict_score(features):
    feature_only = features.drop(columns=['wallet_address'])
    scaled = scaler.transform(feature_only)
    labels = model.predict(scaled)

    label_to_score = {
        0: (900, "Excellent"),
        1: (800, "Safe"),
        2: (600, "Low Risk"),
        3: (400, "Moderate Risk"),
        4: (200, "High Risk"),
}

    features['label'] = labels
    features['credit_score'] = features['label'].map(lambda x: label_to_score[x][0])
    features['risk_level'] = features['label'].map(lambda x: label_to_score[x][1])
    return features


st.title("🧮 DeFi Wallet Credit Scoring App")
st.write("Upload your transaction history JSON to get a wallet credit score and risk level.")

uploaded_file = st.file_uploader("📂 Upload transaction JSON file", type=["json"])
if uploaded_file:
    try:
        data = json.load(uploaded_file)
        if isinstance(data, dict):
            data = [data]
        df = pd.DataFrame(data)
        features = extract_features_from_df(df)
        scored = predict_score(features)

        st.success("✅ Scoring complete!")
        st.dataframe(scored.drop(columns=['label']))

        csv = scored.drop(columns=['label']).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Wallet Scores CSV", csv, file_name="wallet_score.csv")

    except Exception as e:
        st.error(f"Failed to process file: {e}")
