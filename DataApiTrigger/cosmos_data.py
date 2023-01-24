import asyncio
import logging
import os
import time

from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.cosmos.aio import CosmosClient

# from azure.identity import DefaultAzureCredential
# from azure.mgmt.cosmosdb import CosmosDBManagementClient


class CosmosDB:
    def __init__(self, endpoint, key, database_name):
        self.endpoint = endpoint
        self.key = key
        self.database_name = database_name

    async def get_client(self):
        return CosmosClient(self.endpoint, credential=self.key)

    # <create_database_if_not_exists>
    async def get_or_create_db(self, client, database_name):
        try:
            database_obj = client.get_database_client(database_name)
            await database_obj.read()
            return database_obj
        except exceptions.CosmosResourceNotFoundError:
            logging.info("Creating database")
            return await client.create_database(database_name)

    # </create_database_if_not_exists>

    # <create_container_if_not_exists>
    async def get_or_create_container(self, database_obj, container_name):
        try:
            todo_items_container = database_obj.get_container_client(container_name)
            await todo_items_container.read()
            return todo_items_container
        except exceptions.CosmosResourceNotFoundError:
            logging.error("Creating container with a partition key")
        except exceptions.CosmosHttpResponseError:
            logging.error("Fatal")
            raise

    # </create_container_if_not_exists>

    # <method_read_items>
    async def read_items(self, container_obj, items_to_read, partition_key):
        # Read items (key value lookups by partition key and id, aka point reads)
        # <read_item>
        for item in items_to_read:
            item_response = await container_obj.read_item(
                item=item["id"], partition_key=item[partition_key]
            )
            request_charge = container_obj.client_connection.last_response_headers[
                "x-ms-request-charge"
            ]
            logging.info(
                f"Read item with id {item_response['id']}. Operation consumed {request_charge} request units"
            )
        # </read_item>

    # <method_query_items>
    async def query_items(self, container_obj, query_text):
        # enable_cross_partition_query should be set to True as the container is partitioned
        # In this case, we do have to await the asynchronous iterator object since logic
        # within the query_items() method makes network calls to verify the partition key
        # definition in the container
        # <query_items>
        query_items_response = container_obj.query_items(
            query=query_text, enable_cross_partition_query=True
        )
        request_charge = container_obj.client_connection.last_response_headers[
            "x-ms-request-charge"
        ]
        items = [item async for item in query_items_response]
        logging.info(
            f"Query returned {len(items)} items. Operation consumed {request_charge} request units"
        )
        return items

    # </query_items>

    async def build_api_response(self, customerid):
        logging.info(f"Build api response for {customerid}")
        # <create_cosmos_client>
        async with CosmosClient(self.endpoint, credential=self.key) as client:
            # </create_cosmos_client>
            try:
                # create a database
                database_obj = await self.get_or_create_db(client, self.database_name)
                # create a container
                customer_obj = await self.get_or_create_container(
                    database_obj, "customer"
                )
                agent_obj = await self.get_or_create_container(database_obj, "agent")
                policy_obj = await self.get_or_create_container(database_obj, "policy")
                options_obj = await self.get_or_create_container(
                    database_obj, "options"
                )

                policy_info = await self.query_items(
                    policy_obj,
                    f"SELECT top 10 * FROM c WHERE c.customerid = '{customerid}'",
                )
                customer_info = await self.query_items(
                    customer_obj, f"SELECT top 10 * FROM c WHERE c.id = '{customerid}'"
                )
                agent_info = await self.query_items(
                    agent_obj,
                    f"SELECT top 10 * FROM c WHERE c.agent_no = '{policy_info[0]['servingagentid']}'",
                )
                options_info = await self.query_items(
                    options_obj,
                    f"SELECT top 10 * FROM c WHERE c.policyid = '{policy_info[0]['policyno']}'",
                )
                api_response = {
                    "customer": customer_info,
                    "policy": policy_info,
                    "agent": agent_info,
                    "options": options_info,
                }
                # logging.info(api_response)
                return api_response
            except exceptions.CosmosHttpResponseError as e:
                logging.error(f"\ncaught an error. {e.message}")
            except:
                logging.error("\ncaught an error.")

    async def get_id(self, container_name, id):
        logging.info(f"Build api response for {id} in {container_name}")
        # <create_cosmos_client>
        async with CosmosClient(self.endpoint, credential=self.key) as client:
            # </create_cosmos_client>
            try:
                # create a database
                database_obj = await self.get_or_create_db(client, self.database_name)
                container_obj = await self.get_or_create_container(
                    database_obj, container_name
                )
                id_info = await self.query_items(
                    container_obj, f"SELECT * FROM c WHERE c.id = '{id}'"
                )
                return {container_name: id_info}
            except exceptions.CosmosHttpResponseError as error_msg:
                logging.error(f"\ncaught an error. {error_msg.message}")
            except:
                logging.error(f"\ncaught an error.")
