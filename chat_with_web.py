from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from duckduckgo_search import DDGS
import sys

# Initialize Ollama (assumes Ollama server is running locally)
llm = Ollama(model="llama3")

def web_search(query, num_results=3):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            results.append(f"- {r['title']}: {r['body']}")
    return "\n".join(results)

def main():
    if len(sys.argv) < 2:
        print("Usage: python chat_with_web.py 'Your question here'")
        sys.exit(1)

    user_query = sys.argv[1]

    # Step 1: Search the web
    print("[*] Searching the web...")
    search_results = web_search(user_query)

    # Step 2: Build prompt with web results
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

    final_prompt = prompt.format(web_results=search_results, question=user_query)

    # Step 3: Get answer from LLM
    print("[*] Generating answer...\n")
    answer = llm(final_prompt)
    print(answer)

if __name__ == "__main__":
    main()
