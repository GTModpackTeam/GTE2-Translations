import os
import json
import deepl
import shutil
from pathlib import Path

# Language code can be known in https://www.deepl.com/docs-api/general/get-languages
target_lang_code = os.environ["TARGET_LANG_CODE"]
source_lang_code = "JA"  # DeepL source_lang requires language code only (no country code)

# You should set your deepl auth key in your environment variable.
auth_key = os.environ["DEEPL_AUTH_KEY"]

# In some area on this earth, you should set a proper api server site at first.
server_url = "https://api-free.deepl.com"

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def translate_text(text, translator, source_lang=source_lang_code, target_lang=target_lang_code):
    if not text.strip():
        return text
    return translator.translate_text(text, source_lang=source_lang, target_lang=target_lang).text

def translate_betterquesting_properties(properties, translator, keys_to_translate=['name:8', 'desc:8']):
    """Translate name:8 and desc:8 in betterquesting:10 properties"""
    if 'betterquesting:10' in properties:
        for key in keys_to_translate:
            if key in properties['betterquesting:10']:
                original_text = properties['betterquesting:10'][key]
                if original_text:
                    translated_text = translate_text(original_text, translator)
                    properties['betterquesting:10'][key] = translated_text
    return properties

def translate_quest_settings(input_path, output_path, translator):
    """Translate QuestSettings.json (pack_name:8)"""
    if not os.path.exists(input_path):
        print(f"Warning: {input_path} not found, skipping...")
        return

    data = load_json_file(input_path)
    if 'betterquesting:10' in data and 'pack_name:8' in data['betterquesting:10']:
        original_name = data['betterquesting:10']['pack_name:8']
        if original_name:
            data['betterquesting:10']['pack_name:8'] = translate_text(original_name, translator)
    save_json_file(output_path, data)
    print(f"Translated: QuestSettings.json")

def translate_quest_line(input_path, output_path, translator):
    """Translate a single quest line file"""
    data = load_json_file(input_path)
    if 'properties:10' in data:
        data['properties:10'] = translate_betterquesting_properties(data['properties:10'], translator)
    save_json_file(output_path, data)

def translate_quest(input_path, output_path, translator):
    """Translate a single quest file"""
    data = load_json_file(input_path)
    if 'properties:10' in data:
        data['properties:10'] = translate_betterquesting_properties(data['properties:10'], translator)
    save_json_file(output_path, data)

def count_quest_files(quests_dir):
    """Count total number of quest files for progress tracking"""
    count = 0
    for root, dirs, files in os.walk(quests_dir):
        count += len([f for f in files if f.endswith('.json')])
    return count

def translate_quest_lines(input_dir, output_dir, translator):
    """Translate all quest line files"""
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Warning: {input_dir} directory not found, skipping...")
        return

    output_path = Path(output_dir)

    quest_line_files = sorted(input_path.glob('*.json'))
    total = len(quest_line_files)

    if total == 0:
        print(f"Warning: No quest line files found in {input_dir}")
        return

    for index, file_path in enumerate(quest_line_files):
        relative_path = file_path.relative_to(input_path)
        output_file = output_path / relative_path
        translate_quest_line(file_path, output_file, translator)
        progress = (index + 1) / total * 100
        print(f"{progress:.2f}%: QuestLines/{file_path.name}")

def translate_quests(input_dir, output_dir, translator):
    """Translate all quest files recursively"""
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Warning: {input_dir} directory not found, skipping...")
        return

    output_path = Path(output_dir)

    # Count total files for progress
    total_quests = count_quest_files(input_dir)

    if total_quests == 0:
        print(f"Warning: No quest files found in {input_dir}")
        return

    processed = 0

    # Walk through all subdirectories
    for root, dirs, files in os.walk(input_dir):
        root_path = Path(root)
        for file_name in files:
            if file_name.endswith('.json'):
                input_file = root_path / file_name
                relative_path = input_file.relative_to(input_path)
                output_file = output_path / relative_path

                translate_quest(input_file, output_file, translator)

                processed += 1
                progress = processed / total_quests * 100
                print(f"{progress:.2f}%: Quests/{relative_path}")

def main():
    translator = deepl.Translator(auth_key, server_url=server_url)

    # When run via uv with --directory, we need to go up one level
    input_base = "../tmp/DefaultQuests"
    output_base = f"../bqu/DefaultQuests_{target_lang_code}"

    if not os.path.exists(input_base):
        print(f"ERROR: Input directory {input_base} does not exist!")
        return

    # 1. Translate QuestSettings.json
    print("\nTranslating QuestSettings.json...")
    translate_quest_settings(
        f"{input_base}/QuestSettings.json",
        f"{output_base}/QuestSettings.json",
        translator
    )

    # 2. Translate QuestLines
    print("\nTranslating QuestLines...")
    translate_quest_lines(
        f"{input_base}/QuestLines",
        f"{output_base}/QuestLines",
        translator
    )

    # 3. Translate Quests
    print("\nTranslating Quests...")
    translate_quests(
        f"{input_base}/Quests",
        f"{output_base}/Quests",
        translator
    )

    print("\nTranslation completed!")

    # 4. Create ZIP archive for GitHub Actions artifact
    print("\nCreating ZIP archive...")
    zip_output = f"../bqu/DefaultQuests_{target_lang_code}"
    shutil.make_archive(zip_output, 'zip', output_base)
    print(f"ZIP archive created: {zip_output}.zip")

if __name__ == "__main__":
    main()
