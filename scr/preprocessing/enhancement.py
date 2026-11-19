import cv2
import numpy as np

def enchance(card: np.ndarray, clip: float = 2.0, limiar_brilho: int = 245) -> np.ndarray:
    l, a, b = cv2.split(cv2.cvtColor(carta, cv2.COLOR_BGR2LAB))
    l = cv2.createCLAHE(clipLimit=clip, tileGridSize=(8, 8)).apply(l)
    out = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)
    grey = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    _, brightess = cv2.threshold(grey, brightess_treshold, 255, cv2.THRESH_BINARY)
    if brightess.any():
        out = cv2.inpaint(out, brightess, 3, cv2.INPAINT_TELEA)
    return out