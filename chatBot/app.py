import os 
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

st.set_page_config(page_title = "Gemini Chatbot",page_icon = "Bot")
st.title("Gemini Model based Chatbot")

try:
    llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')
    prompt_template = ChatPromptTemplate.from_template("{input}")
    output_parser = StrOutputParser()
    chat_chain = prompt_template | llm | output_parser

except Exception as e:
    st.error(f"An error occured during initialization : {e}")
    st.stop()
    
if "message" not in st.session_state:
    st.session_state.messages = []
    
    
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        
if prompt := st.chat_input("What would you like to ask?"):
    st.session_state.messages.append({"role" : "user","content" : prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                
                response = chat_chain.invoke({"input" : prompt})
                st.markdown(response)
                st.session_state.messages.append({'role' : 'assistant','content' : response})
                
            except Exception as e :
                st.error(f"An error occured while generating the response : {e}")