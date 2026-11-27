from pathlib import Path

APP_NAME = "MinutaFacil"
APP_SUBTITLE = "Conformidade Normativa"

# O PDF define .docx como único formato do MVP (sem .doc, sem PDF).
ALLOWED_EXTENSIONS = (".docx",)

# Provisório: o PDF manda limitar o tamanho do arquivo e o tamanho
# descompactado, mas não fixa os valores.
MAX_UPLOAD_MB = 50
MAX_UNCOMPRESSED_MB = 200
MAX_ZIP_ENTRIES = 10_000

# Ponto de integração para o catálogo aprovado de regras da Classe A.
# Nenhum catálogo existe neste repositório e nenhum foi inventado. A SODS
# precisa aprovar o catálogo; o formato dele ainda não está definido.
CATALOG_PATH = (
    Path(__file__).resolve().parent.parent / "catalog" / "class_a_catalog.json"
)

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
