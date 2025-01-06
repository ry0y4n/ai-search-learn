"""
フィルタイング
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
results = search_client.search(
    search_text="hotels",
    select="HotelId,HotelName,Rating",
    filter="Rating gt 4",
    order_by="Rating desc",
)

for result in results:
    print("{}: {} - {} rating".format(result["HotelId"], result["HotelName"], result["Rating"]))
