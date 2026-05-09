import unittest

from jarvis_memory.graph import build_graph


class TestJarvisMemoryState(unittest.TestCase):
    def test_graph_runs_to_done(self):
        app = build_graph()
        initial_state = {
            "user_input": "Open YouTube and play a song",
            "messages": [],
            "short_term_memory": [],
            "execution_log": [],
        }

        final_state = app.invoke(initial_state)

        self.assertEqual(final_state["phase"], "done")
        self.assertIn("I completed your request", final_state["response"])
        self.assertTrue(len(final_state["execution_log"]) >= 3)
        self.assertIn("Recent important context", final_state["long_term_summary"])

    def test_multistep_execution_advances(self):
        app = build_graph()
        initial_state = {
            "user_input": "Please summarize my current screen",
            "messages": [],
            "short_term_memory": [],
            "execution_log": [],
        }

        final_state = app.invoke(initial_state)

        self.assertGreaterEqual(final_state["current_step"], 2)
        self.assertIn("Executed action", final_state["tool_result"])


if __name__ == "__main__":
    unittest.main()
