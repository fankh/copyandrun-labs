# extract_test.py
from pypdf import PdfReader

reader = PdfReader("company_rules.pdf")
print("쪽 수:", len(reader.pages))
print(repr(reader.pages[0].extract_text()))
