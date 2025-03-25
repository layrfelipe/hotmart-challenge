FROM ollama/ollama:latest

# Install curl (if not already in the base image)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      curl

# Start Ollama temporarily in the background, wait for it, then pull Mistral
RUN ollama serve & \
    curl --retry 10 --retry-connrefused --retry-delay 1 http://localhost:11434/ && \
    curl -X POST -d '{"name": "mistral"}' http://localhost:11434/api/pull
