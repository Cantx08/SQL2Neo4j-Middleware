from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.db.sql_connector import execute_sql_query
from backend.db.neo4j_connector import execute_cypher_query
from backend.logic.sql_parser import parse_sql_type
from backend.logic.translator import translate_sql_to_cypher

app = FastAPI()

class SQLQuery(BaseModel):
    query: str
    target: str

@app.post("/query")
async def run_query(data: SQLQuery):
    sql_type = parse_sql_type(data.query)

    if data.target == "sql":
        try:
            result = execute_sql_query(data.query)
            return {
                "status": "success",
                "translated": None,  # No se traduce a Cypher
                "result": result
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif data.target == "neo4j":
        try:
            # Traducimos a Cypher
            cypher_query = translate_sql_to_cypher(data.query, sql_type)
            # Ejecutamos en Neo4j
            result = execute_cypher_query(cypher_query)
            return {
                "status": "success",
                "translated": cypher_query,
                "result": result
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="Target inválido: debe ser 'sql' o 'neo4j'")
