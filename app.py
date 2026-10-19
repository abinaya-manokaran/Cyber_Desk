import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans

# ---------------------------------------------------------
# Page Configuration & Title
# ---------------------------------------------------------
st.set_page_config(page_title="Community Cyber-Help Desk", layout="wide")

st.title("🛡️ Community Cyber-Help Desk for Rural Safety")
st.write("Real-time AI Scam Detection using Cognitive Analytics (NLP) & Behavioral Risk Profiling (K-Means)")

# ---------------------------------------------------------
# 1. Cognitive Analytics (NLP Model Training)
# ---------------------------------------------------------
training_messages = [
    "Your bank account is blocked. Click the link to update KYC immediately.",
    "Congratulations! You won a lottery of 10 lakhs. Call this number to claim.",
    "Hi Abinaya, are we meeting for project discussion tomorrow at 10 AM?",
    "Urgent: Your electricity bill will be disconnected tonight. Pay via this link.",
    "Your OTP for banking transaction is 4892. Do not share with anyone.",
    "Mom, please pick up some groceries on your way back home.",
    "Your credit card reward points are expiring today. Redeem now.",
    "Hey, let's catch up for coffee this weekend."
]
labels = ['Scam', 'Scam', 'Non-Scam', 'Scam', 'Non-Scam', 'Non-Scam', 'Scam', 'Non-Scam']

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_messages)
nlp_model = MultinomialNB()
nlp_model.fit(X_train, labels)

# ---------------------------------------------------------
# 2. Behavioral Analytics (K-Means Model Training)
# ---------------------------------------------------------
# Behavioral metric: [Monthly Transactions, Digital Literacy Score (1-100)]
user_profiles = np.array([
    [2, 20],   # Rural User 1: Low awareness, low transactions -> High Risk
    [25, 90],  # User 2: Digitally literate -> Low Risk
    [1, 15],   # Rural User 3: Low awareness -> High Risk
    [20, 85]   # User 4: Digitally literate -> Low Risk
])
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans.fit(user_profiles)

# ---------------------------------------------------------
# 3. Quick Sample SMS Buttons for Demo
# ---------------------------------------------------------
st.subheader("📲 Quick Test with Sample Incoming SMS (ஒரே கிளிக்கில் சோதிக்க):")

col1, col2, col3, col4 = st.columns(4)

selected_msg = ""

if col1.button("🚨 Bank Blocked Scam"):
    selected_msg = "Your SBI bank account is blocked today! Click link to unblock KYC."

if col2.button("🚨 Electricity Bill Scam"):
    selected_msg = "Urgent notice: Power will be disconnected at 9 PM. Pay electricity bill now."

if col3.button("✅ Normal Project Msg"):
    selected_msg = "Can you please share the python machine learning notes by evening?"

if col4.button("✅ Banking OTP Msg"):
    selected_msg = "Your OTP for account login is 9876. Do not share it with anyone."

# Custom Text Input field for any other new SMS
user_input = st.text_input("Or enter/paste any custom incoming SMS below:", value=selected_msg)

# ---------------------------------------------------------
# 4. Real-Time Analytics & Output Display
# ---------------------------------------------------------
if st.button("🔍 Analyze Message & User Risk"):
    if user_input.strip() != "":
        # A. Cognitive Analysis (NLP)
        X_test = vectorizer.transform([user_input])
        nlp_prediction = nlp_model.predict(X_test)[0]
        nlp_proba = nlp_model.predict_proba(X_test)[0]
        
        st.markdown("---")
        st.subheader("1. 🧠 Cognitive Analytics Result (NLP Scam Detection)")
        
        if nlp_prediction == 'Scam':
            st.error(f"🚨 **ALERT: SCAM DETECTED!**\n\nThis message contains psychological triggers (Urgency/Fear). Do not click any links.")
        else:
            st.success(f"✅ **SAFE MESSAGE**\n\nThis appears to be a genuine/safe message.")
            
        # B. Behavioral Analysis (K-Means)
        st.subheader("2. 👥 Behavioral Analytics Result (K-Means User Risk Profiling)")
        
        # Simulating rural user risk context
        simulated_rural_user = np.array([[2, 20]])  # Low literacy rural user
        user_cluster = kmeans.predict(simulated_rural_user)[0]
        
        if user_cluster == 0 or nlp_prediction == 'Scam':
            st.warning("⚠️ **Behavioral Risk Segment:** High Vulnerability Group (Rural Context).\n"
                       "Recommendation: Auto-block suspicious links and play Audio Voice Warning in local language.")
        else:
            st.info("ℹ️ **Behavioral Risk Segment:** Low Vulnerability / Digitally Aware Group.")
    else:
        st.warning("Please select a sample message or enter a custom message to analyze.")
