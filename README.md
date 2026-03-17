# Portfolio-Demo-RAG
RAG Q&amp;A demo for a55 phone manual. Usable for more.

## Pipeline

- Install all the requirements in requirements.txt in your python environment.

## Extract

- With pdf scans install Tesseract so pymupdf4llm extract can read this.

## Clean

- Using re
- For clean.py (fix_word_spacing) 

    1. Install LM Studio to locally run llm models on your pc.
    2. In LM Studio download "Qwen2.5 7B Instruct 1M"
    3. Go to dev tab (ctrl + 2)
    4. Start local server
    5. Copy the "Reachable at:" (something like http://x.x.x.x:x)
    6. Insert the url in a .env with the variable LM_STUDIO_URL=http://x.x.x.x:x/v1/chat/completions

## Chunk

- using re
- using json

## Embed

- Model: intfloat/multilingual-e5-base

## ChromaDB

- Install ChromaDB in your python environment (see requirements.txt)
- The databases saves its data in output/chromadb