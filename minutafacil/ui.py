"""Identidade visual e componentes de apresentação.

Os logotipos são placeholders em ``assets/`` e podem ser substituídos sem
mexer em código: basta trocar os arquivos SVG mantendo os nomes.
"""

from __future__ import annotations

from functools import cache
from urllib.parse import quote

import streamlit as st

from . import config

_FONT = '"DM Sans", "Inter", "Segoe UI", system-ui, -apple-system, sans-serif'

THEMES = {
    "dark": {
        "bg": "#06080d",
        "header": "#0b0f16",
        "card": "#0e121a",
        "border": "#232a37",
        "text": "#eef1f6",
        "muted": "#8d97a9",
        "accent": "#7aa2ff",
        "drop": "#0a0d14",
        "btn": "#5b78b8",
        "btn_hover": "#6d8bd0",
        "btn_text": "#0b1020",
        "ok_bg": "#10241b",
        "ok_bd": "#1f5a3c",
        "ok_tx": "#86e0b1",
        "err_bg": "#2a1215",
        "err_bd": "#7a2a31",
        "err_tx": "#ff9ea6",
        "warn_bg": "#2a2110",
        "warn_bd": "#7a5d1c",
        "warn_tx": "#f0cd7a",
    },
    "light": {
        "bg": "#f4f6fa",
        "header": "#ffffff",
        "card": "#ffffff",
        "border": "#d6dce7",
        "text": "#141a24",
        "muted": "#5a6579",
        "accent": "#2c58cc",
        "drop": "#f8f9fc",
        "btn": "#2c58cc",
        "btn_hover": "#2548ab",
        "btn_text": "#ffffff",
        "ok_bg": "#e7f6ee",
        "ok_bd": "#8fd1ae",
        "ok_tx": "#14663f",
        "err_bg": "#fdebec",
        "err_bd": "#eba3a8",
        "err_tx": "#9b1c25",
        "warn_bg": "#fdf4de",
        "warn_bd": "#e6c46d",
        "warn_tx": "#7a5300",
    },
}


@cache
def _svg(name: str) -> str:
    return (config.ASSETS_DIR / name).read_text(encoding="utf-8")


def _upload_icon_uri(color: str) -> str:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 15V4m0 0L8 8m4-4 4 4"/><path d="M4 14v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"/></svg>'
    )
    return 'url("data:image/svg+xml;utf8,' + quote(svg) + '")'


def build_css(theme: str) -> str:
    t = THEMES[theme]
    icon = _upload_icon_uri(t["muted"])
    return f"""
<style>
:root {{ --sd-font: {_FONT}; }}
html, body, .stApp, [data-testid="stAppViewContainer"] {{
  background: {t["bg"]} !important; color: {t["text"]}; font-family: var(--sd-font);
}}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
#MainMenu, footer {{ display: none !important; }}
.block-container {{ max-width: none !important; padding: 0 0 48px 0 !important; }}
.stApp p, .stApp label, .stApp li, .stApp small, .stApp h1, .stApp h2, .stApp h3, .stApp button p, .sd-brand, .sd-nav {{ font-family: var(--sd-font); }}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {{ gap: 0 !important; }}
[data-testid="stMain"], .stMain {{ padding-top: 0 !important; }}

/* cabeçalho */
.st-key-sd-header {{
  background: {t["header"]}; border-bottom: 1px solid {t["border"]};
  padding: 10px 28px; position: sticky; top: 0; z-index: 20;
}}
.st-key-sd-header [data-testid="stHorizontalBlock"] {{ align-items: center; gap: .5rem; }}
.sd-brand {{ display: flex; align-items: center; gap: 12px; }}
.sd-brand svg {{ width: 36px; height: 36px; flex: none; }}
.sd-brand strong {{ font-size: 1.02rem; color: {t["text"]}; letter-spacing: -.01em; }}
.sd-brand span {{ font-size: .86rem; color: {t["muted"]}; margin-left: 10px; }}
.sd-nav {{ display: flex; justify-content: flex-end; gap: 28px; font-size: .86rem; color: {t["muted"]}; }}
.st-key-sd-theme {{ margin-left: auto; }}
.st-key-sd-theme button p {{ display: none !important; }}
.st-key-sd-theme button {{ gap: 0 !important; }}
.st-key-sd-theme button {{
  background: transparent !important; border: 1px solid transparent !important; color: {t["muted"]} !important;
  min-height: 2.2rem; padding: 0 .5rem; border-radius: 8px;
}}
.st-key-sd-theme button:hover {{ border-color: {t["border"]} !important; color: {t["text"]} !important; }}

/* texto de abertura */
.st-key-sd-hero {{ max-width: 760px; margin: 0 auto; padding: 44px 20px 36px; text-align: center; }}
.sd-hero, .sd-hero h1, .sd-hero p {{ text-align: center !important; }}
.sd-hero h1 {{ font-size: 1.85rem; line-height: 1.2; margin: 0 0 12px; color: {t["text"]}; font-weight: 650; letter-spacing: -.02em; }}
.sd-hero p {{ color: {t["muted"]}; font-size: 1.02rem; line-height: 1.6; margin: 0 auto; max-width: 62ch; }}

/* cartão de envio */
.st-key-sd-card {{
  max-width: 880px; margin: 0 auto; padding: 28px 26px 22px;
  background: {t["card"]}; border: 1px solid {t["border"]}; border-radius: 16px;
  width: calc(100% - 40px);
}}
.sd-card-head {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; flex-wrap: wrap; }}
.sd-card-head h2 {{ font-size: 1.25rem; margin: 0 0 4px !important; padding: 0 !important; color: {t["text"]}; font-weight: 650; }}
.sd-card-head p {{ margin: 0 !important; color: {t["muted"]}; font-size: .9rem; }}
.sd-card-head p b {{ color: {t["text"]}; }}
.sd-profile {{
  font-size: .78rem; color: {t["accent"]}; border: 1px solid {t["border"]};
  border-radius: 999px; padding: 4px 11px; white-space: nowrap;
}}

/* área de upload */
.st-key-sd-card [data-testid="stFileUploader"] {{ margin-top: 14px; }}
.st-key-sd-card [data-testid="stFileUploaderDropzone"] {{
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;
  min-height: 210px; background: {t["drop"]}; border: 1.5px dashed {t["border"]}; border-radius: 12px;
  padding: 24px 16px; position: relative; cursor: pointer;
}}
.st-key-sd-card [data-testid="stFileUploaderDropzone"]:hover {{ border-color: {t["accent"]}; }}
.st-key-sd-card [data-testid="stFileUploaderDropzone"]::before {{
  content: ""; width: 44px; height: 44px; background: {icon} center / contain no-repeat; margin-bottom: 6px; order: 0;
}}
.st-key-sd-card [data-testid="stFileUploaderDropzoneInstructions"] {{ display: none !important; }}
.st-key-sd-card [data-testid="stFileUploaderDropzone"]::after {{
  content: "Arraste sua minuta aqui"; color: {t["text"]}; font-weight: 600; font-size: .95rem; order: 1;
}}
.st-key-sd-card [data-testid="stFileUploaderDropzone"] > span {{ order: 2; display: block; }}
.st-key-sd-card [data-testid="stFileUploaderDropzone"] button[data-testid="stBaseButton-secondary"] {{
  background: transparent !important; border: 0 !important; box-shadow: none !important;
  padding: 0 !important; min-height: 0 !important; line-height: 1.2;
}}
.st-key-sd-card [data-testid="stFileUploaderDropzone"] button[data-testid="stBaseButton-secondary"] > * {{ display: none !important; }}
.st-key-sd-card [data-testid="stFileUploaderDropzone"] button[data-testid="stBaseButton-secondary"]::after {{
  content: "ou selecione no seu computador"; font-size: .82rem; color: {t["accent"]}; font-family: var(--sd-font);
}}
.st-key-sd-card [data-testid="stFileUploaderDropzone"] button[data-testid="stBaseButton-secondary"]:hover::after {{ text-decoration: underline; }}
/* com arquivo selecionado: some a chamada e fica só o arquivo */
.st-key-sd-card [data-testid="stFileUploaderDropzone"]:has([data-testid="stFileChips"]) {{
  min-height: 0; padding: 14px 16px; flex-direction: row; justify-content: space-between; border-style: solid;
}}
.st-key-sd-card [data-testid="stFileUploaderDropzone"]:has([data-testid="stFileChips"])::before,
.st-key-sd-card [data-testid="stFileUploaderDropzone"]:has([data-testid="stFileChips"])::after {{ display: none; }}
.st-key-sd-card [data-testid="stFileChips"] {{ color: {t["text"]}; }}
.st-key-sd-card [data-testid="stFileChips"] > div > div > div {{ background: transparent !important; }}
.st-key-sd-card [data-testid="stFileChipName"] {{ color: {t["text"]} !important; }}
.st-key-sd-card [data-testid="stFileChipName"] + div {{ color: {t["muted"]} !important; }}
.st-key-sd-card [data-testid="stFileChip"] small button {{ color: {t["muted"]} !important; }}
.st-key-sd-card [data-testid="stFileChips"] > div {{ background: {t["card"]} !important; border: 1px solid {t["border"]}; border-radius: 10px; }}
.st-key-sd-card [data-testid="stFileUploaderDropzone"] button[data-testid="stBaseButton-borderlessIcon"] {{ color: {t["muted"]} !important; }}
.st-key-sd-card [data-testid="stFileUploaderFile"] {{ color: {t["text"]}; }}
.st-key-sd-card [data-testid="stFileUploaderFile"] small {{ color: {t["muted"]} !important; }}
.st-key-sd-card [data-testid="stFileUploaderFileName"] {{ color: {t["text"]} !important; }}
.st-key-sd-card [data-testid="stFileUploaderDeleteBtn"] button {{
  color: {t["muted"]} !important; font-size: inherit !important; min-height: 1.6rem; padding: 0 .3rem !important;
}}
.st-key-sd-card [data-testid="stFileUploaderDeleteBtn"] button::after {{ content: none; }}

/* botão */
.st-key-sd-start {{ align-self: flex-end; margin-top: 14px; }}
.st-key-sd-start button {{
  background: {t["btn"]} !important; color: {t["btn_text"]} !important; border: 0 !important;
  border-radius: 10px; padding: .55rem 1.1rem; font-weight: 600; font-family: var(--sd-font);
}}
.st-key-sd-start button:hover:not(:disabled) {{ background: {t["btn_hover"]} !important; }}
.st-key-sd-start button:disabled {{ opacity: .55; cursor: not-allowed; }}
.st-key-sd-start button:focus-visible, .st-key-sd-theme button:focus-visible {{
  outline: 2px solid {t["accent"]}; outline-offset: 2px;
}}

/* mensagens */
.sd-msg {{ border-radius: 10px; padding: 11px 14px; margin-top: 12px; font-size: .9rem; line-height: 1.5; border: 1px solid; }}
.sd-msg b {{ font-weight: 650; }}
.sd-ok {{ background: {t["ok_bg"]}; border-color: {t["ok_bd"]}; color: {t["ok_tx"]}; }}
.sd-err {{ background: {t["err_bg"]}; border-color: {t["err_bd"]}; color: {t["err_tx"]}; }}
.sd-warn {{ background: {t["warn_bg"]}; border-color: {t["warn_bd"]}; color: {t["warn_tx"]}; }}
.sd-steps {{ list-style: none; padding: 0; margin: 10px 0 0; }}
.sd-steps li {{ display: flex; gap: 10px; padding: 3px 0; color: {t["text"]}; font-size: .9rem; }}
.sd-steps li i {{ font-style: normal; width: 1.1em; flex: none; }}
.sd-steps .ok i {{ color: {t["ok_tx"]}; }}
.sd-steps .no i {{ color: {t["err_tx"]}; }}
.sd-state-title {{ margin: 18px 0 0; font-size: .95rem; font-weight: 650; color: {t["text"]}; }}
.sd-state-note {{ margin: 8px 0 0; color: {t["muted"]}; font-size: .84rem; line-height: 1.5; }}

/* rodapé */
.sd-footer {{ display: flex; align-items: center; justify-content: center; gap: 10px;
  margin: 26px auto 0; color: {t["muted"]}; font-size: .78rem; }}
.sd-footer svg {{ width: 22px; height: 22px; }}

@media (max-width: 720px) {{
  .st-key-sd-header {{ padding: 8px 14px; }}
  .st-key-sd-header [data-testid="stHorizontalBlock"] {{ flex-wrap: nowrap !important; }}
  .st-key-sd-header [data-testid="stColumn"] {{ min-width: 0 !important; flex: 1 1 auto !important; width: auto !important; }}
  .st-key-sd-header [data-testid="stColumn"]:last-child {{ flex: 0 0 auto !important; }}
  .st-key-sd-start {{ align-self: stretch; }}
  .sd-nav {{ display: none; }}
  .sd-brand span {{ display: none; }}
  .st-key-sd-hero {{ padding: 28px 16px 18px; }}
  .sd-hero h1 {{ font-size: 1.45rem; }}
  .st-key-sd-card {{ padding: 20px 16px 16px; width: calc(100% - 24px); }}
  .st-key-sd-card [data-testid="stFileUploaderDropzone"] {{ min-height: 170px; }}
  .st-key-sd-start button {{ width: 100%; }}
}}
</style>
"""


def inject_theme(theme: str) -> None:
    st.markdown(build_css(theme), unsafe_allow_html=True)


def render_brand() -> str:
    return (
        '<div class="sd-brand">'
        + _svg("logo_smartdocs.svg")
        + f"<div><strong>{config.APP_NAME}</strong><span>{config.APP_SUBTITLE}</span></div></div>"
    )


def render_hero() -> str:
    return (
        '<div class="sd-hero"><h1>Conformidade normativa de minutas</h1>'
        "<p>Envie a minuta de resolução em .docx. Esta versão inicial recebe e valida o arquivo "
        "e resultado verificável.</p></div>"
    )


def render_footer() -> str:
    return (
        '<div class="sd-footer">'
        + _svg("logo_institucional_placeholder.svg")
        + "<span>Espaço reservado para o logotipo institucional</span></div>"
    )


def msg(kind: str, html: str) -> str:
    return f'<div class="sd-msg sd-{kind}">{html}</div>'
