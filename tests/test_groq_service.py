import pytest
import os
from services.groq_service import GroqService

def test_groq_service_missing_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError):
        GroqService(api_key="")
