# Simple Dictionary API (FastAPI)

A small full-stack project built with FastAPI and a minimal HTML/JS frontend.

The app takes a word, fetches data from a public dictionary API, and returns:

- word
- pronunciation
- definition
- synonyms (or antonyms if synonyms are missing)

This was built to practice:
- async requests with httpx
- parsing nested JSON
- Pydantic response models
- basic frontend ↔ backend integration

---

## How to run

1. Clone the repo:
git clone https://github.com/YOUR_USERNAME/dictionary-api.git


2. Create & activate virtual environment:
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the server
uvicorn main:app --reload

5. Open:
http://127.0.0.1:8000/

-------------------------------------------------

Simple learning project for myself