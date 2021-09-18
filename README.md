## custom-ner-annotator

### Credits:
Base code derived from https://github.com/tecoholic/ner-annotator

We have added more features to suppor Spacy3 and more custom requirements



## Starting the application

1. Install the dependencies and start the Python Backend server

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python annotator/server.py
```

2. Open another terminal and start the server for the UI

```sh
cd ui
yarn install
yarn serve
```

Now go to [http://localhost:8080](http://localhost:8080)