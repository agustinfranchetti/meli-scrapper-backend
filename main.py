from typing import Union

from fastapi import FastAPI
from modules.scrapping import search_items
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data/{term}")
def get_data(term: str):
    return search_items(term=term)