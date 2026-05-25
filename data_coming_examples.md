 Here are examples of what the data looks like in those rejected, real-world formats for each of the three
  sources:
  ### 1. SAP (Fuel & Procurement) - The Rejected "IDoc" XML Format
  Instead of a simple flat dictionary like  {"Menge": 500, "Einheit": "L"} , an SAP IDoc (Intermediate Document)
  is a deeply nested XML file used for system-to-system transfers. It contains hundreds of lines of metadata just
  to send a single transaction.
  Example of an SAP IDoc (XML):
      <EDI_DC40>
    <INV_IDOC>
        <TABNAM>EDI_DC40</TABNAM>
        <MANDT>100</MANDT>
        <DOCNUM>0000000000123456</DOCNUM>
        <SNDPRT>LS</SNDPRT>
        <SNDPRN>SAP_ERP</SNDPRN>
      </EDI_DC40>
      <E1EDK01>
        <CURCY>EUR</CURCY>
        <WKURS>1.00000</WKURS>
      <!-- The actual data is buried deep inside segments like this -->
      </E1EDK01>
      <E1EDP01>
        <POSEX>00010</POSEX>
        <MENGE>1500.50</MENGE> <!-- The Amount -->
        <MENEE>L</MENEE> <!-- The Unit -->
        <WERKS>P-01</WERKS> <!-- The Plant -->
      </E1EDP01>
    </INV_IDOC>
  Why it's hard: You have to write complex XML parsing logic to traverse the tree, and you have to know exactly
  which  E1EDP01  segment contains the fuel data versus standard office supplies.
  ──────
  ### 2. Utility Data (Electricity) - The Rejected "Raw PDF Bill" Format
  Instead of getting clean rows of data, extracting data from a PDF bill using OCR (Optical Character
  Recognition) gives you a messy, unstructured block of text where data is determined entirely by X/Y coordinates
  on a page.
  Example of scraped PDF Text:

    PG&E STATEMENT     ACCOUNT: 1234567890
    BILLING PERIOD: Jan 15 2023 - Feb 14 2023    DAYS: 30
    SERVICE ADDRESS: 123 Main St, Factory P-01
    METER   CURRENT READ   PREVIOUS READ   MULTIPLIER   USAGE
    A1B2    54321          49321           1.0          5,000 kWh

    CHARGES:
    Peak Summer Energy                 $540.20
    Off-Peak Summer Energy             $120.50
    Transmission Charge                $45.00
    ------------------------------------------
    TOTAL AMOUNT DUE                   $705.70
  Why it's hard: The parser has to use Regular Expressions (Regex) to hunt for the word "USAGE", look exactly two
  spaces to the right, strip out the comma in  5,000 , and ignore the dollar amounts entirely. If the utility
  company moves the "USAGE" column to the left side of the page next month, the entire parser breaks.
  ──────
  ### 3. Corporate Travel - The Rejected "Full Concur API" Format
  Instead of getting just the flight origin and destination, querying the Concur API for an expense report
  returns a massive JSON payload containing employee profiles, hotel stays, per-diem meals, and flight legs all
  mixed together.
  Example of a Concur Expense Report API Payload (JSON):

    {
      "ExpenseReport": {
        "ReportID": "RPT-987654321",
        "Employee": {
          "Name": "John Doe",
          "CostCenter": "Engineering"
        },
        "Expenses": [
          {
            "ExpenseType": "Meals",
            "Amount": 45.00,
            "Currency": "USD"
          },
          {
            "ExpenseType": "Airfare",
            "Amount": 450.00,
            "Currency": "USD",
            "AirTravelDetails": {
              "TicketNumber": "016123456789",
              "ClassOfService": "Economy",
              "Segments": [
                {
                  "SegmentNumber": 1,
                  "DepartureAirport": "SFO",
                  "ArrivalAirport": "ORD"
                },
                {
                  "SegmentNumber": 2,
                  "DepartureAirport": "ORD",
                  "ArrivalAirport": "JFK"
                }
              ]
            }
          }
        ]
      }
    }

  Why it's hard: You have to write logic to loop through the  Expenses  array, ignore anything that isn't        
  Airfare , and then dig into the nested  Segments  array to stitch together that the user flew from  SFO  ->    
  ORD  -
  >  JFK  and calculate the distance for both legs individually.