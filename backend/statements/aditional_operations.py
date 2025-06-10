import re


def translate_where(where):
    if not where:
        return ""
    # Reemplaza operadores SQL por Cypher
    where = re.sub(r"\s+and\s+", " AND ", where, flags=re.IGNORECASE)
    where = re.sub(r"\s+or\s+", " OR ", where, flags=re.IGNORECASE)
    # LIKE
    where = re.sub(r"(\b\w+\b)\s+like\s+'([^']+)'", r"n.\1 =~ '.*\2.*'", where, flags=re.IGNORECASE)
    # IN
    where = re.sub(r"(\b\w+\b)\s+in\s*\(([^)]+)\)",
                   lambda m: f"n.{m.group(1)} IN [{', '.join([v.strip() for v in m.group(2).split(',')])}]", where,
                   flags=re.IGNORECASE)
    # =, <>, <, >, <=, >= (solo si no empieza por n.)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*=\s*'([^']+)'", r"n.\1 = '\2'", where)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*=\s*([^\s]+)", r"n.\1 = \2", where)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*<>\s*'([^']+)'", r"n.\1 <> '\2'", where)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*<>\s*([^\s]+)", r"n.\1 <> \2", where)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*>=\s*([^\s]+)", r"n.\1 >= \2", where)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*<=\s*([^\s]+)", r"n.\1 <= \2", where)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*>\s*([^\s]+)", r"n.\1 > \2", where)
    where = re.sub(r"(?<!n\.)\b(\w+)\b\s*<\s*([^\s]+)", r"n.\1 < \2", where)
    return where


def translate_having(having):
    # Solo soporta count(n) > x, count(n) = x, etc.
    having = having.replace("count(", "count(")
    having = re.sub(r"count\s*\(\s*\*\s*\)", "count(n)", having, flags=re.IGNORECASE)
    having = re.sub(r"count\s*\(\s*\w+\s*\)", "count(n)", having, flags=re.IGNORECASE)
    having = re.sub(r"count\(n\)\s*([<>=]+)\s*(\d+)", r"count \1 \2", having)
    return having
