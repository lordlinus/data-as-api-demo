# Note: The openai-python library support for Azure OpenAI is in preview.
# import os

import openai

# openai.api_type = "azure"
# openai.api_base = "https://ssattirajuopenai01.openai.azure.com/"
# openai.api_version = "2022-12-01"
# openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAIData:
    def __init__(self, api_type, api_base, api_version, api_key):
        self.api_type = api_type
        self.api_base = api_base
        self.api_version = api_version
        self.api_key = api_key
        openai.api_type = self.api_type
        openai.api_base = self.api_base
        openai.api_version = self.api_version
        openai.api_key = self.api_key

    def get_openai_response(self, prompt):
        return openai.Completion.create(
            engine="davinci-v3",
            prompt=prompt,
            temperature=0.7,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
