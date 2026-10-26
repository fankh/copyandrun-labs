import sys

sys.path.insert(0, "after")
import accounts

accounts.sign_up("alice", "correct horse battery")
print("정상 비밀번호:", accounts.log_in("alice", "correct horse battery"))
print("틀린 비밀번호:", accounts.log_in("alice", "wrong password"))
print("없는 사용자:", accounts.log_in("nobody", "x"))
print("DB 비밀번호 길이:", len(accounts.db["password"]))
