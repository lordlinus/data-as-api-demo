import logging
import os

import nest_asyncio

nest_asyncio.apply()

import azure.functions as func
from azure.functions import HttpRequest
from fastapi import FastAPI, HTTPException

from .cosmos_data import CosmosDB
from .fast_api_app import app
from .open_ai_davinci import OpenAIData
from .purview_data import PurviewData

# <read env setting for Cosmos DB>
endpoint = os.getenv("testcosmos01_ENDPOINT")
key = os.getenv("testcosmos01_KEY")
database_name = os.getenv("testcosmos01_DB")

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant_id = os.getenv("tenant_id")
reference_name_purview = os.getenv("reference_name_purview")

api_type = os.getenv("oa_api_type")
api_base = os.getenv("oa_api_base")
api_version = os.getenv("oa_api_version")
api_key = os.getenv("oa_api_key")

cosmos_data = CosmosDB(endpoint=endpoint, key=key, database_name=database_name)

purview_data = PurviewData(client_id, client_secret, tenant_id, reference_name_purview)

open_ai_davinci = OpenAIData(api_type, api_base, api_version, api_key)


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


@app.get("/catalog/{keyword}")
def catalog(keyword):
    return purview_data.get_search_results(keyword)


@app.get("/davinci/{prompt}")
def catalog(prompt):
    return open_ai_davinci.get_openai_response(prompt)["choices"][0]["text"]


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    # init(app)
    return func.AsgiMiddleware(app).handle(req, context)
