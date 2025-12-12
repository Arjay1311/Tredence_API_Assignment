from .engine import register_node, create_graph
from typing import Dict, Any
import asyncio

# Workflow code : Code Review Mini-Agent 
# if you want to change the workflow, modify the nodes and edges here


@register_node("node_extract")
def node_extract(state: Dict[str, Any], tools):
    code = state.get("code", "")
    res = tools["extract_functions"](code)
    return {"tools_extract_functions": res}

@register_node("node_check_complexity")
def node_check_complexity(state: Dict[str, Any], tools):
    funcs = state.get("tools_extract_functions", {}).get("functions", [])
    res = tools["check_complexity"](funcs)
    return {"tools_check_complexity": res}

@register_node("node_detect_issues")
def node_detect_issues(state: Dict[str, Any], tools):
    code = state.get("code", "")
    res = tools["detect_smells"](code)
    return {"tools_detect_smells": res}

@register_node("node_suggest")
def node_suggest(state: Dict[str, Any], tools):
    res = tools["suggest_improvements"](state)
    # remove prints count from state or decrement issues
    issues = state.get("tools_detect_smells", {}).get("issues", 0)
    # "apply" one improvement that reduces issues by 1
    new_issues = max(0, issues - 1)
    # modify underlying detect_smells entry
    t = dict(state.get("tools_detect_smells", {}))
    t["issues"] = new_issues
    res_state = {"tools_detect_smells": t, "tools_suggestions": res}
    return res_state

@register_node("node_score")
def node_score(state: Dict[str, Any], tools):
    res = tools["compute_quality_score"](state)
    return {"tools_quality": res, "quality_score": res.get("quality_score", 0)}

# example graph
def register_example_graph():
    graph_id = "code_review_example"
    nodes = {
        "extract": "node_extract",
        "check": "node_check_complexity",
        "detect": "node_detect_issues",
        "suggest": "node_suggest",
        "score": "node_score"
    }

    edges = {
        "extract": "check",
        "check": "detect",
        "detect": "score",
        "score": [
            {"cond": "state.get('quality_score',0) >= state.get('quality_threshold', 80)", "next": "END"},
            {"cond": "True", "next": "suggest"}
        ],
        "suggest": "check",
    }

    create_graph(graph_id=graph_id, nodes=nodes, edges=edges, start_node="extract")
    return graph_id


EXAMPLE_GRAPH_ID = register_example_graph()  #example graph, subject to change
