"""
Favicon for TSF: the real brand mark — Logo_1 (red ruled-V) — knocked out of
its cream card and centered LARGE on a rounded square in the site PAPER color
(--paper: oklch(0.975 0.008 75)). Scaled up so it reads at 16-32px.
"""
import math
import numpy as np
from PIL import Image, ImageDraw


def oklch_to_rgb(L, C, H):
    a = C * math.cos(math.radians(H)); b = C * math.sin(math.radians(H))
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    rl = 4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    gl = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bl = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    def g(x):
        x = max(0.0, min(1.0, x))
        x = 12.92*x if x <= 0.0031308 else 1.055*x**(1/2.4) - 0.055
        return round(x*255)
    return (g(rl), g(gl), g(bl), 255)


PAPER = oklch_to_rgb(0.975, 0.008, 75)
print("paper rgb =", PAPER[:3])

# knock the cream card out of Logo_1 -> transparent red ruled-V, autocropped
src = Image.open("branding_new_logos/The-Spinner-Foundation-Logo_1.png").convert("RGBA")
arr = np.asarray(src).astype(np.float32)
dist = np.sqrt(((arr[..., :3] - np.array([240., 234., 228.]))**2).sum(-1))
alpha = np.clip((dist - 24) / (80 - 24), 0, 1) * (arr[..., 3] / 255)
out = arr.copy(); out[..., 3] = alpha * 255
mark = Image.fromarray(out.astype("uint8"), "RGBA")
bbox = mark.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
mark = mark.crop(bbox)

from PIL import ImageFilter

S, RAD, FILL_H, BOLD = 2048, 340, 0.82, 23   # bigger fill + dilate strokes
CRIMSON_RGB = (140, 26, 26)

canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(canvas).rounded_rectangle([0, 0, S - 1, S - 1], radius=RAD, fill=PAPER)
h = int(S * FILL_H); w = round(mark.width * h / mark.height)
mark = mark.resize((w, h), Image.LANCZOS)

# embolden: dilate the alpha, then repaint solid crimson through it (clean, no fringe)
alpha = mark.getchannel("A").filter(ImageFilter.MaxFilter(BOLD))
bold = Image.new("RGBA", mark.size, CRIMSON_RGB + (0,))
bold.putalpha(alpha)

canvas.alpha_composite(bold, ((S - w) // 2, (S - h) // 2))
canvas.resize((512, 512), Image.LANCZOS).save("development/squarespace_upload/favicon.png")
print("wrote development/squarespace_upload/favicon.png  (mark", mark.size, ")")
