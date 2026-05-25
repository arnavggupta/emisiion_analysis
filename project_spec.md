# Project Specification: Enterprise Emissions Data Ingestion Prototype

## 1. Project Objective
Build a robust prototype for a B2B SaaS platform that ingests, normalizes, and allows analysts to review messy enterprise emissions and activity data before locking it for auditing. 

## 2. Tech Stack Requirements
* **Backend:** Django (REST Framework)
* **Frontend:** React
* **Database:** PostgreSQL (Recommended for multi-tenancy and audit tracking)
* **Deployment:** Must be fully deployable to Render, Railway, or a similar PaaS. Local-only builds are unacceptable.

## 3. Core Architectural Requirements (The Data Model)
The data model is the most critical component (35% of the evaluation). The schema MUST explicitly handle the following:
* **Multi-tenancy:** The system must support multiple client companies keeping their data entirely isolated.
* **Scope Categorization:** Every emissions record must be taggable as Scope 1, Scope 2, or Scope 3.
* **Source-of-Truth Tracking:** Every single row must track its origin (which source produced it, when it was ingested, and if/when it was edited by a human).
* **Unit Normalization Engine:** The system must ingest raw data with varying units (e.g., liters, gallons, kWh) and normalize them into a standard carbon computing unit.
* **Audit Trail:** An immutable log of all state changes for every record, particularly analyst approvals and rejections.

## 4. Ingestion Pipelines (The Three Sources)
The application must ingest data from three specific, realistic enterprise sources. **DO NOT use perfectly clean "toy" data.** The system must handle realistic edge cases, incomplete data, and mismatched formats.

### Source A: SAP (Fuel & Procurement)
* **Implementation Strategy:** Design an ingestion endpoint or file upload parser simulating a specific SAP export format (e.g., IDoc, OData, flat file).
* **Edge Cases to Handle:** Inconsistent units, German column headers, obscure date formats, and plant codes that require a relational lookup table to resolve.

### Source B: Utility Data (Electricity)
* **Implementation Strategy:** Design a parser for either a portal CSV export, a raw PDF bill, or a Utility API.
* **Edge Cases to Handle:** Meter readings with varying units, complex tariff structures, and billing periods that overlap across standard calendar months.

### Source C: Corporate Travel (Flights, Hotels, Ground)
* **Implementation Strategy:** Design an ingestion mechanism mimicking platforms like Concur or Navan.
* **Edge Cases to Handle:** Different emission factors based on travel category, and incomplete distance data (e.g., calculating distance solely from provided IATA airport codes).

## 5. Analyst Dashboard (Frontend UX)
The React frontend must provide a streamlined dashboard for a non-engineer data analyst. 
* **Review Queue:** Surface recently ingested rows.
* **Validation Highlighting:** Clearly mark what data successfully parsed, what failed ingestion, and what looks mathematically suspicious.
* **Approval Workflow:** Allow the analyst to edit rows, approve them, and permanently "lock" them for final auditing.

## 6. Required Documentation Generation
The CLI tool must generate the scaffolding for the following four Markdown files in the root directory. (Note to developer: The AI can scaffold these, but YOU must fill in the specific human logic).

* `MODEL.md`: Detailed explanation of the database schema, explicitly detailing how multi-tenancy, Scope 1/2/3, source tracking, and audit trails are handled.
* `DECISIONS.md`: A log of every architectural ambiguity resolved, what subset of each data source was handled vs. ignored, and questions for the Product Manager.
* `TRADEOFFS.md`: A list of exactly three specific features or edge cases deliberately NOT built into this prototype, and the engineering justification why.
* `SOURCES.md`: Detailed research notes on real-world SAP, Utility, and Travel data formats, justifying the fabricated sample data and identifying what would break in a real deployment.

## 7. Execution Directives for Autonomous Agent
1. Scaffold the Django backend and React frontend.
2. Define the core database models per Section 3.
3. Build the normalization utility functions.
4. Implement the three ingestion pipelines with the mandated edge cases.
5. Build the REST API endpoints to serve the analyst dashboard.
6. Build the React UI with a focus on clean, intuitive data tables and approval workflows.
7. Generate sample data scripts that intentionally include messy, realistic data (not perfectly clean rows).
8. Prepare the `Dockerfile` or configuration files required for immediate cloud deployment.