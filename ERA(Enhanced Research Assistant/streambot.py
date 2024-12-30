import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

# app config


def get_response(user_query, message_history):

    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {message_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "message_history": message_history,
        "user_question": user_query,
    })
def main():
    
    st.title("Streaming bot")

    # session state
    
    if "message_history" not in st.session_state:
        st.session_state.message_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?"),
        ]

    
    # conversation
    

    for message in st.session_state.message_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # user input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        st.session_state.message_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = st.write_stream(get_response(user_query, st.session_state.message_history))

        st.session_state.message_history.append(AIMessage(content=response))


if __name__ == "__main__":
     main()
