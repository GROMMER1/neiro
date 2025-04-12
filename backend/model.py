from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from backend.training.auto_learn import save_interaction
from backend.knowledge.search import search_wikipedia

MODEL_NAME = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# История диалога
chat_history_ids = None

def generate_response(user_input):
    global chat_history_ids

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

    # Автообучение
    save_interaction(user_input, response)

    # Подключение знаний: если ответ слишком короткий или однотипный — ищем в Википедии
    if len(response) < 10 or "интересно" in response.lower():
        wiki_info = search_wikipedia(user_input)
        response += f" \n[Источник: Википедия] {wiki_info}"

    # Обновляем историю
    chat_history_ids = output
    return response