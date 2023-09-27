from flask import Flask, request, jsonify
import synonyms_get
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

@app.route('/synonyms/<string:fr>',methods=['GET','POST'])
def synonyms(fr):
    if request.method == 'GET':
        if len(fr) > 0 :
            syns1 = synonyms_get.create_synonym_dict()
            
            # Example usage
            #original_sentence = "The doll was found in garage. The toy could be sold now. The doll was replaced with a dog. "
            #original_sentence ="The software will be used by user to print account report. The report will be printable by employees through system."
            #original_sentence = 'run race stroll rush nice lovely mean kind'
            #original_sentence = "Only collision estimators shall search for recycled parts.  Users without the collision estimator role shall not have access to the search for recycled parts."
            #original_sentence = "Movies can only be streamed if the customer has purchased a movie  and is within the 2-day time period to stream the movie.Daily usage statistics should be logged  and accessible by the user."
            #original_sentence = "The product will require collaboration with a database management system (DBMS).The DBMS may be located on the same machine as the product or on a separate machine residing on the same computer network."
            original_sentence = fr
            new_sentence = synonyms_get.replace_synonyms_in_sentence(original_sentence,syns1)
            #print("Original Sentence:", original_sentence)
            new_sentence= sorted(new_sentence, key=lambda x: x[0])
            #print("Modified Sentence:", new_sentence )

            return jsonify(new_sentence)
            #return jsonify(syns)
        else:
            return 'Nothing Found',404

@app.route('/specify/<string:sent>',methods=['GET','POST'])
def specify(sent):
    if request.method == 'GET':
        if len(sent) > 0 :
            list1=[]
            for k in synonyms_get.nlp(sent).noun_chunks:
              result =[]
              start_char_position = k.start_char
              end_char_position = k.end_char
              #print(k.text)
              text1 = re.sub(r'[^A-Za-z0-9\s]', '', k.text)
              search_term = synonyms_get.remove_stop_words(text1)
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

'''
def get_suggestions(paragraph,syns1):
  #paragraph = input("Enter a paragraph: ")

  corrected_paragraph = synonyms_get.correct_spelling(paragraph)
  filtered_sentence = []
  nouns = []
  proper_nouns = []
  verbs = []
  #sentences = sent_tokenize(paragraph)
  sentences = paragraph
  sent=paragraph
  #for sent in sentences:
  if 1==1:
      doc = nlp(sent)
      for chunk in doc.noun_chunks:
        print(f'******{chunk.text}*******')
        #proper_nouns.append(remove_stop_words(chunk.text))
      #stop words removal
      filtered_sentence = synonyms_get.remove_stop_words(sent)
      #words = word_tokenize(filtered_sentence)
      words = synonyms_get.word_tokenize(sent)

      pos_tags = nltk.pos_tag(words)

      for word, pos in pos_tags:

            if pos.startswith('NN'):  # Checking if the word is a noun
              nouns.append(word)
            if pos.startswith('NNP'): # If the word is a proper noun
              proper_nouns.append(word)
            if pos=='VB': # If the word is a proper noun
              verbs.append(word)

  print("\nOriginal Paragraph:")
  print(paragraph)

  print("\nCorrected Paragraph:")
  print(corrected_paragraph)

  print("\nStop Word Removed: ")
  print(filtered_sentence)
  
  for noun in nouns:
      synonyms1 = get_synonyms(noun)
      synonyms1 = list(set(synonyms1))#unique synonyms

      print(f"Noun:\n")
      print(f"Synonyms for '{noun}': {', '.join(synonyms1)}")

  for noun in proper_nouns:
      synonyms = get_synonyms(noun)
      print(f"Proper Noun:\n")
      print(f"Synonyms for '{noun}': {', '.join(synonyms)}")

  for verb in verbs:
      verb=remove_stop_words(verb)
      if verb:
        synonyms2 = get_synonyms(verb)
        synonyms2 = list(set(synonyms2))

        print(f"Verbs\n ")
        print(f"Synonyms for '{verb}': {', '.join(synonyms2)}")
  

  print(synonyms_get.replace_synonyms_in_sentence(corrected_paragraph,syns1))
  return synonyms_get.replace_synonyms_in_sentence(corrected_paragraph,syns1)
'''
if __name__ == '__main__':
    app.run()
