from ollama_client import OllamaClient

llm = OllamaClient(model="llama3")

text = llm.generate(
    prompt="What is the main purpose of tax?",
    temperature=0.2,
)

print(text)

