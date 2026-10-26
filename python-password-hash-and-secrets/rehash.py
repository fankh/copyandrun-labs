import sys

sys.path.insert(0, "after")
import accounts
from argon2 import PasswordHasher

old = PasswordHasher(time_cost=1, memory_cost=8192, parallelism=1)
accounts.users["carol"] = old.hash("old-parameters")
print("전:", accounts.users["carol"][:36])
print("재해시 필요:", accounts.ph.check_needs_rehash(accounts.users["carol"]))

print("로그인:", accounts.log_in("carol", "old-parameters"))
print("후:", accounts.users["carol"][:36])
print("재해시 필요:", accounts.ph.check_needs_rehash(accounts.users["carol"]))
