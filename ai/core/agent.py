import json

from ai.providers import (
    OpenAIProvider,
    GeminiProvider,
    GrokProvider,
)

from ai.customer.tools import (
    CUSTOMER_TOOLS,
    CUSTOMER_TOOL_FUNCTIONS,
)

from ai.customer.prompts import (
    INSTRUCTION_CONTENT as CUSTOMER_INSTRUCTION_CONTENT,
    ANSWER_INSTRUCTION as CUSTOMER_ANSWER_INSTRUCTION,
    INSIGHT_INSTRUCTION as CUSTOMER_INSIGHT_INSTRUCTION,
)

from ai.product.tools import (
    PRODUCT_TOOLS,
    PRODUCT_TOOL_FUNCTIONS,
)

from ai.product.prompts import (
    INSTRUCTION_CONTENT as PRODUCT_INSTRUCTION_CONTENT,
    ANSWER_INSTRUCTION as PRODUCT_ANSWER_INSTRUCTION,
    INSIGHT_INSTRUCTION as PRODUCT_INSIGHT_INSTRUCTION,
)

from ai.sales.tools import (
    SALES_TOOLS,
    SALES_TOOL_FUNCTIONS,
)

from ai.sales.prompts import (
    INSIGHT_INSTRUCTION as SALES_INSIGHT_INSTRUCTION,
    ANSWER_INSTRUCTION as SALES_ANSWER_INSTRUCTION,
    INSTRUCTION_CONTENT as SALES_INSTRUCTION_CONTENT
    
)
from ai.demandforecasting.tools import (
    DEMAND_FORECASTING_TOOLS,
    DEMAND_FORECASTING_TOOL_FUNCTIONS,
)

from ai.demandforecasting.prompts import (
    INSTRUCTION_CONTENT as DEMAND_FORECASTING_INSTRUCTION_CONTENT,
    ANSWER_INSTRUCTION as DEMAND_FORECASTING_ANSWER_INSTRUCTION,
    INSIGHT_INSTRUCTION as DEMAND_FORECASTING_INSIGHT_INSTRUCTION,
)

from ai.inventory_planning.tools import (
    INVENTORY_PLANNING_TOOLS,
    INVENTORY_PLANNING_TOOL_FUNCTIONS,
)

from ai.inventory_planning.prompts import (
    INSTRUCTION_CONTENT as INVENTORY_PLANNING_INSTRUCTION_CONTENT,
    ANSWER_INSTRUCTION as INVENTORY_PLANNING_ANSWER_INSTRUCTION,
    INSIGHT_INSTRUCTION as INVENTORY_PLANNING_INSIGHT_INSTRUCTION,
)

class Agent:

    def __init__(
        self,
        openai_api_key=None,
        gemini_api_key=None,
        grok_api_key=None,
        domain="customer",
    ):

        self.domain = domain

        self.providers = {}

        if openai_api_key:
            self.providers["openai"] = OpenAIProvider(
                openai_api_key
            )

        if gemini_api_key:
            self.providers["gemini"] = GeminiProvider(
                gemini_api_key
            )

        if grok_api_key:
            self.providers["grok"] = GrokProvider(
                grok_api_key
            )

    # -------------------------------------------------------
    # DOMAIN CONFIGURATION
    # -------------------------------------------------------

    def get_domain_config(self):

        if self.domain == "customer":

            return {
                "tools": CUSTOMER_TOOLS,
                "tool_functions": CUSTOMER_TOOL_FUNCTIONS,
                "instruction": CUSTOMER_INSTRUCTION_CONTENT,
                "answer_instruction": CUSTOMER_ANSWER_INSTRUCTION,
                "insight_instruction": CUSTOMER_INSIGHT_INSTRUCTION,
            }

        elif self.domain == "product":

            return {
                "tools": PRODUCT_TOOLS,
                "tool_functions": PRODUCT_TOOL_FUNCTIONS,
                "instruction": PRODUCT_INSTRUCTION_CONTENT,
                "answer_instruction": PRODUCT_ANSWER_INSTRUCTION,
                "insight_instruction": PRODUCT_INSIGHT_INSTRUCTION,
            }

        elif self.domain == "sales":

            return {
                "tools": SALES_TOOLS,
                "tool_functions": SALES_TOOL_FUNCTIONS,
                "instruction": SALES_INSTRUCTION_CONTENT,
                "answer_instruction": SALES_ANSWER_INSTRUCTION,
                "insight_instruction": SALES_INSIGHT_INSTRUCTION,
            }

        elif self.domain == "demandforecast":

            return {
                "tools": DEMAND_FORECASTING_TOOLS,
                "tool_functions": DEMAND_FORECASTING_TOOL_FUNCTIONS,
                "instruction": DEMAND_FORECASTING_INSTRUCTION_CONTENT,
                "answer_instruction": DEMAND_FORECASTING_ANSWER_INSTRUCTION,
                "insight_instruction": DEMAND_FORECASTING_INSIGHT_INSTRUCTION,
            }

        elif self.domain == "inventory_planning":

            return {
                "tools": INVENTORY_PLANNING_TOOLS,
                "tool_functions": INVENTORY_PLANNING_TOOL_FUNCTIONS,
                "instruction": INVENTORY_PLANNING_INSTRUCTION_CONTENT,
                "answer_instruction": INVENTORY_PLANNING_ANSWER_INSTRUCTION,
                "insight_instruction": INVENTORY_PLANNING_INSIGHT_INSTRUCTION,
            }

        else:

            raise ValueError(
                f"Unsupported analytics domain: {self.domain}"
            )

    # -------------------------------------------------------
    # PROVIDER
    # -------------------------------------------------------

    def get_provider(self, provider):

        if provider not in self.providers:

            raise ValueError(
                f"Provider '{provider}' is not configured."
            )

        return self.providers[provider]

    # -------------------------------------------------------
    # INSIGHT DETECTION
    # -------------------------------------------------------

    def wants_insights(self, question):

        keywords = [
            "insight",
            "insights",
            "why",
            "reason",
            "reasons",
            "pattern",
            "patterns",
            "trend",
            "trends",
            "recommend",
            "recommendation",
            "recommendations",
            "suggest",
            "suggestion",
            "suggestions",
            "business",
            "analysis",
            "analyze",
            "explain",
        ]

        question_lower = question.lower()

        return any(
            keyword in question_lower
            for keyword in keywords
        )

    # -------------------------------------------------------
    # SYSTEM INSTRUCTION
    # -------------------------------------------------------

    def build_instruction(self, question):

        config = self.get_domain_config()

        if self.wants_insights(question):

            specific_instruction = (
                config["insight_instruction"]
            )

        else:

            specific_instruction = (
                config["answer_instruction"]
            )

        return (
            config["instruction"]
            + "\n\n"
            + specific_instruction
        )

    # -------------------------------------------------------
    # TOOL EXECUTION
    # -------------------------------------------------------

    def execute_tool(
        self,
        tool_name,
        arguments,
    ):

        config = self.get_domain_config()

        tool_functions = config["tool_functions"]

        if tool_name not in tool_functions:

            return {
                "error": f"Unknown tool: {tool_name}"
            }

        try:
            print("TOOL NAME:", tool_name)
            print("TOOL ARGUMENTS:", arguments)
            function = tool_functions[
                tool_name
            ]

            result = function(
                **arguments
            )

            return result

        except Exception as e:

            return {
                "error": str(e)
            }

    # -------------------------------------------------------
    # OPENAI
    # -------------------------------------------------------

    def _ask_openai(
        self,
        question,
        instruction,
        chat_history=None,
    ):

        provider = self.get_provider("openai")

        config = self.get_domain_config()

        tools = config["tools"]

        response = provider.generate(
            prompt=question,
            system_instruction=instruction,
            tools=tools,
            chat_history=chat_history,
        )

        # ---------------------------------------------------
        # TOOL LOOP
        # ---------------------------------------------------

        while True:

            tool_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not tool_calls:

                return {
                    "answer": response.output_text,
                    "insights": (
                        response.output_text
                        if self.wants_insights(question)
                        else ""
                    ),
                }

            tool_outputs = []

            for call in tool_calls:

                tool_name = call.name

                arguments = json.loads(
                    call.arguments
                )

                result = self.execute_tool(
                    tool_name,
                    arguments,
                )

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(
                        result,
                        default=str,
                    ),
                })

            response = (
                provider.continue_with_tool_outputs(
                    response_id=response.id,
                    tool_outputs=tool_outputs,
                    system_instruction=instruction,
                    tools=tools,
                )
            )

    # -------------------------------------------------------
    # PUBLIC ASK
    # -------------------------------------------------------

    def ask(
        self,
        question,
        provider="openai",
        chat_history=None,
    ):

        instruction = self.build_instruction(
            question
        )

        if provider == "openai":

            return self._ask_openai(
                question=question,
                instruction=instruction,
                chat_history=chat_history,
            )

        if provider == "gemini":

            llm = self.get_provider("gemini")

            response = llm.generate(
                prompt=question,
                system_instruction=instruction,
            )

            return {
                "answer": response.text,
                "insights": (
                    response.text
                    if self.wants_insights(question)
                    else ""
                ),
            }

        if provider == "grok":

            llm = self.get_provider("grok")

            response = llm.generate(
                prompt=question,
                system_instruction=instruction,
            )

            return {
                "answer": (
                    response.choices[0]
                    .message.content
                ),
                "insights": (
                    response.choices[0]
                    .message.content
                    if self.wants_insights(question)
                    else ""
                ),
            }

        raise ValueError(
            f"Unsupported provider: {provider}"
        )