# Prompt 5: AsyncPG Dependency

**User Request:**
```
I also noticed we are referencing asyncpg in the backend/app/core/database.py code. let's make sure that dependency is included in backend/requirements.txt (add asyncpg==0.30.0) so the postgresql+asyncpg driver and imports resolve
```

**Context:** User identified missing asyncpg dependency that's required for the PostgreSQL async driver used in the database configuration.

**Assistant Response:** Added asyncpg==0.30.0 to requirements.txt to ensure the postgresql+asyncpg database URL scheme works properly with SQLAlchemy async operations.

**Outcome:** Resolved missing dependency for async PostgreSQL operations.