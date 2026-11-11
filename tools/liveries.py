"""为新增关卡补充涂装：qr（外观表）与 Rt（解锁表）。

qr 结构：qr={eagle:{...},...,wakulla:{suit:"#17191b",lit:"#4a4f52",hood:"#0f1112",fin:"#d8e43a"}},In=t=>...
Rt 结构：Rt=[{...},{id:"wakulla",...,lock:()=>i("...","...")}],qr={...
"""

# qr 表中追加的外观（插在 wakulla 条目之后、qr 表闭合之前）
QT = ',sharkcave:{suit:"#0f3b46",lit:"#2e8ba0",hood:"#0a2a33",fin:"#ffd166"},bluehole:{suit:"#10304f",lit:"#2f7fc4",hood:"#0a1f36",fin:"#e8f4ff"},nutmeg:{suit:"#4a3a26",lit:"#8a6f45",hood:"#33281a",fin:"#d9b382"}'

# Rt 表中追加的涂装条目（插在 wakulla 条目之后、数组闭合之前）
RT = ',{id:"sharkcave",code:11,caseId:"sharkcave",name:()=>i("鲨鱼洞涂装","Shark Cave livery"),blurb:()=>i("马尔代夫浅蓝的干衣，砂金色脚蹼。","A Maldives blue drysuit with sand-gold fins."),lock:()=>i("先结案「鲨鱼洞」（案卷八）","Close Case 8, Shark Cave, first")},{id:"bluehole",code:12,caseId:"bluehole",name:()=>i("蓝洞涂装","Blue Hole livery"),blurb:()=>i("深海的靛蓝干衣，冰白色脚蹼。","An indigo drysuit for deep blue, with ice-white fins."),lock:()=>i("先结案「达哈卜蓝洞」（案卷九）","Close Case 9, Da Dahab Blue Hole, first")},{id:"nutmeg",code:13,caseId:"nutmeg",name:()=>i("油灰涂装","Nutmeg livery"),blurb:()=>i("黏土色的干衣，赭石脚蹼。","A clay-brown drysuit with ochre fins."),lock:()=>i("先结案「坚果油灰洞」（案卷十）","Close Case 10, Nutmeg Cave, first")}'

# 锚点：wakulla 涂装条目的结尾（Rt 表里，紧跟数组闭合）
RT_ANCHOR = 'lock:()=>i("先结案「瓦库拉泉」（案卷七）","Close Case 7, Wakulla Springs, first")}]'
QR_ANCHOR = 'fin:"#d8e43a"}},In=t=>'
