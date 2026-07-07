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

        # Extração e carregamento das guias
        for chunk in extractor.extrair_guias():
            loader.carregar_guias(chunk)
    

        # Extração e carregamento das especialidades
        df_especialidades = extractor.extrair_especialidades()
        loader.carregar_especialidades(df_especialidades)

    finally:
        extractor.desconectar_extract()
        loader.desconectar_load()