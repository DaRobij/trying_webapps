from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from duckduckgo_search import DDGS

app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI API!"}

llm = Ollama(model="llama3")

class QueryRequest(BaseModel):
    question: str

def web_search(query, num_results=3):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            results.append(f"- {r['title']}: {r['body']}")
    return "\n".join(results)

@app.post("/ask")
def ask_ai(req: QueryRequest):
    # Decide if a web search is necessary
    if "search" in req.question.lower():  # You can modify this logic
        search_results = web_search(req.question)
    else:
        search_results = ""

    prompt_template = """
    You are a helpful assistant with access to web search results.
    Answer the user's question using the information below.

    Web search results:
    {web_results}

    Question: {question}

    Answer:
    """

    prompt = PromptTemplate(
        input_variables=["web_results", "question"],
        template=prompt_template
    )

    final_prompt = prompt.format(web_results=search_results, question=req.question)
    answer = llm(final_prompt)

    return {"answer": answer}

