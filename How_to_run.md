# Getting Started
### 1. Clone the repository:

Open the folder you want to clone
```bash
git clone https://github.com/kashish-gulati-python/ai-assistant.git4
```

## A. Run the project locally

### 2. Move to ./backend

Open the project in VS Code
Open Git bash terminal in VS Code
```bash
cd backend
python -m venv venv
```

### 3. Install uv

```bash
pip install uv
```
This will create a .venv folder in ./backend. This file is your environment that you will be using to run the project in local

### 4. Activate virtual environment

```bash
source venv/Scripts/activate
```

### 4. Sync uv

```bash
uv Sync
```

### 5. Create a new .env file in ai-assistant/backend with below content

```
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/ai-assistant-db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=ai-assistant-db
```
Press Ctlr + S to save the file content

### 6. Run the backend

```
uvicorn app.main:app --reload
```
It must give following output in the terminal when you are running locally:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [29112] using WatchFiles
postgresql+psycopg://postgres:password@localhost:5432/ai-assistant-db
INFO:     Started server process [15644]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:65411 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:65411 - "GET /openapi.json HTTP/1.1" 200 OK
```
Press Ctrl + C in the terminal to stop the FastAPI reloader process

### 7. Run the APIs

Now go to http://localhost:8000/docs in your browser and check the APIs using "Try it Out" button
You can check the Postgres table to see if it's getting updated using pgadmin (Only for local run)

## B. Run the project in Docker

### 1. Run Docker Desktop

Open Docker Desktop in Windows and keep it running on background

### 2. Setup Docker compose

In your project terminal in VS Code, run following command for the first time:
```bash
docker compose up --build
```
When you want to run next time, no need to use `--build`, simply use:
```bash
docker compose up
```
Go to Step 7 in "Run the project locally" above.

----------------------------------------------------

If any error, try to use ChatGPT or Whatsapp in the group.