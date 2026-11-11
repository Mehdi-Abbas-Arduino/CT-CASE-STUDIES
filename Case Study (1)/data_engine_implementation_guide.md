# Session 2: Data Engine Implementation Guide

This document provides a clean structure for building **Script 1 (The Data Engine)** and **Script 2 (The Sentence Generator)**, while detailing how to process Gutenberg raw text files correctly.

---

## What is the Value of the Start Marker?

In Project Gutenberg text files, the standard start marker line looks like this:

```text
*** START OF THE PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***
```

or for slightly different book releases:

```text
*** START OF THIS PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***
```

### Why line.startswith() is Required
Because every book title inside the marker changes (e.g., `... EBOOK MOBY DICK ***`), you **cannot** check for exact equality (`line == START_MARKER`). 

Instead, define your marker prefix as:
```python
START_MARKER = "*** START OF"
END_MARKER = "*** END OF"
```
And check lines using `.startswith()`:
```python
if line.startswith(START_MARKER):
    inside_book = True
```

---

## 1. Script 1: Data Engine (`build_data_engine.py`)

This script reads raw text files from the corpus folder, strips headers/footers, cleans/tokenizes words, and saves word counts to a JSON file on disk.

```python
import os
import json

START_MARKER = "*** START OF"
END_MARKER = "*** END OF"
CORPUS_DIR = "corpus"
OUTPUT_FILE = "models/word_count.json"

def strip_boilerplate(file_path):
    """Reads a file and strips Gutenberg header and footer text."""
    lines = []
    inside_book = False
    found_start = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            clean_line = line.strip()
            
            # Check for start marker
            if clean_line.startswith(START_MARKER):
                inside_book = True
                found_start = True
                continue
            
            # Check for end marker
            if clean_line.startswith(END_MARKER):
                inside_book = False
                break
            
            if inside_book:
                lines.append(clean_line)

    # Fallback safety: If markers were missing, keep full text instead of losing data
    if not found_start:
        print(f"Warning: No start marker found in {file_path}. Using full file.")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return " ".join(lines)

def clean_word(raw_token):
    """Normalizes tokens: lowercases and strips surrounding non-alphanumeric noise."""
    token = raw_token.lower().strip('"', "'.!?,:;_()-[]{}*")
    # Drop pure numbers or empty strings
    if token.isdigit() or not token:
        return None
    return token

def tokenize(text):
    """Splits raw text into a list of normalized tokens."""
    tokens = []
    raw_words = text.split()
    for raw_w in raw_words:
        w = clean_word(raw_w)
        if w:
            tokens.append(w)
    return tokens

def count_words(tokens, word_counts=None):
    """Tallies frequencies using dict.get()."""
    if word_counts is None:
        word_counts = {}
    for token in tokens:
        word_counts[token] = word_counts.get(token, 0) + 1
    return word_counts

def build_engine():
    total_counts = {}
    
    if not os.path.exists("models"):
        os.makedirs("models")

    # Iterate over files in the corpus folder
    for filename in os.listdir(CORPUS_DIR):
        file_path = os.path.join(CORPUS_DIR, filename)
        if os.path.isfile(file_path):
            print(f"Processing: {filename}")
            raw_text = strip_boilerplate(file_path)
            tokens = tokenize(raw_text)
            count_words(tokens, total_counts)

    # Save to JSON on disk
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(total_counts, f, indent=2)

    print(f"\nProcessing complete! Vocabulary size: {len(total_counts)} unique tokens.")
    print(f"Counts saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    build_engine()
```

---

## 2. Script 2: Unigram Generator (`generate_text.py`)

This standalone generator loads the JSON counts file and rolls the "loaded die".

```python
import json
import random

MODEL_FILE = "models/word_count.json"

def weighted_pick(weights_dict):
    """
    Ruler and Dart Algorithm:
    1. Sum weights (ruler length)
    2. Pick random point (dart)
    3. Walk through cumulative weight until passing dart
    """
    total_weight = sum(weights_dict.values())
    dart = random.uniform(0, total_weight)
    
    running_total = 0
    for key, weight in weights_dict.items():
        running_total += weight
        if running_total >= dart:
            return key
            
    return list(weights_dict.keys())[0]

def make_sentence(weights_dict, length=10):
    words = []
    for _ in range(length):
        word = weighted_pick(weights_dict)
        words.append(word)
    return " ".join(words)

if __name__ == "__main__":
    # Load counts from JSON disk interface
    with open(MODEL_FILE, "r", encoding="utf-8") as f:
        word_counts = json.load(f)

    print("Generating Unigram Sentences:\n" + "-"*30)
    for i in range(5):
        print(f"Sentence {i+1}: {make_sentence(word_counts, length=12)}")
```