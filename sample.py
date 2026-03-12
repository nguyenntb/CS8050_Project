from openai import OpenAI

client = OpenAI(
    base_url="http://10.0.0.159:1234/v1",
    api_key="lm-studio"
)

completion = client.chat.completions.create(
    model="meta-llama-3.1-8b-instruct",
    messages=[
        {"role": "user", "content": "Explain what an LLM is."}
    ],
    temperature=0.7,
    max_tokens=50
)

print(completion.choices[0].message.content)