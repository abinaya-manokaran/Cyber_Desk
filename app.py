import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans

# Page Configuration
st.set_page_config(page_title="Rural Cyber Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Rural Community Cyber-Help Desk")

# Language Selection
language = st.sidebar.selectbox("Select Language / மொழி", ["Tanglish", "Tamil (தமிழ்)", "English"])

# ---------------------------------------------------------
# 1. COGNITIVE ANALYTICS (NLP SCAM DETECTOR)
# ---------------------------------------------------------
# Model Training (Expanded with diverse patterns)
training_messages = [
    "Your bank account is blocked. Click link to update KYC immediately.",
    "Congratulations! You won a lottery of 10 lakhs. Call this number to claim.",
    "Urgent: Your electricity bill will be disconnected tonight. Pay via this link.",
    "Your credit card reward points are expiring today. Redeem now.",
    "Free loan approved up to 5 Lakhs! Click here to get instant money in account.",
    "Hi, are we meeting for project discussion tomorrow at 10 AM?",
    "Your OTP for banking transaction is 4892. Do not share with anyone.",
    "Mom, please pick up some groceries on your way back home.",
    "Hey, let's catch up for coffee this weekend.",
    "Dear customer, your Amazon order #10492 has been dispatched successfully."
]
labels = ['Scam', 'Scam', 'Scam', 'Scam', 'Scam', 'Non-Scam', 'Non-Scam', 'Non-Scam', 'Non-Scam', 'Non-Scam']

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_messages)
nlp_model = MultinomialNB()
nlp_model.fit(X_train, labels)

st.header("1. Cognitive Analytics: Real-Time SMS Detector (NLP)")

# Quick Sample Message Buttons for Easy Demo
st.write("👉 **Quick Demo Samples (Click to test instantly):**")
col1, col2, col3 = st.columns(3)

sample_text = ""
if col1.button("📩 Test Sample 1 (Banking Scam)"):
    sample_text = "Your ATM Card is deactivated! Click link to update KYC or account will be closed."
if col2.button("📩 Test Sample 2 (Lottery Scam)"):
    sample_text = "Urgent! Claim your cash prize of Rs 50,000 by clicking this link."
if col3.button("📩 Test Sample 3 (Safe SMS)"):
    sample_text = "Your doctor appointment is confirmed for tomorrow 5 PM."

# User Input Box
user_message = st.text_area("Or enter any incoming SMS received on phone:", value=sample_text, height=100)

if st.button("🔍 Analyze Message (Cognitive Check)"):
    if user_message.strip() != "":
        X_test = vectorizer.transform([user_message])
        prediction = nlp_model.predict(X_test)[0]
        
        if prediction == 'Scam':
            st.error("🚨 **ALERT: SCAM DETECTED!** Idhu oru fake / fraud message. Link-ai click செய்ய வேண்டாம்!")
        else:
            st.success("✅ **SAFE MESSAGE:** Idhu oru normal-ana safe message thaan.")
    else:
        st.warning("Please enter or select a message to analyze.")

st.markdown("---")

# ---------------------------------------------------------
# 2. BEHAVIORAL ANALYTICS (K-MEANS USER RISK CLUSTERING)
# ---------------------------------------------------------
st.header("2. Behavioral Analytics: User Risk Profiling (K-Means)")
st.write("Gramathu makkalin digital use-case vechu avanga 'High Cyber Risk'-la irukankala nu find pannuthoi.")

# K-Means Training Data
behavior_data = {
    'User_ID': [101, 102, 103, 104, 105, 106],
    'Monthly_Transactions': [2, 25, 3, 22, 1, 18],
    'Digital_Awareness_Score (Out of 100)': [20, 90, 25, 85, 15, 88]
}
df_beh = pd.DataFrame(behavior_data)

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
df_beh['Risk_Cluster'] = kmeans.fit_predict(df_beh[['Monthly_Transactions', 'Digital_Awareness_Score (Out of 100)']])
df_beh['Risk Level'] = df_beh['Risk_Cluster'].map({0: '🔴 High Cyber Risk (Needs Help)', 1: '🟢 Safe / Digitally Aware'})

st.dataframe(df_beh[['User_ID', 'Monthly_Transactions', 'Digital_Awareness_Score (Out of 100)', 'Risk Level']])
