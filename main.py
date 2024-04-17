import json

from fastapi import FastAPI

from modules import Piece, Composer


with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)


app = FastAPI()

@app.get("/composers")
def get_composers():
    return composers_list

@app.get("/pieces")
def get_piece():
    return piece_list

@app.post("/composers")
def create_composer(composer: Composer):
    composers_list.append(composer)

@app.post("/pieces")
def create_pieces(piece: Piece):
    piece_list.append(piece)

@app.put("/composers/{composer_id}")
def update_composer(composer: Composer, composer_id: int):
    for i in composers_list:
        print(i)
        if i["composer_id"] == composer_id:
            i.update(composer.model_dump())

@app.put("/pieces/{piece_name}")
def update_piece(piece: Piece, piece_name: str):
    for i in piece_list:
        if i["piece_name"] == piece_name:
            i.update(piece.model_dump())

@app.delete("/composers/{composer_id}")
def delete_composer(composer_id: int):
    for i in composers_list:
        if i["composer_id"] == composer_id:
            composers_list.remove(i)

@app.delete("/pieces/{piece_name}")
def delete_piece(piece_name: str):
    for i in piece_list:
        if i["piece_name"] == piece_name:
            piece_list.remove(i)