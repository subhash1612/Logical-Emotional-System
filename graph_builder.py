from langgraph.graph import StateGraph, START, END
from schemas import State
from agents import classify_message, router, therapist_agent, logical_agent

def build_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("classifier", classify_message)
    graph_builder.add_node("router", router)
    graph_builder.add_node("therapist", therapist_agent)
    graph_builder.add_node("logical", logical_agent)

    graph_builder.add_edge(START, "classifier")
    graph_builder.add_edge("classifier", "router")
    graph_builder.add_conditional_edges(
        "router",
        lambda state: state.get("next"),
        {"therapist": "therapist", "logical": "logical"}
    )
    graph_builder.add_edge("therapist", END)
    graph_builder.add_edge("logical", END)
    return graph_builder.compile()