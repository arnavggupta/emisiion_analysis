# Data Source Research & Reality Check

This document outlines research notes on real-world SAP, Utility, and Travel data formats, justifying the fabricated sample data and identifying what would break in a real deployment.

## 1. SAP (Fuel & Procurement)
* **Real-world format:** SAP exports are often IDocs (XML-based) or flat files exported from ALV grids. Column headers are frequently localized based on the user's login language (e.g., German: `Menge`, `Einheit`, `Werk`).
* **Fabrication Justification:** The sample data uses a flattened JSON dictionary mimicking a parsed CSV row. We intentionally mixed German headers and English headers to simulate exports coming from different regional divisions of a multinational company.
* **What would break in reality:** Real SAP data often uses comma (`,`) as a decimal separator in European locales (e.g., `1.500,50` instead of `1500.50`). Our current parser assumes standard `float()` parsing which would fail on commas. A robust system requires locale-aware numeric parsing.

## 2. Utility Data (Electricity)
* **Real-world format:** Utilities often provide CSV portal exports or EDI (Electronic Data Interchange) formats like EDI 810. Billing periods are notorious for not aligning with calendar months, and tariffs are split into complex peak/off-peak/shoulder buckets.
* **Fabrication Justification:** We used simplified `peak_kwh` and `offpeak_kwh` fields. We intentionally included records with overlapping/suspiciously long billing periods (e.g., 90 days) to test the parser's anomaly detection logic.
* **What would break in reality:** Many utility bills don't provide just kWh; they provide Demand charges (kW) and reactive power (kVAR). Real-world parsers must also handle estimated vs. actual meter reads.

## 3. Corporate Travel (Navan / Concur)
* **Real-world format:** Concur exports are heavily denormalized flat files or API JSON payloads. Flights are often broken down by flight legs (segments), not just origin and final destination.
* **Fabrication Justification:** We mocked a simple Origin-Destination IATA pair. We included edge cases like lower-case IATA codes and unknown routes.
* **What would break in reality:** A direct SFO-JFK distance is easy to calculate, but a real Concur extract might list SFO-ORD and ORD-JFK as separate line items or combined. Real travel carbon calculation requires a massive external database (like Climatiq) to factor in aircraft type, radiative forcing index (RFI), and exact routing rather than a simple hardcoded distance dictionary.
