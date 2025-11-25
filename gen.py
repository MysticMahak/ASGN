"""
Append synthetic PII NER examples to dev.jsonl

Usage:
python gen.py --per_label 30

This will generate ~30 samples per label and APPEND them to data/dev.jsonl

python append_synthetic_to_dev.py --per_label 25
This will generate ~25 samples per label and APPEND them to data/dev.jsonl
"""

import argparse
import json
import random
import uuid
from datetime import datetime

FIRST_NAMES = ["john", "ramesh", "sarah", "maria", "alex", "li", "olga", "mohit"]
LAST_NAMES = ["doe", "sharma", "kumar", "singh", "garcia", "ng", "ivanova"]
CITIES = ["new york", "mumbai", "los angeles", "delhi", "london", "bengaluru"]
LOCATIONS = ["main street", "sector 17", "market road", "downtown plaza"]
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "example.com"]

LABELS = ["CREDIT_CARD", "PHONE", "EMAIL", "PERSON_NAME", "DATE", "CITY", "LOCATION"]

PREFIXES = ["i think", "please note", "hello", "my info is", "hey", "listen", "just so you know"]
SUFFIXES = ["thanks", "please update", "for reference", "thank you", "if needed"]

def gen_credit_card(spoken=False):
    blocks = ["4242", "1234", "1111", "9999", "0000"]
    card = " ".join(random.choice(blocks) for _ in range(4))
    if spoken:
        digit_map = {"0":"oh","1":"one","2":"two","3":"three","4":"four","5":"five","6":"six","7":"seven","8":"eight","9":"nine"}
        return " ".join(digit_map[d] for d in card.replace(" ",""))
    return card

def gen_phone(spoken=False):
    digits = "".join(str(random.randint(0,9)) for _ in range(10))
    if spoken:
        word_map = {"0":"oh","1":"one","2":"two","3":"three","4":"four","5":"five","6":"six","7":"seven","8":"eight","9":"nine"}
        return " ".join(word_map[d] for d in digits)
    fmt = random.choice(["{}-{}-{}", "({}) {}-{}", "{} {} {}", "{}{}{}"])
    return fmt.format(digits[:3], digits[3:6], digits[6:10])

def gen_email(spoken=False):
    local = random.choice(["john.doe", "ramesh", "maria_88", "alex99"])
    domain = random.choice(EMAIL_DOMAINS)
    if spoken:
        return local.replace(".", " dot ") + " at " + domain.replace(".", " dot ")
    return f"{local}@{domain}"

def gen_person_name(spoken=False): return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
def gen_date(spoken=False): 
    year = random.randint(1990, 2024)
    month = random.randint(1,12)
    day = random.randint(1,28)
    return f"{day:02d}/{month:02d}/{year}"

def gen_city(spoken=False): return random.choice(CITIES)
def gen_location(spoken=False): return random.choice(LOCATIONS)

GEN_FN = {
    "CREDIT_CARD": gen_credit_card,
    "PHONE": gen_phone,
    "EMAIL": gen_email,
    "PERSON_NAME": gen_person_name,
    "DATE": gen_date,
    "CITY": gen_city,
    "LOCATION": gen_location,
}

def build_sentence(entity, label):
    tpl = random.choice([
        "{prefix} {entity} {suffix}",
        "{prefix} {entity}",
        "{entity} {suffix}",
        "the {label} is {entity}",
        "i believe {entity} is correct",
        "please note {entity} for reference",
        "can you verify {entity} ?",
    ])
    sentence = tpl.format(
        prefix=random.choice(PREFIXES),
        entity=entity,
        suffix=random.choice(SUFFIXES),
        label=label.lower()
    )
    return " ".join(sentence.split())

def make_example(label, spoken=False):
    ent = GEN_FN[label](spoken)
    sent = build_sentence(ent, label)
    start = sent.find(ent)
    if start == -1:
        start = len(sent)
        sent += " " + ent
    end = start + len(ent)
    return {
        "id": f"synth_{label.lower()}_{uuid.uuid4().hex[:8]}",
        "text": sent,
        "entities": [{"start": start, "end": end, "label": label}],
    }

def append_to_dev(dev_path, per_label, spoken_rate, seed):
    random.seed(seed)
    total = 0

    with open(dev_path, "a", encoding="utf-8") as f:
        for label in LABELS:
            for _ in range(per_label):
                spoken = random.random() < spoken_rate
                ex = make_example(label, spoken)
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")
                total += 1

    print(f"✔ Appended {total} synthetic examples to {dev_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev_path", default="data/dev.jsonl")
    ap.add_argument("--per_label", type=int, default=20)
    ap.add_argument("--spoken_rate", type=float, default=0.3)
    ap.add_argument("--seed", type=int, default=42)

    args = ap.parse_args()
    append_to_dev(args.dev_path, args.per_label, args.spoken_rate, args.seed)
