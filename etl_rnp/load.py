from airflow.hooks.base import BaseHook
import logging
import oracledb
from utils.sql_loader import load_sql
from utils.delete_data import delete_data
from utils.load_data import load_data
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

        self.sql_insert_guias = load_sql(
                "load",
                "insert_guias.sql"
            )

        self.sql_insert_especialidades = load_sql(
            "load",
            "insert_especialidades.sql"
        )

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
        

    def carregar_guias(self, chunk):
        load_data(
            self.connection,
            chunk,
            self.sql_insert_guias,
            "guias"
        )

    def carregar_especialidades(self, df_especialidades):
        load_data(
            self.connection,
            df_especialidades,
            self.sql_insert_especialidades,
            "especialidades"
        )