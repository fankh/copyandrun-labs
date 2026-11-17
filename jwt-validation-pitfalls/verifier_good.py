"""고친 검증: 알고리즘을 서버가 고정하고, 만료 시각, 발급자, 대상, 필수 항목을 모두 확인한다."""
import jwt

ISS, AUD = "https://auth.lab", "shop-api"


def verify(token, public_pem):
    return jwt.decode(
        token, public_pem, algorithms=["RS256"],
        issuer=ISS, audience=AUD, leeway=5,
        options={"require": ["exp", "iat", "iss", "aud", "sub"]},
    )
