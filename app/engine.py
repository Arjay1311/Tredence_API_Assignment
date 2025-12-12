import asyncio
import uuid
from typing import Dict, Any, Callable, Optional, List, Union
from .tools import TOOLS
import logging

logger = logging.getLogger("workflow_engine")     # logging
logger.setLevel(logging.INFO)


GRAPHS: Dict[str, Dict[str, Any]] = {}
RUNS: Dict[str, Dict[str, Any]] = {}


NODE_REGISTRY: Dict[str, Callable] = {}

def register_node(name: str):
    def deco(fn):
        NODE_REGISTRY[name] = fn
        return fn
    return deco

def _eval_cond(cond: str, state: Dict[str, Any]) -> bool:
    try:
        return bool(eval(cond, {"__builtins__": {}}, {"state": state}))
    except Exception:
        return False

async def _call_node_fn(fn, state: Dict[str, Any]) -> Dict[str, Any]:
    """call node function, handle async if needed"""
    result = fn(state, TOOLS)
    if asyncio.iscoroutine(result):
        result = await result

    if isinstance(result, dict):
        return result
    return state

def create_graph(graph_id: Optional[str], nodes: Dict[str, str], edges: Dict[str, Union[str, List[Dict[str,str]]]], start_node: str) -> str:
    gid = graph_id or str(uuid.uuid4())
    GRAPHS[gid] = {
        "nodes": nodes, 
        "edges": edges,
        "start_node": start_node
    }
    return gid

def get_next_node(graph: Dict[str, Any], current: str, state: Dict[str, Any]) -> Optional[str]:
    edges = graph["edges"]
    if current not in edges:
        return None
    nxt = edges[current]
    if isinstance(nxt, str):
        return nxt
    
    for entry in nxt:
        cond = entry.get("cond", "False")
        if _eval_cond(cond, state):
            return entry.get("next")
    return None

async def run_graph_sync(graph_id: str, initial_state: Dict[str, Any], max_steps: int = 200) -> Dict[str, Any]:
    logger.info(f"[RUN START] graph_id={graph_id}, initial_state={initial_state}")

    if graph_id not in GRAPHS:
        logger.error(f"[ERROR] Graph {graph_id} not found")
        raise ValueError("graph not found")

    graph = GRAPHS[graph_id]
    state = dict(initial_state)
    log = []

    current = graph["start_node"]
    steps = 0
    run_id = str(uuid.uuid4())

    RUNS[run_id] = {"state": state, "log": log, "status": "running", "current_node": current}

    try:
        while current is not None and steps < max_steps:
            logger.info(f"[NODE START] run={run_id}, node={current}, step={steps}")
            steps += 1

            node_map = graph["nodes"]

            if current not in node_map:
                logger.warning(f"[SKIP] Node '{current}' not defined")
                log.append({"node": current, "status": "skipped", "reason": "node not defined"})
                break

            func_name = node_map[current]

            if func_name not in NODE_REGISTRY:
                logger.warning(f"[SKIP] Function '{func_name}' not registered")
                log.append({"node": current, "status": "skipped", "reason": f"function {func_name} not registered"})
                break

            fn = NODE_REGISTRY[func_name]
            log.append({"node": current, "status": "started"})

            try:
                new_state = await _call_node_fn(fn, state)

                if isinstance(new_state, dict):
                    state.update(new_state)

                logger.info(f"[NODE COMPLETE] node={current}, state={state}")

                log.append({
                    "node": current,
                    "status": "completed",
                    "state_snapshot": dict(state)
                })

            except Exception as e:
                logger.error(f"[NODE ERROR] node={current}, error={e}")
                log.append({"node": current, "status": "error", "error": str(e)})
                RUNS[run_id]["status"] = "error"
                break

            next_node = get_next_node(graph, current, state)
            logger.info(f"[NEXT NODE] {current} → {next_node}")

            if next_node is None or next_node == "END":
                current = None
                break

            current = next_node

        final_status = "completed" if steps < max_steps else "max_steps_reached"

        RUNS[run_id]["state"] = state
        RUNS[run_id]["log"] = log
        RUNS[run_id]["status"] = final_status
        RUNS[run_id]["current_node"] = current

        logger.info(f"[RUN END] run={run_id}, status={final_status}, final_state={state}")

        return {"run_id": run_id, "state": state, "log": log, "status": final_status}

    except Exception as e:
        logger.error(f"[RUN ERROR] {e}")
        RUNS[run_id]["status"] = "error"
        log.append({"error": str(e)})
        raise

