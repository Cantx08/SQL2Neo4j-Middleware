import re

from backend.statements.aditional_operations import translate_where


def translate_update(query):
    query = query.strip()
    if query.endswith(";"):
        query = query[:-1].strip()
    match = re.match(
        r"update\s+(\w+)\s+set\s+(.+?)\s+where\s+(.+)\s*$", query, re.IGNORECASE)
    if not match:
        raise ValueError("Formato UPDATE inválido.")
    table, set_part, where = match.groups()
    set_pairs = [p.strip() for p in set_part.split(",")]
    set_clause = ", ".join([
        f"n.{k.strip()} = {v.strip() if v.strip().isdigit() else repr(v.strip().strip('\'\"'))}"
        for k, v in (p.split("=") for p in set_pairs)
    ])
    return f"MATCH (n:{table.capitalize()}) WHERE {translate_where(where)} SET {set_clause} RETURN n"
