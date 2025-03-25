import json
import autogen

class FilterAgent:
    def __init__(self, llmConfig: list[dict[str, any]]):
        self.llmConfig = llmConfig
        # Load filters from filters.json
        with open("filters.json", "r") as f:
            self.filters = json.load(f)

    def runUserGoal(self, user_query: str):
        # Define the assistant agent
        assistant = autogen.AssistantAgent(
            name="FilterAgent",
            system_message=(
                "You are an intelligent identity filter assistant. Your task is to extract appropriate filters based on user queries.\n\n"
                f"Available Filters:\n{json.dumps(self.filters, indent=4)}\n\n"
                f"User Query: \"{user_query}\"\n\n"
                "Respond strictly in this JSON format:\n"
                "Filters: {\n"
                "    \"filtername\": \"filter_subdomain\",\n"
                "    \"filtername2\": \"filter_subdomain2\"\n"
                "}"
            ),
            llm_config={"config_list": self.llmConfig},
        )

        # Generate a response directly
        response = assistant.generate_reply(
            messages=[{"role": "user", "content": user_query}]
        )
        return response