from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from backend.training.auto_learn import save_interaction
from backend.knowledge.search import search_wikipedia

MODEL_NAME = "microsoft/DialoGPT-small"

tokenizer = None
model = None
chat_history_ids = None

def generate_response(user_input):
    global tokenizer, model, chat_history_ids

    # Ленивая загрузка
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    with torch.no_grad():
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # Объединяем с историей (если есть)
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

        # Генерация
        output = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.75
        )

        response = tokenizer.decode(output[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        chat_history_ids = output

    save_interaction(user_input, response)

    if len(response) < 10 or "интересно" in response.lower():
        wiki_info = search_wikipedia(user_input)
        if wiki_info:
            response += f"\n\n📚 Кстати: {wiki_info}"

    return response