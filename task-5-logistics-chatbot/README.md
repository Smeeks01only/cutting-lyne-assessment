---
title: Logistics Chatbot
emoji: 📦
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---

# Cutting Lyne Logistics Assistant

A sophisticated, NLP-powered logistics assistant designed to answer customer queries regarding shipping, tracking, and customs documentation.

## Architecture
- **Framework:** FastAPI
- **Retrieval:** TF-IDF Lexical Search (Lightweight footprint for 512MB RAM constraints)
- **Integration:** REST API connection to the Shipment Risk & ETA microservice.
