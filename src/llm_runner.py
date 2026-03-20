from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

torch.manual_seed(42)

MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
#MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    quantization_config=bnb_config
)


def run_llm(prompt):
    messages = [ 
            {"role": "user", "content": prompt} 
        ]
    
    inputs = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=400,
        do_sample=True,
        temperature=0.1,
        top_p=0.9,
        eos_token_id=tokenizer.eos_token_id,
        stop=["END_JSON"]
    )

    generated_tokens = outputs[0][inputs.shape[1]:]

    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    if "END_JSON" in response:
        response = response.split("END_JSON")[0] + "END_JSON"

    return response