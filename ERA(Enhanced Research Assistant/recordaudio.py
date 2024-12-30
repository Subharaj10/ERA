import streamlit as st
import speech_recognition as sr

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.text("Listening...")
        audio = r.listen(source)
        try:
            st.text("Recognizing...")
            text = r.recognize_google(audio)
            return text
        except:
            st.text("Sorry, I did not get that")
            return ""

def main():
    st.title("Speech to Text")
    if st.button("Speak"):
        text = record_audio()
        st.text("Text: "+text)

if __name__ == "__main__":
    main()
