
import streamlit as st
# import os
import chatweb
import csvqa
import pdfchat
import pdfqa
import streambot

import streamlit as st

st.set_page_config(
    page_title="Enhanced Research Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Welcome to ERA!")

# Define the pages for the navigation bar
pages = ["Home","ChatPdf", "ChatWeb", "Q&A CSV","Q&A PDF","StreamBot"]

# Create the navigation bar
page = st.sidebar.radio("Navigation Menu", pages)


# Depending on the selected page, you can display different content
if page == "Home":
    st.markdown("<h1 style='text-align: center;'>Enhanced Research Assistant!👨‍💻</h1>", unsafe_allow_html=True)

    st.markdown('<p style="font-size:20px; text-align: center; "> <i>Leveraging Large Language Models to Synthesize Information from PDF, CSV, and Web Data...</i> </p>', unsafe_allow_html=True)
    
    st.markdown('<p style = "font-size:17px;">The project aims to develop an advanced research assistant tool that utilizes Large Language Models (LLMs) to interact with and synthesize information from multiple data sources, including PDF documents, CSV files, and websites. This tool will help researchers efficiently gather and process information from diverse formats, providing comprehensive insights and automated analysis.</p>', unsafe_allow_html=True)
    st.subheader("", divider='rainbow')

    st.markdown("<h1 style='text-align: center;'>Functionalitie's we Provide💡</h1>", unsafe_allow_html=True)
    
    st.markdown('<p style="font-size:25px; text-decoration: underline; "> <i>Streambot</i> </p>', unsafe_allow_html=True)
    st.write("This Streambot is powered by cutting-edge Large Language Models (LLMs), allowing for natural and informative conversations. Ask questions, get summaries of complex topics, or simply have a stimulating discussion. The LLM technology adapts to your conversation, providing insightful responses that go beyond simple keywords. Experience the future of chatbots - intelligent, engaging, and always learning.")

    st.markdown('<p style="font-size:25px; text-decoration: underline; "> <i>ChatPdf</i> </p>', unsafe_allow_html=True)
    st.write("ChatPDF is an AI-powered tool that revolutionizes the way you interact with PDF documents. It uses natural language processing to transform your reading of a PDF document into a dynamic conversation. Simply upload any PDF and start asking it questions, just like you would when chatting with an assistant. This tool is powered by ChatGPT, which is an advanced AI interface. It’s like ChatGPT, but specifically for research papers. This makes reading journal articles easier and faster. It’s a great tool for summarizing a PDF document and understanding everything mentioned in that document. It’s going viral all over the world and is revolutionizing the understanding of research worldwide.")
    
    st.markdown('<p style="font-size:25px; text-decoration: underline; "> <i>ChatWeb</i> </p>', unsafe_allow_html=True)
    st.write("ChatWeb is an online communication platform that enables real-time interaction between businesses and customers. It enhances customer service by providing immediate responses to queries. This tool can significantly improve customer satisfaction and increase business performance. It can incorporate automated chatbots for basic queries and human agents for more complex issues. Overall, ChatWeb is a powerful tool for boosting customer experience and business growth.")
    
    st.markdown('<p style="font-size:25px; text-decoration: underline;"> <i>Q&A CSV</i> </p>', unsafe_allow_html=True)
    st.write("Question and Answer CSV Reader sites are platforms that allow users to upload CSV files containing question and answer data. These sites use advanced algorithms to parse the data and provide an interactive interface for users to query the data. They are particularly useful for researchers and data scientists who work with large datasets and need to extract specific information quickly and efficiently. These platforms often support natural language processing, enabling users to ask questions in plain English and receive accurate answers. Overall, they offer a powerful tool for managing and interacting with question and answer data.")

    st.markdown('<p style="font-size:25px; text-decoration: underline; "> <i>Q&A Pdf</i> </p>', unsafe_allow_html=True)
    st.write("Question and Answer PDF Reader sites are platforms that leverage AI to interact with PDF documents in a conversational manner. Users can upload PDF files and ask questions directly to the document, receiving answers extracted from the text. These platforms use natural language processing to understand the content and provide accurate responses. They are particularly useful for researchers, students, and professionals who need to extract specific information from lengthy documents quickly and efficiently.")
    
    

elif page == "ChatWeb":
    chatweb.main()

elif page == "Q&A CSV":
    csvqa.main()

elif page == "Q&A PDF":
    pdfqa.main()

elif page == "ChatPdf":
    pdfchat.main()

elif page == "StreamBot":
    streambot.main()
