For this prototype, I chose to ingest all three sources as Flat JSON Dictionaries (which simulates a parsed CSV
  file or a flattened API payload).
  Here is exactly which formats I chose for each source based on the spec, why I chose them, and why I rejected
  the alternatives:
  ### 1. SAP (Fuel & Procurement)

  • What I Chose: Flat file / CSV equivalent.
  • Why: In enterprise environments, legacy systems are frequently set up to drop nightly CSV exports onto an
  SFTP server. It is a highly realistic scenario.
  • What I Rejected (IDoc & OData): SAP IDocs are incredibly massive, complex XML files with deep hierarchies
  that take days just to map. An OData API requires mocking active network connections and authentication.
  Rejecting these allowed me to focus on the actual data edge cases (like translating the German headers  Menge 
  and  Einheit ) rather than building an enterprise XML parser.
  ### 2. Utility Data (Electricity)

  • What I Chose: Portal CSV Export.
  • Why: Simulating a CSV download from a provider like PG&E or Duke Energy is the most common way analysts
  manually deal with utility data today. It allowed me to instantly access the  peak_kwh  and  period_start 
  dates.
  • What I Rejected (PDF Bills & APIs): I completely rejected parsing raw PDF bills. PDF parsing (using OCR) is
  notoriously brittle and breaks the second the utility company changes their font or layout. Building a reliable
  PDF parser is a project of its own and would have distracted from building the core emissions logic.
  ### 3. Corporate Travel (Concur/Navan)

  • What I Chose: Simplified API JSON Payload.
  • Why: I used a flat JSON payload representing a single flight segment (Origin, Destination, Travel Class).
  • What I Rejected (Full Concur API Payload): Real Concur API payloads are deeply nested with traveler profiles,
  expense report IDs, hotel folios, and meal receipts. I rejected using a fully nested expense report because our
  goal was strictly carbon calculation. Flattening it down to just the flight segment allowed the prototype to
  immediately calculate distance from the IATA airport codes without getting bogged down in expense management
  data structures.
