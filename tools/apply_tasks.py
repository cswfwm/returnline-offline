"""注入拍摄任务与水质考察任务的支持代码。

1) rf 的 switch 增加 photo / sample 分支
2) 追加 pf2 / qf2 绘制函数
3) 物品交互增加 photo / sample 两个 kind（拾取时分别记录照片与样本）
4) 目标判定支持 flags 上的 photo_<id> / sample_<id>
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from task_cards import SWITCH_CASES, DRAW_FUNCS

SRC = os.path.join(ROOT, 'src', 'origin-main.js')


def build():
    src = open(SRC, encoding='utf-8').read()
    if 'pf2(' in src:
        print('task cards already patched')
        return

    # 1) switch 分支
    anchor = 'case"relic":ff(o,s,n,e.icon??"coin");break;'
    if anchor not in src:
        raise SystemExit('switch anchor not found')
    src = src.replace(anchor, anchor + SWITCH_CASES, 1)

    # 2) 绘制函数
    anchor2 = 'function rf(t,e){'
    i = src.index(anchor2)
    src = src[:i] + DRAW_FUNCS.strip() + '\n' + src[i:]

    # 3) 交互：photo / sample 物品
    old = ':l.kind==="relic"?{key:"E",label:i(`捡起${l.label}`,`Pick up ${Ut(l.label)}`),act:()=>this.takeRelic(l)}'
    new = (':l.kind==="photo"?{key:"E",label:i(`在「${l.label}」拍一张`,`Take a photo at “${Ut(l.label)}”`),act:()=>this.takePhoto(l)}'
           ':l.kind==="sample"?{key:"E",label:i(`在「${l.label}」取样`,`Take a sample at “${Ut(l.label)}”`),act:()=>this.takeSample(l)}'
           + old)
    if old not in src:
        raise SystemExit('interaction anchor not found')
    src = src.replace(old, new, 1)

    # 4) takePhoto / takeSample 方法：插在 takeRelic 之后
    anchor3 = 'takeRelic(e){const a=this.player,s=e.relic;'
    i = src.index(anchor3)
    methods = (
        'takePhoto(e){const a=this.player;e.taken=!0;this.sendTake(e);'
        'this.ev("photo",Y,a.x,a.y,i(`在${e.label}拍了一张`,`Photographed ${Ut(e.label)}`));'
        'this.fx.push({kind:"treasure",x:e.x,y:e.y});'
        'const k=`photo_${e.id}`;(this.flags[k]??=0);this.flags[k]++;'
        'this.say(i(`拍好了：${e.label}。这张要带出水才算数。`,`Shot: ${Ut(e.label)}. It only counts once it is out of the water.`),5,"story");'
        'this.openInspect({art:"photo",title:e.label,lines:e.desc??[]});'
        'e.onTake?.(this)}'
        'takeSample(e){const a=this.player;e.taken=!0;this.sendTake(e);'
        'this.ev("sample",Y,a.x,a.y,i(`在${e.label}取了水样`,`Sampled at ${Ut(e.label)}`));'
        'this.fx.push({kind:"clip",x:e.x,y:e.y});'
        'const k=`sample_${e.id}`;(this.flags[k]??=0);this.flags[k]++;'
        'this.say(i(`水样取好了：${e.label}。编号要记在板子上。`,`Sample taken: ${Ut(e.label)}. Write the number on the slate.`),5,"story");'
        'this.openInspect({art:"sample",title:e.label,lines:e.desc??[],samples:[1,2,3]});'
        'e.onTake?.(this)}'
    )
    src = src[:i] + methods + src[i:]

    open(SRC, 'w', encoding='utf-8').write(src)
    print('task cards injected')


if __name__ == '__main__':
    build()
