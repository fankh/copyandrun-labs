awk 'function r(n) { x = (x * 1103515245 + 12345) % 2147483648; return int(x / 65536) % n + 1 }
BEGIN {
  x = 42
  split("8.8.8.8 8.8.8.8 8.8.8.8 1.1.1.1 1.1.1.1 9.9.9.9 208.67.222.222 10.0.0.15 10.0.0.15 192.168.1.20", ip, " ")
  split("200 200 200 200 200 200 301 403 404 404 500", st, " ")
  split("/ /login /api/items /admin /static/app.js /search", pa, " ")
  split("GET GET GET POST", me, " ")
  for (i = 0; i < 120; i++) {
    h = 8 + r(6); m = r(60) - 1; s = r(60) - 1
    printf "{\"index\":{}}\n"
    printf "{\"@timestamp\":\"2026-10-16T%02d:%02d:%02dZ\",\"source\":{\"ip\":\"%s\"},\"http\":{\"request\":{\"method\":\"%s\"},\"response\":{\"status_code\":%s}},\"url\":{\"path\":\"%s\"}}\n", h, m, s, ip[r(10)], me[r(4)], st[r(11)], pa[r(6)]
  }
}' > access-bulk.ndjson
