# MySQL Setup

This is optional. The Streamlit app uses SQLite locally when no MySQL settings are provided.

## Configure MySQL

Install MySQL Server locally or use an existing MySQL instance. Create the `ai_analyst` database and a user with access to it. Copy `.env.example` to `.env` and set:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=ai_analyst
MYSQL_USER=ai_analyst
MYSQL_PASSWORD=ai_analyst_local
```

The application does not require MySQL for local use. If these variables are absent, it uses a local SQLite database automatically.

## Prepare and load data

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/prepare_dataset.py
python scripts/load_mysql.py
```

For production, replace the example password, use a secret manager, and grant the analyst account only `SELECT` privileges after loading the table. Do not expose port 3306 publicly.
