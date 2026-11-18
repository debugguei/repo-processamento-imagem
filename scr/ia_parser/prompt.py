KEYS = ["name", "edition", "collector_number", "mana_cost", "type", "rarity", "confidence"]

TEMPLATE = """You extract data from Magic: The Gathering cards from OCR text (may contain errors).
Respond ONLY with a JSON with the keys: {keys}.
- name: card name in English if possible
- edition: set code (ex: "KTK", "MH3")
- rarity: Common, Uncommon, Rare or Mythic
- confidence: 0 to 1
Use null when you don't know. Do not make up information.
NAME: {name}
TYPE: {type}
FOOTER: {footer}"""

def prompt_builder(texts: dict) -> str:
    return TEMPLATE.format(keys=", ".join(KEYS),
                           name=texts.get("name"), type=texts.get("type"),
                           footer=texts.get("footer"))