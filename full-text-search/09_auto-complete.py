"""
オートコンプリート機能（ユーザーが検索ボックスに入力したときに一致する可能性があるものを提供することができる）
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

# Autocomplete a query
search_suggestion = 'sa'
results = search_client.autocomplete(
    search_text=search_suggestion, 
    suggester_name="sg",
    mode='twoTerms')

print("Autocomplete for:", search_suggestion)
for result in results:
    print (result['text'])
