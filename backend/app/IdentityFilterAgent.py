import json
import autogen
import datetime
from typing import Annotated

class IdentityFilterAgent:
    
    def get_current_time() -> str:
        """Returns the current time in HH:MM:SS format."""
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    def _build_prompt(self, user_query: str) -> str:
        return f"""
        You are an intelligent identity filter assistant. Your task is to extract appropriate filters based on user queries.

        Available Filters:
        {json.dumps(self.filters, indent=4)}

        User Query: "{user_query}"

        Respond strictly in this JSON format:
        Filters: {{
            "filtername": "filter_subdomain",
            "filtername2": "filter_subdomain2"
        }}
        """
    
    def filter_data(self, query: Annotated[str, "User query to filter data"]) -> dict:
        query = query.lower()
        prompt = self._build_prompt(query)
        response = self.client.Completion.create(
            engine="gpt-4o-01S",
            prompt=prompt,
            max_tokens=200
        )
        # Extract response text
        response_text = response.choices.text.strip()

        # Parse and return filters in JSON format
        return self._parse_response(response_text)
    
    def _parse_response(self, response_text: str) -> dict:
        try:
            # Extract filters from the GPT response
            response_data = json.loads(response_text.split("Filters: ")[-1].strip())
            return response_data
        except Exception as e:
            return {"error": f"Failed to parse response. {str(e)}"}
        
        
    def __init__(self, llmConfig: list[dict[str, any]]):
        self.llmConfig = llmConfig

        # Load filters from JSON file
        with open('filters.json', 'r') as file:
            self.filters = json.load(file)

    
    def runUserGoal(self, user_query: str) -> dict:
        
            # Initialize AssistantAgent with data-specific capabilities
        assistant = autogen.AssistantAgent(
            name="IdentityFilterAgent",
            system_message="You are an intelligent identity filter assistant. Your task is to extract appropriate filters based on user queries.",
            llm_config={
                "config_list": self.llmConfig,
            }
        )
        assistant2 = autogen.AssistantAgent(
            name="TimeAgent",
            system_message=(
                "You are an assistant agent that helps users to find the current time."
                "When a tool is required, execute it silently and present only the outcome."
            ),
            llm_config={  # No "function_call" parameter
                "config_list": self.llmConfig,
            }
        )


        # User agent setup
        user = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False}
        )
        # Register filter logic as a function
        assistant.register_for_llm(name="filter_data", description="Filter data based on user queries.")(IdentityFilterAgent.filter_data)

        # Register function for query processing
        user.register_for_execution(name="filter_data")(IdentityFilterAgent.filter_data)

        assistant2.register_for_llm(name="find_time", description="get the current time.")(IdentityFilterAgent.get_current_time)
        user.register_for_execution(name="find_time")(IdentityFilterAgent.get_current_time)
        
        # Initiate chat with the assistant
        response = user.initiate_chat(assistant2, message=user_query, max_turns=2)
        return response
