import logging

from azure.cosmos import exceptions
from azure.cosmos.aio import CosmosClient


class CosmosDB:
    def __init__(self, endpoint, key, database_name):
        self.endpoint = endpoint
        self.key = key
        self.database_name = database_name

    async def get_id(self, container_name, item_id):
        logging.info(f"Build api response for {item_id} in {container_name}")
        async with CosmosClient(self.endpoint, credential=self.key) as client:
            try:
                database = client.get_database_client(self.database_name)
                container = database.get_container_client(container_name)
                q = container.query_items(
                    f"SELECT * FROM c WHERE c.id = '{item_id}'",
                    enable_cross_partition_query=True,
                )
                res = [item async for item in q]
                return res
            except exceptions.CosmosResourceExistsError as error_msg:
                logging.error(error_msg)
                raise

    async def build_api_response(self, customerid):
        logging.info(f"Build api response for {customerid}")
        # <create_cosmos_client>
        async with CosmosClient(self.endpoint, credential=self.key) as client:
            database = client.get_database_client(self.database_name)
            customer_container = database.get_container_client("customer")
            agent_container = database.get_container_client("agent")
            policy_container = database.get_container_client("policy")
            options_container = database.get_container_client("options")

            policy_info, customer_info = (
                policy_container.query_items(
                    f"SELECT top 10 * FROM c WHERE c.customerid = '{customerid}'"
                ),
                customer_container.query_items(
                    f"SELECT top 10 * FROM c WHERE c.id = '{customerid}'"
                ),
            )

            policy_res = [x async for x in policy_info]
            customer_res = [x async for x in customer_info]

            agent_info, options_info = (
                agent_container.query_items(
                    f"SELECT top 10 * FROM c WHERE c.agent_no = '{policy_res[0]['servingagentid']}'"
                ),
                options_container.query_items(
                    f"SELECT top 10 * FROM c WHERE c.policyid = '{policy_res[0]['policyno']}'"
                ),
            )
            agent_res = [x async for x in agent_info]
            options_res = [x async for x in options_info]

            api_response = {
                "customer": customer_res,
                "policy": policy_res,
                "agent": agent_res,
                "options": options_res,
            }
            return api_response
        # except exceptions.CosmosHttpResponseError as error_msg:
        #     logging.error(f"\ncaught an error. {error_msg.message}")
        # except Exception as error_msg:
        #     logging.error(f"\nError. {error_msg}")
