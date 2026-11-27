"""Auxiliares de teste: monta pacotes .docx mínimos sem depender de python-docx."""
import io
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.'
    'wordprocessingml.document.main+xml"/></Types>'
)
CONTENT_TYPES_MACRO = CONTENT_TYPES.replace(
    "wordprocessingml.document.main+xml", "wordprocessingml.document.macroEnabled.main+xml"
)
DOCUMENT = (
    '<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/'
    'wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Texto ficticio.</w:t></w:r></w:p></w:body></w:document>'
)


def make_docx(extra: dict[str, bytes] | None = None, content_types: str = CONTENT_TYPES, drop: tuple[str, ...] = ()) -> bytes:
    parts = {"[Content_Types].xml": content_types.encode(), "word/document.xml": DOCUMENT.encode()}
    parts.update(extra or {})
    for name in drop:
        parts.pop(name, None)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    return buf.getvalue()


@pytest.fixture
def valid_docx() -> bytes:
    return make_docx()
