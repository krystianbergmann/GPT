import streamlit as st
import requests
import json

# Ustawienie klucza API OpenAI
API_KEY = 'API KEY'


# Funkcja do wysyłania żądania do API Moderation
def moderate_text(input_text):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "input": input_text
    }

    response = requests.post(
        'https://api.openai.com/v1/moderations',
        headers=headers,
        data=json.dumps(data)
    )

    return response.json()


# Tworzenie interfejsu w Streamlit
st.title("Text Moderation App")
st.write("Enter text to check its moderation status:")

# Pole do wpisania tekstu
user_input = st.text_area("Enter your text here:")

# Gdy użytkownik naciśnie przycisk "Submit"
if st.button("Submit"):
    if user_input:
        # Wywołanie funkcji moderation
        result = moderate_text(user_input)

        # Sprawdzenie czy tekst został oflagowany
        flagged = result["results"][0]["flagged"]

        # Stylowanie wyświetlania TRUE/FALSE w zależności od wartości flagged
        if flagged:
            st.markdown(f"<h2 style='color:red; font-size: 30px;'>Text flagged: {flagged}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='color:green; font-size: 30px;'>Text flagged: {flagged}</h2>",
                        unsafe_allow_html=True)

        # Wyświetlenie wyników moderacji
        categories = result["results"][0]["category_scores"]

        st.write("Moderation Results:")

        for category, score in categories.items():
            percentage = round(score * 100, 2)
            st.write(f"{category}: {percentage}%")
            st.progress(percentage / 100)
    else:
        st.write("Please enter some text.")
