import os
import json
import deepl

# Language code can be known in https://www.deepl.com/docs-api/general/get-languages
target_lang_code = os.environ["TARGET_LANG_CODE"]

# You should set your deepl auth key in your environment variable.
auth_key = os.environ["DEEPL_AUTH_KEY"]

# In some area on this earth, you should set a proper api server site at first.
server_url = "https://api-free.deepl.com"

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def translate_text(text, translator, source_lang='JA', target_lang=target_lang_code):
    if not text.strip():
        return text
    return translator.translate_text(text, source_lang=source_lang, target_lang=target_lang).text

def translate_json_values(json_data, translator, keys_to_translate=['name:8', 'desc:8']):
    quest_database = json_data.get('questDatabase:9', {})
    total_quests = len(quest_database)
    for index, (quest_id, quest_data) in enumerate(quest_database.items()):
        for key in keys_to_translate:
            if key in quest_data.get('properties:10', {}).get('betterquesting:10', {}):
                original_text = quest_data['properties:10']['betterquesting:10'][key]
                if original_text:
                    translated_text = translate_text(original_text, translator)
                    quest_data['properties:10']['betterquesting:10'][key] = translated_text
        progress = (index + 1) / total_quests * 100
        print(f"{progress:.2f}%: {quest_id}")
    return json_data

def save_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def main():
    translator = deepl.Translator(auth_key, server_url=server_url)
    json_data = load_json_file("./DefaultQuests.json")
    translated_json_data = translate_json_values(json_data, translator)
    save_json_file("./bqu/DefaultQuests_" + target_lang_code + ".json", translated_json_data)

if __name__ == "__main__":
    main()
