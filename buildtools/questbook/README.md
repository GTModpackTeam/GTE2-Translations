# GTE2 Translation - Questbook

## How to use translated questbook

1. Go to the [releases page](https://github.com/GTModpackTeam/GTE2-Translations/releases) and download the latest version
2. Download the `GTExpert2-<version>-questbook-<language>.zip` file for your language (e.g., `GTExpert2-X.Y.Z-questbook-en-US.zip`)
3. Open your GTE2 instance folder and navigate to `config/betterquesting/`
4. Delete the existing `DefaultQuests` folder
5. Extract the ZIP file directly into `config/betterquesting/DefaultQuests/`
   - This will create a new `DefaultQuests` folder with translated content
6. Launch the game and enjoy!

## Available Languages

Currently supported languages:
- English (US): `GTExpert2-X.Y.Z-questbook-en-US.zip`

## For Developers

### Running translation locally

```bash
# Set environment variables
export DEEPL_AUTH_KEY="your-api-key"
export TARGET_LANG_CODE="en-US"
export INPUT_DIR="/path/to/tmp/DefaultQuests"
export OUTPUT_DIR="/path/to/bqu"

# Run translation
cd buildtools
uv sync
uv run python ./questbook/translate_v2.py
```

### Translation workflow

The translation is automated via GitHub Actions:
1. Downloads quest files from the main GTE2 repository
2. Translates them using DeepL API (Japanese → Target Language)
3. Creates a ZIP file with translated quests
4. Uploads to GitHub Releases
