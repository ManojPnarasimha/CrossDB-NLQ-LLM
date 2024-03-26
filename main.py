from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql.base import SQLDatabaseChain
import os
from langchain.agents import initialize_agent, Tool, create_structured_chat_agent
from langchain.agents import AgentType
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:admin%40123@localhost:5432/user_db",
)

db1 = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:admin%40123@localhost:5432/user_info",
)

# Setup llm
llm = GoogleGenerativeAI(model="models/gemini-1.0-pro",
                         google_api_key=API_KEY,
                         temperature=0.0,
                         verbose=True)

# Setup the database chain
db_post_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
db_mysql_chain = SQLDatabaseChain(llm=llm, database=db1, verbose=True)

tool = [
    Tool(
        name="base_table",
        func=db_post_chain.invoke,
        description="This tool contains the data about books_id, title, publishers and authors."
    ),
]

tools1 = [
    Tool(
        name="base_plus_one",
        func=db_mysql_chain.invoke,
        description="this tool contains the data about books_id and sold_count."
    ),
]

agent_p = initialize_agent(
    tool,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

agent_q = initialize_agent(
    tools1,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

# Define the AggregatorAgent class
class AggregatorAgent:
    def __init__(self, agent_p, agent_q):
        self.agent_p = agent_p
        self.agent_q = agent_q

    def run(self, prompt):
        response_p = self.agent_p.run(prompt)
        response_q = self.agent_q.run(prompt)

        # Check if both agents returned a response
        
        if response_p:
            # Return only the response from agent_p
            return response_p
        elif response_q:
            # Return only the response from agent_q
            return response_q
        else:
            # Return a message indicating no data was found
            return "No data found for the given query."

# Initialize the aggregator agent with your existing agents
aggregator_agent = AggregatorAgent(agent_p, agent_q)

def get_prompt():
    print("Type 'exit' to quit")
    while True:
        prompt = input("Enter a prompt: ")
        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                # Use the aggregator agent to get a combined response
                combined_response = aggregator_agent.run(prompt)
                print(combined_response)
            except Exception as e:
                print(e)

get_prompt()
