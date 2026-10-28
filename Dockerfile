# Official Python image; digest fixes the base used by this build.
FROM python@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8
LABEL org.opencontainers.image.title="aws-ecs-secure-deployment"       org.opencontainers.image.description="Minimal Flask ECS learning project"       org.opencontainers.image.source="https://github.com/TobiOnline/aws-ecs-secure-deployment"
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt     && python -m pip uninstall --yes pip     && groupadd --gid 10001 app     && useradd --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app
COPY app/ ./app/
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3     CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--worker-tmp-dir", "/tmp", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"]
