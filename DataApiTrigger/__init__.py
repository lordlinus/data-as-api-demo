import logging
import os

import nest_asyncio

from .cosmos_data import CosmosDB
from .fast_api_app import app

nest_asyncio.apply()

import azure.functions as func
from azure.functions import HttpRequest
from fastapi import FastAPI, HTTPException
from nicegui import ui

# <read env setting for Cosmos DB>
endpoint = os.getenv("testcosmos01_ENDPOINT")
key = os.getenv("testcosmos01_KEY")
database_name = os.getenv("testcosmos01_DB")

cosmos_data = CosmosDB(endpoint=endpoint, key=key, database_name=database_name)


@app.get("/")
def read_root():
    return {"Hello": "Sunil"}


@app.get("/customer/{id}")
async def customerInfo(id):
    return await cosmos_data.get_id("customer", id)


@app.get("/policy/{id}")
async def policyInfo(id):
    return await cosmos_data.get_id("policy", id)


@app.get("/agent/{id}")
async def agentInfo(id):
    return await cosmos_data.get_id("agent", id)


@app.get("/options/{id}")
async def optionsInfo(id):
    return await cosmos_data.get_id("options", id)


@app.get("/api/{customerid}")
async def sampleAPI(customerid):
    return await cosmos_data.build_api_response(customerid)


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    # init(app)
    return func.AsgiMiddleware(app).handle(req, context)
