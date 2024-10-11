import json
import os
import requests
from langchain.tools import tool

class SearchTools():

    @tool("Search the internet")
    def search_internet(query):
        """Search the internet about a given topic and return relevant results"""
        print("Searching the internet...")
        
        # Extract the query string if `query` is a dictionary
        if isinstance(query, dict):
            query_string = query.get('title', 'No title provided')
        else:
            query_string = str(query)  # Fallback to string conversion if not a dictionary

        print("Query:", query_string)  # Ensure query is a string
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query_string, "num": 5, "tbm": "nws"})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        
        # Log the entire response object for debugging
        response_json = response.json()
        print("API Response JSON:", response_json)
        
        # Check if there is an 'organic' key in the response
        if 'organic' not in response_json:
            return "Sorry, I couldn't find anything about that. There might be an error with your Serper API key."
        else:
            results = response_json['organic']
            string = []
            for result in results[:5]:
                try:
                    # Attempt to extract the date
                    date = result.get('date', 'Date not available')
                    string.append('\n'.join([
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Date: {date}",  # Include the date in the output
                        f"Snippet: {result['snippet']}",
                        "\n-----------------"
                    ]))
                except KeyError:
                    continue

            return '\n'.join(string)
