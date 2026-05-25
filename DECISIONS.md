# Architectural Decisions Log

This log captures the architectural ambiguities resolved during the prototyping of the BreatheSG application.

## 1. Local Database Strategy vs Production
* **Context:** The specification highly recommended PostgreSQL. However, during local development execution, Docker daemon was unavailable.
* **Decision:** We use SQLite for local development (configured via Django's default settings fallbacks in the event of missing Docker) but ensure all schema choices and code use standard ORM structures compatible with Postgres.
* **Question for PM:** For staging environments, do we want to force Postgres immediately, or is SQLite sufficient for the earliest non-production previews?

## 2. API Design & Frontend Integration
* **Context:** We needed a way to display records, highlight errors, and allow the analyst to edit and lock them.
* **Decision:** We used Django REST Framework (`djangorestframework`) to build an API. The frontend is fully decoupled using React (Vite) and fetches data over HTTP. 

## 3. Scope of Data Handled vs Ignored
* **SAP Data:** We explicitly handle fuel amounts and handle German translation mapping (`Menge` -> Amount, `Einheit` -> Unit). We ignore complex hierarchical plant structures and use a simple flat lookup dict for `Werk` codes.
* **Utility Data:** We handle peak/off-peak sum calculations. We flag overlapping or abnormal billing periods (e.g., >35 days) as suspicious but do not attempt to prorate them across months in this prototype.
* **Corporate Travel:** We mock an IATA distance calculator for specific airport pairs. We ignore layovers, exact aircraft models, and non-air travel (e.g. hotel stays) for this prototype.

## 4. Frontend Styling Strategy
* **Decision:** Used Vanilla CSS with modern aesthetics (glassmorphism, radial gradients) as instructed to avoid Tailwind unless explicitly requested. This gives maximum flexibility and a premium feel.
