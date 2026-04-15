from typing import TypedDict, Optional

class ChurnAgentState(TypedDict):
    # Input
    customer_id:        str
    customer_data:      dict

    # Thresholds from UI
    high_threshold:     float
    medium_threshold:   float

    # ML output
    churn_probability:  float
    risk_level:         str

    # LLM output
    churn_reason:       str
    retention_message:  str

    # Agent decision
    action_taken:       str

    # Human approval
    human_approved:     Optional[bool]

    # Final
    report:             str