# potato-sorter

FLASK_APP=api FLASK_ENV=development flask run

# Testing the API:

To get the json state of a potato:

curl -H'Accept: application/json' 'localhost:5000/potato/29b3883f-da01-46d5-8059-db699fae07c5'