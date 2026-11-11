"""引擎侧改造：解除占位关卡的锁定，并更新相关文案。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'origin-main.js')

# xc：若关卡已有真实数据就直接使用，不再强制锁定成空壳
OLD_XC = ('function xc(t){return{...Qr[t],locked:!0,brief:[],plan:[],objectives:[],'
          'spawn:{x:0,y:0},kit:{cylL:12,startBar:200,stages:0,stageL:0,stageBar:0,'
          'reel:0,mix:"air",lights:1},cave:void 0}}')
NEW_XC = ('function xc(t){const c=Qr[t];if(c&&c.cave)return c;'
          'return{...c,locked:!0,brief:[],plan:[],objectives:[],'
          'spawn:{x:0,y:0},kit:{cylL:12,startBar:200,stages:0,stageL:0,stageBar:0,'
          'reel:0,mix:"air",lights:1},cave:void 0}}')

OLD_VN = 'const Vn=()=>i("完整版（案卷三到七）即将登陆 Steam。","The full game (Cases 3 to 7) is coming to Steam.")'
NEW_VN = 'const Vn=()=>i("所有案卷均已开放，全部可玩。","Every case is open and playable.")'

OLD_SMALL = ('${i("第一、二卷与每日一洞在这里免费玩 · 第三至七卷在完整版里，即将登陆 Steam",'
              '"Cases 1–2 and daily caves are free here · Cases 3–7 are in the full game, coming to Steam")}')
NEW_SMALL = '${i("所有案卷与每日一洞均可游玩","All cases and the daily cave are playable")}'


def build():
    src = open(SRC, encoding='utf-8').read()
    if NEW_XC in src:
        print('engine already patched')
        return
    for old, new in ((OLD_XC, NEW_XC), (OLD_VN, NEW_VN), (OLD_SMALL, NEW_SMALL)):
        if old not in src:
            raise SystemExit('engine anchor not found:\n' + old[:120])
        src = src.replace(old, new, 1)
    open(SRC, 'w', encoding='utf-8').write(src)
    print('engine patched')


if __name__ == '__main__':
    build()
