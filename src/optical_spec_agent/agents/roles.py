"""Sub-agent roles used in the local preview collaboration trace."""

from __future__ import annotations


AGENT_ROLES: tuple[tuple[str, str], ...] = (
    ("SpecAgent", "Interprets user intent or an OpticalSpec and identifies missing fields."),
    ("MaterialAgent", "Suggests materials from the local preview material catalog."),
    ("GeometryAgent", "Identifies geometry family and geometry fields needed for preview."),
    ("AdapterAgent", "Recommends an open-source-first adapter and explains maturity limits."),
    ("WorkflowAgent", "Creates a local preview workflow plan with no solver execution by default."),
    ("EvidenceAgent", "Attaches validation evidence and states what is and is not verified."),
    ("SafetyAgent", "Checks no overclaim, no default solver/LLM, and no publication controls."),
    ("RecommendationAgent", "Summarizes next actions for the user or maintainer."),
)
