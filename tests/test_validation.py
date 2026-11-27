import io
import zipfile

import pytest

from smartdocs.validation import format_size, validate_upload
from tests.conftest import CONTENT_TYPES_MACRO, make_docx


def test_valid_docx_is_accepted(valid_docx):
    r = validate_upload("minuta.docx", valid_docx)
    assert r.ok and r.code == "ok" and r.filename == "minuta.docx" and r.size_bytes == len(valid_docx)


def test_extension_is_case_insensitive(valid_docx):
    assert validate_upload("MINUTA.DOCX", valid_docx).ok


def test_real_docx_made_by_word_library_is_accepted(tmp_path):
    docx = pytest.importorskip("docx")
    path = tmp_path / "m.docx"
    d = docx.Document()
    d.add_paragraph("ficticio")
    d.save(path)
    assert validate_upload("m.docx", path.read_bytes()).ok


@pytest.mark.parametrize("name", [None, ""])
def test_missing_file(name, valid_docx):
    assert validate_upload(name, valid_docx).code == "no_file"


def test_missing_data():
    assert validate_upload("a.docx", None).code == "no_file"


@pytest.mark.parametrize("name", ["a.doc", "a.pdf", "a.txt", "a.docm", "a.docx.exe", "a", "a.docx.pdf"])
def test_wrong_extension_is_rejected(name, valid_docx):
    r = validate_upload(name, valid_docx)
    assert not r.ok and r.code == "bad_extension"


def test_empty_file():
    assert validate_upload("a.docx", b"").code == "empty"


def test_too_large(valid_docx):
    r = validate_upload("a.docx", valid_docx, max_bytes=10)
    assert r.code == "too_large"


def test_text_renamed_as_docx_is_rejected():
    assert validate_upload("a.docx", b"isto nao e um docx").code == "bad_signature"


def test_pdf_renamed_as_docx_is_rejected():
    assert validate_upload("a.docx", b"%PDF-1.4 conteudo").code == "bad_signature"


def test_ole_container_gets_specific_message():
    r = validate_upload("a.docx", bytes.fromhex("D0CF11E0A1B11AE1") + b"\x00" * 64)
    assert r.code == "ole_container" and "senha" in r.message


def test_zip_that_is_not_word_package():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("qualquer.txt", "x")
    assert validate_upload("a.docx", buf.getvalue()).code == "not_word_package"


def test_zip_with_wrong_main_content_type():
    bad = make_docx(content_types=CONTENT_TYPES_MACRO.replace("macroEnabled.main+xml", "sheet.main+xml").replace("wordprocessingml.document", "spreadsheetml"))
    assert validate_upload("a.docx", bad).code == "not_word_package"


def test_truncated_zip_is_corrupted(valid_docx):
    assert validate_upload("a.docx", valid_docx[: len(valid_docx) // 2]).code == "corrupted"


def test_macro_part_is_rejected():
    assert validate_upload("a.docx", make_docx({"word/vbaProject.bin": b"\x00"})).code == "has_macros"


def test_macro_enabled_content_type_is_rejected():
    assert validate_upload("a.docx", make_docx(content_types=CONTENT_TYPES_MACRO)).code == "has_macros"


def test_uncompressed_size_limit(valid_docx):
    bomb = make_docx({"word/media/x.bin": b"\x00" * 100_000})
    r = validate_upload("a.docx", bomb, max_uncompressed_bytes=10_000)
    assert r.code == "too_large_uncompressed"


def test_too_many_entries():
    many = make_docx({f"word/p{i}.xml": b"x" for i in range(20)})
    assert validate_upload("a.docx", many, max_entries=10).code == "too_many_parts"


def test_path_in_filename_is_not_exposed(valid_docx):
    r = validate_upload("C:\\Users\\fulano\\docs\\minuta.docx", valid_docx)
    assert r.ok and r.filename == "minuta.docx"
    r2 = validate_upload("/home/fulano/minuta.docx", valid_docx)
    assert r2.filename == "minuta.docx"


def test_error_messages_do_not_leak_internal_details():
    r = validate_upload("a.docx", b"PK\x03\x04lixo")
    assert not r.ok
    for term in ("Traceback", "Exception", "/home", "zipfile"):
        assert term not in r.message


def test_format_size():
    assert format_size(500) == "500 B"
    assert format_size(36_600) == "36.6 KB"
    assert format_size(2_500_000) == "2.5 MB"
