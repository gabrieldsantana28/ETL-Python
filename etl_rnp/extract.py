from airflow.hooks.base import BaseHook
import oracledb
import logging 
from datetime import datetime
import pandas as pd
from pathlib import Path
from utils.sql_loader import load_sql
from utils.extract_data import extract_chunks, extract_dataframe
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

    # ----------------------------- FUNÇÕES - CONEXÃO ORACLE ----------------------------- #
    
    def conectar_extract(self):

        conn_id = os.getenv('OWNER_SGU')
        
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
        
        logger.info('Conectado ao Oracle')

    def desconectar_extract(self):
        if self.connection:
            self.connection.close()
            logger.info('Desconectado do Oracle')

    # ----------------------------- FUNÇÕES - EXTRAÇÃO DOS DADOS ----------------------------- #

    def extrair_guias(self):

        logger.info(f'Iniciando extração da competência: {COMPETENCIAATUAL}')

        yield from extract_chunks(
            self.connection, 
            'extract', 
            'select_guias_atendimento.sql', 
            params={'competencia': COMPETENCIAATUAL,
                    'paggerado': PAGGERADO,
                    'unimedexecde': UNIMEDEXECDE,
                    'unimedexecate': UNIMEDEXECATE,
                    'tipoprest': TIPOPREST}, 
            chunksize=15000
        )

    def extrair_especialidades(self):
        logger.info('Iniciando extração das especialidades')

        return extract_dataframe(
            self.connection, 
            'extract', 
            'select_especialidades.sql'
        )   

    
    def extrair_itens(self):
        logger.info('Iniciando extração dos itens')

        yield from extract_chunks(
            self.connection, 
            'extract', 
            'select_itens.sql', 
            chunksize=15000
        )

    def extrair_itens_especialidades(self):
        logger.info('Iniciando extração da tabela itens_especialidades')

        yield from extract_chunks(
            self.connection, 
            'extract', 
            'select_itens_especialidades.sql', 
            chunksize=15000
        )