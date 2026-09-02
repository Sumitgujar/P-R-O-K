# PROK AI service layer

This package holds replaceable AI-facing adapters and ports. It is deliberately separate from the FastAPI routes and product services.

Foundation rule: an AI adapter may explain approved knowledge or deterministic results, but it cannot read/write MongoDB directly or make attendance, scholarship, enrollment, or document approval decisions.
