#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plot Benders 300-second campaign figures from CSV evidence only.

No third-party Python packages required. Writes simple PNG charts with stdlib.
"""
from __future__ import annotations

import csv
import math
import os
import struct
import zlib
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "results", "benders_300s_campaign.csv")
FIG_DIR = os.path.join(ROOT, "results", "figures")

OUTPUTS = {
    "runtime_by_instance": "benders_300s_runtime_by_instance.png",
    "nodes_by_instance": "benders_300s_nodes_by_instance.png",
    "lazy_cuts_by_instance": "benders_300s_lazy_cuts_by_instance.png",
    "runtime_vs_N": "benders_300s_runtime_vs_N.png",
    "status_summary": "benders_300s_status_summary.png",
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
BLUE = (31, 119, 180)
GREEN = (44, 160, 44)
ORANGE = (255, 127, 14)
RED = (214, 39, 40)
PURPLE = (148, 103, 189)
COLORS = [BLUE, ORANGE, GREEN, RED, PURPLE, (140, 86, 75)]

FONT = {
    " ": ["000", "000", "000", "000", "000", "000", "000"],
    "0": ["111", "101", "101", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "010", "010", "111"],
    "2": ["111", "001", "001", "111", "100", "100", "111"],
    "3": ["111", "001", "001", "111", "001", "001", "111"],
    "4": ["101", "101", "101", "111", "001", "001", "001"],
    "5": ["111", "100", "100", "111", "001", "001", "111"],
    "6": ["111", "100", "100", "111", "101", "101", "111"],
    "7": ["111", "001", "001", "010", "010", "100", "100"],
    "8": ["111", "101", "101", "111", "101", "101", "111"],
    "9": ["111", "101", "101", "111", "001", "001", "111"],
    "A": ["010", "101", "101", "111", "101", "101", "101"],
    "B": ["110", "101", "101", "110", "101", "101", "110"],
    "C": ["111", "100", "100", "100", "100", "100", "111"],
    "D": ["110", "101", "101", "101", "101", "101", "110"],
    "E": ["111", "100", "100", "110", "100", "100", "111"],
    "F": ["111", "100", "100", "110", "100", "100", "100"],
    "G": ["111", "100", "100", "101", "101", "101", "111"],
    "H": ["101", "101", "101", "111", "101", "101", "101"],
    "I": ["111", "010", "010", "010", "010", "010", "111"],
    "J": ["001", "001", "001", "001", "101", "101", "111"],
    "K": ["101", "101", "110", "100", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "100", "100", "111"],
    "M": ["101", "111", "111", "101", "101", "101", "101"],
    "N": ["101", "111", "111", "111", "111", "111", "101"],
    "O": ["111", "101", "101", "101", "101", "101", "111"],
    "P": ["111", "101", "101", "111", "100", "100", "100"],
    "Q": ["111", "101", "101", "101", "111", "001", "001"],
    "R": ["111", "101", "101", "111", "110", "101", "101"],
    "S": ["111", "100", "100", "111", "001", "001", "111"],
    "T": ["111", "010", "010", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "101", "101", "111"],
    "V": ["101", "101", "101", "101", "101", "101", "010"],
    "W": ["101", "101", "101", "101", "111", "111", "101"],
    "X": ["101", "101", "101", "010", "101", "101", "101"],
    "Y": ["101", "101", "101", "010", "010", "010", "010"],
    "Z": ["111", "001", "001", "010", "100", "100", "111"],
    "-": ["000", "000", "000", "111", "000", "000", "000"],
    "_": ["000", "000", "000", "000", "000", "000", "111"],
    ".": ["000", "000", "000", "000", "000", "000", "010"],
    ":": ["000", "010", "000", "000", "010", "000", "000"],
    "/": ["001", "001", "001", "010", "100", "100", "100"],
    "=": ["000", "000", "111", "000", "111", "000", "000"],
    "%": ["101", "001", "010", "010", "010", "100", "101"],
}


class Canvas:
    def __init__(self, w: int, h: int, bg=WHITE) -> None:
        self.w = w
        self.h = h
        self.pixels = [[bg for _ in range(w)] for _ in range(h)]

    def set(self, x: int, y: int, color) -> None:
        if 0 <= x < self.w and 0 <= y < self.h:
            self.pixels[y][x] = color

    def line(self, x0: int, y0: int, x1: int, y1: int, color=BLACK) -> None:
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def rect(self, x0: int, y0: int, x1: int, y1: int, color, fill=True) -> None:
        x0, x1 = sorted((max(0, x0), min(self.w - 1, x1)))
        y0, y1 = sorted((max(0, y0), min(self.h - 1, y1)))
        if fill:
            for y in range(y0, y1 + 1):
                row = self.pixels[y]
                for x in range(x0, x1 + 1):
                    row[x] = color
        else:
            self.line(x0, y0, x1, y0, color)
            self.line(x1, y0, x1, y1, color)
            self.line(x1, y1, x0, y1, color)
            self.line(x0, y1, x0, y0, color)

    def circle(self, cx: int, cy: int, r: int, color) -> None:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.set(x, y, color)

    def text(self, x: int, y: int, text: str, color=BLACK, scale=2) -> None:
        cursor = x
        for ch in text.upper():
            glyph = FONT.get(ch, FONT.get(" "))
            if glyph is None:
                cursor += 4 * scale
                continue
            for gy, line in enumerate(glyph):
                for gx, bit in enumerate(line):
                    if bit == "1":
                        self.rect(cursor + gx * scale, y + gy * scale, cursor + (gx + 1) * scale - 1, y + (gy + 1) * scale - 1, color)
            cursor += 4 * scale

    def save_png(self, path: str) -> None:
        raw = bytearray()
        for row in self.pixels:
            raw.append(0)
            for r, g, b in row:
                raw.extend((r, g, b))
        def chunk(tag: bytes, data: bytes) -> bytes:
            return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack("!IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        png += chunk(b"IEND", b"")
        with open(path, "wb") as f:
            f.write(png)


def load_rows(path: str) -> Tuple[List[Dict[str, str]], List[str]]:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])


def missing_columns(header: Sequence[str], required: Iterable[str]) -> List[str]:
    have = set(header)
    return [c for c in required if c not in have]


def as_float(value: str) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.upper() == "NA":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def sort_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    def key(row: Dict[str, str]) -> Tuple[str, int, int, str]:
        n = as_float(row.get("N", ""))
        p = as_float(row.get("p", ""))
        return (row.get("family", ""), int(n if n is not None else -1), int(p if p is not None else -1), row.get("instance", ""))
    return sorted(rows, key=key)


def nice_max(values: List[float]) -> float:
    vmax = max(values) if values else 1.0
    if vmax <= 0:
        return 1.0
    exp = math.floor(math.log10(vmax))
    base = 10 ** exp
    for mult in (1, 2, 5, 10):
        if vmax <= mult * base:
            return mult * base
    return 10 * base


def draw_axes(c: Canvas, left: int, top: int, right: int, bottom: int, ymax: float, title: str, ylabel: str) -> None:
    c.text(20, 15, title[:64], BLACK, 2)
    c.text(20, 40, ylabel[:42], BLACK, 1)
    c.line(left, bottom, right, bottom, BLACK)
    c.line(left, top, left, bottom, BLACK)
    for i in range(6):
        y = bottom - int((bottom - top) * i / 5)
        c.line(left - 4, y, right, y, GRAY if i else BLACK)
        val = ymax * i / 5
        label = f"{val:.3g}" if ymax < 10 else f"{val:.0f}"
        c.text(6, y - 6, label, BLACK, 1)


def save_bar_by_instance(rows: List[Dict[str, str]], value_col: str, ylabel: str, title: str, filename: str) -> None:
    rows = sort_rows(rows)
    values: List[float] = []
    for row in rows:
        value = as_float(row.get(value_col, ""))
        if value is not None:
            values.append(value)
    w, h = 1200, 650
    c = Canvas(w, h)
    left, top, right, bottom = 80, 75, w - 30, h - 95
    ymax = nice_max(values)
    draw_axes(c, left, top, right, bottom, ymax, title, ylabel)
    n = len(values)
    step = (right - left) / max(n, 1)
    bar_w = max(2, int(step * 0.7))
    for i, value in enumerate(values):
        x0 = int(left + i * step + step * 0.15)
        x1 = x0 + bar_w
        y = bottom - int((value / ymax) * (bottom - top))
        c.rect(x0, y, x1, bottom - 1, BLUE)
        if i % max(1, n // 12) == 0:
            c.text(x0, bottom + 10, str(i + 1), BLACK, 1)
    c.text(left, h - 45, "X INDEX = CSV ROW ORDER AFTER FAMILY,N,P,INSTANCE SORT", BLACK, 1)
    c.save_png(os.path.join(FIG_DIR, filename))


def save_runtime_vs_n(rows: List[Dict[str, str]], filename: str) -> None:
    pts: List[Tuple[float, float, str]] = []
    for row in rows:
        n = as_float(row.get("N", ""))
        t = as_float(row.get("Ttot", ""))
        fam = row.get("family", "unknown")
        if n is not None and t is not None and n > 0 and t > 0:
            pts.append((n, t, fam))
    w, h = 900, 620
    c = Canvas(w, h)
    left, top, right, bottom = 90, 75, w - 40, h - 80
    nmin = min(p[0] for p in pts) if pts else 1
    nmax = max(p[0] for p in pts) if pts else 10
    tmin = min(p[1] for p in pts) if pts else 0.01
    tmax = max(p[1] for p in pts) if pts else 1
    tmin = max(tmin, 1e-6)
    c.text(20, 15, "BENDERS 300S: RUNTIME VS N", BLACK, 2)
    c.text(20, 40, "Y LOG SCALE, SECONDS", BLACK, 1)
    c.line(left, bottom, right, bottom, BLACK)
    c.line(left, top, left, bottom, BLACK)
    for i in range(6):
        x = left + int((right - left) * i / 5)
        c.line(x, bottom, x, top, GRAY)
        c.text(x - 10, bottom + 10, f"{nmin + (nmax - nmin) * i / 5:.0f}", BLACK, 1)
    log_min, log_max = math.log10(tmin), math.log10(tmax)
    if abs(log_max - log_min) < 1e-9:
        log_max = log_min + 1
    for i in range(6):
        y = bottom - int((bottom - top) * i / 5)
        c.line(left, y, right, y, GRAY if i else BLACK)
        val = 10 ** (log_min + (log_max - log_min) * i / 5)
        c.text(8, y - 6, f"{val:.2g}", BLACK, 1)
    fams = sorted({p[2] for p in pts})
    color_map = {fam: COLORS[i % len(COLORS)] for i, fam in enumerate(fams)}
    for n, t, fam in pts:
        x = left + int((n - nmin) / max(nmax - nmin, 1) * (right - left))
        y = bottom - int((math.log10(t) - log_min) / (log_max - log_min) * (bottom - top))
        c.circle(x, y, 5, color_map[fam])
    for i, fam in enumerate(fams):
        y = 70 + i * 18
        c.rect(right - 160, y, right - 150, y + 10, color_map[fam])
        c.text(right - 145, y, fam[:18], BLACK, 1)
    c.save_png(os.path.join(FIG_DIR, filename))


def save_status_summary(rows: List[Dict[str, str]], filename: str) -> None:
    counts = Counter(row.get("status", "UNKNOWN") or "UNKNOWN" for row in rows)
    labels = list(counts.keys())
    values = [float(counts[label]) for label in labels]
    w, h = 800, 500
    c = Canvas(w, h)
    left, top, right, bottom = 80, 75, w - 40, h - 90
    ymax = nice_max(values)
    draw_axes(c, left, top, right, bottom, ymax, "BENDERS 300S: STATUS SUMMARY", "COUNT")
    step = (right - left) / max(len(labels), 1)
    for i, (label, value) in enumerate(zip(labels, values)):
        x0 = int(left + i * step + step * 0.15)
        x1 = int(left + (i + 1) * step - step * 0.15)
        y = bottom - int((value / ymax) * (bottom - top))
        c.rect(x0, y, x1, bottom - 1, GREEN)
        c.text(x0, y - 18, str(int(value)), BLACK, 1)
        c.text(x0, bottom + 10, label[:22], BLACK, 1)
    c.save_png(os.path.join(FIG_DIR, filename))


def main() -> int:
    os.makedirs(FIG_DIR, exist_ok=True)
    rows, header = load_rows(CSV_PATH)
    generated: List[str] = []
    skipped: Dict[str, List[str]] = defaultdict(list)
    figure_specs = [
        ("runtime_by_instance", ["instance", "p", "Ttot"], lambda: save_bar_by_instance(rows, "Ttot", "TTOT SECONDS", "BENDERS 300S: RUNTIME BY INSTANCE", OUTPUTS["runtime_by_instance"])),
        ("nodes_by_instance", ["instance", "p", "nodes"], lambda: save_bar_by_instance(rows, "nodes", "B&B NODES", "BENDERS 300S: NODES BY INSTANCE", OUTPUTS["nodes_by_instance"])),
        ("lazy_cuts_by_instance", ["instance", "p", "lazy_cuts"], lambda: save_bar_by_instance(rows, "lazy_cuts", "LAZY CUTS", "BENDERS 300S: LAZY CUTS BY INSTANCE", OUTPUTS["lazy_cuts_by_instance"])),
        ("runtime_vs_N", ["family", "N", "Ttot"], lambda: save_runtime_vs_n(rows, OUTPUTS["runtime_vs_N"])),
        ("status_summary", ["status"], lambda: save_status_summary(rows, OUTPUTS["status_summary"])),
    ]
    for name, required, func in figure_specs:
        missing = missing_columns(header, required)
        if missing:
            skipped[name].extend(missing)
            continue
        func()
        generated.append(os.path.join("results", "figures", OUTPUTS[name]))
    print(f"CSV: {os.path.relpath(CSV_PATH, ROOT)}")
    print(f"Rows: {len(rows)}")
    print("Generated:")
    for path in generated:
        print(f"  {path}")
    if skipped:
        print("Skipped:")
        for name, cols in skipped.items():
            print(f"  {name}: missing {', '.join(cols)}")
    else:
        print("Skipped: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
