# syntax=docker/dockerfile:1.7
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROME_DRIVER=/usr/bin/chromedriver

# Install system dependencies and Google Chrome for headless automation
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        fonts-liberation \
        gnupg \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatspi2.0-0 \
        libcairo2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libglib2.0-0 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libpango-1.0-0 \
        libx11-6 \
        libx11-xcb1 \
        libxau6 \
        libxcb1 \
        libxcb-dri3-0 \
        libxcomposite1 \
        libxcursor1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxi6 \
        libxrandr2 \
        libxrender1 \
        libxshmfence1 \
        libxslt1.1 \
        tzdata \
        unzip \
        wget \
        xdg-utils \
        xvfb \
 && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repository and install the stable channel
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-keyring.gpg \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends google-chrome-stable \
 && rm -rf /var/lib/apt/lists/*

# Create an unprivileged user to run the application
ARG APP_USER=appuser
RUN groupadd --system ${APP_USER} \
 && useradd --system --create-home --gid ${APP_USER} ${APP_USER}

WORKDIR /app

COPY --chown=${APP_USER}:${APP_USER} requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY --chown=${APP_USER}:${APP_USER} . .

RUN mkdir -p /app/cache /app/logs \
 && chown -R ${APP_USER}:${APP_USER} /app/cache /app/logs

# Install gosu for dropping privileges in entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

COPY --chown=root:root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
