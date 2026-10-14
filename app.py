import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# App Title & Language Selection
st.title("🛡️ Rural Community Cyber-Help Desk: Real-Time Scam Detector")

# Language Selector Sidebar or Selectbox
language = st.selectbox(
    "Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["Tanglish", "Tamil (தமிழ்)", "English"]
)

# Dynamic text mapping based on language selection
if language == "Tamil (தமிழ்)":
    subtitle = "கிராமப்புற மக்களுக்கு வரும் சந்தேகத்திற்கிடமான குறுஞ்செய்திகளை (SMS) உடனடியாகப் பகுப்பாய்வு செய்து மோசடியா என கண்டறியும் உதவி மையம்."
    input_label = "போனுக்கு வந்த சந்தேகத்திற்கிடமான குறுஞ்செய்தியை இங்கே உள்ளிடவும்:"
    button_label = "செய்தியைப் பகுப்பாய்வு செய் (Analyze)"
    scam_alert = "🚨 எச்சரிக்கை: மோசடி கண்டறியப்பட்டது! இது ஒரு போலியான குறுஞ்செய்தி. யாரும் எந்த இணைப்பையும் (Link) கிளிக் செய்ய வேண்டாம்!"
    safe_alert = "✅ பாதுகாப்பு: இது ஒரு சாதாரண பாதுகாப்பான குறுஞ்செய்திதான்."
    warning_msg = "தயவுசெய்து குறுஞ்செய்தியை உள்ளிடவும்."
elif language == "English":
    subtitle = "An automated help desk tool designed to instantly analyze suspicious SMS messages for rural communities."
    input_label = "Enter or paste the suspicious SMS received on your phone:"
    button_label = "Analyze Message"
    scam_alert = "🚨 ALERT: SCAM DETECTED! This is a fraudulent message. Do not click any links!"
    safe_alert = "✅ SAFE: This is a normal, legitimate message."
    warning_msg = "Please enter a message to analyze."
else:  # Tanglish
    subtitle = "Gramathu makkaluku varum sandhegathukuriya messegai inge analyze seidhu Scam-la illaya nu kandupidiungal."
    input_label = "Phone-ku vantha sandhegathukuriya message-ah inge type pannunga:"
    button_label = "Message-ah Analyze Pannunga"
    scam_alert = "🚨 ALERT: SCAM DETECTED! Idhu oru fake / fraud message. Yaarum link-ai click seyyavendam!"
    safe_alert = "✅ SAFE: Idhu oru normal-ana non-scam message thaan."
    warning_msg = "Dayavu seidhu message-ai type seyyavum."

st.write(subtitle)

# 1. Training Real-world scam dataset (Core Logic in English)
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

# Model Training pipeline using Naive Bayes & CountVectorizer
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_messages)
nlp_model = MultinomialNB()
nlp_model.fit(X_train, labels)

# 2. Real-Time User Input Box
user_message = st.text_input(input_label)

if st.button(button_label):
    if user_message.strip() != "":
        X_test = vectorizer.transform([user_message])
        prediction = nlp_model.predict(X_test)[0]
        
        # Real-time visual alert
        if prediction == 'Scam':
            st.error(scam_alert)
        else:
            st.success(safe_alert)
    else:
        st.warning(warning_msg)
