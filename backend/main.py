from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from pydantic import BaseModel, Field

from retrieval import find_chunks  # 추가


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.post("/api/chat")
def chat(request: ChatRequest):
    chunks = find_chunks(request.question)
    if not chunks:
        # 자료를 못 찾으면 모델을 호출하지 않습니다.
        return {
            "answer": "자료에서 관련 내용을 찾지 못했습니다.",
            "sources": [],
        }

    # 찾은 문단들을 하나의 자료로 합칩니다.
    context = "\n\n".join(chunk["text"] for chunk in chunks)

    prompt = f"""아래 자료를 바탕으로 질문에 답하세요.
자료에 없으면 찾을 수 없다고 말하세요.

자료:
{context}

질문: {request.question}"""

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )

    sources = []
    for chunk in chunks:
        name = chunk["source"]
        if name not in sources:
            sources.append(name)
    return {"answer": interaction.output_text, "sources": sources}