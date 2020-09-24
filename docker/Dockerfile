FROM python:3.8-slim-buster
LABEL maintainer="LSDopen - Stefan Lesicnik (stefan@lsdopen.io)"

ENV REDIS_DUMP_BACKUP_VERSION "v0.1-alpha"

ENV REDIS_DUMP_BACKUP_ARCHIVE "${REDIS_DUMP_BACKUP_VERSION}.tar.gz"
ENV REDIS_DUMP_BACKUP_URL "https://github.com/lsdopen/redis-dump-backup/archive/${REDIS_DUMP_BACKUP_ARCHIVE}"

WORKDIR /app

RUN apt-get update && \
  apt-get install -y --no-install-recommends wget redis-tools

# Download / Check / Install
RUN cd /tmp \
    # Get REDIS-DUMP-BACKUP
    && wget -qO ${REDIS_DUMP_BACKUP_ARCHIVE} "${REDIS_DUMP_BACKUP_URL}" \
    # Install
    && tar -xzvf ${REDIS_DUMP_BACKUP_ARCHIVE} -C /app --strip-components=1 \
    # Cleanup downloaded archive
    && rm -rf /tmp/${REDIS_DUMP_BACKUP_ARCHIVE}

RUN pip install pipenv && \
  apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
  pipenv install --deploy --system && \
  apt-get remove -y gcc python3-dev libssl-dev && \
  apt-get autoremove -y && \
  pip uninstall pipenv -y

CMD ["python", "redis-dump-backup.py"]
