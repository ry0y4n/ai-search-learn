"""
キーに基づいてドキュメントを検索（検索結果の項目を選択したときにドリルスルーを提供する時に便利）
"""
from azure.core.credentials import AzureKeyCredential

from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
import os
from dotenv import load_dotenv

# python-dotenv
load_dotenv()

search_endpoint: str = os.getenv("SEARCH_ENDPOINT")
search_api_key: str = os.getenv("SEARCH_KEY")
index_name: str = os.getenv("INDEX_NAME")

credential = AzureKeyCredential(search_api_key)
search_client = SearchClient(endpoint=search_endpoint,
                      index_name=index_name,
                      credential=credential)

# Look up a specific document by ID
result = search_client.get_document(key="3")

print("Details for hotel '3' are:")
print("Name: {}".format(result["HotelName"]))
print("Rating: {}".format(result["Rating"]))
print("Category: {}".format(result["Category"]))
