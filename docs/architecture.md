# Architecture

```mermaid
flowchart LR
    U[CSV or Excel upload] --> L[data_loader]
    L --> C[data_cleaning]
    C --> P[data_profiling]
    C --> E[EDA and KPIs]
    C --> D[SQLAlchemy / MySQL]
    Q[Business question] --> G[SQL generator]
    G --> V[Read-only validator]
    V --> D
    D --> A[Grounded explanation]
    E --> I[Insight engine]
    I --> R[Markdown/PDF report]
```

The LLM is an optional interpretation layer. Numeric findings are computed by Python or validated SQL before explanation. SQL mutation is blocked by the validator and database access is intended to use a read-only MySQL account.
