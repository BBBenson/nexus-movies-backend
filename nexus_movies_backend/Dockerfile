FROM python:3.12.2-slim-bullseye

WORKDIR /usr/src/nexus_movies_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install system dependencies including graphviz and build tools
RUN apt-get update && apt-get install -y \
    graphviz \
    graphviz-dev \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Convert Windows line endings and make entrypoint executable
RUN if [ -f "/usr/src/nexus_movies_backend/entrypoint.sh" ]; then \
        sed -i 's/\r$//g' /usr/src/nexus_movies_backend/entrypoint.sh && \
        chmod +x /usr/src/nexus_movies_backend/entrypoint.sh; \
    fi

# Create and switch to non-root user
RUN useradd -m appuser
USER appuser

ENTRYPOINT [ "/usr/src/nexus_movies_backend/entrypoint.sh" ]