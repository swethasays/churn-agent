from langgraph.graph import StateGraph, END
from agent.state import ChurnAgentState
from agent.nodes import (
    validate_data,
    predict_churn,
    explain_churn,
    analyze_and_respond,
    route_by_risk,
    handle_high_risk,
    handle_medium_risk,
    handle_low_risk,
    generate_report
)

def build_graph():
    graph = StateGraph(ChurnAgentState)

    graph.add_node("validate",    validate_data)
    graph.add_node("predict",     predict_churn)
    graph.add_node("explain",     explain_churn)
    graph.add_node("analyze",     analyze_and_respond)
    graph.add_node("high_risk",   handle_high_risk)
    graph.add_node("medium_risk", handle_medium_risk)
    graph.add_node("low_risk",    handle_low_risk)
    graph.add_node("report",      generate_report)

    graph.set_entry_point("validate")
    graph.add_edge("validate", "predict")
    graph.add_edge("predict",  "explain")
    graph.add_edge("explain",  "analyze")

    graph.add_conditional_edges(
        "analyze",
        route_by_risk,
        {
            "high_risk":   "high_risk",
            "medium_risk": "medium_risk",
            "low_risk":    "low_risk"
        }
    )

    graph.add_edge("high_risk",   "report")
    graph.add_edge("medium_risk", "report")
    graph.add_edge("low_risk",    "report")
    graph.add_edge("report",      END)

    return graph.compile()

churn_agent = build_graph()