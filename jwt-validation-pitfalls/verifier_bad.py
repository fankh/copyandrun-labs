"""검증을 잘못 구현한 예: 토큰 헤더의 알고리즘을 믿고, 만료와 대상(aud)을 보지 않는다."""
import jwt


def verify(token, public_pem):
    alg = jwt.get_unverified_header(token)["alg"]          # 잘못: 헤더가 알려 주는 알고리즘을 그대로 허용
    key = public_pem if alg != "none" else None
    return jwt.decode(
        token, key, algorithms=[alg],
        options={"verify_exp": False, "verify_aud": False, "verify_iss": False},
    )
