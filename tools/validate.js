// 在 Node 中加载离线包，校验关卡数据能被引擎正常构建。
const noop = () => {};
class MO { constructor(cb) { this.cb = cb; } observe() {} disconnect() {} }
globalThis.MutationObserver = MO;
globalThis.window = globalThis;
Object.defineProperty(globalThis, 'navigator', { value: { languages: ['zh-CN'], language: 'zh-CN', userAgent: 'node' }, configurable: true });
globalThis.location = { search: '', href: 'http://localhost/', hostname: 'localhost', origin: 'http://localhost' };
globalThis.localStorage = { getItem: () => null, setItem: noop, removeItem: noop };
globalThis.matchMedia = () => ({ matches: false, addEventListener: noop, removeEventListener: noop });
globalThis.requestAnimationFrame = (f) => setTimeout(() => f(0), 0);
globalThis.cancelAnimationFrame = noop;
const mkEl = () => ({ style: {}, dataset: {}, classList: { add: noop, remove: noop, contains: () => false }, addEventListener: noop, removeEventListener: noop, appendChild: noop, setAttribute: noop, getAttribute: () => null, querySelector: () => null, querySelectorAll: () => [], getContext: () => null, getBoundingClientRect: () => ({ width: 0, height: 0, left: 0, top: 0 }) });
globalThis.document = { createElement: mkEl, createElementNS: mkEl, getElementById: () => mkEl(), querySelector: () => null, querySelectorAll: () => [], addEventListener: noop, removeEventListener: noop, documentElement: mkEl(), head: mkEl(), body: mkEl(), fonts: { ready: Promise.resolve(), add: noop }, visibilityState: 'visible', hasFocus: () => true };
globalThis.AudioContext = class { constructor() { this.destination = {}; this.currentTime = 0; } createGain() { return { gain: { value: 0, setValueAtTime: noop, linearRampToValueAtTime: noop }, connect: noop }; } createOscillator() { return { frequency: { value: 0, setValueAtTime: noop }, type: '', connect: noop, start: noop, stop: noop }; } createBufferSource() { return { buffer: null, connect: noop, start: noop, stop: noop }; } createBiquadFilter() { return { frequency: { value: 0 }, type: '', Q: { value: 0 }, connect: noop }; } createBuffer() { return { getChannelData: () => new Float32Array(1) }; } createDynamicsCompressor() { return { connect: noop }; } createStereoPanner() { return { pan: { value: 0 }, connect: noop }; } resume() { return Promise.resolve(); } close() { return Promise.resolve(); } decodeAudioData() { return Promise.resolve({}); } };
globalThis.HTMLCanvasElement = class {};

const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const src = fs.readFileSync(path.join(root, 'src/game.js'), 'utf8');
const out = src.replace('export{cb as startGame};', 'export{cb as startGame, ks, pl, xc, Qr, kc, vc, wc};');
const checkPath = path.join(root, 'src/check-tmp.mjs');
fs.writeFileSync(checkPath, out);

import('../src/check-tmp.mjs').then((mod) => {
  const { ks, pl } = mod;
  let bad = 0;
  for (const lv of ks) {
    if (lv.locked) { console.log(`SKIP  ${lv.id} (locked)`); continue; }
    if (!lv.cave) { console.log(`EMPTY ${lv.id}`); bad++; continue; }
    try {
      const g = new pl(lv.cave);
      const relics = (lv.relics ?? []).length;
      const objs = (lv.objectives ?? []).length;
      console.log(`OK    ${lv.id.padEnd(12)} nodes=${lv.cave.nodes.length} edges=${lv.cave.edges.length} relics=${relics} obj=${objs} grid=${g.W}x${g.H}`);
    } catch (e) {
      bad++;
      console.log(`FAIL  ${lv.id}: ${e.message}`);
    }
  }
  console.log(bad ? `\n${bad} 个关卡不可用` : '\n全部关卡可构建');
  process.exit(bad ? 1 : 0);
}).catch((e) => { console.error('LOAD_FAIL', e && e.message); process.exit(2); });
