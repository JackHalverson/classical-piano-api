import json
from fastapi import FastAPI, HTTPException, status
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
def get_piece(composer_id: int = None):
    if composer_id:
        return [piece for piece in piece_list if piece["composer_id"] == composer_id]
    return piece_list

@app.post("/composers")
def create_composer(composer: Composer):
    for i in composers_list:
        if i["composer_id"] == composer.composer_id:
            raise HTTPException(status_code=400, detail="Composer ID already exists")
    if composers_list:
        max_id = max(i["composer_id"] for i in composers_list)
    else:
        max_id = 0
    composer.composer_id = max_id + 1
    composers_list.append(composer)
    return {"message": "Composer created successfully"}, status.HTTP_201_CREATED

@app.post("/pieces")
def create_pieces(piece: Piece):
    if not (1 <= piece.difficulty <= 10):
        raise HTTPException(status_code=400, detail="Difficulty must be between 1 and 10")
    
    if not any(composer["composer_id"] == piece.composer_id for composer in composers_list):
        raise HTTPException(status_code=400, detail="Composer ID doesn't exist")
    
    piece_list.append(piece)
    return {"message": "Piece created successfully"}, status.HTTP_201_CREATED

@app.put("/composers/{composer_id}")
def update_composer(composer: Composer, composer_id: int):
    for i in composers_list:
        if i["composer_id"] == composer_id:
            i.update(composer.model_dump())
            return {"message": "Composer updated successfully"}, status.HTTP_200_OK
    raise HTTPException(status_code=404, detail="Composer not found")

@app.put("/pieces/{piece_name}")
def update_piece(piece: Piece, piece_name: str):
    for i in piece_list:
        if i["name"] == piece_name:
            i.update(piece.model_dump())
            return {"message": "Piece updated successfully"}, status.HTTP_200_OK
    raise HTTPException(status_code=404, detail="Piece not found")

@app.delete("/composers/{composer_id}")
def delete_composer(composer_id: int):
    for i in composers_list:
        if i["composer_id"] == composer_id:
            composers_list.remove(i)
            return {"message": "Composer deleted successfully"}, status.HTTP_200_OK
    raise HTTPException(status_code=404, detail="Composer not found")

@app.delete("/pieces/{piece_name}")
def delete_piece(piece_name: str):
    for i in piece_list:
        if i["name"] == piece_name:
            piece_list.remove(i)
            return {"message": "Piece deleted successfully"}, status.HTTP_200_OK
    raise HTTPException(status_code=404, detail="Piece not found")
