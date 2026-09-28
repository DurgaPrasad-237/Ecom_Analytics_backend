                    ┌──────────────────────────────┐
                    │          USER                │
                    │                              │
                    │  Dashboard / Chat Question   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │         STREAMLIT             │
                    │                              │
                    │  ┌────────────────────────┐  │
                    │  │ Customer               │  │
                    │  │ Orders                 │  │
                    │  │ Shipments              │  │
                    │  │ Payments               │  │
                    │  │ Ratings                │  │
                    │  │ Order Items            │  │
                    │  └────────────────────────┘  │
                    │                              │
                    │        Chat UI Component      │
                    └──────────────┬───────────────┘
                                   │
                         HTTP / API Requests
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │          FASTAPI              │
                    │                              │
                    │   Customer API                │
                    │   Orders API                  │
                    │   Shipments API               │
                    │   Payments API                │
                    │   Ratings API                 │
                    │   Order Items API             │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
          ┌───────────────────┐          ┌────────────────────┐
          │ Analytics Layer   │          │   AI Agent Layer   │
          │                   │          │                    │
          │ analysis.py       │          │ Customer Agent     │
          │ visualization.py  │          │ Orders Agent       │
          │ data_loader.py    │          │ Payments Agent     │
          │                   │          │ etc.               │
          └─────────┬─────────┘          └─────────┬──────────┘
                    │                              │
                    │                              ▼
                    │                    ┌──────────────────┐
                    │                    │      Gemini      │
                    │                    │       LLM        │
                    │                    └────────┬─────────┘
                    │                             │
                    │                       Tool Selection
                    │                             │
                    │                             ▼
                    │                    ┌──────────────────┐
                    │                    │   AI Tools       │
                    │                    │                  │
                    │                    │ monthly_signup() │
                    │                    │ signup_gender()  │
                    │                    │ churn()          │
                    │                    │ etc.             │
                    │                    └────────┬─────────┘
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │        DATA LAYER             │
                    │                              │
                    │ Processed CSV / MySQL        │
                    │                              │
                    │ customers_processed.csv      │
                    │ orders_processed.csv         │
                    │ shipments_processed.csv      │
                    │ payments_processed.csv       │
                    │ ratings_processed.csv        │
                    │ order_items_processed.csv    │
                    └──────────────────────────────┘