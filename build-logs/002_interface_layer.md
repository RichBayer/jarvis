# Build Log 002 – Interface Layer

Date: March 2026

## Goal

Add a browser-based interface to the Jarvis system so the local model can be accessed through a web UI instead of only the CLI.

This phase introduces Open WebUI and connects it to the existing Ollama runtime.

---

## Docker Installation

Docker was installed inside the WSL Ubuntu environment using the Ubuntu package repository.

Command used:

sudo apt install docker.io

The Docker engine was verified using the standard test container.

Command used:

docker run hello-world

![Docker installation verification](../docs/screenshots/interface/docker-install-verification.png)

This confirmed that the container runtime is working correctly.

---

## Deploying Open WebUI

Open WebUI was deployed as a Docker container.

Command used:

docker run -d \
-p 3000:8080 \
-v open-webui:/app/backend/data \
--name open-webui \
ghcr.io/open-webui/open-webui:main

The container exposes port 3000 on the host and maps it to port 8080 inside the container.

![Open WebUI container running](../docs/screenshots/interface/webui-container-running.png)

This creates a persistent Docker volume so configuration and chat history survive container restarts.

The interface is available at:

http://localhost:3000

---

## Connecting Open WebUI to Ollama

Initially the container could not detect the local Ollama models.

Investigation showed that Ollama was listening only on the loopback interface.

127.0.0.1:11434

Containers cannot access services bound only to localhost.

The Ollama systemd service was modified to listen on all network interfaces.

Override created using:

sudo systemctl edit ollama

Service override added:

[Service]
Environment="OLLAMA_HOST=0.0.0.0"

The service was reloaded and restarted.

Commands used:

sudo systemctl daemon-reload  
sudo systemctl restart ollama

Verification command:

ss -tulnp | grep 11434

![Ollama API listening on all interfaces](../docs/screenshots/interface/ollama-api-listening.png)

The output confirms that Ollama is now listening on:

*:11434

This allows containers and other services to reach the API.

---

## Interface Verification

After restarting the WebUI container, the interface successfully detected the installed model.

Available model:

llama3.1:8b

A test conversation was executed through the browser interface to confirm the full stack is working.

![Open WebUI chat with local model](../docs/screenshots/interface/webui-chat-working.png)

System stack:

Browser  
Open WebUI container  
Ollama API  
Llama 3.1 model  
RTX 3060 GPU

---

## Current System State

Jarvis now has two working interfaces for interacting with the local AI runtime.

CLI interface:

ai "explain Linux permissions"

Browser interface:

Open WebUI at http://localhost:3000

Both interfaces communicate with the same Ollama runtime.

---

## Next Steps

Future work will focus on improving usability and expanding system capabilities.

Planned tasks:

- enable streaming responses in WebUI
- add additional models optimized for coding and Linux tasks
- improve CLI helper functions
- begin development of the knowledge and memory layer