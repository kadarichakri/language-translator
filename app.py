import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

st.set_page_config(page_title="Translator with Speech", layout="centered")

st.title("Language Translator + Speech")

# Language list
languages = {
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "English": "en"
}

# Session state (for clear button)
if "text" not in st.session_state:
    st.session_state.text = ""

if "output" not in st.session_state:
    st.session_state.output = ""

# Input
text = st.text_area("Enter text", value=st.session_state.text)

target_language = st.selectbox("Choose language", list(languages.keys()))

col1, col2, col3 = st.columns(3)

# Translate button
with col1:
    if st.button("Translate"):
        if text.strip() == "":
            st.warning("Enter text first")
        else:
            try:
                translated = GoogleTranslator(
                    source="auto",
                    target=languages[target_language]
                ).translate(text)

                st.session_state.output = translated
            except Exception as e:
                st.error("Error in translation")
                st.write(e)

# Speak button
with col2:
    if st.button("Speak"):
        if st.session_state.output:
            try:
                tts = gTTS(st.session_state.output, lang=languages[target_language])
                audio_file = "speech.mp3"
                tts.save(audio_file)

                audio_bytes = open(audio_file, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")

            except Exception as e:
                st.error("Speech generation failed")
                st.write(e)
        else:
            st.warning("Translate text first")

# Clear button
with col3:
    if st.button("Clear"):
        st.session_state.text = ""
        st.session_state.output = ""
        st.rerun()

# Output display
if st.session_state.output:
    st.success("Translated Text:")
    st.write(st.session_state.output)


