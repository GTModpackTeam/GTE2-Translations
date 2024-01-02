# GTE2 Translation
## Running the script
### Questbook translation

For this you're going to need a [DeepL](https://www.deepl.com) account. The entirety of the questbook as of writing this is around ~120k characters, so it comfortably fits in the monthly DeepL free tier quota.
```
$ mv /path/to/your/ftbutils .
$ pip3 install -r requirements.txt
$ DEEPL_AUTH_KEY="<insert your deepl key here>" python3 translate.py
$ mv ftbutils-tl /path/to/your/ftbutils
```

To update certain quests without having to re-translate everything (which takes quite a bit), simply delete them from the `ftbutils-tl` folder and run the script again. You can use the provided `update.py` script for this, it checks for file differences between `./ftbquests` and `./ftbquests-new`, then deletes the corresponding translation from `./ftbquests-tl`. After doing that, you can just get rid of the old quests folder and rename the new one to `ftbquests`, then run the translation script.

## Credits

- The person who created the automatic translation of the FTB Quest is [gte2-translation](https://github.com/spx01/gte2-translation).
