# Azure Functions Project with FastAPI Framework

## Introduction

This project is a Azure Functions project that uses FastAPI framework. FastAPI is a modern, fast, web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Reference Links

- [Using FastAPI Framework with Azure Functions](https://learn.microsoft.com/en-us/samples/azure-samples/fastapi-on-azure-functions/azure-functions-python-create-fastapi-app/)

- [Azure Purview REST API](https://learn.microsoft.com/en-us/azure/purview/tutorial-using-rest-apis)

- [Azure OpenAI REST API reference](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference)

## Prerequisites

- Python 3.7 or later
- Azure Functions Core Tools v4 ( latest)
- Azure CLI

## Setup

1. Clone this repository

   ```bash

   git clonehttps://github.com/lordlinus/data-as-api-demo.git
   ```

2. Install dependencies

   ```bash

   cd data-as-api-demo
   pip install -r requirements.txt
   ```

3. Create an Azure Functions app in the cloud:

   ```css
   az login
   az functions app create --name <app-name> --storage-account <storage-account-name> --runtime python --consumption-plan-location <location>
   ```

4. Set the environment variable in the Azure Functions app:

   ```css
   az webapp config appsettings set --name <app-name> --settings FUNCTIONS_EXTENSION_VERSION=~4
   ```

## Deployment

1. Publish the Azure Functions app to the cloud:

```bash

func azure functionapp publish <app-name>
```

## Endpoints

The API has the following endpoint:

- `/davinci`: A GET request to this endpoint with a question/prompt will return the answer from the model.
- `/catalog`: A GET request to this endpoint with a keyword will return the answer from the Purview catalog.

## Conclusion

With this project, you have a fully functional Azure Functions app using FastAPI framework. This can serve as a starting point for building more complex APIs.
