# duo-logstalgia
# Streams Duo Authentication Logs to Logstalgia Custom Log Format.
# See README.md for documentation.

FROM python:alpine

# Alpine packages to install.
ENV APK_PACKAGES \
    alpine-sdk \
    libffi-dev \
    tzdata

# PyPI packages to install.
ENV PIP_PACKAGES \
    termcolor \
    duo_client

# Install the above packages, configure system time and create the project directory.
RUN apk --no-cache add $APK_PACKAGES && \
    pip --no-cache-dir install $PIP_PACKAGES && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone && \
    apk del tzdata && \
    mkdir -p /opt/project

WORKDIR /opt/project
COPY src .

# Compile Python source, then remove it.
RUN python -m compileall -b .; \
    find . -name "*.py" -type f -print -delete

ENTRYPOINT ["python","-u", "main.pyc"]