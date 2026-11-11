"""把 Qr 里的占位关卡替换为完整关卡定义，并输出 src/game.js。"""
import importlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'origin-main.js')
OUT = os.path.join(ROOT, 'src', 'game.js')

sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'levels'))

QR_START = 'Qr={'
QR_END = 'kc=['

MODULES = [
    'eagle', 'skylight', 'tham', 'plura', 'wakulla',
    'sharkcave', 'bluehole', 'nutmeg',
]


def load_patches():
    patches = {}
    for name in MODULES:
        path = os.path.join(ROOT, 'tools', 'levels', name + '.js')
        if not os.path.exists(path):
            continue
        body = open(path, encoding='utf-8').read().strip()
        m = re.match(r'\{id:"([a-z0-9-]+)"', body)
        if not m:
            raise SystemExit(f'{name}: 缺少 id')
        patches[m.group(1)] = body
    return patches


def build():
    src = open(SRC, encoding='utf-8').read()
    i = src.index(QR_START)
    j = src.index(QR_END, i)
    head, seg, tail = src[:i + len('Qr={')], src[i + len('Qr={'):j], src[j:]

    # 找出每个关卡对象在 seg 中的起止位置
    starts = [(m.start(), m.group(1)) for m in re.finditer(r'(?:^|,)([a-z][a-z0-9]*):\{id:"', seg)]
    spans = []
    for n, (pos, key) in enumerate(starts):
        obj_start = seg.index('{', pos)
        obj_end = starts[n + 1][0] + 1 if n + 1 < len(starts) else len(seg)
        raw = seg[obj_start:obj_end].rstrip().rstrip(',')
        spans.append((obj_start, obj_end, key, raw))

    patches = load_patches()
    rebuilt = []
    used = set()
    for obj_start, obj_end, key, raw in spans:
        rebuilt.append(f'{key}:{patches.get(key, raw)}')
        used.add(key)

    # 新增关卡：原表里没有的 key，追加到末尾
    added = [k for k in patches if k not in used]
    for key in added:
        rebuilt.append(f'{key}:{patches[key]}')

    new = head + ','.join(rebuilt) + '},' + tail

    # 关卡清单同步扩展
    extra = [k for k in added if k in patches]
    if extra:
        new = new.replace('kc=["eagle","skylight","tham","plura","wakulla"]',
                          'kc=["eagle","skylight","tham","plura","wakulla",' +
                          ','.join(f'"{k}"' for k in extra) + ']', 1)

    open(OUT, 'w', encoding='utf-8').write(new)
    print('patched levels:', ', '.join(sorted(patches)) or '(none)')
    if extra:
        print('new cases:', ', '.join(extra))


if __name__ == '__main__':
    build()
