import logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def delete_data(connection, sql_delete, params=None, descricao="registros"):
    cursor = connection.cursor()

    try:
        cursor.execute(sql_delete, params or {})
        registros_deletados = cursor.rowcount
        connection.commit()
        logger.info(
            f"{registros_deletados} {descricao} removidos com sucesso"
        )
        
    except Exception as e:
        connection.rollback()
        logger.error(
            f"Erro ao remover {descricao}: {e}"
        )
        raise
    
    finally:
        cursor.close()