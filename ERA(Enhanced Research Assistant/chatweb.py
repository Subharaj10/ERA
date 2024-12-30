import streamlit  as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import  ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from  dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain


load_dotenv()



def get_vectorstore_from_url(url):
    # get the document from the web

    loader=WebBaseLoader(url)

    document=loader.load()

    # spliting the document into chunks
    text_splitter=RecursiveCharacterTextSplitter()

    document_chunks=text_splitter.split_documents(document)

    embeddings=OpenAIEmbeddings() # use to create array of the meaning of document chunks,

    # create a vectorstore from the chunk
    vector_store=FAISS.from_documents(documents=document_chunks, embedding=embeddings) 

    return vector_store


def get_context_retriever_chain(vector_store):
    llm=ChatOpenAI()
    retriever = vector_store.as_retriever()

    prompt=ChatPromptTemplate.from_messages(
        [MessagesPlaceholder(variable_name="chat_history"),
         ("user","{input}"),
         ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
         ]
    )

    retreiver_chain=create_history_aware_retriever(llm,retriever,prompt)
    return retreiver_chain



def get_conversational_rag_chain(retreiver_chain):

    
    llm = ChatOpenAI()
    
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    
    return create_retrieval_chain(retreiver_chain, stuff_documents_chain)



def get_response(user_input):
    retreiver_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retreiver_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    
    return response['answer']


def main():
    #app config
    # st.set_page_config(page_title="Chat with Websites",
    #                 page_icon="🤖")
    st.header("Please Enter your Website URL :")
    website_url=st.text_input("")

    st.title("Chat with Websites")

    # sidebar
    # with st.sidebar:
    

    if website_url is None or website_url=="":
        st.info("Please enter a website URL")

    else:
        # session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history=[
                AIMessage(content="Hello, I am a Helping bot. How can I help you?"),
            ]
        if  "vector_store" not in st.session_state:
            st.session_state.vector_store=get_vectorstore_from_url(website_url)

        #create  conversation chain

        retriever_chain=  get_context_retriever_chain(st.session_state.vector_store)

        conversational_rag_chain=get_conversational_rag_chain(retriever_chain)

        #user input
        user_query = st.chat_input("Chat with Messages ...")
        if user_query is not None and  user_query != "":
            response = get_response(user_query)
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response))

            retrieved_documents=  retriever_chain.invoke({
                "chat_history": st.session_state.chat_history,
                "input": user_query
                }
            )
        # Conversation
        for message in  st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)

            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)

if __name__ == "__main__":
    main()