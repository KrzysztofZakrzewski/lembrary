# LemLibrary

LemLibrary is a project created out of a passion for the works of Stanisław Lem.  
As a fan of his books, I built an interactive "Lem library" that uses text embeddings
and semantic search to help users discover Lem's works based on topics, questions
and interests they provide.

The library currently contains 20 titles, but I believe fans of Lem will still find
something interesting to explore.

## Features

- Semantic search for Stanisław Lem books
- Book recommendations based on user topics and questions
- Dynamic translation of the interface and descriptions using an LLM
- Book covers and descriptions displayed in the results

## Tech Stack

- Python
- Streamlit
- OpenAI embeddings
- Qdrant vector database

## Requirements

The project requires **Conda** to manage the Python environment.

## Run Locally

Clone the repository and run the application using Conda:

```bash
conda create -n lemlibrary python=3.11
conda activate lemlibrary

pip install -r requirements.txt

streamlit run app.py

## How it works

```mermaid
flowchart TD
    A[User selects language] --> B[Normalize language using LLM]
    B --> C[Store language in session_state]

    D[User enters topic or question] --> E[Generate embedding from query]
    E --> F[Vector search in Qdrant]

    F --> G[Top matching Lem books]
    G --> H[Render results in Streamlit]
    C --> H
    H --> I[Translate UI and descriptions to selected language]
```

## Architecture
```mermaid
.
├── app.py
├── assets
│   ├── main
│   │   ├── 1966_rakieta-778x1024-1©_by_Tomasz_Lem.jpg
│   │   └── 1966_rakieta-778x1024-1©_by_Tomasz_Lem_movie.mp4
│   └── pictures
|       └── pisc.jpg
├── develop-eggs
|
├── Dockerfile
├── README.md
├── requirements.txt
├── src
│   ├── books.py
│   ├── embeddings.py
│   ├── translation_ai.py
│   └── vectorstore.py
└── ui
    ├── lnadingpage.py
    └── media.py
```

## Stanisław Lem


(1921–2006) was one of the most outstanding science fiction writers of the 20th century, as well as an essayist, futurologist and philosopher. He was born in Lviv and, after World War II, settled in Kraków, where he spent most of his life. His work combined scientific imagination, sharp satire and deep reflection on the nature of humanity, technology and the future of civilization.

Lem is the author of such works as Solaris, The Cyberiad, The Fables of Robots, The Star Diaries and Tales of Pirx the Pilot. His books have been translated into more than 40 languages, with total sales exceeding 45 million copies, making him the most widely translated Polish author.

A characteristic element of his style was intelligent humor, grotesque imagery, irony and philosophical provocation. Lem used science fiction not only to imagine the future, but above all to critically comment on the modern world, human weaknesses and the limits of human knowledge.

To this day he remains one of the most important and original figures in world science fiction literature, and his works continue to inspire scientists, philosophers, programmers and artists around the globe.