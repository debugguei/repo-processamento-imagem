import boto3
import cv2
import numpy as np

from src.config import AWS_REGION

_rek = boto3.client("rekognition", region_name=AWS_REGION)

def read_text(img_bgr: np.ndarray, min_conf: float = 70) -> list[str]:
    ok, buf = cv2.imencode(".png", img_bgr)
    if not ok:
        return []
    r = _rek.detect_text(Image={"Bytes": buf.tobytes()})
    return [d["DetectedText"] for d in r["TextDetections"]
            if d["Type"] == "LINE" and d["Confidence"] >= min_conf]