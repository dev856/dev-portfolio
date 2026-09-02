"""Generate animated demo GIFs for the portfolio 'Studio in Motion' strip.

Creates programmatic, royalty-free animated loops with Pillow so the
portfolio ships with polished motion content and zero external deps.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "images" / "gifs"
W, H = 440, 248
FRAMES = 28

BG = (9, 8, 18)
PANEL = (14, 13, 26)
INK = (244, 245, 251)
VIOLET = (139, 92, 246)
VIOLET_HI = (167, 139, 250)
CYAN = (34, 211, 238)
ROSE = (244, 114, 182)
TEAL = (45, 212, 191)
GRID = (46, 44, 70)


def lerp(a: tuple, b: tuple, t: float) -> tuple:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def glow(draw: ImageDraw.ImageDraw, xy, r, color, rings=3):
    x, y = xy
    for i in range(rings, 0, -1):
        rad = r + i * 3
        alpha_color = lerp(PANEL, color, 0.16 / i)
        draw.ellipse((x - rad, y - rad, x + rad, y + rad), fill=alpha_color)


def panel_base() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # vignette corners
    d.rectangle((0, 0, W, H), fill=BG)
    for gy in range(0, H, 22):
        d.line((0, gy, W, gy), fill=lerp(BG, PANEL, 0.6), width=1)
    for gx in range(0, W, 22):
        d.line((gx, 0, gx, H), fill=lerp(BG, PANEL, 0.6), width=1)
    d.rectangle((4, 4, W - 5, H - 5), outline=GRID, width=1)
    return img


def save_gif(name: str, frames: list[Image.Image], duration: int = 90) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )
    kb = path.stat().st_size / 1024
    print(f"{name:24s} {kb:7.1f} KB  {len(frames)} frames")
    return path


# ---------------------------------------------------------------- neural net
def gen_neural_net() -> None:
    rng = random.Random(7)
    layers = [3, 5, 5, 2]
    xs = [60, 175, 290, 390]
    nodes = []
    for li, (n, x) in enumerate(zip(layers, xs)):
        col = []
        for i in range(n):
            y = H / 2 + (i - (n - 1) / 2) * (46 if n > 3 else 52)
            col.append((x, int(y)))
        nodes.append(col)

    edges = []
    for li in range(len(nodes) - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                edges.append((a, b, rng.random()))

    frames = []
    for f in range(FRAMES):
        t = f / FRAMES
        img = panel_base()
        d = ImageDraw.Draw(img)
        pulse = (math.sin(t * 2 * math.pi) + 1) / 2
        for a, b, jitter in edges:
            wave = (math.sin(t * 2 * math.pi - jitter * 4) + 1) / 2
            shade = lerp(GRID, VIOLET, 0.22 + 0.5 * wave)
            d.line((a[0] + 10, a[1], b[0] - 10, b[1]), fill=shade, width=1)
            mx = a[0] + (b[0] - a[0]) * wave
            my = a[1] + (b[1] - a[1]) * wave
            glow(d, (mx, my), 2, CYAN, 2)
            d.ellipse((mx - 2, my - 2, mx + 2, my + 2), fill=CYAN)
        for li, col in enumerate(nodes):
            for ni, (x, y) in enumerate(col):
                beat = (math.sin(t * 2 * math.pi - li * 0.7 - ni * 0.35) + 1) / 2
                r = 6 + 2 * beat
                glow(d, (x, y), r, VIOLET_HI if li % 2 else CYAN, 3)
                d.ellipse((x - r, y - r, x + r, y + r), fill=lerp(VIOLET, INK, beat), outline=INK, width=1)
        d.text((16, 16), "forward pass · epoch " + str(int(t * 99)), fill=lerp(BG, VIOLET_HI, 0.5 + 0.5 * pulse))
        frames.append(img)
    save_gif("neural-network.gif", frames, 100)


# ------------------------------------------------------------- pose estimation
def gen_pose() -> None:
    joints = {
        "head": (220, 52), "neck": (220, 84), "chest": (220, 104),
        "hip": (220, 156), "lknee": (196, 196), "rknee": (244, 196),
        "lankle": (188, 236), "rankle": (252, 236),
        "lshoulder": (196, 96), "rshoulder": (244, 96),
        "lelbow": (176, 124), "relbow": (264, 124),
        "lwrist": (160, 92), "rwrist": (280, 92),
    }
    bones = [
        ("head", "neck"), ("neck", "chest"), ("chest", "hip"),
        ("hip", "lknee"), ("lknee", "lankle"), ("hip", "rknee"), ("rknee", "rankle"),
        ("chest", "lshoulder"), ("chest", "rshoulder"),
        ("lshoulder", "lelbow"), ("lelbow", "lwrist"),
        ("rshoulder", "relbow"), ("relbow", "rwrist"),
    ]
    frames = []
    for f in range(FRAMES):
        t = f / FRAMES
        img = panel_base()
        d = ImageDraw.Draw(img)
        sway = math.sin(t * 2 * math.pi)
        j = {k: (x + int(sway * (10 if k in ("lwrist", "rwrist", "head") else 4)), y) for k, (x, y) in joints.items()}
        for b in bones:
            a, c = j[b[0]], j[b[1]]
            d.line((a, c), fill=lerp(VIOLET, CYAN, (math.sin(t * 2 * math.pi) + 1) / 2), width=3)
        for name, (x, y) in j.items():
            beat = (math.sin(t * 2 * math.pi - y / 90) + 1) / 2
            color = TEAL if name in ("lknee", "lankle") else VIOLET_HI
            glow(d, (x, y), 4, color, 3)
            d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=INK if beat > 0.5 else color)
        # angle arc
        ax, ay = j["lknee"]
        for k in range(0, 10):
            ang = math.radians(200 + k * 16 + t * 40)
            px, py = ax + math.cos(ang) * 26, ay + math.sin(ang) * 26
            d.point((px, py), fill=TEAL)
        d.text((16, 16), "pose 03 · tadasana · 31 fps", fill=TEAL)
        d.text((16, H - 26), "angle deviation: " + f"{abs(sway) * 6.2:.1f} deg", fill=lerp(BG, CYAN, 0.6))
        frames.append(img)
    save_gif("pose-estimation.gif", frames, 100)


# ------------------------------------------------------------- topic modeling
def gen_topics() -> None:
    rng = random.Random(11)
    topics = [
        ("DATA", 36, VIOLET_HI), ("MODELS", 30, CYAN), ("CLOUD", 26, ROSE),
        ("NLP", 22, TEAL), ("APIS", 20, VIOLET), ("VISION", 24, CYAN),
        ("STREAMLIT", 18, ROSE), ("SQL", 16, TEAL),
    ]
    seeds = [rng.uniform(0, math.tau) for _ in topics]
    frames = []
    for f in range(FRAMES):
        t = f / FRAMES
        img = panel_base()
        d = ImageDraw.Draw(img)
        for i, (label, r, color) in enumerate(topics):
            ang = seeds[i] + t * math.tau * (0.5 + (i % 3) * 0.25)
            rad = 30 + (i % 4) * 24
            x = W / 2 + math.cos(ang) * rad * 1.8
            y = H / 2 + math.sin(ang) * rad * 0.85
            breath = 1 + 0.12 * math.sin(t * math.tau * 2 + i)
            rr = int(r * breath)
            glow(d, (x, y), rr, color, 4)
            d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=color, width=2)
            tw = d.textlength(label)
            d.text((x - tw / 2, y - 5), label, fill=INK)
        d.text((16, 16), "LDA · 7 topics · coherence 0.68", fill=VIOLET_HI)
        frames.append(img)
    save_gif("topic-modeling.gif", frames, 110)


# ----------------------------------------------------------- satellite / geosp
def gen_satellite() -> None:
    rng = random.Random(3)
    basin = [(rng.randint(30, W - 30), rng.randint(30, H - 40)) for _ in range(90)]
    frames = []
    for f in range(FRAMES):
        t = f / FRAMES
        img = panel_base()
        d = ImageDraw.Draw(img)
        sweep_x = 20 + (W - 40) * t
        # river channel
        pts = []
        for k in range(40):
            px = 20 + k * (W - 40) / 39
            py = H / 2 + math.sin(k * 0.35) * 46 + math.sin(k * 0.08) * 26
            pts.append((px, py))
        d.line(pts, fill=lerp(BG, TEAL, 0.45), width=5)
        d.line(pts, fill=TEAL, width=1)
        for p in basin:
            hot = p[0] <= sweep_x
            c = lerp(GRID, TEAL, 0.85) if hot else lerp(BG, VIOLET, 0.3)
            d.point(p, fill=c)
            if hot and (p[0] + p[1]) % 7 == 0:
                glow(d, p, 1, TEAL, 2)
        # satellite icon
        sx, sy = sweep_x, 26
        d.line((sx, 14, sx, H - 12), fill=lerp(BG, CYAN, 0.5), width=1)
        glow(d, (sx, sy), 6, CYAN, 4)
        d.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), fill=BG, outline=CYAN, width=2)
        d.rectangle((sx - 16, sy - 3, sx - 9, sy + 3), fill=VIOLET_HI)
        d.rectangle((sx + 9, sy - 3, sx + 16, sy + 3), fill=VIOLET_HI)
        d.text((16, 16), "MODIS pass · basin discharge forecast", fill=CYAN)
        d.text((16, H - 26), "XGBoost r2=0.87  LSTM r2=0.84", fill=TEAL)
        frames.append(img)
    save_gif("satellite-vision.gif", frames, 90)


# ------------------------------------------------------------- data analytics
def gen_dashboard() -> None:
    rng = random.Random(21)
    series1 = [rng.uniform(0.2, 0.9) for _ in range(36)]
    series2 = [rng.uniform(0.15, 0.75) for _ in range(36)]
    bars = [rng.uniform(0.3, 1.0) for _ in range(12)]
    frames = []
    for f in range(FRAMES):
        t = f / FRAMES
        img = panel_base()
        d = ImageDraw.Draw(img)
        gx0, gy0, gx1, gy1 = 28, 30, W - 28, H - 44
        d.rectangle((gx0, gy0, gx1, gy1), outline=GRID, width=1)
        for k in range(1, 5):
            yy = gy0 + (gy1 - gy0) * k / 5
            d.line((gx0, yy, gx1, yy), fill=lerp(BG, PANEL, 0.9), width=1)
        # animated line chart
        shift = int(t * len(series1))
        def yv(seq, i):
            v = seq[(i + shift) % len(seq)]
            return gy1 - (gy1 - gy0 - 8) * v - 4
        for series, color in ((series1, CYAN), (series2, ROSE)):
            pts = [(gx0 + (gx1 - gx0) * i / (len(series) - 1), yv(series, i)) for i in range(len(series))]
            d.line(pts, fill=color, width=2)
            hx, hy = pts[-1]
            glow(d, (hx, hy), 3, color, 3)
        # bars bottom
        bw = 14
        for i, b in enumerate(bars):
            bb = b * (0.75 + 0.25 * math.sin(t * math.tau + i))
            bx = gx0 + 4 + i * (bw + 6)
            bh = 20 * bb
            d.rectangle((bx, gy1 + 8, bx + bw, gy1 + 8 + bh), fill=lerp(PANEL, VIOLET_HI, 0.3 + 0.4 * bb))
        d.text((16, 16), "eda · 12,842 rows · streaming", fill=VIOLET_HI)
        frames.append(img)
    save_gif("data-pulse.gif", frames, 100)


# -------------------------------------------------------------- fabric defect
def gen_fabric() -> None:
    rng = random.Random(5)
    weave = []
    for yy in range(8, H - 8, 8):
        for xx in range(8, W - 8, 8):
            weave.append((xx, yy, rng.random()))
    defect = (W * 0.62, H * 0.55)
    frames = []
    for f in range(FRAMES):
        t = f / FRAMES
        img = panel_base()
        d = ImageDraw.Draw(img)
        scan_y = 12 + (H - 24) * t
        for xx, yy, j in weave:
            base = lerp(BG, PANEL, 0.5 + 0.3 * j)
            scanned = yy <= scan_y
            if scanned:
                base = lerp(base, VIOLET, 0.18)
            d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=base)
            if scanned and abs(xx - defect[0]) < 30 and abs(yy - defect[1]) < 26:
                pulse = (math.sin(t * math.tau * 2) + 1) / 2
                glow(d, (xx, yy), 3, ROSE, 3)
                d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=lerp(ROSE, INK, pulse))
        d.line((6, scan_y, W - 6, scan_y), fill=CYAN, width=2)
        glow(d, (W * 0.2, scan_y), 2, CYAN, 2)
        if scan_y > defect[1] - 10:
            dx, dy = defect
            pulse = (math.sin(t * math.tau * 3) + 1) / 2
            d.rectangle((dx - 34, dy - 26, dx + 34, dy + 26), outline=ROSE, width=2)
            d.text((dx - 30, dy - 40), "defect 0.94", fill=ROSE)
            glow(d, (dx, dy), 4 + int(4 * pulse), ROSE, 3)
        d.text((16, 16), "fabrisense · textile scan", fill=CYAN)
        frames.append(img)
    save_gif("fabric-scan.gif", frames, 90)


if __name__ == "__main__":
    gen_neural_net()
    gen_pose()
    gen_topics()
    gen_satellite()
    gen_dashboard()
    gen_fabric()
    print("done ->", OUT)
