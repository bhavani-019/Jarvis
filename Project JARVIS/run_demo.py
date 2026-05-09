from jarvis_memory import build_graph


def main() -> None:
    app = build_graph()
    initial_state = {
        "user_input": "Look at my screen and summarize the graph",
        "messages": [],
        "short_term_memory": [],
        "execution_log": [],
    }

    final_state = app.invoke(initial_state)

    print("\n=== FINAL RESPONSE ===")
    print(final_state.get("response", "No response"))

    print("\n=== PHASE LOG ===")
    for item in final_state.get("execution_log", []):
        print(item)

    print("\n=== LONG TERM SUMMARY ===")
    print(final_state.get("long_term_summary", "No summary"))


if __name__ == "__main__":
    main()
