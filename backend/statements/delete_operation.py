import re

from backend.statements.aditional_operations import translate_where


def translate_delete(query):
    query = query.strip()
    if query.endswith(";"):
        query = query[:-1].strip()
    match = re.match(
        r"delete from\s+(\w+)\s+where\s+(.+);?$", query, re.IGNORECASE)
    if not match:
        raise ValueError("Formato DELETE inválido.")
    table, where = match.groups()
    return f"MATCH (n:{table.capitalize()}) WHERE {translate_where(where)} DETACH DELETE n"
