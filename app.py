import streamlit as st
import base64
from tempfile import NamedTemporaryFile
from audiorecorder import audiorecorder
from whispercpp import Whisper
from elevenlabs import voices, generate, save, set_api_key, stream

#######
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#######
import openai

# Download whisper.cpp
#w = Whisper('tiny')

#def inference(audio):
#    # Save audio to a file:
#    with NamedTemporaryFile(suffix=".mp3") as temp:
#        with open(f"{temp.name}", "wb") as f:
#            f.write(audio.tobytes())
#        result = w.transcribe(f"{temp.name}")
#        text = w.extract_text(result)
#    return text[0]

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

# Streamlit
with st.sidebar:
#    audio = audiorecorder("Click to send voice message", "Recording... Click when you're done", key="recorder")
    st.title("Echo Bot with Whisper")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#def stream_write(prompt: str):
#    st.markdown(prompt)
#    for chunk in openai.ChatCompletion.create(
#            model="gpt-3.5-turbo",
#            messages=[{"role": "user", "content": prompt}],
#            stream=True,
#            ):
#        st.markdown(chunk)
#        if (text_chunk:=chunk["choices"][0]["delta"].get("content")) is not None:
#            yield text_chunk

def stream_write(prompt: str):
    st.markdown("TWTWTQW")
    #yield "Hi there "
    return "I'm a helpful assistant "

# React to user input
#if (prompt := st.chat_input("Your message")) or len(audio):
if prompt := st.chat_input("Your message"):
   # If it's coming from the audio recorder transcribe the message with whisper.cpp
#    if len(audio)>0:
#        prompt = inference(audio)

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

#    response = f"{prompt}"
    # Display assistant response in chat message container
    st.write(prompt)
    text_stream = stream_write(prompt)
    with st.chat_message("assistant"):
#        audio = generate(text=f"{response}", voice="Rachel", model="eleven_monolingual_v1")
#        with NamedTemporaryFile(suffix=".mp3") as temp:
#            tempname = temp.name
#            save(audio, tempname)
#            autoplay_audio(tempname)
        st.markdown(prompt)
        audio_stream = generate(
                text = text_stream,
                voice = "Rachel",
                stream=True
                )
        autoplay_audio(audio_stream)
#        with NamedTemporaryFile(suffix=".mp3") as temp:
#            tempname = temp.name
#            save(audio_stream, tempname)
#            autoplay_audio(tempname)

#        output = stream(audio_stream)


    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
