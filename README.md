# DocuFetch
Lanngchain powered information retrival system for my personal use

## Usage

Install python dependencies from requirements.txt

`python3 ./data-loader/main.py <base_url>`

Example
`python3 ./data-loader/main.py http://resume.ryanrozario.com/`

This will run a web crawler and get data from all sites in the domain of base_url
The crawler will start from base url
Data gets stored in a chroma db

Limited to 10 url (can be modified in webbase_loader.py )

Then run `uvicorn data-retriver.server:app --reload` to spin up a api server to query the information

You can query at `http://localhost:8000/query`

Body:
`{"input": "what does ryan rozario do"}`

## Todo
[] Make a data loader api rather than a job that has to be run at the start
[] Improve crawler to use a particular base url rather than domain
[] Try to see if using bfs gives better results

