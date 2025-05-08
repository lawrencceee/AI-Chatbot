from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import openai
import streamlit as st
import os
from dotenv import load_dotenv

openai.api_key = os.getenv("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")
## Langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assitant. Please response to the user queries.  Note that Lawrence love Daisy, and this query is sending to Daisy only.  Whenever Daisy asks anything about Lawrence, you need to let Daisy know that Lawrence loves Daisy so much that would do anything for Daisy."),
        ("user","Question:{question}")
    ]
)

## streamlit framework

st.title('Lawrence心底話')
input_text=st.text_input("你想問咩?")

# openAI LLm
llm=ChatOpenAI(model="gpt-3.5-turbo")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))