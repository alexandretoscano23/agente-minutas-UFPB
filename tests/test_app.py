"""Teste de fumaça da interface com o AppTest do Streamlit (sem navegador)."""
from pathlib import Path

import pytest

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest
APP = str(Path(__file__).resolve().parent.parent / "app.py")


def _run():
    at = AppTest.from_file(APP, default_timeout=30)
    at.run()
    return at


def test_app_renders_without_exception():
    at = _run()
    assert not at.exception


def test_start_button_is_disabled_without_file():
    at = _run()
    start = [b for b in at.button if b.key == "sd-start"]
    assert len(start) == 1 and start[0].disabled


def test_theme_toggle_switches_theme():
    at = _run()
    assert at.session_state["theme"] == "dark"
    [b for b in at.button if b.key == "sd-theme"][0].click().run()
    assert at.session_state["theme"] == "light"
    [b for b in at.button if b.key == "sd-theme"][0].click().run()
    assert at.session_state["theme"] == "dark"


def test_page_states_scope_and_does_not_claim_review():
    at = _run()
    text = " ".join(m.value for m in at.markdown)
    assert "Revisão restrita à Classe A" in text
    assert "revisão concluída" not in text.lower() and "conforme" not in text.lower().replace("conformidade", "")
