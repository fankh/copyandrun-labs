// 공격자 시점: 보이는 DB 이름, 급여 문서 읽기, 실패할 때의 오류 문구를 그대로 출력한다
const say = (label, f) => { try { print(label + ': ' + f()); } catch (e) { print(label + ': 거절 - ' + String(e.message).slice(0, 80)); } };
say('DB 목록', () => db.adminCommand({ listDatabases: 1, nameOnly: true }).databases.map((d) => d.name).join(','));
say('hr.salaries', () => JSON.stringify(db.getSiblingDB('hr').salaries.find({}, { _id: 0 }).toArray()));
say('shop 쓰기', () => 'ok=' + db.getSiblingDB('shop').probe.updateOne({ _id: 2 }, { $set: { t: 1 } }, { upsert: true }).acknowledged);
