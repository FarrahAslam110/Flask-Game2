from flask import Flask, request, jsonify
import specific_words
import re

#nlp = spacy.load("en_core_web_md")

app= Flask (__name__)
#nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return 'Hello World'

@app.route('/<name>')
def print_name(name):
    return 'Hi ,{}'.format(name)



@app.route('/specify/<string:sent>',methods=['GET','POST'])
def specify(sent):
    if request.method == 'GET':
        if len(sent) > 0 :
            list1=[]
            for k in specific_words.nlp(sent).noun_chunks:
              result =[]
              start_char_position = k.start_char
              end_char_position = k.end_char
              #print(k.text)
              text1 = re.sub(r'[^A-Za-z0-9\s]', '', k.text)
              search_term = specific_words.remove_stop_words(text1)
              specific_terms = specific_words.search_term_wiki(search_term)
              #print(f'{search_term} : {specific_terms}')
              result=specific_terms
              specific_terms = specific_words.search_term_FR_dataset(search_term)
              #print(f'{search_term} : {specific_terms}')
              result.extend(specific_terms)
              #print(k.text,start_char_position,end_char_position)
              if len(result)>0:
                list1.append((start_char_position, end_char_position,k.text, result))
            return jsonify(list1)
            #return jsonify(syns)
        else:
            return 'Nothing Found',404



