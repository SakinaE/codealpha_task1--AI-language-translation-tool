import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS

# Title
st.title("🌍 AI Language Translation Tool")

# History Storage
if "history" not in st.session_state:
    st.session_state.history = []

# Input text
text = st.text_area("Enter Text")

# Language list
languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh-CN"
}

# Select source language
source_lang = st.selectbox(
    "Source Language",
    list(languages.keys())
)

# Select target language
target_lang = st.selectbox(
    "Target Language",
    list(languages.keys())
)

# Translate button
if st.button("Translate"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:

        # Language Detection
        if len(text.split()) >= 3:
            detected_lang = detect(text)
            st.write("Detected Language:", detected_lang)
        else:
            st.info(
                "Enter at least 3 words for accurate language detection."
            )

        # Translation
        translated = GoogleTranslator(
            source=languages[source_lang],
            target=languages[target_lang]
        ).translate(text)

        st.success("Translation Completed ✅")

        st.text_area(
            "Translated Text",
            translated,
            height=120
        )

        # Save History
        st.session_state.history.append(
            {
                "Original": text,
                "Translated": translated
            }
        )

        # Text-to-Speech
        try:
            tts = gTTS(
                text=translated,
                lang=languages[target_lang]
            )

            tts.save("translated.mp3")

            audio_file = open(
                "translated.mp3",
                "rb"
            )

            st.audio(audio_file.read())

        except:
            st.warning(
                "Audio not available for this language."
            )

# Translation History
st.subheader("📜 Translation History")

for item in reversed(st.session_state.history):
    st.write("Original:", item["Original"])
    st.write("Translated:", item["Translated"])
    st.markdown("---")
