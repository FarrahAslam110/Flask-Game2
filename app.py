from flask import Flask, request, jsonify
import synonyms_get
import specific_words
import re
import requests
import pandas as pd

#nlp = spacy.load("en_core_web_md")

app= Flask (__name__)
#nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return 'Hello World'

@app.route('/<name>')
def print_name(name):
    return 'Hi ,{}'.format(name)

csv_file_path = 'https://raw.githubusercontent.com/FarrahAslam110/gamify/main/software_requirements_extended.csv'
def read_csv():
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path) # Display the first few rows of the DataFrame (optional)
    data_column = df.iloc[:, 1]  # Assuming the second column is at index 1 (0-based indexing)
    data_column = df["Requirement"]
    df=[]
 # Process the data
    text = []  # To store the original text
    for line in data_column:
        line = str(line).strip()  # Convert to string and remove leading/trailing whitespace
        line = re.sub(r'[^A-Za-z0-9\s]', '', line)
        if line:  # Check if the line is not empty
            # Split the line into tokens and remove the first two tokens
                tokens = line.split()
                #sentences.append(word_tokenize(" ".join(tokens)))  # Tokenize the sentence
                text.append(" ".join(tokens))
    return text

file_path="https://raw.githubusercontent.com/FarrahAslam110/gamify/main/FinalDataset2.txt"
def read_txt():
    text=[]
    try:
        response = requests.get(file_path)
        response.raise_for_status()  # Check if the request was successful
        file_content = response.text  # Get the file content as text

        # Process the file_content as needed
        for line in file_content.split('|'):
            #for field in line:
              line = line.strip()  # Remove leading/trailing whitespace without converting to str
                #print(field)
              line = re.sub(r'[^A-Za-z0-9\s]', '', line)
              text.append(line)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the file: {e}")
        return text
    

@app.route('/specify/<string:sent>',methods=['GET','POST'])
def specify(sent):
    if request.method == 'GET':
      if len(sent) > 0 :
            text = read_csv()
            text.extend(read_txt())
            #print(text)

            list1=[]
            for k in specific_words.nlp(sent).noun_chunks:
              #print(k.text)
              text1 = re.sub(r'[^A-Za-z0-9\s]', '', k.text)

              search_term = specific_words.remove_stop_words(text1)
              specific_terms = specific_words.search_term_FR_dataset2(search_term,text) 
              #print(f'{search_term} : {specific_terms}')
              specific_terms.extend(specific_words.search_term_wiki2(search_term))
              print(f'{search_term} : {specific_terms}')
              #print(k.text,start_char_position,end_char_position)
              if len(specific_terms)>0:
                list1.append((k.start_char, k.end_char,k.text, specific_terms))
            return jsonify(list1)
            #return jsonify(syns)
        
      else:
            return 'Nothing Found',404



