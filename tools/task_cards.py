"""扩展 inspect 卡片绘制：新增「拍摄记录」与「水质样本」两类任务卡。

在 rf 的 switch 中插入 case "photo" / case "sample"，并追加两个绘制函数。
"""

# switch 内新增分支（插在 default 之前）
SWITCH_CASES = 'case"photo":pf2(o,s,n,e);break;case"sample":qf2(o,s,n,e);break;'

# 新增绘制函数：拍摄记录卡、水质样本卡
DRAW_FUNCS = r'''
function pf2(t,e,a,s){const n=e/2,o=a/2;t.save();t.translate(n,o);t.fillStyle="#111417";be(t,-200,-90,400,180,10),t.fill();t.fillStyle="#1b1f23";be(t,-188,-78,376,156,8),t.fill();const r=t.createRadialGradient(-40,-30,6,0,0,120);r.addColorStop(0,"rgba(150,215,235,0.55)"),r.addColorStop(.45,"rgba(50,100,120,0.35)"),r.addColorStop(1,"rgba(8,16,20,0.15)");t.fillStyle=r,t.beginPath(),t.arc(0,0,86,0,Math.PI*2),t.fill();t.strokeStyle="rgba(210,235,245,0.5)",t.lineWidth=4,t.beginPath(),t.arc(0,0,86,0,Math.PI*2),t.stroke();t.fillStyle="#0c1013";be(t,-150,-62,120,54,8),t.fill();t.fillStyle="#f2c230";t.beginPath(),t.arc(-104,-40,8,0,Math.PI*2),t.fill();t.fillStyle="#e7e2d2";t.font='bold 17px "PingFang SC","Noto Sans SC",sans-serif';t.textAlign="left";t.fillText(s.title??i("拍摄记录","Photo record"),-188,-96);t.fillStyle="rgba(215,230,235,0.75)";t.font='14px "PingFang SC","Noto Sans SC",sans-serif';const lines=(s.lines??[]).slice(0,3);lines.forEach((l,k)=>t.fillText(String(l).slice(0,34),-186,-52+k*24));t.restore();Ts(t,n,o,240)}
function qf2(t,e,a,s){const n=e/2,o=a/2;t.save();t.translate(n,o);t.fillStyle="rgba(140,210,230,0.10)";t.fillRect(-210,-96,420,192);const pts=[[-140,-30],[0,-52],[140,-22]];pts.forEach(([x,y],k)=>{t.fillStyle="#bfe4ee";t.globalAlpha=.9;t.beginPath();t.moveTo(x-34,y+42);t.lineTo(x-34,y-34);t.lineTo(x-16,y-44);t.lineTo(x+16,y-44);t.lineTo(x+34,y-34);t.lineTo(x+34,y+42);t.closePath();t.fill();t.globalAlpha=1;t.fillStyle="rgba(90,180,210,0.55)";t.fillRect(x-30,y+4,60,34);t.fillStyle="#f2e8cf";t.font='bold 13px "PingFang SC","Noto Sans SC",sans-serif';t.textAlign="center";t.fillText(s.samples?.[k]??String(k+1),x,y+26)});t.fillStyle="#e7e2d2";t.font='bold 17px "PingFang SC","Noto Sans SC",sans-serif';t.textAlign="left";t.fillText(s.title??i("水质样本","Water sample"),-206,-92);t.fillStyle="rgba(215,230,235,0.72)";t.font='13px "PingFang SC","Noto Sans SC",sans-serif';const lines=(s.lines??[]).slice(0,3);lines.forEach((l,k)=>t.fillText(String(l).slice(0,40),-206,52+k*20));t.restore()}
'''

# 物品渲染：拍摄点与取样点的世界内提示
ITEM_RENDER_HINT = None
