from airflow.hooks.base import BaseHook
import oracledb
import logging 
from datetime import datetime
import pandas as pd
from pathlib import Path
from utils.sql_loader import load_sql
import os
from dotenv import load_dotenv
from configs import PAGGERADO, UNIMEDEXECDE, UNIMEDEXECATE, TIPOPREST, COMPETENCIAATUAL
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv() # Carrega variáveis do arquivo .env

logger = logging.getLogger(__name__)

class Extract:
    
    try:
        oracledb.init_oracle_client()
    except Exception:
        pass
 
    def __init__(self):
        self.connection = None
    
    def conectar_extract(self):

        conn_id = os.getenv("OWNER_SGU")
        
        conn = BaseHook.get_connection(conn_id)
        
        dsn = oracledb.makedsn(
            conn.host,
            conn.port or 1521,
            service_name=conn.schema
        )
        
        self.connection = oracledb.connect(
            user=conn.login,
            password=conn.password,
            dsn=dsn
        )
        
        logger.info("Conectado ao Oracle")

    def desconectar_extract(self):
        if self.connection:
            self.connection.close()
            logger.info("Desconectado do Oracle")

    # ----------------------------- FUNÇÕES - EXTRAÇÃO DOS DADOS ----------------------------- #

    def extrair_guias(self):

        logger.info(f"Iniciando extração da competência: {COMPETENCIAATUAL}")

        qr_dados_guias = load_sql(
            'extract',
            'select_guias_atendimento.sql'
        )
        chunks = pd.read_sql(qr_dados_guias, self.connection, params={"competencia": COMPETENCIAATUAL,
                                                                        "paggerado": PAGGERADO,
                                                                        "unimedexecde": UNIMEDEXECDE,
                                                                        "unimedexecate": UNIMEDEXECATE,
                                                                        "tipoprest": TIPOPREST}, 
                                                                        chunksize=15000)
                
        for chunk in chunks:
            yield chunk

    def extrair_especialidades(self):

        logger.info("Iniciando extração das especialidades")

        qr_dados_especialidades = load_sql(
            "extract",
            "select_especialidades.sql"
        )

        df_especialidades = pd.read_sql(
            qr_dados_especialidades,
            self.connection
        )

        return df_especialidades
    
    def extrair_itens(self):
        
        logger.info("Iniciando extração dos itens")

        qr_dados_itens = load_sql(
            "extract",
            "select_itens.sql"
        )
        chunks = pd.read_sql(qr_dados_itens, self.connection, chunksize=15000)

        for chunk in chunks:
            yield chunk

    def extrair_itens_especialidades(self):

        logger.info("Iniciando extração da tabela itens_especialidades")

        qr_dados_itens_especialidades = load_sql(
            "extract",
            "select_itens_especialidades.sql"
        )

        chunks = pd.read_sql(
            qr_dados_itens_especialidades,
            self.connection,
            chunksize=15000
        )

        return chunks