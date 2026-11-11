"""注入新增关卡的涂装：qr（外观表）与 Rt（解锁表）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from liveries import QT, RT, RT_ANCHOR, QR_ANCHOR

SRC = os.path.join(ROOT, 'src', 'origin-main.js')


def build():
    src = open(SRC, encoding='utf-8').read()
    if 'caseId:"sharkcave"' in src:
        print('liveries already patched')
        return

    # Rt 表：wakulla 条目的 `}` 之后插入新条目
    if RT_ANCHOR not in src:
        raise SystemExit('Rt anchor not found')
    src = src.replace(
        RT_ANCHOR,
        'lock:()=>i("先结案「瓦库拉泉」（案卷七）","Close Case 7, Wakulla Springs, first")}' + RT + ']',
        1)

    # qr 表：wakulla 条目之后、qr 表闭合之前插入新外观
    if QR_ANCHOR not in src:
        raise SystemExit('qr anchor not found')
    src = src.replace(QR_ANCHOR, 'fin:"#d8e43a"' + QT + '}},In=t=>', 1)

    open(SRC, 'w', encoding='utf-8').write(src)
    print('liveries injected')


if __name__ == '__main__':
    build()
