import wikipediaapi
import requests

def search_wikipedia(query, lang='ru'):
    wiki = wikipediaapi.Wikipedia(lang)
    page = wiki.page(query)
    if page.exists():
        return page.summary[0:1000]  # Ограничим объём
    return "Информация в Википедии не найдена."

def search_google(query, api_key, cse_id):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            return data["items"][0]["snippet"]
        return "Ничего не найдено в Google."
    except Exception as e:
        return f"Ошибка при поиске: {e}"