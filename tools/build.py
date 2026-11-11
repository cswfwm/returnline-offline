"""一键构建：从干净的引擎源文件生成最终游戏包 src/game.js。

流程（顺序固定，全部幂等）：
1. 恢复 src/origin-main.js 为上游原始文件（由 tools/upstream/ 备份）
2. 注入关卡解锁改造（xc 不再锁死有数据的关卡）
3. 注入装备表扩展（福利补偿设备等）
4. 注入任务系统（拍摄任务、水质考察任务）
5. 注入涂装（新增关卡的解锁外观）
6. 按 tools/levels/*.js 替换/追加关卡数据，生成 src/game.js
7. 组装离线网页资源到 apk/app/src/main/assets/www

用法：python3 tools/build.py
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
UPSTREAM = os.path.join(TOOLS, 'upstream', 'main-D610L1x0.js')
ORIGIN = os.path.join(ROOT, 'src', 'origin-main.js')
GAME = os.path.join(ROOT, 'src', 'game.js')
WWW = os.path.join(ROOT, 'apk', 'app', 'src', 'main', 'assets', 'www')


def run(script):
    r = subprocess.run([sys.executable, os.path.join(TOOLS, script)], cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f'{script} 执行失败')


def restore_upstream():
    if not os.path.exists(UPSTREAM):
        raise SystemExit(f'缺少上游原始文件: {UPSTREAM}')
    shutil.copy2(UPSTREAM, ORIGIN)
    print('restored upstream source')


def build_www():
    os.makedirs(os.path.join(WWW, 'assets'), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, 'assets')):
        shutil.copy2(os.path.join(ROOT, 'assets', f), os.path.join(WWW, 'assets', f))
    shutil.copy2(GAME, os.path.join(WWW, 'assets', 'main-D610L1x0.js'))
    for name in ('preload-helper-PPVm8Dsz.js', 'main-B_Pg_0u3.css', 'index-BLF9EMSn.js'):
        src = os.path.join(ROOT, 'assets', name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(WWW, 'assets', name))
    print('www assets assembled')


def main():
    restore_upstream()
    run('apply_engine.py')
    run('apply_gear.py')
    run('apply_tasks.py')
    run('apply_liveries.py')
    run('apply.py')
    build_www()


if __name__ == '__main__':
    main()
