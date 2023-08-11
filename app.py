import os
import openai
import streamlit as st
import base64
from tempfile import NamedTemporaryFile
from audiorecorder import audiorecorder
from whispercpp import Whisper
from elevenlabs import voices, generate, save, set_api_key, stream
from thispersondoesnotexist import get_online_person, save_picture
#######
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())
#######
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

example1 = "Give me a haiku about AI"
example2 = "A one-sentence relaxing speech"

# Streamlit
with st.sidebar:
    audio = audiorecorder("Click to send voice message", "Recording... Click when you're done", key="recorder")
    st.title("AI Assistant")
    st.image("a_beautiful_person.jpeg", width=200)
    if st.button("Generate a new Image"):
        picture = get_online_person()
        save_picture(picture, "a_beautiful_person.jpeg")
        st.experimental_rerun()
    st.subheader("Examples:")
    Example1 = st.button(example1)
    Example2 = st.button(example2)
    prompt_user = "You are a helpful AI assistant."
    voice_name = st.selectbox(
    'Voice',
    ('Rachel', 'Adam', 'Dorothy', 'Daniel'))
    language = st.radio(
    "Language",
    ('English', 'Other'))
    prompt_received = st.text_area("Give instructions to your AI assistant (optional):", max_chars=2000)
    if len(prompt_received)>0:
        prompt_user = prompt_received
    prompt_1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
    prompt_user),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

    st.subheader("Current instructions:\n\n"+f":blue[{prompt_user}]")



from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                 streaming=True,
                 temperature=.7)

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)


memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt_1, llm=llm)

# Download whisper.cpp
w = Whisper('tiny')

def inference(audio):
    # Save audio to a file:
    with NamedTemporaryFile(suffix=".mp3") as temp:
        with open(f"{temp.name}", "wb") as f:
            f.write(audio.tobytes())
        result = w.transcribe(f"{temp.name}")
        text = w.extract_text(result)
    return text[0]

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




# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if (prompt := st.chat_input("Your message")) or len(audio) or Example1 or Example2:
    if Example1:
        prompt = example1
    if Example2:
        prompt = example2

#if prompt := st.chat_input("Your message"):
   # If it's coming from the audio recorder transcribe the message with whisper.cpp
    if len(audio)>0:
        prompt = inference(audio)

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = conversation.predict(input=prompt)
    #response = f"{prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        model_name = "eleven_monolingual_v1" if language == "English" else "eleven_multilingual_v1"
        audio = generate(text=f"{response}", voice=voice_name, model=model_name)
        with NamedTemporaryFile(suffix=".mp3") as temp:
            tempname = temp.name
            save(audio, tempname)
            autoplay_audio(tempname)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
