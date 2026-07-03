import logging

from etl_rnp.utils.sql_loader import load_sql 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def load_data(connection, chunk, sql_insert, descricao):
        logger.info(f"Carregando {len(chunk)} {descricao}")

        cursor = connection.cursor()

        dados = [tuple(x) for x in chunk.values]
        
        qr_insert = load_sql(
            "load",
            sql_insert
        )

        try:
            cursor.executemany(
                qr_insert, 
                dados
            )

            connection.commit()
            logger.info(
                f"{len(dados)} {descricao} carregados com sucesso"
            )

        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            connection.rollback()
            raise

        finally:
            cursor.close()