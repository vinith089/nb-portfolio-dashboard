# Prompt 9: Backend Local Testing

**User Request:**

```
user pastes errors from terminal outlining docker errors
```

**User Context:**
User tried to test the backend locally by:

1. Starting the database with docker-compose.dev.yml
2. Attempting to curl the backend at localhost:8000 (not running)
3. Trying to start the backend with uvicorn but it's not installed in venv

**Issue:** Backend not running locally and uvicorn not available.

**Assistant Response:** Install the minimal backend requirements locally and start the FastAPI development server to test API connectivity.

**Outcome:** Get the backend running locally for API testing with the containerized database.
