"""가장 흔한 실수: 클레임을 읽으려고 decode 하면서 서명 확인을 꺼 둔 채로 인증에 쓴다."""
import jwt


def verify(token, public_pem):
    return jwt.decode(token, options={"verify_signature": False})
