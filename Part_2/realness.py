# Import modules
import sys
import os
import time
import nltk
from nltk.corpus import words
import requests
import time
import xlsxwriter
import pandas as pd
import spacy
from spacy.util import is_package
from spacy.cli import download

if is_package("en_core_web_lg"):
    print(f"Model en_core_web_lg is already installed.")
else:
    print(f"Model en_core_web_lg not found. Downloading...")
    download("en_core_web_lg")

nlp = spacy.load("en_core_web_lg")


# Read the file
input_file = sys.argv[1]

df = pd.read_excel(input_file)
print('file is loaded')

df_tess = df[df["OCR"]=="tesseract"]
df_doctr = df[df["OCR"]=="doctr"]


# Processing 
def paper_real_words(paper_interest):
    #returns the words that are not real
    
    
    def force_utf8(value):
        try:
            return value.encode('utf-8').decode('utf-8', errors='replace')
        except Exception:
            return "ENCODING_ERROR"

    def paper_word_processing(paper_interest):
        df_new = df
        df_new_sorted = df_new.sort_values(by='Word')
        df_new_sorted['Word'] = df_new_sorted['Word'].astype(str)
        df_new_sorted['Word'] =  df_new_sorted['Word'].apply(force_utf8)
        return df_new_sorted['Word'].drop_duplicates().reset_index(drop=True)

    def to_lowercase(data):
        if isinstance(data, list):  
            return [to_lowercase(item) for item in data]
        elif isinstance(data, str):  
            return data.lower()
        else:  
            return data
    
    word_set = words.words()
    lowercase_word_set = to_lowercase(word_set)
    
    def is_real_word_nltk(word):
        if word.isnumeric():
            return True
        else:
            return word.lower() in lowercase_word_set
   
    def is_real_word_spacy(word):
        token = nlp.vocab[word]
        return not token.is_oov
    
    def check_word_in_pubmed(word, api_key=None):
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
        params = {
            'db': 'pubmed',               # Search in the PubMed database
            'term': word,                 # The word to search for
            'retmax': '1',                # Limit the number of results (1 is enough for existence check)
            'usehistory': 'y',            # Use history to get more results if needed
            'api_key': api_key,           # Optional: your API key for more requests
            'retmode': 'xml',             # Get results in XML format
        }
        response = requests.get(base_url, params=params)
        time.sleep(2)
        if response.status_code == 200:
            xml_data = response.text
            # Check if the term exists in the response (looking for the count of results)
            if "<Count>0</Count>" in xml_data:
                return False
            else:
                return True
        else:
            return False

    
    after_nltk = paper_word_processing(paper_interest)
    x_nltk = after_nltk.apply(lambda word: is_real_word_nltk(word))
    
    print('paper words',len(after_nltk))
    print('false words remaining after nltk', (x_nltk==False).sum())
    
    after_spacy = after_nltk[x_nltk==False].reset_index(drop=True)
    x_spacy = after_spacy.apply(lambda word: is_real_word_spacy(word))

    print('false words remaining after spacy', (x_spacy==False).sum())

    after_pubmed = after_spacy[x_spacy==False].reset_index(drop=True)
    x_pubmed = after_pubmed.apply(lambda word: check_word_in_pubmed(word))
    xxx_nltk = after_pubmed.apply(lambda word: check_word_in_pubmed(word))
    
    print('false words remaining after pubmed ', (x_spacy==False).sum())
    
    x_final = after_pubmed[x_pubmed==False].reset_index(drop=True)
    realness = round(1 - ((x_pubmed==False).sum()/len(x)),2)
    return realness, x_final

print('finish processing')


# Export the data
realness1, words1 = paper_real_words(df_tess)
realness2, words2 = paper_real_words(df_doctr)

df_out = pd.DataFrame()
df_out['words_tess'] = words1
df_out['realness_tess'] = realness1
df_out['words_doctr'] = words2
df_out['realness_doctr'] = realness2

output_file = f"{input_file.removesuffix('.xlsx')}_realness.xlsx"
df_out.to_excel(output_file, index=False)

print('finished')
