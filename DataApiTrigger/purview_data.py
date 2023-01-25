import logging

from azure.core.exceptions import HttpResponseError
from azure.identity import ClientSecretCredential
from azure.purview.catalog import PurviewCatalogClient


class PurviewData:
    def __init__(self, client_id, client_secret, tenant_id, reference_name_purview):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.reference_name_purview = reference_name_purview

    def get_credentials(self):
        credentials = ClientSecretCredential(
            client_id=self.client_id,
            client_secret=self.client_secret,
            tenant_id=self.tenant_id,
        )
        return credentials

    def get_catalog_client(self):
        credentials = self.get_credentials()
        client = PurviewCatalogClient(
            endpoint=f"https://{self.reference_name_purview}.purview.azure.com/",
            credential=credentials,
            logging_enable=True,
        )
        return client

    def get_search_results(self, keywords):
        body_input = {"keywords": keywords}

        try:
            catalog_client = self.get_catalog_client()
        except ValueError as e:
            logging.error(e)

        try:
            response = catalog_client.discovery.query(search_request=body_input)
            return response
        except HttpResponseError as e:
            logging.error(e)
