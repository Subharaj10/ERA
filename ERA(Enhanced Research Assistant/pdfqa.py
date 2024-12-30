from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from recordaudio import record_audio

os.environ['OPENAI_API_KEY'] = "sk-proj-FYOWwZzLmg1bXbdtvAbGT3BlbkFJli0DaVTavhvOs3obgapF"
os.environ['HUGGINGFACEHUB_API_TOKEN']="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"
repoid="mistralai/Mistral-7B-Instruct-v0.2"
key="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"

def main():
    load_dotenv()
    # st.set_page_config(page_title="Ask your Pdf")
    st.header("Ask your PDF💬")
    # upload the pdf file
    pdf=st.file_uploader("Upload your PDF",type="pdf")

    # extract the text from the file
    if pdf is not None:
        pdf_reader=PdfReader(pdf)
        text=""
        for page in pdf_reader.pages:
            text+=page.extract_text()
        
    # spiliting into chuncks
        text_splitter=CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
        
        chunks = text_splitter.split_text(text)

        # Create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base=FAISS.from_texts(chunks,embeddings)

         # show user input
        user_question = st.text_input("Ask a question about your PDF:")
        audio_button=st.button("record audio")
        if audio_button:
            audio_query=record_audio()
            user_question = audio_query
        st.write(user_question)
        if user_question:
            docs = knowledge_base.similarity_search(user_question)



            llm = OpenAI()
            # llm=HuggingFaceEndpoint(repo_id=repoid,max_length=128,temperature=0.7,token=key)
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs,question=user_question)
            print(cb)
           
            st.write(response)
        
if __name__=='__main__':
    main()