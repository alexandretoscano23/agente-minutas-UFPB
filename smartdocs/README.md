# SmartDocs: entrada de minutas para a revisão restrita à Classe A

Primeira parte do projeto de automação da revisão técnico-normativa de minutas de resolução da UFPB.
Esta entrega implementa **somente** a tela inicial e o fluxo de recebimento de documentos.
**Nenhuma revisão normativa é executada.**

## Como executar

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
streamlit run app.py
```

Testes: `python -m pytest -q`

## O que existe

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Tela inicial, upload, botão "Iniciar análise" e mensagens de estado |
| `smartdocs/config.py` | Constantes (formatos, limites, ponto de integração do catálogo) |
| `smartdocs/validation.py` | Validação do arquivo (extensão, vazio, tamanho, assinatura, estrutura do pacote Word, macros, limite descompactado) |
| `smartdocs/review.py` | Perfil "Revisão restrita à Classe A" e estado inicial da operação |
| `smartdocs/ui.py` | Tema escuro/claro, CSS e componentes visuais |
| `assets/*.svg` | Logotipos **fictícios e substituíveis** (mantenha os nomes dos arquivos) |
| `.streamlit/config.toml` | Limite de upload do servidor e tema base |
| `tests/` | 40 testes (validação, revisão e interface) |

## Comportamento

1. Sem arquivo, o botão fica desativado.
2. O arquivo é validado ao ser selecionado. Se for recusado, a tela mostra o motivo em português e o botão continua desativado.
3. Com arquivo válido, o botão é ativado. Ao clicar, o arquivo é validado de novo e a tela mostra o estado da operação.
4. Hoje o estado é sempre **"Análise não iniciada"**, com os bloqueios listados: catálogo aprovado de regras da Classe A não encontrado e mecanismo de processamento ainda não implementado. Nenhum resultado normativo é simulado.
5. Trocar o arquivo limpa o estado anterior.

## Decisões técnicas desta etapa (não são requisitos do PDF)

- **Limite de 50 MB** (visto na imagem de referência) e **200 MB descompactados**: valores provisórios, pois o PDF manda limitar mas não fixa números.
- **O seletor não filtra por tipo** no navegador, para que as recusas apareçam com mensagem em português. A validação no servidor é quem decide.
- **Macros são recusadas** (parte `vbaProject.bin` ou tipo de conteúdo habilitado para macros).
- **Tema claro/escuro** por botão no cabeçalho, em CSS. O tema escuro é o padrão, como na referência.
- **PRPG, PRA e Sobre** são apenas rótulos visuais, sem links, porque não há destinos definidos.
- **`catalog/class_a_catalog.json`** é só o ponto de integração previsto; o arquivo não existe e nenhum formato foi definido.

## O que NÃO existe (fora do escopo)

Catálogo de regras e qualquer correção automática; Classes B e C; verificação independente; escrita no Word, comentários e marcação em vermelho; relatório de auditoria; hash e armazenamento imutável do original; fila, workers, banco de dados e autenticação; IA e RAG; suporte a `.doc` e a PDF como entrada.

O arquivo enviado fica apenas na memória do servidor Streamlit durante a sessão. Esta aplicação não o grava em disco, não o registra em logs e não o envia a serviços externos.

## Dependências

- `streamlit`: interface do protótipo, conforme o PDF de arquitetura.
- `pytest` (apenas desenvolvimento): testes.

Não foram adicionados LangChain, FAISS, Gemini nem `python-docx` (usado só opcionalmente em um teste, que é ignorado se a biblioteca não estiver instalada).

## Pendências que dependem de decisão ou material

1. Catálogo aprovado de regras da Classe A (SODS), com fonte e versão por regra.
2. Valores definitivos dos limites de tamanho.
3. Política para vínculos externos e objetos embutidos: o PDF cita "rejeição de macros e vínculos externos", mas hiperlinks comuns também são vínculos externos, então essa regra não foi implementada sem uma definição.
4. Logotipos oficiais e destinos de PRPG, PRA e Sobre.
5. Mecanismo de processamento da Classe A e perfil de autorização por categoria.
