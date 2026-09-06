# Cutting Lyne Freight & Logistics - Technical Assessment

**Candidate:** Tinashe Dzikiti  
**Email:** sirbasil.100@gmail.com
**Phone:** 077243207
**GitHub Repository:** https://github.com/Smeeks01only/cutting-lyne-assessment

---

## Executive Summary & Approach
This repository contains the complete implementation for the Cutting Lyne Technical Assessment. My approach prioritized **modularity, clean architecture, and practical deployability** across all tasks, adhering to modern software engineering best practices. 

Rather than building a monolithic application, I structured the assessment into isolated, well-defined components. Where applicable, I utilized lightweight machine learning models (TF-IDF/LinearSVC) and strict dependency management to ensure the prototypes could be seamlessly deployed to free-tier cloud environments (Render) without exhausting memory limits.

Below is a summary of the approach taken for each task:

### Task 1: Customs Classification AI
- **Folder:** `task-1-customs-classification/`
- **Approach:** Built a machine learning pipeline using `scikit-learn` to classify product descriptions into accurate HS codes. I trained a `LinearSVC` model with a `TfidfVectorizer` for blazing-fast inference, deliberately avoiding heavy LLMs for a task that requires categorical precision. The model is exposed via a robust `FastAPI` backend and integrated into a premium, responsive dark-mode HTML/Vanilla JS frontend.

### Task 2: Data Pipeline System Design
- **Folder:** `task-2-data-pipeline-design/`
- **Approach:** Architected a scalable ETL data pipeline capable of handling high-volume logistics data. The design leverages cloud-native principles, proposing an S3 landing zone, Apache Airflow for orchestration, Snowflake for the data warehouse, and Metabase for analytics. This approach ensures raw data is immutable and separates compute from storage for cost-efficiency. (Available in Markdown, PDF and Word formats).

### Task 3: Shipment Tracking API
- **Folder:** `task-3-shipment-api/`
- **Approach:** Developed a standalone microservice using `FastAPI` and `SQLAlchemy`. The service dynamically calculates ETAs based on origin/destination points and evaluates shipments through a procedural Risk Engine to flag potential compliance or delay issues. It is completely containerizable and currently deployed live on Render as a decoupled backend.

### Task 4: AI Tool Evaluation
- **Folder:** `task-4-ai-tool-evaluation/`
- **Approach:** Conducted a comprehensive market analysis of existing AI solutions in the freight forwarding space. Evaluated specialized platforms (like Altana and Flexport AI) against generic foundational models, providing a strategic recommendation based on accuracy, cost and seamless API integration capabilities. (Available in Markdown, PDF, and Word formats).

### Task 5: Logistics Chatbot Prototype
- **Folder:** `task-5-logistics-chatbot/`
- **Approach:** Built an end-to-end NLP customer service chatbot. I implemented a hybrid intent-classification and lexical retrieval system (TF-IDF) over a custom logistics knowledge base. When the "Shipment Tracking" intent is triggered, the chatbot automatically extracts the tracking number (e.g., `CLF-2026-001`) and makes a live secure HTTP request to the **Task 3 API** to fetch real-time data. It features a fully responsive, modern web UI with dynamic viewport handling for mobile devices.

---

## Live Demos
- **Task 5 (Chatbot):** `https://cutting-lyne-assessment-logistics-chatbot.onrender.com`

*Note: The prototypes are hosted on Render's free tier, which spins down after 15 minutes of inactivity. The initial request may take ~30 seconds to wake the server, but subsequent requests will be instant.*
