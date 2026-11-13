
import os
import asyncio
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from tools import tools


# -------------------------------------------------
# 1. PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="DAtheon AI Chat Assistant",
    page_icon="🤖",
    layout="centered"
)


# -------------------------------------------------
# 2. LOAD GEMINI API KEY
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR.parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()


# -------------------------------------------------
# 3. INITIALIZE GEMINI MODEL
# -------------------------------------------------

@st.cache_resource
def create_agent():

    llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0,
    streaming=True
)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a helpful AI assistant.

            You can use these tools:
            1. Web Search
            2. Calculator
            3. Local File Reader

            Select the appropriate tools whenever required.
            Explain your answers clearly."""
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )


agent_executor = create_agent()


# -------------------------------------------------
# 4. SESSION STATE
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------------------------------------
# 5. APPLICATION HEADER
# -------------------------------------------------

st.title("🤖 DAtheon AI Chat Assistant")

st.write(
    "Ask questions, perform calculations, "
    "search the web, and read local files."
)

st.caption("Powered by Python, Streamlit, LangChain and Gemini")

st.divider()


# -------------------------------------------------
# 6. DISPLAY CHAT HISTORY
# -------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])




# -------------------------------------------------
# 7. CHAT INPUT AND STREAMING RESPONSE
# -------------------------------------------------

if user_input := st.chat_input("Ask me anything..."):

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:

            async def token_stream():

                async for event in agent_executor.astream_events(
                    {
                        "input": user_input,
                        "chat_history": st.session_state.chat_history
                    },
                    version="v2"
                ):

                    if event.get("event") == "on_chat_model_stream":

                        chunk = event.get("data", {}).get("chunk")
                        content = getattr(chunk, "content", "")

                        if isinstance(content, str):
                            if content:
                                yield content

                        elif isinstance(content, list):
                            for part in content:
                                if isinstance(part, dict) and part.get("type") == "text":
                                    text_part = part.get("text", "")
                                    if text_part:
                                        yield text_part

            # Display genuine token streaming
            async def display_stream():

                collected_tokens = []

                async for token in token_stream():
                    collected_tokens.append(token)

                    response_placeholder.markdown(
                        "".join(collected_tokens) + "▌"
                    )

                return "".join(collected_tokens)

            answer = asyncio.run(display_stream())

            if not answer:
                answer = "Sorry, I couldn't generate a response. Please try again."

            response_placeholder.markdown(answer)

            # Save conversation
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.session_state.chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=answer)
            ])

        except Exception as error:
            st.exception(error)


# -------------------------------------------------
# 8. SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write("DAtheon Internship - Task 4")

    st.write("Available Tools:")

    st.write("- 🔎 Web Search")
    st.write("- 🧮 Calculator")
    st.write("- 📄 Local File Reader")

    st.divider()

    if st.button("Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.chat_history = []

        st.rerun()

