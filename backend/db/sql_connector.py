import pyodbc

def get_sql_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;DATABASE=TestMiddlewareDB;UID=sa;PWD=P@ssw0rd;"
    )
    return conn

def execute_sql_query(query: str):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    if query.strip().lower().startswith("select"):
        result = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    else:
        conn.commit()
        result = f"{cursor.rowcount} filas afectadas."

    cursor.close()
    conn.close()
    return result
