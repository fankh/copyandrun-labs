// 앱용(shop 읽기쓰기)과 보고용(hr 읽기) 사용자를 admin DB에 만든다
const a = db.getSiblingDB('admin');
a.createUser({ user: 'app', pwd: 'App-lab-1', roles: [{ role: 'readWrite', db: 'shop' }] });
a.createUser({ user: 'report', pwd: 'Report-lab-1', roles: [{ role: 'read', db: 'hr' }] });
