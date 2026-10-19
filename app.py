import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans

st.set_page_config(page_title="Rural Cyber-Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Community Cyber-Help Desk for Rural Awareness")
st.write("Real-Time Cognitive Scam Detection & Behavioral Risk Analytics")

# Tab Selection for Modules
tab1, tab2 = st.tabs(["🧠 Cognitive Analytics (NLP Scam Alert)", "📊 Behavioral Analytics (K-Means Risk)"])

# ---------------------------------------------------------
# TAB 1: COGNITIVE ANALYTICS (NLP REAL-TIME NOTIFICATION)
# ---------------------------------------------------------
with tab1:
    st.header("Cognitive Analytics: Real-Time SMS Scam Detection")
    st.info("💡 Concept: Automated background service listens to incoming SMS and triggers immediate notification for rural users.")

    # Train NLP Model
    training_messages = [
        "Your bank account is blocked. Click link to update KYC immediately.",
        "Congratulations! You won a lottery of 10 lakhs. Call this number to claim.",
        "Hi, are we meeting for project discussion tomorrow at 10 AM?",
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

    # Simulated Incoming SMS Notification
    st.subheader("📲 Simulated Incoming Phone Notification")
    
    sample_sms = st.selectbox("Simulate Incoming SMS on Rural User's Phone:", [
        "Urgent: Your electricity bill will be disconnected tonight. Pay via this link.",
        "Hi Abinaya, are we meeting for project discussion tomorrow?",
        "Your bank account is blocked. Click the link to update KYC immediately."
    ])

    if st.button("Trigger Phone Notification"):
        X_test = vectorizer.transform([sample_sms])
        prediction = nlp_model.predict(X_test)[0]

        # Display like a phone banner alert
        st.markdown("---")
        st.caption("🔔 **INCOMING NOTIFICATION BANNER**")
        if prediction == 'Scam':
            st.error(f"🚨 **ALERT: FRAUD / SCAM SMS DETECTED!**\n\n**Message:** {sample_sms}\n\n⚠️ *Warning: Do NOT click any links or reply to this message!*")
        else:
            st.success(f"✅ **SAFE SMS**\n\n**Message:** {sample_sms}\n\n*This message appears to be safe.*")

# ---------------------------------------------------------
# TAB 2: BEHAVIORAL ANALYTICS (K-MEANS CLUSTERING)
# ---------------------------------------------------------
with tab2:
    st.header("Behavioral Analytics: User Risk Segmentation (K-Means)")
    st.write("Grouping rural users based on transaction frequency and digital literacy to identify high-risk individuals.")

    # Behavioral Data
    behavior_data = {
        'User_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Monthly_Transactions': [2, 25, 22, 3, 20, 1, 18, 24, 4, 15],
        'Digital_Awareness_Score': [20, 90, 88, 25, 82, 15, 85, 92, 30, 78]
    }
    df_behavior = pd.DataFrame(behavior_data)

    X_behavior = df_behavior[['Monthly_Transactions', 'Digital_Awareness_Score']]
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    df_behavior['Risk_Cluster'] = kmeans.fit_predict(X_behavior)

    # Plot Clusters
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df_behavior[df_behavior['Risk_Cluster'] == 0]['Monthly_Transactions'], 
               df_behavior[df_behavior['Risk_Cluster'] == 0]['Digital_Awareness_Score'], 
               color='red', s=100, label='High Cyber Risk Group (Low Literacy)')

    ax.scatter(df_behavior[df_behavior['Risk_Cluster'] == 1]['Monthly_Transactions'], 
               df_behavior[df_behavior['Risk_Cluster'] == 1]['Digital_Awareness_Score'], 
               color='green', s=100, label='Low Risk / Digitally Aware Group')

    ax.set_title('K-Means Behavioral Segmentation')
    ax.set_xlabel('Monthly Digital Transactions')
    ax.set_ylabel('Digital Awareness Score')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
