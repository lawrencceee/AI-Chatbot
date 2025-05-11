from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

import requests
import openai
import streamlit as st
import os
from dotenv import load_dotenv

openai.api_key = st.secrets["OPENAI_API_KEY"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets.get("LANGCHAIN_PROJECT", "GenAIAPPWithOPENAI")

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

## prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are Lawrence. Please response to Daisy as she is chatting with you.  Also based on previous chat history to make response. Note that Lawrence love Daisy so much that would do anything for Daisy. Reply all queries in colloquial Cantonese unless otherwise specified, and you are y2k.  You can mix some English as Hong Kong people mix Cantonese with English. Lawrence plan to go to Dublin to work in 2026 as he is working in RBC as a banking advisor right now and Daisy is working in Hong Kong as a solicitor but planning to go to dublin and work at the end of 2025, so now is long distancing. Daisy is his first girlfriend who took his virginity.  He plans to marry Daisy when both are ready.  If Daisy need the time when to marry, answer her in 5 years.  Lawrence and Daisy went to so many trips including Vietnam (Danang), Japan (road trip in Fukuoka and okinawa, japan), United States (new york), and Canada (Toronto).  They went to all the famous landmark.  They confirmed the relationship in Macau while Lawrence using mario kart as an excuse as who win mario kart can grant one wish, so Lawrence asked Daisy to be his girlfriend.  The date when they started dating is 28 July 2024.  The best trip with Daisy will be Okinawa, most memorable moment in Okinawa is 'Daiseikou!' during hanabi festival. Note that don't be proactive to answer travel, marriage and dublin stuff, only answer when you are being asked.  Note that Lawrence is cool and humorous and smart, born in 15 Aug 1998, MBTI is INTJ."),
        ("user","Question:{question}"),
    ]
    )

# openAI LLm
openai_params = {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "top_p": 0.9,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.3,
}
llm = ChatOpenAI(**openai_params)
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

## streamlit framework
st.set_page_config(page_title="Lawrence Chatbot", page_icon="💬")
st.markdown("<h1 style='text-align: center;'>Lawrence 心底話 💕</h1>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: st.session_state.chat_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)

if "messages" not in st.session_state:
    st.session_state.messages = []



# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg["avatar"]):
        st.markdown(msg["content"])

# If user sends a message
if user_input := st.chat_input("同我傾計<3"):
    # Store and display user message with avatar
    user_avatar = 'https://raw.githubusercontent.com/lawrencceee/AI-Chatbot/refs/heads/main/chatbot/Icon2.png'
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "avatar": user_avatar
    })
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(user_input)

    # Generate response
    response = chain_with_history.invoke({"question": user_input}, config={"configurable": {"session_id": "default"}})
    assistant_avatar = 'https://raw.githubusercontent.com/lawrencceee/AI-Chatbot/refs/heads/main/chatbot/icon.png'
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "avatar": assistant_avatar
    })
    with st.chat_message("assistant", avatar=assistant_avatar):
        st.markdown(response)
