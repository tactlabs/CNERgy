## CNERgy - Custom NER Annotator

## Credits:
Base code derived from https://github.com/tecoholic/ner-annotator

We have added more features to suppor Spacy3 and more custom requirements



## Starting the application (Spacy 3)

1. Install the dependencies and start the Python Backend server

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python annotator/server.py
```

2. Open another terminal and start the jinja server for the UI

```sh
source env/bin/activate
cd ui-jinja
python server.py
```

Now go to [http://localhost:8080](http://localhost:8080)


### To DO list:

- [] Create Jinja based UI as the existing Vuejs UI is hard for python developers 
- [x] Check Yelp vs Yarn and use the best. If Yelp needed, use it.
- [] Dockerize it (Devops)
- [x] Existing code work only for Spacy 2. We have to support for both Spacy2 and Spacy 3.
- [] Double click is not working as expected
- [] Unselect option can be improved
- [] Paragraph gap is missing
- [] Unique keys collected has to be shown in left
- [] CSV file support


## Known Limitations:

- USE_LOCAL_TOKENIZER should currently be False when running this until our new patch has been tested.
- Data with special characters can not be used for now.
- 