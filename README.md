# Portfolio Monitoring Dashboard

A full-stack portfolio monitoring dashboard for Portfolio Managers overseeing multiple investment funds. Built with Next.js FastAPI, featuring a PostgreSQL database containerized with Docker.

![dashboard screenshot](https://res.cloudinary.com/dwvlpyo5f/image/upload/v1756330848/Screenshot_2025-08-27_at_5.37.55_PM_bgwenx.png)

### Feature Set

- **Dashboard Overview**: Portfolio summary with real-time fund data, total AUM, current values, and performance metrics
- **Fund Detail Pages**: Complete fund information with holdings tables, performance charts, and peer comparisons
- **Live API Integration**: Frontend fetches and displays real data from FastAPI backend
- **Interactive Charts**: Performance trends and peer comparison visualizations using Recharts
- **Responsive Design**: Professional financial UI that works across desktop and mobile devices

## Technology Stack

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety throughout the application
- **Tailwind CSS** - Utility-first styling with custom design system
- **Shadcn/ui** - Modern, accessible UI components
- **Custom React Hooks** - Data fetching with loading/error states
- **Recharts** - Data visualization and charting

### Backend

- **FastAPI** - Modern Python web framework with async support
- **PostgreSQL** - Robust relational database for financial data
- **SQLAlchemy** - Async ORM with comprehensive relationship modeling
- **Pydantic** - Data validation and serialization
- **Uvicorn** - High-performance ASGI server

### DevOps & Infrastructure

- **Docker** - Database containerization
- **Docker Compose** - Container orchestration for development
- **PostgreSQL** - Containerized database with persistent volumes

## Project Structure

```
nb-portfolio-dashboard/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Configuration and database
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic layer
│   │   └── main.py         # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── app/           # App Router pages and layouts
│   │   ├── components/    # Reusable React components
│   │   ├── lib/          # Utilities and configurations
│   │   ├── stores/       # Zustand state management
│   │   ├── types/        # TypeScript definitions
│   │   └── hooks/        # Custom React hooks
│   ├── package.json      # Node.js dependencies
│   └── Dockerfile        # Frontend container configuration
├── database/             # Database schemas and migrations
│   ├── schema.sql        # PostgreSQL database schema
│   └── seed_data.sql     # Sample data for development
├── prompts/              # AI-assisted development documentation
├── docker-compose.yml    # Development orchestration
├── .env.example         # Environment variables template
```

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **Node.js 18+** and **npm**
- **Python 3.9+** and **pip**

### Step 1: Start Database

```bash
# Clone repository and start database container
gh repo clone Adamhunter108/nb-portfolio-dashboard
cd nb-portfolio-dashboard
docker-compose up -d postgres

# Verify container is running
docker ps
```

### Step 2: Start Backend API

```bash
# In Terminal 1: Setup and start FastAPI backend
cd backend
python3 -m venv venv
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API running at: http://localhost:8000
# Database automatically seeded with sample fund data on first run
```

### Step 3: Start Frontend

```bash
# In Terminal 2: Setup and start Next.js frontend
cd frontend
npm install
npm run dev

# Dashboard at: http://localhost:3000
```

### Access Your Portfolio Dashboard

- **Portfolio Dashboard**: http://localhost:3000 - Live fund data and interactive charts
- **API Documentation**: http://localhost:8000/docs - Interactive FastAPI docs
- **Health Check**: http://localhost:8000/health - Verify API is running

### 🛑 Stop Services

```bash
# Stop frontend: Ctrl+C in Terminal 2
# Stop backend: Ctrl+C in Terminal 1
# Stop database: docker-compose down
```

## 📝 AI-Assisted Development

This project was developed with AI assistance. All prompts and interactions are documented in the `prompts/` directory as requested in the assignment requirements.
