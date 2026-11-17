"""Presidio 로 같은 파일을 스캔합니다. extra=True 이면 한국어 recognizer 를 더합니다."""
from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.predefined_recognizers import KrBrnRecognizer, KrRrnRecognizer

LANG = "en"   # 설치한 NLP 모델은 영어 작은 모델 하나뿐이라 모든 분석을 en 으로 돌립니다.
TYPE_MAP = {"EMAIL_ADDRESS": "EMAIL", "PHONE_NUMBER": "PHONE", "KR_MOBILE": "PHONE",
            "CREDIT_CARD": "CARD", "KR_RRN": "RRN", "KR_BRN": "BRN"}


def build(extra):
    nlp = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": LANG, "model_name": "en_core_web_sm"}],
    }).create_engine()
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers(nlp_engine=nlp, languages=[LANG])
    if extra:
        # 내장 한국어 recognizer 는 기본 언어가 ko 라서 en 으로 다시 만들어 등록합니다.
        registry.add_recognizer(KrRrnRecognizer(supported_language=LANG))
        registry.add_recognizer(KrBrnRecognizer(supported_language=LANG))
        # 직접 만든 recognizer: 010 휴대전화 번호(하이픈, 공백, +82 표기)
        registry.add_recognizer(PatternRecognizer(
            supported_entity="KR_MOBILE",
            supported_language=LANG,
            patterns=[Pattern("KR mobile", r"(?<!\d)(?:\+82[-\s]?10|010)[-\s]?\d{4}[-\s]?\d{4}(?!\d)", 0.6)],
        ))
    return AnalyzerEngine(registry=registry, nlp_engine=nlp, supported_languages=[LANG])


def scan_text(engine, text, threshold=0.5):
    out, other = [], {}
    for r in engine.analyze(text=text, language=LANG, score_threshold=threshold):
        kind = TYPE_MAP.get(r.entity_type)
        if kind:
            out.append({"type": kind, "start": r.start, "end": r.end, "score": round(r.score, 2)})
        else:
            other[r.entity_type] = other.get(r.entity_type, 0) + 1
    return out, other
