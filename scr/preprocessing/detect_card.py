import cv2
import numpy as np

def _order(pts: np.ndarray) -> np.ndarray:
    s, d = pts.sum(1), np.diff(pts, axis=1).ravel()
    return np.array([pts[s.argmin()], pts[d.argmin()],
                     pts[s.argmax()], pts[d.argmax()]], dtype="float32")

def extract_card(img: np.ndarray, w: int, h: int) -> np.ndarray:
    gray = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    _, bin_ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bin_ = cv2.morphologyEx(bin_, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cnts, _ = cv2.findContours(bin_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return cv2.resize(img, (w, h))
    c = max(cnts, key=cv2.contourArea)
    if cv2.contourArea(c) < 0.2 * img.shape[0] * img.shape[1]:
        return cv2.resize(img, (w, h))  # contour too small: assume photo already cropped
    box = cv2.boxPoints(cv2.minAreaRect(c))
    destination = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype="float32")
    M = cv2.getPerspectiveTransform(_order(box), destination)
    return cv2.warpPerspective(img, M, (w, h))
