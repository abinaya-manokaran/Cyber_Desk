import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Community Cyber-Help Desk", layout="wide")

st.title("🛡️ Community Cyber-Help Desk: Real-Time AI Scam & Risk Analyzer")
st.markdown("**Empowering Rural Communities with Cognitive NLP Detection & Behavioral Analytics**")

# Language Selection
language = st.sidebar.selectbox("🌐 Select Language / மொழி:", ["Tanglish", "Tamil (தமிழ்)", "English"])

# Initialize Session State for Real-Time Tracking
if 'message_count' not in st.session_state:
    st.session_state.message_count = 3
if 'scam_received' not in st.session_state:
    st.session_state.scam_received = 1
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 1. COGNITIVE ANALYTICS: MODEL TRAINING (NLP) ---
training_messages = [
    "Your bank account is blocked. Click the link to update KYC immediately.",
    "Congratulations! You won a lottery of 10 lakhs. Call this number to claim.",
    "Urgent: Your electricity bill will be disconnected tonight. Pay via this link.",
    "Your credit card reward points are expiring today. Redeem now.",
    "Hi, are we meeting for project discussion tomorrow at 10 AM?",
    "Your OTP for banking transaction is 4892. Do not share with anyone.",
    "Mom, please pick up some groceries on your way back home.",
    "Hey, let's catch up for coffee this weekend."
]
labels = ['Scam', 'Scam', 'Scam', 'Scam', 'Non-Scam', 'Non-Scam', 'Non-Scam', 'Non-Scam']

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_messages)
nlp_model = MultinomialNB()
nlp_model.fit(X_train, labels)

# --- SIDEBAR: SIMULATOR & INPUT ---
st.sidebar.header("📲 Incoming SMS Notification Simulator")
st.sidebar.info("Simulating automatic SMS detection for rural users")

# Preset Sample Messages
sample_option = st.sidebar.selectbox("📩 Pick a Sample Incoming Message:", [
    "Select a message...",
    "ALERT: Your SBI Debit Card is suspended. Verify details at http://sbi-fake.com",
    "Electricity disconnect notice: Pay Rs. 4500 immediately to avoid power loss.",
    "Dear Abinaya, please send the project PDF file before 5 PM today.",
    "Your account credited with Rs 5000 via UPI transaction."
])

custom_input = st.sidebar.text_area("✍️ Or Type Any New Custom Message:")

# Determine active message
active_msg = ""
if custom_input.strip() != "":
    active_msg = custom_input.strip()
elif sample_option != "Select a message...":
    active_msg = sample_option

# --- MAIN DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🧠 Cognitive Analytics (NLP Scam Detector)")
    
    if active_msg != "":
        # Real-time Prediction
        X_test = vectorizer.transform([active_msg])
        prediction = nlp_model.predict(X_test)[0]
        
        # Display simulated phone notification
        st.markdown("### 🔔 Simulated Phone Notification")
        if prediction == 'Scam':
            st.error(f"🚨 **SCAM ALERT DETECTED!**\n\n**Incoming Msg:** \"{active_msg}\"\n\n⚠️ *Warning:* Fraudulent keywords found. Do NOT click any links or share OTPs!")
            st.session_state.scam_received += 1
        else:
            st.success(f"✅ **SAFE MESSAGE**\n\n**Incoming Msg:** \"{active_msg}\"\n\n👍 This message appears legitimate and safe.")
            
        st.session_state.message_count += 1
        st.session_state.history.append({"Message": active_msg, "Result": prediction})
    else:
        st.info("👈 Select a sample message or type a new one from the sidebar to analyze in real-time!")

    # Live History Table
    if st.session_state.history:
        st.markdown("#### 📜 Live Incoming SMS Stream History")
        st.dataframe(pd.DataFrame(st.session_state.history).tail(5), use_container_width=True)

with col2:
    st.subheader("📊 Behavioral Analytics (Real-Time Risk Segmentation)")
    
    # --- 2. BEHAVIORAL ANALYTICS: K-MEANS CLUSTERING ---
    # Dummy rural users dataset
    user_data = {
        'User_ID': ['User 1', 'User 2', 'User 3', 'Current User'],
        'Total_Messages_Received': [12, 45, 8, st.session_state.message_count],
        'Scam_Messages_Exposed': [1, 28, 0, st.session_state.scam_received]
    }
    df_users = pd.DataFrame(user_data)
    
    # Feature matrix
    X_behavior = df_users[['Total_Messages_Received', 'Scam_Messages_Exposed']]
    
    # Fit K-Means
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    df_users['Risk_Cluster'] = kmeans.fit_predict(X_behavior)
    
    # Current User Risk Mapping
    current_user_cluster = df_users.loc[df_users['User_ID'] == 'Current User', 'Risk_Cluster'].values[0]
    
    if current_user_cluster == 1:
        st.warning("⚠️ **Current Behavioral Risk Level:** HIGH RISK USER\n\n(High exposure to scam messages. Automated Help-Desk assistance recommended!)")
    else:
        st.success("🟢 **Current Behavioral Risk Level:** MODERATE / SAFE USER")

    # K-Means Cluster Graph
    fig, ax = plt.subplots(figsize=(6, 4))
    for cluster in [0, 1]:
        cluster_data = df_users[df_users['Risk_Cluster'] == cluster]
        label_name = 'High Risk Cluster' if cluster == 1 else 'Low/Moderate Risk Cluster'
        color = 'red' if cluster == 1 else 'green'
        ax.scatter(cluster_data['Total_Messages_Received'], cluster_data['Scam_Messages_Exposed'], 
                   color=color, label=label_name, s=150)
    
    ax.set_title("User Risk Segmentation (K-Means Clustering)")
    ax.set_xlabel("Total SMS Received")
    ax.set_ylabel("Scam SMS Exposure")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
