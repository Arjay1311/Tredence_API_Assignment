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
1. Clone Repo:
`git clone https://github.com/your-username/workflow-engine.git`

2. Install dependencies:
   `pip install fastapi uvicorn pydantic`
   
3. Start the FastAPI server:
   `uvicorn app.main:app --reload`
   
4. Try example:
   
   4.1 **Create the workflow graph:**
   
   - Use the `/graph/create` endpoint in Swagger UI or via POST request.
   - Provide a **graph ID**, **nodes** (mapping of node names to registered functions), **edges** (how nodes connect, including conditions for branching), and **start node**.

   4.2 **Run the workflow**
   
   - Use the `/graph/run` endpoint.
   - Specify the **graph ID** and an **initial state** containing:
     - The code to analyze.
     - Any thresholds, e.g., `quality_threshold`.
   - The server will return a **run ID**, the **final state**, and a **log of all nodes executed**.

   4.3 **Check the workflow state**
   
   - Use the `/graph/state/{run_id}` endpoint.
   - Replace `{run_id}` with the ID returned from the run call.
   - This will show the **current state**, **execution log**, **status**, and the **current node** being executed.


## Output of an Example Run

### 1. POST /graph/create

**Request (Swagger UI / POST call)**  
![POST Graph Create - Request](pics/post%20-%20graph%20-%20create.png)

**Server Response**  
![POST Graph Create - Response](pics/post%20-%20graph%20-%20create%20-%20server_response%20(1).png)

---

### 2. POST /graph/run

**Request (Run the workflow with initial state)**  
![POST Graph Run - Request](pics/post%20-%20graph%20-%20run%20(1).png)

**Server Response**  
![POST Graph Run - Response](pics/post%20-%20graph%20-%20run%20-%20server_response%20(1).png)

---

### 3. GET /graph/state/{run_id}

**Check workflow state using the run ID**  
![GET Graph State - Browser View](pics/get%20-%20graph%20-%20state%20-%20{run%20id}%20(1).png)


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

