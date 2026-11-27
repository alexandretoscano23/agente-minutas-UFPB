from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from . import config
from .validation import ValidationResult, validate_upload


class RunStatus(str, Enum):
    REJECTED = "rejected"  # arquivo não passou na validação de entrada
    BLOCKED = "blocked"  # arquivo válido, mas a análise real depende de itens ausentes


@dataclass(frozen=True)
class Blocker:
    code: str
    message: str


@dataclass(frozen=True)
class ReviewStart:
    profile: str
    status: RunStatus
    validation: ValidationResult
    blockers: list[Blocker] = field(default_factory=list)


def catalog_file_present() -> bool:
    """Só verifica se o arquivo existe. Aprovação e conteúdo não são verificados."""
    return config.CATALOG_PATH.is_file()


def start_review(filename: str | None, data: bytes | None) -> ReviewStart:
    """Valida de novo a entrada e informa o estado inicial da operação."""
    validation = validate_upload(filename, data)
    if not validation.ok:
        return ReviewStart(config.PROFILE_LABEL, RunStatus.REJECTED, validation)

    blockers: list[Blocker] = []
    if not catalog_file_present():
        blockers.append(
            Blocker(
                "catalog_missing",
                "Catálogo aprovado de regras da Classe A: não encontrado. Depende de aprovação da SODS.",
            )
        )
    blockers.append(
        Blocker(
            "engine_missing",
            "Mecanismo de processamento da Classe A: ainda não implementado.",
        )
    )
    return ReviewStart(config.PROFILE_LABEL, RunStatus.BLOCKED, validation, blockers)
