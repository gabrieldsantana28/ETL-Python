from airflow.hooks.base import BaseHook
import logging
import oracledb
from utils.sql_loader import load_sql
from utils.delete_data import delete_data
import os
from dotenv import load_dotenv
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

logger = logging.getLogger(__name__)

class Load: 

    def __init__(self):
        self.connection = None

    def conectar_load(self):

        conn_id = os.getenv("OWNER_GUIAS")

        conn = BaseHook.get_connection(conn_id)
        logger.info("Conectado ao banco de carga")

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

    def desconectar_load(self):
        if self.connection:
            self.connection.close()
            logger.info("Desconectado")

    def deletar_dados(self, competencia):

        delete_data(
            self.connection,
            load_sql("load", "delete_guias.sql"),
            {"competencia": competencia}
        )

        delete_data(
            self.connection,
            load_sql("load", "delete_especialidades.sql")
        )
        

    def carregar(self, chunk):
        logger.info(f"Carregando {len(chunk)} registros")

        cursor = self.connection.cursor()

        dados = [tuple(x) for x in chunk.values]
        
        qr_insert = load_sql(
            "load",
            "insert_guias.sql"
        )

        try:
            cursor.executemany(
                qr_insert, 
                dados
            )

            self.connection.commit()
            logger.info(
                f"{len(dados)} registros carregados com sucesso"
            )

        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    def carregar_especialidades(self, df_especialidades):
        logger.info(f"Carregando {len(df_especialidades)} registros")

        cursor = self.connection.cursor()

        dados = [tuple(x) for x in df_especialidades.values]

        qr_insert = load_sql(
            "load",
            "insert_especialidades.sql"
        )

        try:
            cursor.executemany(
                qr_insert,
                dados
            )

            self.connection.commit()

            logger.info(
                f"{len(df_especialidades)} especialidades carregadas com sucesso"
            )

        except Exception as e:
            self.connection.rollback()
            logger.error(f"Erro ao carregar especialidades: {e}")
            raise

        finally:
            cursor.close()