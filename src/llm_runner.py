from openai import OpenAI 

client = OpenAI( 
    base_url="http://10.0.0.159:1234/v1", 
    api_key="lm-studio" 
)

MODEL_NAME = "meta-llama-3.1-8b-instruct"

def run_llm(prompt):
    """ 
    Sends a prompt to the local LM Studio model and returns the response text. 
    """

    completion = client.chat.completions.create( 
        model=MODEL_NAME, 
        messages=[ 
            {"role": "user", "content": prompt} 
        ], 
        temperature=0.2, 
        max_tokens=300 
    ) 
    
    response = completion.choices[0].message.content 
    
    return response