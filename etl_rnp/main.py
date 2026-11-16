from configs import COMPETENCIAATUAL
from extract import Extract
from load import Load

def executar():

    extractor = Extract()
    loader = Load()

    try:
        extractor.conectar_extract()
        loader.conectar_load()

        # EXTRACÃO E CARREGAMENTO DE DADOS
        for chunk in extractor.extrair_guias():
            loader.carregar_guias(chunk)

        especialidades = extractor.extrair_especialidades()
        loader.carregar_especialidades(especialidades)

        for chunk in extractor.extrair_itens():
            loader.carregar_itens(chunk)

        for chunk in extractor.extrair_itens_especialidades():
            loader.carregar_itens_especialidades(chunk)

    finally:
        extractor.desconectar_extract()
        loader.desconectar_load()