"""Validação de arquivos enviados.

Não confia só na extensão: confere assinatura, estrutura do pacote Office e
presença de macros. Nada é extraído para o disco e nenhum conteúdo do
documento é interpretado ou executado.
"""
from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath

from . import config

_ZIP_SIGNATURE = b"PK\x03\x04"
_OLE_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")  # .doc antigo ou docx com senha
_WORD_MAIN_TYPE = b"wordprocessingml.document.main+xml"
_MAX_CONTENT_TYPES_BYTES = 1_000_000


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    code: str
    message: str
    filename: str = ""
    size_bytes: int = 0


def format_size(size_bytes: int) -> str:
    if size_bytes < 1000:
        return f"{size_bytes} B"
    if size_bytes < 1_000_000:
        return f"{size_bytes / 1000:.1f} KB"
    return f"{size_bytes / 1_000_000:.1f} MB"


def _safe_name(filename: str) -> str:
    """Só o nome final, sem caminho (não expõe nem confia em diretórios)."""
    return PureWindowsPath(PurePosixPath(filename or "").name).name.strip()


def _fail(code: str, message: str, name: str = "", size: int = 0) -> ValidationResult:
    return ValidationResult(False, code, message, name, size)


_NOT_WORD = "O arquivo não é um documento do Word válido (.docx)."
_MACROS = "O documento contém macros e foi recusado. Salve uma cópia .docx sem macros."


def validate_upload(
    filename: str | None,
    data: bytes | None,
    *,
    max_bytes: int = config.MAX_UPLOAD_MB * 1024 * 1024,
    max_uncompressed_bytes: int = config.MAX_UNCOMPRESSED_MB * 1024 * 1024,
    max_entries: int = config.MAX_ZIP_ENTRIES,
) -> ValidationResult:
    if not filename or data is None:
        return _fail("no_file", "Selecione uma minuta em .docx para continuar.")

    name = _safe_name(filename)
    size = len(data)

    if not name.lower().endswith(config.ALLOWED_EXTENSIONS):
        return _fail(
            "bad_extension",
            "Formato não aceito. Envie a minuta em .docx. "
            "Arquivos .doc e PDF não são aceitos nesta versão.",
            name, size,
        )
    if size == 0:
        return _fail("empty", "O arquivo está vazio. Selecione outra minuta.", name, size)
    if size > max_bytes:
        return _fail(
            "too_large",
            f"O arquivo tem {format_size(size)} e o limite é {format_size(max_bytes)}.",
            name, size,
        )
    if data.startswith(_OLE_SIGNATURE):
        return _fail(
            "ole_container",
            "O arquivo parece ser um .doc antigo ou um documento protegido por senha. "
            "Abra no Word e salve como .docx sem senha.",
            name, size,
        )
    if not data.startswith(_ZIP_SIGNATURE):
        return _fail(
            "bad_signature",
            "O conteúdo não corresponde a um arquivo .docx. "
            "Salve a minuta como .docx no Word e tente de novo.",
            name, size,
        )

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as pkg:
            infos = pkg.infolist()
            if len(infos) > max_entries:
                return _fail("too_many_parts", "O arquivo tem estrutura interna anormal e foi recusado.", name, size)
            if sum(i.file_size for i in infos) > max_uncompressed_bytes:
                return _fail(
                    "too_large_uncompressed",
                    "O conteúdo descompactado excede o limite permitido e o arquivo foi recusado.",
                    name, size,
                )
            names = {i.filename.lower() for i in infos}
            if "[content_types].xml" not in names or "word/document.xml" not in names:
                return _fail("not_word_package", _NOT_WORD, name, size)
            if any(n.endswith("vbaproject.bin") for n in names):
                return _fail("has_macros", _MACROS, name, size)
            ct_info = next(i for i in infos if i.filename.lower() == "[content_types].xml")
            if ct_info.file_size > _MAX_CONTENT_TYPES_BYTES:
                return _fail("not_word_package", _NOT_WORD, name, size)
            content_types = pkg.read(ct_info).lower()
    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError, OSError, EOFError, ValueError):
        return _fail(
            "corrupted",
            "Não foi possível ler o arquivo. Ele pode estar corrompido ou protegido por senha.",
            name, size,
        )

    if b"macroenabled" in content_types:
        return _fail("has_macros", _MACROS, name, size)
    if _WORD_MAIN_TYPE not in content_types:
        return _fail("not_word_package", _NOT_WORD, name, size)

    return ValidationResult(True, "ok", "Arquivo validado: formato .docx.", name, size)
