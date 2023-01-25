import asyncio
import logging

from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.cosmos.aio import CosmosClient

endpoint = "https://test-cosmos-01.documents.azure.com:443"
key = "ZUBnJorHc2OOEFaiDXAhPzfVrbUm04x9BM1ILF2m8scj2XYIcoo0oNEsgUwNcdUmrqDSsmvKXE4fACDbh0pf6A=="
connection_string = "AccountEndpoint=https://test-cosmos-01.documents.azure.com:443/;AccountKey=ZUBnJorHc2OOEFaiDXAhPzfVrbUm04x9BM1ILF2m8scj2XYIcoo0oNEsgUwNcdUmrqDSsmvKXE4fACDbh0pf6A==;"
database_name = "db01"
container_name = "customer"
import os


async def examples_async():
    async with CosmosClient(endpoint, key) as client:
        try:
            database = client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            async for item in container.query_items(
                query="SELECT top 10 * FROM c ",
                enable_cross_partition_query=True,
            ):
                print(item)
            # print(dir(database))
        except exceptions.CosmosResourceExistsError:
            database = client.get_database_client(database=database_name)
    # return await database.read()


loop = asyncio.get_event_loop()
loop.run_until_complete(examples_async())

# async def get_client(self):
#     return CosmosClient(self.endpoint, credential=self.key)


# # <create_database_if_not_exists>
# async def get_or_create_db(client, database_name):
#     try:
#         database_obj = client.get_database_client(database_name)
#         await database_obj.read()
#         return database_obj
#     except exceptions.CosmosResourceNotFoundError:
#         logging.info("Creating database")
#         return await client.create_database(database_name)

# get_or_create_db(get_client, database_name)

# </create_database_if_not_exists>

# <create_container_if_not_exists>
# async def get_or_create_container(database_obj, container_name):
#     try:
#         todo_items_container = database_obj.get_container_client(container_name)
#         await todo_items_container.read()
#         return todo_items_container
#     except exceptions.CosmosResourceNotFoundError:
#         logging.error("Creating container with a partition key")
#     except exceptions.CosmosHttpResponseError:
#         logging.error("Fatal")
#         raise

#     # </create_container_if_not_exists>


# # <create_cosmos_client>
# async with CosmosClient(endpoint, credential=key, id="test") as client:
#     # </create_cosmos_client>
#     try:
#         # create a database
#         database_obj = await get_or_create_db(client, self.database_name)
#         container_obj = await get_or_create_container(database_obj, container_name)
#         id_info = await query_items(
#             container_obj, f"SELECT * FROM c WHERE c.id = '{id}'"
#         )
#         return {container_name: id_info}
#     except exceptions.CosmosHttpResponseError as error_msg:
#         logging.error(f"\ncaught an error. {error_msg.message}")
#     except:
#         logging.error(f"\ncaught an error.")
