# JARVIS Memory and State Management (LangGraph)

This module implements your Phase 4 deliverable:
- Explicit agent state flow (`reasoning -> planning -> executing -> responding`)
- Short-term and long-term memory updates
- Context injection helpers for reasoning
- Execution logging for demo/review visibility

## Setup

```bash
python3 -m pip install -r requirements.txt
```

## Run demo

```bash
python3 run_demo.py
```

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

## Integration point

Replace `_mock_tool_executor()` in `jarvis_memory/nodes.py` with your teammate's tool integration function.
