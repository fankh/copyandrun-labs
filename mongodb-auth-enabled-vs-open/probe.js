// 접속한 사용자로 다섯 가지를 시도하고 한 줄로 출력한다: 읽기 쓰기 타DB읽기 보이는DB수 DB삭제
const ok = (f) => { try { f(); return 'O'; } catch (e) { return 'X'; } };
const shop = db.getSiblingDB('shop');
const hr = db.getSiblingDB('hr');
const r = ok(() => shop.orders.findOne());
const w = ok(() => shop.probe.updateOne({ _id: 1 }, { $set: { t: 1 } }, { upsert: true }));
const h = ok(() => hr.salaries.findOne());
let n = 0;
try {
  n = db.adminCommand({ listDatabases: 1, nameOnly: true }).databases
    .filter((d) => !['admin', 'config', 'local'].includes(d.name)).length;
} catch (e) { n = 0; }
const d = ok(() => { if (db.getSiblingDB('tmpdrop').dropDatabase().ok !== 1) throw 1; });
print([r, w, h, n, d].join(' '));
