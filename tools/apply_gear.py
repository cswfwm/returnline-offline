"""把新增装备条目注入 ii（装备说明页）数组。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from gear_items import GEAR_ITEMS

SRC = os.path.join(ROOT, 'src', 'origin-main.js')

ANCHOR = '],Fs=t=>`gear:${t}`'


def build():
    src = open(SRC, encoding='utf-8').read()
    if 'emergency-kit' in src:
        print('gear already patched')
        return
    i = src.index('const ii=[{id:"backup-light"')
    j = src.index(ANCHOR, i)
    seg = src[i:j]
    if not seg.rstrip().endswith('}'):
        raise SystemExit('无法识别 ii 数组结尾')
    new = seg.rstrip() + GEAR_ITEMS + src[j:]
    out = src[:i] + new
    open(SRC, 'w', encoding='utf-8').write(out)
    print('gear items injected')


if __name__ == '__main__':
    build()
