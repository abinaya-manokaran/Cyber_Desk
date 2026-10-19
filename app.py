import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# App Title & Language Selection
st.title("🛡️ Rural Community Cyber-Help Desk: Real-Time Scam Detector")

language = st.selectbox(
    "Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["Tanglish", "Tamil (தமிழ்)", "English"]
)

if language == "Tamil (தமிழ்)":
    subtitle = "கிராமப்புற மக்களுக்கான உடனடி சைபர் மோசடி கண்டறியும் மையம்."
    input_label = "சந்தேகத்திற்கிடமான குறுஞ்செய்தியை உள்ளிடவும் (அல்லது கீழே உள்ள சாம்பிள் பட்டன்களைக் கிளிக் செய்யவும்):"
    button_label = "பகுப்பாய்வு செய் (Analyze)"
    scam_alert = "🚨 எச்சரிக்கை: மோசடி கண்டறியப்பட்டது! இது ஒரு போலியான குறுஞ்செய்தி."
    safe_alert = "✅ பாதுகாப்பு: இது ஒரு சாதாரண பாதுகாப்பான குறுஞ்செய்திதான்."
    warning_msg = "தயவுசெய்து குறுஞ்செய்தியை உள்ளிடவும்."
elif language == "English":
    subtitle = "Automated Scam SMS Detection Portal for Rural Communities."
    input_label = "Enter suspicious SMS (or click sample test buttons below):"
    button_label = "Analyze Message"
    scam_alert = "🚨 ALERT: SCAM DETECTED! This is a fraudulent message."
    safe_alert = "✅ SAFE: This is a normal, legitimate message."
    warning_msg = "Please enter a message to analyze."
else:  # Tanglish
    subtitle = "Gramathu makkalukana real-time scam message analyzer portal."
    input_label = "Message-ah type pannunga (or keela irukura sample buttons-ah click pannunga):"
    button_label = "Analyze Message"
    scam_alert = "🚨 ALERT: SCAM DETECTED! Idhu oru fake / fraud message."
    safe_alert = "✅ SAFE: Idhu oru normal-ana non-scam message thaan."
    warning_msg = "Dayavu seidhu message-ai type seyyavum."

st.write(subtitle)

# Model Training Pipeline
training_messages = [
    "Your bank account is blocked. Click the link to update KYC immediately.",
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

# Quick Sample Buttons for Easy Demo Testing
st.markdown("### 🔘 Quick Sample Test (Quick Click for Rural Users / Demo):")
col1, col2 = st.columns(2)

selected_sample = ""

with col1:
    if st.button("📱 Test Bank Blocked SMS"):
        selected_sample = "Your bank account is blocked. Click the link to update KYC immediately."
    if st.button("⚡ Test Electricity Bill SMS"):
        selected_sample = "Urgent: Your electricity bill will be disconnected tonight. Pay via this link."

with col2:
    if st.button("🎁 Test Lottery Winning SMS"):
        selected_sample = "Congratulations! You won a lottery of 10 lakhs. Call this number to claim."
    if st.button("💬 Test Normal Personal SMS"):
        selected_sample = "Hi, are we meeting for project discussion tomorrow at 10 AM?"

# Input Field
user_message = st.text_input(input_label, value=selected_sample)

if st.button(button_label) or selected_sample != "":
    if user_message.strip() != "":
        X_test = vectorizer.transform([user_message])
        prediction = nlp_model.predict(X_test)[0]
        
        if prediction == 'Scam':
            st.error(scam_alert)
        else:
            st.success(safe_alert)
    else:
        st.warning(warning_msg)
