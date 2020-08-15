## Setup

```
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

# potato-sorter - for deployment
$ ssh root@potatosorter.com


$ waitress-serve --call "api:create_app"


# potato-sorter

FLASK_APP=api FLASK_ENV=development flask run

# Testing the API:

To get the json state of a potato:

curl -H'Accept: application/json' 'localhost:5000/potato/29b3883f-da01-46d5-8059-db699fae07c5'
