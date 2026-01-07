import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('GUARDIAN_API_KEY')

print(API_KEY)

def search_guardian_articles(api_key, search_term='', page=1, page_size=100, format_='json'):
    '''Retrieves meta data of articles matching the search term'''
    search_term = search_term.replace(' ', '%20')
    
    # Now, we'll make the request
    url = 'https://content.guardianapis.com/football'
    print(search_term)
    params = {'api-key':API_KEY,
             'format':'json',
              'page':page,
              'page-size':page_size,
             'q':search_term}
    
    response = requests.get(url, params=params)
    print(response)
    return response.json()

def guardian_articles_dataframe(api_key, search_term='', number_of_records=200):
    '''Returns a dataframe with article information from the Guardian API
    
    var:
        search_term: Query string passed to the Guardian API to search the server database
        
        api_key: key required to access the Guardian API. Available for free from Guardian Developer website
        
        number_of_records: Indicates the  number of records to return in the dataframe'''
    # Instantiate the pandas dataframe
    # Iterate through a series of API calls to retrieve the records, and append to dataframe

    searched_articles = search_guardian_articles(api_key=API_KEY, search_term=search_term, page_size=number_of_records, page=1)['response']['results']
    print(searched_articles)
    # Make row data with name of article, and url
    df = pd.json_normalize(searched_articles)

    return df


# Example usage to search for Arsenal matches

search_term = 'Premier AND League'

df = guardian_articles_dataframe(api_key=API_KEY, search_term=search_term)
df.head()

all_body_text = []
# Iterate through a series of API calls to retrieve the text for the articles
for index, row in df.iterrows():
    url_id = row['id']
    url = f'https://content.guardianapis.com/{url_id}'
    
    params = {
        "api-key": API_KEY,
        "show-fields": "headline,bodyText"
    }

    response = requests.get(url, params=params).json()

    content = response["response"]["content"]
    headline = content["fields"]["headline"]
    body_text = content["fields"]["bodyText"]

    all_body_text.append(body_text)

    print(headline)
    print(index)
    print("\n")
    print(body_text)

# Save the body texts to a text file
with open('guardian_articles_body_text.txt', 'w', encoding='utf-8') as f:
    for text in all_body_text:
        f.write(text)
        f.write("\n\n---\n\n")  # Separator between articles    