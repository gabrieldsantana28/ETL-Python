from configs import COMPETENCIAATUAL
from extract import Extract
from load import Load

def executar():

    extractor = Extract()
    loader = Load()

    try:
        extractor.conectar_extract()
        loader.conectar_load()

        loader.deletar_dados(COMPETENCIAATUAL)

        for chunk in extractor.extrair_dados():
            loader.carregar(chunk)

    finally:
        extractor.desconectar_extract()
        loader.desconectar_load()