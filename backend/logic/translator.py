from backend.statements.create_operation import translate_insert
from backend.statements.read_operation import translate_select
from backend.statements.update_operation import translate_update
from backend.statements.delete_operation import translate_delete


def translate_sql_to_cypher(query: str, sql_type: str):
    query = query.strip()
    if sql_type == "insert":
        return translate_insert(query)
    elif sql_type == "select":
        return translate_select(query)
    elif sql_type == "update":
        return translate_update(query)
    elif sql_type == "delete":
        return translate_delete(query)
    else:
        raise ValueError("Tipo de consulta no soportado aún.")
