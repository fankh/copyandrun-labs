// 시험용 데이터: shop.orders 3건, hr.salaries 2건
db.getSiblingDB('shop').orders.insertMany([{ item: 'pen' }, { item: 'ink' }, { item: 'pad' }]);
db.getSiblingDB('hr').salaries.insertMany([{ name: 'kim', pay: 5000 }, { name: 'lee', pay: 6000 }]);
