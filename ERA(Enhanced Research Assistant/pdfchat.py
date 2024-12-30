import os 
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceEndpoint
from htmlTemplate import css, bot_template, user_template

os.environ['HUGGINGFACEHUB_API_TOKEN']="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"
repoid="mistralai/Mistral-7B-Instruct-v0.2"
key="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"

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings=OpenAIEmbeddings()
    # embeddings=HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device":"cuda"})
    vectorstore=FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore



def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm=HuggingFaceEndpoint(repo_id=repoid,max_length=128,temperature=0.7,token=key)
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain



def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                with st.chat_message("user"):
                    st.write(message.content)
            else:
                with st.chat_message("AI"):
                    st.write(message.content)






def main():
    load_dotenv()
    # st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")
    st.write(css,unsafe_allow_html=True)
         
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
   

    st.header("Chat with multiple PDFs. ")
    st.subheader("Your documents")
    pdf_docs=st.file_uploader("Upload your  PDFs here and click on 'Process'.",accept_multiple_files=True)
    process_button=st.button("Process")
    user_question= st.text_input("Ask any question about your documents ?")
    query_button=st.button("Ask  a question")
    if query_button:
        if user_question:
            handle_userinput(user_question)
    
   
#   with st.sidebar:
    
    if process_button:
        with st.spinner("Processing..."):
            # get the pdf text
            raw_text=get_pdf_text(pdf_docs)
               

            # get the text  chunks
            text_chunks=get_text_chunks(raw_text)

            #create vector Embeddings.
            vectorstore= get_vectorstore(text_chunks)

            # coversation chain
            st.session_state.conversation = get_conversation_chain(vectorstore) 


if __name__ == "__main__":
    main()