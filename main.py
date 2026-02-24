from fastapi import FastAPI, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from schemas import Word
import httpx
 
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/words/{word}", response_model = Word)
async def get_word(word: str):
    word = word.lower().strip()
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)

    if response.status_code != 200:
        raise HTTPException(status_code = 404, detail = "There is no such word, gng")
    
    data = response.json()

    name = data[0]["word"]
    pronunciation = "N/A"
    definition = "N/A"
    synonyms = []

    for phonetic in data[0].get("phonetics", []):
        if "text" in phonetic:
            pronunciation = phonetic["text"]
            break
    
    for meaning in data[0].get("meanings", []):
        k = meaning.get("definitions", [])
        if k:
            definition = k[0].get("definition", [])
            break

    twoSame = False

    for i in range(len(data)):
        for synonym in data[i].get("meanings", []):
            if "synonyms" in synonym:
                synonyms = synonym["synonyms"]
                if synonyms != []:
                    #print(synonyms, '\n')
                    if(len(synonyms) > 2 and synonyms[0] == synonyms[1]):
                        twoSame = True
                    break
        if synonyms != []:
            break
    gh = 0
    #print(len(synonyms), '\n')
    if len(synonyms) == 0:
        for i in range(len(data)):
            for antonym in data[i].get("meanings", []):
                if "antonyms" in antonym:
                    synonyms = antonym["antonyms"]
                    if synonyms != []:
                        gh = 1
                    break
            if synonyms != []:
                break
    if twoSame:
        synonyms = synonyms[1:3]
    else:
        synonyms = synonyms[:2]
    #print(name, pronunciation, definition, synonyms, sep = '\n')

    if gh == 0:
        return {
            "word": name,
            "pronunciation": pronunciation,
            "definition": definition,
            "synonyms": synonyms
        }
    else:
        return {
            "word": name,
            "pronunciation": pronunciation,
            "definition": definition,
            "antonyms": synonyms
        }

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = Path("static") / "index.html"
    return index_path.read_text(encoding="utf-8")