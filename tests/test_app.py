from app import __version__
from typing import Any


def test_version() -> Any:
    assert __version__ == '0.1.0'
