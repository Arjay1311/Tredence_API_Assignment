# Workflow Engine

## What it is
A compact workflow/agent engine that supports:
- Nodes as Python functions (sync/async)
- Shared state (dict) flowing across nodes
- Edges with conditional branching
- Simple looping
- Tools registry (callable helpers)
- FastAPI endpoints to create graphs, run them, and query run state

For this **Workflow Engine Code Review Mini Agent** is used as Workflow.

## Files
- app/main.py - FastAPI endpoints
- app/engine.py - core graph engine
- app/tools.py - simple tool functions & registry
- app/workflows.py - example nodes + registers example graph
- app/schemas.py - Pydantic request/response models

## How to Run
1. Install:
   `pip install fastapi uvicorn pydantic
2. Start:
   `uvicorn app.main:app --reload
3. Try example:
   POST to `/graph/run` with graph_id `code_review_example` and an initial state containing `code` and `quality_threshold`.

## What the workflow engine supports
- Node functions (sync/async)
- Conditional branching via Python expressions
- Loops via routing edges back to earlier nodes
- Tool registry for reusable helper functions
- Run logging and basic run state querying

## What I'd improve with more time
- Replace `eval` with a safe expression evaluator
- Background/asynchronous run (start run -> return run_id; stream logs via WebSocket)
- Persistent storage (SQLite/Postgres) for graphs and runs, instead of in-memory storage
- Authentication + multi-tenant graphs
- Better error handling and structured logging

