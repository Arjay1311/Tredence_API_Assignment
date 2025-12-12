
from typing import Dict, Any

def extract_functions(code: str) -> Dict[str, Any]:
    lines = code.splitlines()
    funcs = []
    for l in lines:
        lstr = l.strip()
        if lstr.startswith("def "):
            name = lstr.split("(")[0].replace("def ", "").strip()
            funcs.append(name)
    return {"functions": funcs, "count": len(funcs)}

def check_complexity(funcs: list) -> Dict[str, Any]:
    # complexity logic
    complexities = {f: len(f) + 1 for f in funcs}
    total = sum(complexities.values())
    return {"complexities": complexities, "total_complexity": total}

def detect_smells(code: str) -> Dict[str, Any]:
    # counting TODO, long lines, prints
    issues = 0
    lines = code.splitlines()
    long_lines = sum(1 for l in lines if len(l) > 120)
    todos = sum(1 for l in lines if "TODO" in l or "FIXME" in l)
    prints = sum(1 for l in lines if "print(" in l)
    issues = long_lines + todos + prints
    return {"issues": issues, "long_lines": long_lines, "todos": todos, "prints": prints}

def suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    # sample improvements
    suggestions = []
    if state.get("tools_detect_smells", {}).get("issues", 0) > 0:
        suggestions.append("Remove debug prints and TODOs; shorten long lines.")
    if state.get("tools_check_complexity", {}).get("total_complexity", 0) > 10:
        suggestions.append("Consider refactoring large functions into smaller ones.")
    return {"suggestions": suggestions}

def compute_quality_score(state: Dict[str, Any]) -> Dict[str, Any]:
    issues = state.get("tools_detect_smells", {}).get("issues", 0)
    complexity = state.get("tools_check_complexity", {}).get("total_complexity", 0)

    score = max(0, 100 - (issues * 10) - complexity)
    return {"quality_score": score}


TOOLS = {
    "extract_functions": extract_functions,
    "check_complexity": check_complexity,
    "detect_smells": detect_smells,
    "suggest_improvements": suggest_improvements,
    "compute_quality_score": compute_quality_score,
}
