from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

torch.manual_seed(42)

MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    load_in_4bit=True
)


def run_llm(prompt):
    formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>"

    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=400,
        temperature=0,
        do_sample=False
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("<|assistant|>")[-1].strip()