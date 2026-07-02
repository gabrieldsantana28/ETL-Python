from pathlib import Path

def load_sql(etapa, file_name):

    sql_file = (    
        Path(__file__).parent.parent
        / "sql"
        / etapa
        / file_name
    )

    if not sql_file.exists():
        raise FileNotFoundError(
            f"Arquivo SQL não encontrado: {sql_file}"
        )

    with open(sql_file, "r", encoding="utf-8") as file:
        return file.read()