FROM python:3.12-slim
WORKDIR /work
RUN pip install --no-cache-dir presidio-analyzer==2.2.366 spacy==3.8.18 \
 && python -m spacy download en_core_web_sm
COPY make_data.py scan_regex.py scan_presidio.py compare.py /work/
CMD ["sleep", "3600"]
