"""SmartDocs: tela inicial e fluxo de entrada da revisão restrita à Classe A."""

from __future__ import annotations

import html

import streamlit as st
from smartdocs.review import RunStatus, start_review
from smartdocs.validation import format_size, validate_upload

from smartdocs import config, ui

st.set_page_config(
    page_title=f"{config.APP_NAME} | {config.APP_SUBTITLE}",
    page_icon="📄",
    layout="wide",
)

st.session_state.setdefault("theme", "dark")


def _toggle_theme() -> None:
    st.session_state["theme"] = (
        "light" if st.session_state["theme"] == "dark" else "dark"
    )


ui.inject_theme(st.session_state["theme"])

# ---------------------------------------------------------------- cabeçalho
with st.container(key="sd-header"):
    c_brand, c_nav, c_theme = st.columns([5, 4, 1], vertical_alignment="center")
    c_brand.markdown(ui.render_brand(), unsafe_allow_html=True)
    is_dark = st.session_state["theme"] == "dark"
    with c_theme:
        st.button(
            "Tema",
            key="sd-theme",
            icon=":material/light_mode:" if is_dark else ":material/dark_mode:",
            help="Mudar para o tema claro" if is_dark else "Mudar para o tema escuro",
            on_click=_toggle_theme,
        )

# ---------------------------------------------------------------- abertura
with st.container(key="sd-hero"):
    st.markdown(ui.render_hero(), unsafe_allow_html=True)

# ---------------------------------------------------------------- cartão de envio
with st.container(key="sd-card"):
    st.markdown(
        '<div class="sd-card-head"><div><h2>Envie sua minuta</h2>'
        f"<p>Aceitamos arquivos <b>.docx</b> de até {config.MAX_UPLOAD_MB} MB.</p></div>",
        unsafe_allow_html=True,
    )

    # Sem filtro de tipo no seletor: a validação própria devolve mensagens em português.
    uploaded = st.file_uploader(
        "Minuta em .docx",
        accept_multiple_files=False,
        label_visibility="collapsed",
        key="sd-upload",
    )

    name = uploaded.name if uploaded else None
    data = uploaded.getvalue() if uploaded else None
    file_id = uploaded.file_id if uploaded else None

    # A validação roda uma vez por arquivo selecionado.
    cached = st.session_state.get("validation")
    if cached is None or cached[0] != file_id:
        cached = (file_id, validate_upload(name, data))
        st.session_state["validation"] = cached
    check = cached[1]

    if uploaded is not None:
        label = html.escape(check.filename or name or "")
        if check.ok:
            st.markdown(
                ui.msg(
                    "ok",
                    f"<b>{label}</b> ({format_size(check.size_bytes)})<br>{html.escape(check.message)}",
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                ui.msg("err", f"<b>Arquivo recusado.</b> {html.escape(check.message)}"),
                unsafe_allow_html=True,
            )

    start = st.button(
        "Iniciar análise",
        key="sd-start",
        type="primary",
        icon=":material/play_arrow:",
        disabled=not (uploaded is not None and check.ok),
    )

    if start:
        # Valida de novo antes de iniciar, sem confiar no estado da tela.
        st.session_state["run"] = (file_id, start_review(name, data))

    run = st.session_state.get("run")
    if run and run[0] == file_id and uploaded is not None:
        result = run[1]
        if result.status is RunStatus.REJECTED:
            st.markdown(
                ui.msg(
                    "err",
                    f"<b>Não foi possível iniciar.</b> {html.escape(result.validation.message)}",
                ),
                unsafe_allow_html=True,
            )
        else:
            steps = [
                '<li class="ok"><i>&#10003;</i><span>Arquivo recebido e validado (.docx).</span></li>'
            ]
            steps += [
                f'<li class="no"><i>&#10007;</i><span>{html.escape(b.message)}</span></li>'
                for b in result.blockers
            ]
            st.markdown(
                f'<p class="sd-state-title">Estado da operação: {html.escape(result.profile)}</p>'
                f'<ul class="sd-steps">{"".join(steps)}</ul>'
                + ui.msg(
                    "warn",
                    "<b>Análise não iniciada.</b> Nenhuma revisão foi executada, o documento não foi alterado "
                    "e nenhum resultado normativo foi gerado.",
                )
                + '<p class="sd-state-note">Esta aplicação não grava o arquivo em disco nem o envia a serviços externos.</p>',
                unsafe_allow_html=True,
            )

st.markdown(ui.render_footer(), unsafe_allow_html=True)
