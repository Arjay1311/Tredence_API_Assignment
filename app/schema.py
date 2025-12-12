from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Union

class NodeDef(BaseModel):
    name: str
    func: str  

class GraphCreate(BaseModel):
    graph_id: Optional[str] = None
    nodes: Dict[str, str]   # node_name -> func_name
    edges: Dict[str, Union[str, List[Dict[str, str]]]]
    start_node: str

class GraphCreateResp(BaseModel):
    graph_id: str

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = {}
    max_steps: Optional[int] = 200

class RunResp(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    log: List[Dict[str, Any]]

class RunStateResp(BaseModel):
    run_id: str
    state: Dict[str, Any]
    log: List[Dict[str, Any]]
    status: str
    current_node: Optional[str]
