// 校验关卡 JS 文件：语法正确 + 结构完整。
// 用法：node tools/check-levels.js
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const dir = path.join(__dirname, '..', 'tools', 'levels');
const files = fs.readdirSync(dir).filter((f) => f.endsWith('.js')).sort();
let bad = 0;

for (const f of files) {
  const body = fs.readFileSync(path.join(dir, f), 'utf8').trim();
  const tmp = path.join('/tmp', `lv-${f}`);
  fs.writeFileSync(tmp, `const i=(a,b)=>a;\nconst X=${body};\n`);
  try {
    execFileSync('node', ['--check', tmp], { stdio: 'pipe' });
  } catch (e) {
    bad++;
    const msg = (e.stderr || '').toString().split('\n').slice(0, 6).join('\n');
    console.log(`FAIL  ${f}\n${msg}\n`);
    continue;
  }
  // 结构检查
  const need = ['id:', 'cave:{', 'nodes:[', 'edges:[', 'relics:[', 'objectives:[', 'setup(t){', 'update(t'];
  const miss = need.filter((k) => !body.includes(k));
  if (miss.length) {
    bad++;
    console.log(`FAIL  ${f}: 缺少字段 ${miss.join(', ')}\n`);
    continue;
  }
  const id = (body.match(/\{id:"([a-z0-9-]+)"/) || [])[1] || '?';
  console.log(`OK    ${f.padEnd(20)} id=${id}`);
}

console.log(bad ? `\n${bad} 个关卡文件有问题` : '\n全部关卡文件通过');
process.exit(bad ? 1 : 0);
