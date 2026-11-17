FROM python:3.12-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends libimage-exiftool-perl libarchive-zip-perl \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir pillow piexif python-docx
WORKDIR /work
COPY make_samples.py inspect_meta.py clean_meta.py compare_thumb.py /work/
CMD ["sleep", "3600"]
