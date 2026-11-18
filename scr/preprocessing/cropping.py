import numpy as np

ROIS = {
    #         y0    y1    x0    x1
    "name":   (0.03, 0.10, 0.05, 0.80),
    "type":   (0.55, 0.62, 0.05, 0.85),
    "footer": (0.92, 0.99, 0.03, 0.60),
}

def crop(card: np.ndarray, rois: dict = ROIS) -> dict[str, np.ndarray]:
    h, w = card.shape[:2]
    return {k: card[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]
            for k, (y0, y1, x0, x1) in rois.items()}