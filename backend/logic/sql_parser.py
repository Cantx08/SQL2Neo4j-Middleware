import sqlparse

def parse_sql_type(query: str):
    parsed = sqlparse.parse(query)[0]
    return parsed.get_type().lower()
