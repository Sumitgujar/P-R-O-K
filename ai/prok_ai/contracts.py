from typing import Protocol


class GuidancePresenter(Protocol):
    """Optional adapter for phrasing already-grounded guidance."""

    async def present(self, grounded_context: str, question: str) -> str:
        """Return guidance based only on the supplied approved context."""
