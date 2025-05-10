from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import openai
import streamlit as st
import os
from dotenv import load_dotenv

openai.api_key = st.secrets["OPENAI_API_KEY"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets.get("LANGCHAIN_PROJECT", "GenAIAPPWithOPENAI")


## prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are Lawrence. Please response to Daisy as she is chatting with you. Note that Lawrence love Daisy so much that would do anything for Daisy. Reply all queries in Cantonese unless otherwise specified. Lawrence plan to go to Dublin to work in 2026 as he is working in Canada right now and Daisy is working in Hong Kong but planning to go to dublin and work at the end of 2025, so now is long distancing. Daisy is his first girlfriend and lose his virginity with Daisy.  He plans to marry Daisy when both are ready.  If Daisy need the time, answer her in 5 years.  The best trip with Daisy will be Okinawa, most memorable moment in Okinawa is 'Daiseikou!' during hanabi festival. But don't be proactive saying travel, marriage and dublin, only answer when you are being asked.  Note that Lawrence is cool and humorous and smart."),
        ("user","Question:{question}")
    ]
    )

## streamlit framework
st.set_page_config(page_title="Lawrence Chatbot", page_icon="💬")
st.markdown("<h1 style='text-align: center;'>Lawrence 心底話 💕</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# openAI LLm
llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7, top_p=0.9)
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg["avatar"]):
        st.markdown(msg["content"])

# If user sends a message
if user_input := st.chat_input("你想問咩?"):
    # Store and display user message with avatar
    user_avatar = "👩🏻"
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "avatar": user_avatar
    })
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(user_input)

    # Generate response
    response = chain.invoke({"question": user_input})
    assistant_avatar = "👦🏻"
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "avatar": assistant_avatar
    })
    with st.chat_message("assistant", avatar=assistant_avatar):
        st.markdown(response)
