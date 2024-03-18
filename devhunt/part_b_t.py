import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to generate code snippet and explanation
def generate_code_and_explanation(query):
    # Tokenize the query
    input_ids = tokenizer.encode(query, return_tensors="pt")

    # Generate text based on input query
    output = model.generate(input_ids, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)

    # Decode generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract code snippet and explanation from generated text
    code_snippet = ""
    explanation = ""
    parts = generated_text.split("Explanation:")
    if len(parts) > 1:
        code_snippet = parts[0].strip()
        explanation = parts[1].strip()
    elif len(parts) == 1:
        code_snippet = parts[0].strip()
        explanation = "No explanation available."

    return code_snippet, explanation

query = "How to sort a list in Python?"
code_snippet, explanation = generate_code_and_explanation(query)
print("Generated Code Snippet:")
print(code_snippet)
print("\nExplanation:")
print(explanation)

