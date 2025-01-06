"""
特定のフィールドにクエリ実行の範囲を制限
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

# Run an empty query (returns selected fields, all documents)
results =  search_client.search(query_type='simple',
    search_text="sublime" ,
    search_fields=["HotelName"],
    select='HotelId,HotelName')

for result in results:
    print("{}: {}".format(result["HotelId"], result["HotelName"]))
