from smartdocs import config, review
from smartdocs.review import RunStatus, start_review


def test_valid_file_is_blocked_never_completed(valid_docx):
    r = start_review("m.docx", valid_docx)
    assert r.status is RunStatus.BLOCKED
    assert r.profile == "Revisão restrita à Classe A"
    assert {s.value for s in RunStatus} == {"rejected", "blocked"}  # não existe estado "concluída"


def test_blockers_list_missing_catalog_and_engine(valid_docx, monkeypatch, tmp_path):
    monkeypatch.setattr(config, "CATALOG_PATH", tmp_path / "nao_existe.json")
    codes = {b.code for b in start_review("m.docx", valid_docx).blockers}
    assert codes == {"catalog_missing", "engine_missing"}


def test_engine_blocker_remains_even_if_catalog_file_exists(valid_docx, monkeypatch, tmp_path):
    f = tmp_path / "catalogo.json"
    f.write_text("{}")
    monkeypatch.setattr(config, "CATALOG_PATH", f)
    codes = {b.code for b in start_review("m.docx", valid_docx).blockers}
    assert codes == {"engine_missing"}


def test_invalid_file_is_rejected_on_start():
    r = start_review("m.pdf", b"%PDF")
    assert r.status is RunStatus.REJECTED and not r.validation.ok and r.blockers == []


def test_no_file_is_rejected_on_start():
    assert start_review(None, None).status is RunStatus.REJECTED


def test_start_does_not_modify_input_bytes(valid_docx):
    original = bytes(valid_docx)
    start_review("m.docx", valid_docx)
    assert valid_docx == original


def test_start_does_not_write_files(valid_docx, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    start_review("m.docx", valid_docx)
    assert list(tmp_path.iterdir()) == []


def test_catalog_not_shipped_with_project():
    assert not review.catalog_file_present()
