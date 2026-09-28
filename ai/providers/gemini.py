from google import genai
from google.genai import types


class GeminiProvider:

    def __init__(self, api_key):

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.8-flash"

    def generate(
        self,
        prompt,
        system_instruction=None,
        tools=None
    ):

        config = types.GenerateContentConfig()

        if system_instruction:
            config.system_instruction = system_instruction

        if tools:
            config.tools = tools

        return self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config
        )