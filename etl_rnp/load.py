from airflow.hooks.base import BaseHook
import logging
import oracledb
from utils.sql_loader import load_sql
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

        cursor = self.connection.cursor()

        qr_delete = load_sql(
            "load",
            "delete_guias.sql"
        )

        try:

            cursor.execute(
                qr_delete,
                {"competencia": competencia}
            )

            registros_deletados = cursor.rowcount

            self.connection.commit()

            logger.info(
                f"{registros_deletados} registros da competência "
                f"{competencia} removidos com sucesso"
            )

        except Exception as e:

            self.connection.rollback()

            logger.error(
                f"Erro ao remover dados da competência "
                f"{competencia}: {e}"
            )

            raise

        finally:
            cursor.close()

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

        quantidade = len(df_especialidades)

        logger.info(f"Carregando {quantidade} especialidades")

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
                f"{quantidade} especialidades carregadas com sucesso"
            )

        except Exception as e:
            self.connection.rollback()
            logger.error(f"Erro ao carregar especialidades: {e}")
            raise

        finally:
            cursor.close()