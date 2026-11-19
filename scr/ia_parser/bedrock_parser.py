import json

import boto3

from scr.config import AWS_REGION, BEDROCK_MODEL_ID
from scr.ia_parser.prompt import KEYS, prompt_builder

_br = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def _extract_json(txt: str) -> dict:
    ini, fim = txt.find("{"), txt.rfind("}")
    if ini == -1 or fim == -1:
        raise ValueError(f"LLM não retornou JSON: {txt[:200]}")
    dados = json.loads(txt[ini:fim + 1])
    return {k: dados.get(k) for k in KEYS}

def parse(texts: dict) -> dict:
    r = _br.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt_builder(texts)}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 300},
    )
    return _extract_json(r["output"]["message"]["content"][0]["text"])