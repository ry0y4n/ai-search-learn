# Set up the query for generating responses
from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider
from azure.search.documents import SearchClient
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# python-dotenv
load_dotenv()

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
openai_client = AzureOpenAI(
    api_version="2024-06-01",
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    azure_ad_token_provider=token_provider
)

search_client = SearchClient(
    endpoint=os.getenv("AISEARCH_ENDPOINT"),
    index_name="hotels-sample-index",
    credential=credential
)

# This prompt provides instructions to the model
GROUNDED_PROMPT="""
You are a friendly assistant that recommends hotels based on activities and amenities.
Answer the query using only the sources provided below in a friendly and concise bulleted manner.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
Sources:\n{sources}
"""

# Query is the question being asked. It's sent to the search engine and the LLM.
query="Can you recommend a few hotels with complimentary breakfast?"

# Set up the search results and the chat thread.
# Retrieve the selected fields from the search index related to the question.
search_results = search_client.search(
    search_text=query,
    top=5,
    select="Description,HotelName,Tags"
)
sources_formatted = "\n".join([f'{document["HotelName"]}:{document["Description"]}:{document["Tags"]}' for document in search_results])

response = openai_client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": GROUNDED_PROMPT.format(query=query, sources=sources_formatted)
        }
    ],
    model=os.getenv("AOAI_DEPLOYMENT_NAME")
)

print(response.choices[0].message.content)