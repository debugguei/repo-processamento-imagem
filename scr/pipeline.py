import json
import sys
import time
from pathlib import Path

import cv2

from src.ia_parser.bedrock_parser import parse
from src.ocr.rekognition_ocr import read_text
from src.pre_processing.detect_card import extract_card
from src.pre_processing.enhance import enhance
from src.pre_processing.crops import crop

def process(path: str, debug: bool = False) -> tuple[dict, dict]:
    timings: dict[str, float] = {}
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(path)

    t0 = time.perf_counter()
    card = enhance(extract_card(img))
    rois = crop(card)
    timings["pre"] = time.perf_counter() - t0

    if debug:
        out = Path("debug_output"); out.mkdir(exist_ok=True)
        cv2.imwrite(str(out / "card.png"), card)
        for k, v in rois.items():
            cv2.imwrite(str(out / f"{k}.png"), v)

    t0 = time.perf_counter()
    texts = {k: " ".join(read_text(v)) for k, v in rois.items()}
    timings["ocr"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    data = parse(texts)
    timings["llm"] = time.perf_counter() - t0

    timings["total"] = sum(timings.values())
    return data, timings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data, timings = process(sys.argv[1], debug="--debug" in sys.argv)
    print(json.dumps({"data": data, "timings_s": timings}, ensure_ascii=False, indent=2))