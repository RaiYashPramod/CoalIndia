import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

def main():
    # Get Groq API key
    groq_api_key = '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'

    # Set up Streamlit interface
    st.title("CoalIndia Chatbot!")
    st.sidebar.title('Customization')

    # Add customization options to the sidebar
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )

    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value=5)
    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    # Chat history array to store last 10 messages
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.chat_input("Ask a question:")

    # Display last 10 messages in chat UI
    for message in st.session_state.chat_history[-10:]:
        st.chat_message(f"User").markdown(message['human'])
        st.chat_message("CoalExpert").markdown(message['AI'])
        

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)
    conversation = ConversationChain(llm=groq_chat, memory=memory)

    # If the user has asked a question
    if user_question:
        # The chatbot's answer is generated by sending the full prompt to the Groq API
        response = conversation(user_question)
        message = {'human': user_question, 'AI': response['response']}
        st.session_state.chat_history.append(message)
        st.chat_message(f"User").markdown(message['human'])
        st.write("Chatbot:", response['response'])

if __name__ == "__main__":
    main()
