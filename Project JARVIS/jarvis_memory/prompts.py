REASONING_PROMPT_TEMPLATE = """
You are JARVIS reasoning controller.
Use user input and memory context to infer intent.
Return one short intent label.

User input:
{user_input}

Context:
{context}
""".strip()


PLANNING_PROMPT_TEMPLATE = """
You are JARVIS planner.
Create a short, ordered plan with action steps.
""".strip()
