# Build Log 001 – Runtime Stack

Date: March 2026

## Goal

Bring up the local AI runtime for the Jarvis system and confirm that
a model can run successfully on the workstation.

This phase focuses only on the runtime layer. Higher level components
(UI, memory systems, automation, etc.) will be added later.

---

## System Environment

Host machine
Lenovo Legion desktop

CPU
AMD Ryzen 7 5800X

RAM
32 GB

GPU
NVIDIA RTX 3060 (12 GB VRAM)

Operating system
Windows 11 with WSL2 Ubuntu

Jarvis repository location

/home/richb/ai/projects/jarvis

---

## Installing the Runtime (Ollama)

Ollama was installed inside the WSL Ubuntu environment using the
official installation script.

Command used:

curl -fsSL https://ollama.com/install.sh | sh

The installer completed successfully and reported that the NVIDIA GPU
was detected.

The local Ollama API is now running at:

127.0.0.1:11434

Screenshot

![Ollama installation](../docs/screenshots/runtime/ollama-installation.png)

---

## Downloading the First Model

For the initial test model I chose:

llama3.1:8b

This model size fits comfortably on the RTX 3060 with 12 GB of VRAM.

Command used:

ollama pull llama3.1:8b

The download completed successfully and passed SHA256 verification.

Screenshot

Screenshot

![Model download](../docs/screenshots/runtime/model-download.png)

---

## Verifying the Runtime

To confirm the runtime was working correctly, the model was launched
interactively.

Command used:

ollama run llama3.1:8b

Test prompt used:

Explain in one sentence what Linux is.

The model returned a valid response, confirming that:

* the Ollama runtime is functioning
* the model loads correctly
* inference works inside WSL

Screenshot

Screenshot

![First model response](../docs/screenshots/runtime/model-first-response.png)

---

## Investigating Model Storage

After verifying the runtime worked, I checked where Ollama stores
model files on disk.

Runtime libraries are located at:

/usr/local/lib/ollama

Model data is stored under the Ollama service account:

/usr/share/ollama/.ollama/models

The actual model weights are stored in the blobs directory:

/usr/share/ollama/.ollama/models/blobs

The Llama 3.1 8B model appears as a ~4.6 GB blob file.

Screenshot

Screenshot

![Model storage location](../docs/screenshots/runtime/model-storage-location.png)

---

## Current Status

At this point the Jarvis system has a working local AI runtime.

Working components:

* WSL Ubuntu environment
* Ollama runtime installed
* Llama 3.1 8B model downloaded
* local inference verified

This is the first phase where the system can actually run an AI model.

---

## Notes for Future Work

Currently Ollama stores models inside the WSL filesystem.

The long-term design for this project places models on the NVMe AI
workspace:

/mnt/g/ai/models

Relocating the model storage will be evaluated later once the rest of
the runtime stack is in place.

---

## Next Steps

Next phase will focus on the user interface layer:

* install Open WebUI
* connect the UI to the Ollama API
* continue building the Jarvis system components
