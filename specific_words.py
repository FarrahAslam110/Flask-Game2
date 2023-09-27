import requests
#from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import re
import pandas as pd
#import spacy
#import urllib.request

# Load the spaCy model
import en_core_web_md
nlp = en_core_web_md.load()

def categorize_noun_type(text):
    # Process the text with spaCy
    doc = nlp(text)
    #print(doc.text)
    # Check if any named entities are present (proper noun)
    if any(ent.label_ == "PERSON" or ent.label_ == "ORG" or ent.label_ == "LOC" or ent.label_ == "MONEY" or ent.label_ == "GPE" or ent.label_ == "TIME" for ent in doc.ents):
        return "Proper Noun"

    for token in doc:
          doc2=nlp(token.text)
          for token2 in doc2:
            if token2.tag_ == "NNP" or token2.tag_ == "NNPS":
              #print(f'{token2}:{token2.tag_}')
              return "Proper Noun"

    # Check if any tokens are common nouns
    if any(token.pos_ == "NOUN" for token in doc):
        return "Common Noun"

    # If neither condition is met, it may be an ambiguous or non-noun phrase
    return "Other"

def search_term_FR_dataset(target_word):

 # Specify the path to the XLSX file
 csv_file_path = "software_requirements_extended.csv"
 #csv_file_path = "https://drive.google.com/uc?export=download&id=12gZxy_A68Pwth2nEuVpVbX0gnNCB3uvD"
 csv_file_path = 'https://raw.githubusercontent.com/FarrahAslam110/gamify/main/software_requirements_extended.csv'


 # Read the CSV file into a DataFrame
 df = pd.read_csv(csv_file_path) # Display the first few rows of the DataFrame (optional)
 data_column = df.iloc[:, 1]  # Assuming the second column is at index 1 (0-based indexing)
 data_column = df["Requirement"]
 #data_column

 # Process the data
 sentences = []
 text = []  # To store the original text

 for line in data_column:
    line = str(line).strip()  # Convert to string and remove leading/trailing whitespace
    line = re.sub(r'[^A-Za-z0-9\s]', '', line)
    if line:  # Check if the line is not empty
        # Split the line into tokens and remove the first two tokens
        tokens = line.split()
        #sentences.append(word_tokenize(" ".join(tokens)))  # Tokenize the sentence
        text.append(" ".join(tokens))


  # Specify the path to your ARFF file
 # Specify the path to your text file
 #file_path = 'Final Dataset2.txt'
 file_path="https://raw.githubusercontent.com/FarrahAslam110/gamify/main/FinalDataset2.txt"
 #file_path = 'https://drive.google.com/uc?export=download&id=1-0TPULuQYHdOHCYJssxN4kdDcX7uaACe'
 #text =[]
 # Open the file in read mode
 #data = urllib.request.urlopen(file_path)

 #with open(file_path, 'r', encoding='utf-8') as file:
    # Read and process each line
#  for line in file:
# for line_bytes in data:
    # Assuming 'data' contains bytes
    #line = line_bytes.decode('utf-8')  # Decode the bytes into a string using the appropriate encoding
  # Process the fields as needed
    # Process the fields as needed
#    fields = line.strip().split('|')
 try:
  response = requests.get(file_path)
  response.raise_for_status()  # Check if the request was successful
  file_content = response.text  # Get the file content as text

    # Process the file_content as needed
  for line in file_content.split('|'):
      for field in line:
          field = field.strip()  # Remove leading/trailing whitespace without converting to str
            #print(field)
          field = re.sub(r'[^A-Za-z0-9\s]', '', field)
          text.append(field)
     
 except requests.exceptions.RequestException as e:
    print(f"Error fetching the file: {e}")
 # Print the noun chunks
 noun_chunks =[]
 unique_set =[]
 noun_chunks_u =[]
 text= " ".join(text)
    #print(text)
 doc = nlp(text)
 noun_chunks = [remove_stop_words(chunk.text.lower()) for chunk in doc.noun_chunks if chunk.text.lower().endswith(target_word) and remove_stop_words(chunk.text.lower()) != target_word.lower()]
    #print(noun_chunks)
 unique_set = set(noun_chunks)
 noun_chunks_u = list(unique_set)

 return noun_chunks_u



def search_term_wiki(search_term):

 # Set the URL for the MediaWiki API
 api_url = "https://en.wikipedia.org/w/api.php"

 # Set the parameters for the API request
 params = {
    "action": "query",
    "list": "search",
    "srsearch": search_term,
    "srlimit": 1000,  # Increase the limit of search results
    "format": "json",
 }

 # Send the API request
 response = requests.get(api_url, params=params)
 data = response.json()

 # Process the search results
 search_results = data.get("query", {}).get("search", [])

 special_words =[]
 # Print search results
 for result in search_results:
    title = result.get("title", "").lower()
    snippet = result.get("snippet", "")

    if title.lower().endswith(search_term) and categorize_noun_type(title) != "Proper Noun" :
        #print(f"Matching Title: {title}")
        #print(f"Title:{title}  \nSnippet: {snippet}\n")
        #print(f"'{title}' is a {categorize_noun_type(title.lower())}.")
        doc = nlp(title)
        #if any(token.pos_ == "NOUN" for token in doc)
        for t in doc.noun_chunks:
          if t.text.lower().endswith(search_term) and remove_stop_words(t.text.lower()) != search_term:
           special_words.append(remove_stop_words(t.text))

 unique_set = set(special_words)
 noun_chunks_u = list(unique_set)
 return noun_chunks_u



def search_term_FR_dataset2(target_word,ds):
    noun_chunks_u =[]
        #text= " ".join(text)
    #print(ds)
    for text in ds:
        #print(text)
        doc = nlp(text)
        noun_chunks = [remove_stop_words(chunk.text.lower()) for chunk in doc.noun_chunks if chunk.text.lower().endswith(target_word) and remove_stop_words(chunk.text.lower()) != target_word.lower()]
    #print(noun_chunks)
        noun_chunks = set(noun_chunks)
        noun_chunks_u = list(noun_chunks)

    return noun_chunks_u



import requests

def search_term_wiki2(search_term):
    # Set the URL for the MediaWiki API
    api_url = "https://en.wikipedia.org/w/api.php"

    # Set the parameters for the API request
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "srlimit": 1000,  # Increase the limit of search results
        "format": "json",
    }

    # Send the API request and handle errors
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Wikipedia: {e}")
        return []

    # Process the search results more efficiently
    special_words = set()  # Use a set to efficiently track unique special words

    for result in data.get("query", {}).get("search", []):
        title = result.get("title", "").lower()
        if title.endswith(search_term) and categorize_noun_type(title) != "Proper Noun":
            doc = nlp(title)
            special_words.update(
                remove_stop_words(t.text.lower())
                for t in doc.noun_chunks
                if t.text.lower().endswith(search_term) and remove_stop_words(t.text.lower()) != search_term
            )

    return list(special_words)



import nltk
try:
  nltk.data.find('tokenizers/punkt')
except LookupError:
  nltk.download('punkt')
try:
  nltk.data.find('corpora/stopwords')
except LookupError:
  nltk.download('stopwords')
try:
  nltk.data.find('corpora/wordnet')
except LookupError:
  nltk.download('wordnet')

from nltk.corpus import wordnet,stopwords
from nltk.tokenize import word_tokenize

def remove_stop_words(text):
  words = nltk.word_tokenize(text)
  stop_words = set(stopwords.words('english'))

  # Tokenize the text
  # Get the list of English stop words
  # Remove stop words from the tokenized words
  filtered_words = [word for word in words if word.lower() not in stop_words]
  # Join the filtered words to form a sentence
  filtered_text = ' '.join(filtered_words)
  return filtered_text
