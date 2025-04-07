# OtoGen
OtoGen is a simple python script/utility that aims to make otoing process easier by converting user made audcity labels into oto

## What can this script do?
Right now it can oto a very simple CVVC voicebank, so far the script only handles Medial [CV] and [V C] transitions but i hope to handle other types of phonemes for english(and other languages)soon

## Usage
1. Install Python AND add it to path(If you don't have python installed I recommend Python 3.10 to avoid issues since thats the version I use for developement)
2. Create a seprate folder for your labels that contains ONLY the labels
3. Add your consonants and vowels into config.ini file into their respective lists(additional info is in example file)
4. Open CMD and type ```cd [path to your folder with main.py]```, after this type 
```python main.py [path to you labels folder]```
(if any of your folders have spaces in them put them in "" otherwise program will error out)

<sup><sub>(I'm gonna work on a video guide later)</sub></sup>

## Labeling
There are several things to remember when labeling for OtoGen
1. Label files need to have same name as .wav file they're targeting except with .txt extension
2. You have to label start, start of the stable part and end of unstable part of every symbol(except sil)
3. Silence is labeled as sil
4. There should always be a sil after the last symbol in your label
5. When labeling plosives always put a sil about 60-80 milliseconds before start of your first consonant so the script recognises them as such
6. Do NOT use vLabler audacity labeler for this, it's output is slightly different from audacity and the script doesnt handle it right now

