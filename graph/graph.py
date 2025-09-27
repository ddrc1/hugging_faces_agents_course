from langgraph.graph import StateGraph, START, END

from graph.graph_state import GraphState
from graph.nodes.agent_node import agent_node


graph = StateGraph(state_schema=GraphState)

graph.add_node(action="agent_node", node=agent_node)

graph.add_edge(START, "agent_node")
graph.add_edge("agent_node", END)

compiled_graph = graph.compile()