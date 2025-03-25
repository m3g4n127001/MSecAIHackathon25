import autogen
import json

# Load data from JSON file
def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

data = load_data()

# Function to filter data.json based on the query
def filter_data(query: str) -> str:
    query = query.lower()

    if "criticality" in query and "very high" in query:
        results = [entry for entry in data if entry.get('Criticality') == 'Very High']
        return json.dumps(results, indent=2) if results else "No users found with criticality level 'Very High'."

    if "role" in query:
        role_query = query.split("role ")[-1].strip()
        results = [entry for entry in data if role_query.lower() in entry.get('Role', '').lower()]
        return json.dumps(results, indent=2) if results else f"No users found with role '{role_query}'."

    return "Sorry, I couldn't understand your query."

class DataAgent:
    def __init__(self, llmConfig: list[dict[str, any]]):
        self.llmConfig = llmConfig

    def runUserGoal(self, user_query):
        # Initialize AssistantAgent with data-specific capabilities
        assistant = autogen.AssistantAgent(
            name="DataAgent",
            system_message="You are an assistant that specializes in answering questions about identity data.",
            llm_config={
                "config_list": self.llmConfig,
            }
        )

        # Register filter logic as a function
        assistant.register_for_llm(name="filter_data", description="Filter data.json based on user queries.")(filter_data)

        # User agent setup
        user = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False}
        )

        # Register function for query processing
        user.register_for_execution(name="filter_data")(filter_data)

        # Initiate chat with the assistant
        response = user.initiate_chat(assistant, message=user_query, max_turns=3)
        return response

