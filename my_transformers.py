from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2"  

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

input_text = "你想和模型聊天吗？"

inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**inputs)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)
