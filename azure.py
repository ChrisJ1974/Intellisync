import os
import pyodbc, struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Revenue(BaseModel):
    year: int
    grossrevenue: float
    netrevenue: float
    beginninginventory: float
    purchases: float
    endinginventory: float
    grossrevenue: float
    sellingexpenses: float
    adminexpenses: float
    RDexpenses: float
    depAm:  float
    intIncome: float
    intExpense: float
    
connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

app = FastAPI()


@app.get("/all")
def get_revenue(grossrevenue, netrevenue, beginninginventory, purchases, endinginventory, sellingexpenses, adminexpenses, RDexpenses, depAm, intIncome, intExpense):
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT GrossSales_Revenue, NetSalesRevenue FROM Revenue where Year = 2023")

        for row in cursor.fetchall():
            print(row.FirstName, row.LastName)
            rows.append(f"{row.ID}, {row.FirstName}, {row.LastName}")
    return rows

@app.get("/person/{person_id}")
def get_person(person_id: int):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Persons WHERE ID = ?", person_id)

        row = cursor.fetchone()
        return f"{row.ID}, {row.FirstName}, {row.LastName}"



    return item

def get_conn():
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn
