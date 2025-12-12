from fastapi import FastAPI, HTTPException
from .schema import GraphCreate, GraphCreateResp, RunRequest, RunResp, RunStateResp
from .engine import create_graph, GRAPHS, run_graph_sync, RUNS
from .workflows import EXAMPLE_GRAPH_ID
import uvicorn
import logging
logger = logging.getLogger("workflow_api")
logger.setLevel(logging.INFO)


app = FastAPI(title="Mini Workflow Engine")

@app.post("/graph/create", response_model=GraphCreateResp)
def api_create_graph(payload: GraphCreate):
    logger.info(f"[API] Creating graph {payload.graph_id}")
    gid = create_graph(payload.graph_id, payload.nodes, payload.edges, payload.start_node)
    logger.info(f"[API] Graph created id={gid}")
    return {"graph_id": gid}


@app.post("/graph/run", response_model=RunResp)
async def api_run_graph(req: RunRequest):
    logger.info(f"[API] Run request graph_id={req.graph_id}, state={req.initial_state}")

    if req.graph_id not in GRAPHS:
        logger.warning(f"[API ERROR] Graph {req.graph_id} not found")
        raise HTTPException(status_code=404, detail="graph not found")

    result = await run_graph_sync(req.graph_id, req.initial_state, max_steps=req.max_steps)

    logger.info(f"[API] Run completed run_id={result['run_id']}")

    return {"run_id": result["run_id"], "final_state": result["state"], "log": result["log"]}


@app.get("/graph/state/{run_id}", response_model=RunStateResp)
def api_get_run_state(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail="run not found")
    r = RUNS[run_id]
    return {"run_id": run_id, "state": r["state"], "log": r["log"], "status": r["status"], "current_node": r.get("current_node")}

# root
@app.get("/")
def root():
    return {"message": "Mini Workflow Engine. Example graph id: " + EXAMPLE_GRAPH_ID}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

