# Product Strategy for AI-Enhanced Program Data Extractor

## Strategic Goal

As a Product Strategist, the mission is to evolve this technical PoC into a valuable tool that contributes directly to Studyportals’ strategic objectives:

- Significantly improve data collection **efficiency**
- Ensure **data accuracy**
- Handle **scale** (200k+ programs)
- Keep information **up-to-date**

---

## Current State

- Processes **a single URL** at a time
- Supports **mock or local LLM-based extraction**
- Outputs to **console or file**

---

## Top 5 Priority Features

### 1. **PostgreSQL Database Integration**

**What:**  
Implement functionality to connect to a PostgreSQL database and store extracted structured data (program name, fee, deadline, requirements, URL, timestamp, etc.) using a well-defined schema.

**Why (Strategy):**  
This is the **foundation** for scale, historical tracking, analysis, and change detection. It moves the project from script to system and enables strategic workflows.

**Addresses:**  
✅ Scale  
✅ Data Persistence  

---

### 2. **Scalable Input & Batch Processing**

**What:**  
Allow processing a **list of URLs** from a source (text file, CSV, or ideally a database table). Add batch processing capability to handle URLs sequentially.

**Why (Strategy):**  
Single-URL input doesn't scale. This feature proves the ability to handle **thousands** of programs and tests DB integration under realistic usage.

**Addresses:**  
✅ Scale  
✅ Efficiency  

---

### 3. **Data Versioning & Change Detection Logic**

**What:**  
Enhance the DB schema to **store historical versions** of program data. Compare each new scrape with the last version and flag differences (e.g., fee, deadlines).

**Why (Strategy):**  
Delivers on the promise of smart crawlers. Helps data operators **focus on what changed**, reducing manual re-checks.

**Addresses:**  
✅ Up-to-dateness  
✅ Efficiency  
✅ Accuracy  

---

### 4. **LLM Confidence Scoring & Basic Validation Rules**

**What:**  
Add basic logic to **score the quality** of extractions. Use rules like:

- Are all fields present?
- Does the fee look like a currency?
- Is the deadline in a valid date format?

Flag low-confidence entries for review.

**Why (Strategy):**  
AI isn't perfect. We need to **know when to trust it** and when to review. Prevents bad data and builds trust in automation.

**Addresses:**  
✅ Accuracy  
✅ Efficiency  

---

### 5. **Cloud-Ready Packaging (Containerization - Docker)**

**What:**  
Write a `Dockerfile` to package the app and its dependencies. Ensure the app runs inside a Docker container.

**Why (Strategy):**  
Sets up for future **cloud deployment**. Simplifies local testing, operationalization, and shows readiness for production environments.

**Addresses:**  
✅ Scalability  
✅ Operationalization Readiness  

---

## Prioritization Rationale

1. **Database Storage** – foundational for persistent, scalable architecture  
2. **Batch Input** – adds scale and real-world processing capability  
3. **Change Detection** – unlocks automation value  
4. **Confidence/Validation** – ensures quality control  
5. **Containerization** – prepares for deployment and consistent runtime  

> This approach delivers incremental value while ensuring each new capability is built on a stable, production-oriented foundation.
