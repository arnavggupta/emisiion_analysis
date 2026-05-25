# Engineering Tradeoffs

This document lists three specific features or edge cases deliberately NOT built into this prototype, and the engineering justification.

## 1. Real-Time Emissions Factor API Integration
* **Tradeoff:** Instead of querying an external database like Climatiq or the EPA for up-to-date emissions factors, we hardcoded a static `EMISSION_FACTORS` dictionary.
* **Justification:** External APIs introduce latency, rate limits, and require secret management. For a prototype focused on *ingestion workflows* and *analyst approval UX*, a static mock provides deterministic results, faster local development, and removes a point of failure during demos.

## 2. Advanced User Authentication & Role-Based Access Control (RBAC)
* **Tradeoff:** The API endpoints and the React frontend do not implement JWT/Session authentication. There is no concept of an "Admin" vs "Analyst" user login flow.
* **Justification:** Building secure auth flows is time-consuming and generic. The core unique value proposition of this prototype is the data normalization and audit workflow. We assume the user is a trusted analyst (`changed_by` defaults to "Analyst") to focus engineering effort on the core data model.

## 3. Prorating Overlapping Utility Bills
* **Tradeoff:** When a utility bill spans across two calendar months (e.g. Jan 15 - Feb 14), we simply flag it if it's longer than 35 days. We do *not* split the emissions proportionally between January and February.
* **Justification:** Prorating requires complex date math and assumptions about daily consumption consistency (which is rarely true due to weekends/holidays). For V1, simply highlighting the anomaly for the human analyst to review is a safer approach than opaque, automatic mathematical splitting.
