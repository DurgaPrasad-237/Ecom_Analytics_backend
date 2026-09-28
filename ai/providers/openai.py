from openai import OpenAI


class OpenAIProvider:

    def __init__(self, api_key):

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = "gpt-5.4-nano"

    def generate(
        self,
        prompt,
        system_instruction=None,
        tools=None,
        chat_history=None,
    ):

        conversation = []

        # Previous conversation
        if chat_history:

            conversation.extend(
                chat_history
            )

        # Current question
        conversation.append({
            "role": "user",
            "content": prompt,
        })

        kwargs = {
            "model": self.model,
            "input": conversation,
        }

        if system_instruction:
            kwargs["instructions"] = system_instruction

        if tools:
            kwargs["tools"] = tools

        return self.client.responses.create(
            **kwargs
        )

    def continue_with_tool_outputs(
        self,
        response_id,
        tool_outputs,
        system_instruction=None,
        tools=None,
    ):

        kwargs = {
            "model": self.model,
            "previous_response_id": response_id,
            "input": tool_outputs,
        }

        if system_instruction:
            kwargs["instructions"] = system_instruction

        if tools:
            kwargs["tools"] = tools

        return self.client.responses.create(
            **kwargs
        )