// 교차 확인: 다른 구현(Node jsonwebtoken)으로 같은 토큰을 고정 알고리즘 설정에서 검증한다.
// 사용: node node_verify.js 폴더
const fs = require("fs");
const jwt = require("jsonwebtoken");
const dir = process.argv[2];
const tokens = JSON.parse(fs.readFileSync(`${dir}/tokens.json`, "utf8"));
const pub = fs.readFileSync(`${dir}/server_pub.pem`);
let accepted = 0;
for (const [name, tok] of Object.entries(tokens)) {
  let r;
  try {
    jwt.verify(tok, pub, { algorithms: ["RS256"], issuer: "https://auth.lab", audience: "shop-api" });
    r = "수락";
    if (name !== "정상 토큰") accepted++;
  } catch (e) {
    r = "거절 (" + e.name + ")";
  }
  console.log(`  ${name.padEnd(10)} ${r}`);
}
console.log(`  공격 토큰 수락 ${accepted}건`);
process.exit(accepted ? 1 : 0);
