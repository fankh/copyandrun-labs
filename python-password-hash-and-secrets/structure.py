import time

from argon2 import PasswordHasher, extract_parameters

ph = PasswordHasher()
print("time_cost:", ph.time_cost, " memory_cost(KiB):", ph.memory_cost, " parallelism:", ph.parallelism)

start = time.perf_counter()
stored = ph.hash("correct horse battery")
print("hash 소요(초):", round(time.perf_counter() - start, 3))

print(stored)
for part in stored.split("$")[1:]:
    print("  ", part)
print(extract_parameters(stored))
print("같은 비밀번호를 다시 해시:", ph.hash("correct horse battery") != stored)
