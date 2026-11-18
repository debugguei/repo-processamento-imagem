from difflib import SequenceMatcher
from functools import lru_cache

from mtgsdk import Card

def _yes(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return False
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.75

@lru_cache(maxsize=1024)
def _buscar(nome: str) -> tuple:
    return tuple(Card.where(name=nome).where(pageSize=50).all())

def _para_dict(c) -> dict:
    return {
        "name": c.name, "edicao": c.set, "nome_edicao": c.set_name,
        "collector_number": c.number, "mana_cost": c.mana_cost,
        "type": c.type, "rarity": c.rarity,
        "multiverse_id": c.multiverse_id, "imagem_url": c.image_url,
    }

def valide(data:dict, min_sim: float = 0.75) -> dict:
    name = (data.get("name") or "").strip()
    if not name:
        return {**data, "validated": False, "score": 0.0}

    candidates = _buscar(name)
    if not candidates and " " in name:
        candidates = _buscar(max(name.split(), key=len))
    if not candidates:
        return {**data, "validated": False, "score": 0.0}

    def score(c) -> float:
        s = SequenceMatcher(None, name.lower(), c.name.lower()).ratio() * 0.6
        if data.get("edicao") and c.set and data["edicao"].upper() == c.set.upper():
            s += 0.25
        if data.get("collector_number") and str(data["collector_number"]).lstrip("0") == str(c.number).lstrip("0"):
            s += 0.15
        return s

    best = max(candidates, key=score)
    if SequenceMatcher(None, name.lower(), best.name.lower()).ratio() < min_sim:
        return {**data, "validated": False, "score": round(score(best), 3)}
    return {**_para_dict(best), "foil": data.get("foil"),
            "validated": True, "score": round(score(best), 3)}

