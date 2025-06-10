import re

from backend.statements.aditional_operations import translate_where, translate_having


def translate_select(query):
    # SELECT [campos] FROM tabla [WHERE ...] [GROUP BY ...] [HAVING ...];
    select_match = re.match(
        r"select\s+(.*?)\s+from\s+(\w+)(?:\s+where\s+(.*?))?(?:\s+group by\s+(.*?))?(?:\s+having\s+(.*?))?;?$",
        query, re.IGNORECASE)
    if not select_match:
        raise ValueError("Formato SELECT inválido.")
    fields, table, where, group_by, having = select_match.groups()
    table = table.capitalize()
    match_clause = f"MATCH (n:{table})"
    where_clause = f" WHERE {translate_where(where)}" if where else ""
    if fields.strip() == "*":
        return_fields = "n"
    else:
        return_fields = ", ".join([f"n.{f.strip()}" for f in fields.split(",")])
    group_by_clause = ""
    having_clause = ""
    if group_by:
        group_fields = [f.strip() for f in group_by.split(",")]
        group_by_clause = f" WITH {', '.join([f'n.{f}' for f in group_fields])}, count(n) as count"
        return_fields = ", ".join([f"n.{f}" for f in group_fields] + ["count"])
        if having:
            having_clause = f" WHERE {translate_having(having)}"
    return f"{match_clause}{where_clause}{group_by_clause}{having_clause} RETURN {return_fields}"
