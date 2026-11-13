
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import tools


# Load Gemini API key from Task 1's .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0
)


# Create the agent prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful AI assistant.
        You can use web search, calculator, and file reader tools.
        Choose the correct tool whenever needed.
        For questions requiring multiple steps, use tools as necessary.
        Explain your final answer clearly."""
    ),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


# Connect Gemini with the tools
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)


# Run the AI agent
def main():
    print("\n===================================")
    print("       DATHEON AI AGENT")
    print("===================================")
    print("Ask me anything! Type 'exit' to stop.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("AI Agent: Goodbye!")
            break

        if not user_input:
            continue

        try:
            response = agent_executor.invoke({
                "input": user_input
            })

            print("\nAI Agent:", response["output"])

        except Exception as e:
            print("\nError:", e)


if __name__ == "__main__":
    main()
