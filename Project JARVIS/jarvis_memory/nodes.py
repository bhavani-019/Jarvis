from __future__ import annotations

from .memory import (
    append_execution_log,
    build_context_for_reasoning,
    summarize_long_term_memory,
    update_short_term_memory,
)
from .state import JarvisState


def _mock_tool_executor(action: str, target: str) -> str:
    """
    Placeholder tool runner.
    Replace this with teammate's real tool integration function.
    """
    return f"Executed action='{action}' on target='{target}'"


def reason_node(state: JarvisState) -> JarvisState:
    state["phase"] = "reasoning"
    context = build_context_for_reasoning(state)
    user_input = state.get("user_input", "").lower()

    if "summarize" in user_input:
        intent = "summarize_content"
    elif "open" in user_input or "play" in user_input:
        intent = "open_or_play"
    elif "suggest" in user_input:
        intent = "advice_request"
    else:
        intent = "general_assistance"

    state["intent"] = intent
    append_execution_log(state, f"[reasoning] intent={intent}")
    update_short_term_memory(
        state,
        {"type": "reasoning", "content": f"Intent: {intent}. Context used: {context}"},
    )
    return state


def plan_node(state: JarvisState) -> JarvisState:
    state["phase"] = "planning"
    intent = state.get("intent", "general_assistance")

    if intent == "summarize_content":
        plan = [
            {"action": "capture_screen", "target": "current_screen"},
            {"action": "summarize_text", "target": "captured_content"},
        ]
    elif intent == "open_or_play":
        plan = [{"action": "open_app_or_site", "target": state.get("user_input", "")}]
    elif intent == "advice_request":
        plan = [{"action": "generate_suggestions", "target": state.get("user_input", "")}]
    else:
        plan = [{"action": "answer_directly", "target": state.get("user_input", "")}]

    state["plan"] = plan
    state["current_step"] = 0
    append_execution_log(state, f"[planning] steps={len(plan)}")
    update_short_term_memory(state, {"type": "planning", "content": f"Plan created: {plan}"})
    return state


def execute_node(state: JarvisState) -> JarvisState:
    state["phase"] = "executing"
    plan = state.get("plan", [])
    current = state.get("current_step", 0)

    if current >= len(plan):
        state["tool_result"] = "No steps left to execute."
        append_execution_log(state, "[executing] no-op, plan already completed")
        return state

    step = plan[current]
    result = _mock_tool_executor(step["action"], step["target"])
    state["tool_result"] = result
    state["current_step"] = current + 1

    append_execution_log(state, f"[executing] step={current + 1}/{len(plan)} result={result}")
    update_short_term_memory(state, {"type": "execution", "content": result})
    return state


def respond_node(state: JarvisState) -> JarvisState:
    state["phase"] = "responding"
    result = state.get("tool_result", "No result generated.")
    state["response"] = f"I completed your request. Latest result: {result}"

    messages = list(state.get("messages", []))
    if state.get("user_input"):
        messages.append({"role": "user", "content": state["user_input"]})
    messages.append({"role": "assistant", "content": state["response"]})
    state["messages"] = messages

    update_short_term_memory(state, {"type": "response", "content": state["response"]})
    summarize_long_term_memory(state)
    append_execution_log(state, "[responding] response generated and memory updated")
    state["phase"] = "done"
    return state
