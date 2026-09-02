import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


def test_health_route_is_published_in_openapi() -> None:
    """The foundation's public health contract remains versioned and discoverable."""
    schema = app.openapi()
    assert "/api/v1/health" in schema["paths"]
