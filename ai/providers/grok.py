from openai import OpenAI


class GrokProvider:

    def __init__(self, api_key):

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )

        self.model = "grok-4.7"

    def generate(
        self,
        prompt,
        system_instruction=None,
        tools=None
    ):

        messages = []

        if system_instruction:

            messages.append({
                "role": "system",
                "content": system_instruction
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        kwargs = {
            "model": self.model,
            "messages": messages
        }

        if tools:
            kwargs["tools"] = tools

        return self.client.chat.completions.create(
            **kwargs
        )