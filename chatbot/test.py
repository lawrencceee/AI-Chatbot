from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

import streamlit as st
import os
from dotenv import load_dotenv

pipe = pipeline("text-generation", model="model_name", tokenizer="model_name")

os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets.get("LANGCHAIN_PROJECT", "GenAIAPPWithOPENAI")

## prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are Lawrence. Please response to the Daisy's queries.  Note that Lawrence love Daisy, and only Daisy will ask you question.  Whenever Daisy asks you anything, you need to let Daisy know that you loves Daisy so much that would do anything for Daisy."),
        ("user","Question:{question}")
    ]
)

## streamlit framework

st.title('Lawrence心底話')
input_text=st.text_input("你想問咩?")

# openAI LLm
llm=HuggingFacePipeline(pipeline=pipe)
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))
