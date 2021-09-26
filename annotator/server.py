import nltk
import spacy
from spacy.lang.en import English
from flask import Flask, request
from flask_cors import cross_origin

from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")
# nlp = English()

USE_LOCAL_TOKENIZER = False

def get_tokens_local(text):

    token_list = []

    start_index = 0
    doc = nlp(text)
    for sent in doc.sents:

        for token in sent:
            token_index = (token.i - sent.start)
            
            token_length = len(token.text)
    
            token_end   = start_index + token_length
            
            # print(start_index, token_end)

            current_token_tuple = (start_index, token_end, token.text)
            token_list.append(current_token_tuple)
            
            start_index = start_index + token_length +1


    return token_list
    

def get_tokens_nltk(text):

    try:
        spans = list(TreebankWordTokenizer().span_tokenize(text))
    except LookupError:
        nltk.download('punkt')
        spans = list(TreebankWordTokenizer().span_tokenize(text))

    result = [(s[0], s[1], text[s[0]:s[1]]) for s in spans]

    return result


@app.route("/tokenize", methods=["POST"])
@cross_origin()
def tokenize():
    text = request.json["text"]

    if(USE_LOCAL_TOKENIZER):
        token_list = get_tokens_local(text)
        return {"tokens": token_list}

    return {"tokens": get_tokens_nltk(text)}


@app.route("/detokenize", methods=["POST"])
@cross_origin()
def detokenize():
    tokens = request.json["tokens"]
    return {"text": TreebankWordDetokenizer().detokenize(tokens)}

def startpy():

    text = "Welcome to TactLabs. It's awesome!!"

    result = get_tokens_nltk(text)
    print(result)

    result = get_tokens_local(text)
    print(result)


if __name__ == "__main__":

    app.run(host = '0.0.0.0', port = 5555, debug = True)

    # startpy()
