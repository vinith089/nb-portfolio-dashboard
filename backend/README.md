# Portfolio Monitoring Dashboard - Backend API

A FastAPI backend service for managing investment funds, holdings, and stock price data for portfolio monitoring and analysis.

## Tech Stack

- **Framework**: FastAPI 0.116.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.36 (async)
- **Validation**: Pydantic 2.10.4

## Getting Started

### Prerequisites

- Python 3.9+
- Virtual environment
- Docker and Docker Compose (for database)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Interactive API documentation is available at `http://localhost:8000/docs`

## API Endpoints

### Fund Management Endpoints

Base path: `/api/v1/funds`

| Method   | Path                     | Description                            |
| -------- | ------------------------ | -------------------------------------- |
| `GET`    | `/`                      | List all funds with optional filtering |
| `GET`    | `/{fund_id}`             | Get specific fund details by ID        |
| `POST`   | `/`                      | Create a new fund                      |
| `PUT`    | `/{fund_id}`             | Update an existing fund                |
| `DELETE` | `/{fund_id}`             | Delete a fund                          |
| `GET`    | `/{fund_id}/performance` | Get fund performance data              |
| `GET`    | `/{fund_id}/peers`       | Get peer comparison data               |
| `GET`    | `/{fund_id}/stats`       | Get fund statistics and metrics        |

#### Fund Endpoints Details

##### `GET /api/v1/funds/`

List all funds with pagination and optional filtering.

**Query Parameters:**

- `skip` (int, default: 0) - Number of funds to skip for pagination
- `limit` (int, default: 100, max: 1000) - Number of funds to return
- `search` (string, optional) - Search funds by name or manager name

**Response:** Array of Fund objects with summary information

**Example:**

```bash
curl "http://localhost:8000/api/v1/funds/?search=Tech&limit=10"
```

##### `GET /api/v1/funds/{fund_id}`

Retrieve detailed information for a specific fund.

**Path Parameters:**

- `fund_id` (int, required) - Unique fund identifier

**Response:** Complete Fund object with detailed information

**Example:**

```bash
curl "http://localhost:8000/api/v1/funds/1"
```

##### `POST /api/v1/funds/`

Create a new investment fund.

**Request Body:** FundCreate schema

```json
{
  "name": "Tech Innovation Fund",
  "strategy": "growth",
  "inception_date": "2024-01-15",
  "manager_name": "John Smith",
  "expense_ratio": 0.0075,
  "description": "Focused on innovative technology companies",
  "total_aum": 10000000.0
}
```

**Response:** Created Fund object with ID and timestamps

##### `PUT /api/v1/funds/{fund_id}`

Update an existing fund's information.

**Path Parameters:**

- `fund_id` (int, required) - Fund ID to update

**Request Body:** FundUpdate schema (partial update)

```json
{
  "name": "Updated Fund Name",
  "description": "Updated description"
}
```

**Response:** Updated Fund object

##### `DELETE /api/v1/funds/{fund_id}`

Delete a fund and all associated data.

**Path Parameters:**

- `fund_id` (int, required) - Fund ID to delete

**Response:** HTTP 204 No Content on success

##### `GET /api/v1/funds/{fund_id}/performance`

Get historical performance data for a fund.

**Path Parameters:**

- `fund_id` (int, required) - Fund ID

**Query Parameters:**

- `days` (int, default: 30, max: 365) - Number of days of performance data to return

**Response:** FundPerformanceResponse with historical NAV and return data

##### `GET /api/v1/funds/{fund_id}/peers`

Get peer comparison data for benchmarking analysis.

**Path Parameters:**

- `fund_id` (int, required) - Fund ID

**Response:** PeerComparisonResponse with similar funds for comparison

##### `GET /api/v1/funds/{fund_id}/stats`

Get comprehensive statistics and metrics for a fund.

**Path Parameters:**

- `fund_id` (int, required) - Fund ID

**Response:** Dictionary with fund statistics including AUM, holdings count, cost basis, etc.

### Holdings Management Endpoints

Base path: `/api/v1/holdings`

| Method   | Path                      | Description                               |
| -------- | ------------------------- | ----------------------------------------- |
| `GET`    | `/`                       | List all holdings with optional filtering |
| `GET`    | `/{holding_id}`           | Get specific holding details by ID        |
| `POST`   | `/`                       | Create a new holding                      |
| `PUT`    | `/{holding_id}`           | Update an existing holding                |
| `DELETE` | `/{holding_id}`           | Delete a holding                          |
| `GET`    | `/fund/{fund_id}/summary` | Get holdings summary for a fund           |
| `GET`    | `/fund/{fund_id}/sectors` | Get sector breakdown for fund holdings    |
| `GET`    | `/fund/{fund_id}/top`     | Get top holdings by value for a fund      |

#### Holdings Endpoints Details

##### `GET /api/v1/holdings/`

List holdings with optional filtering capabilities.

**Query Parameters:**

- `skip` (int, default: 0) - Number of holdings to skip
- `limit` (int, default: 100, max: 1000) - Number of holdings to return
- `ticker` (string, optional) - Filter by specific ticker symbol
- `fund_id` (int, optional) - Filter by specific fund
- `search` (string, optional) - Search by ticker or company name

**Response:** Array of Holding objects

##### `GET /api/v1/holdings/{holding_id}`

Get detailed information for a specific holding.

**Path Parameters:**

- `holding_id` (int, required) - Holding identifier

**Response:** Complete Holding object with calculated metrics

##### `POST /api/v1/holdings/`

Create a new holding within a fund.

**Request Body:** HoldingCreate schema

```json
{
  "fund_id": 1,
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "shares": 1000.0,
  "purchase_price": 150.25,
  "purchase_date": "2024-01-15",
  "sector": "Technology",
  "market_cap": 3000000000000
}
```

**Response:** Created Holding object

##### `PUT /api/v1/holdings/{holding_id}`

Update an existing holding's information.

**Request Body:** HoldingUpdate schema (partial updates)

```json
{
  "shares": 1200.0,
  "sector": "Information Technology"
}
```

##### `DELETE /api/v1/holdings/{holding_id}`

Remove a holding from a fund.

**Response:** HTTP 204 No Content on success

##### `GET /api/v1/holdings/fund/{fund_id}/summary`

Get summary statistics for all holdings in a fund.

**Response:** Summary object with total holdings, cost basis, unique tickers, and sectors

##### `GET /api/v1/holdings/fund/{fund_id}/sectors`

Get sector breakdown showing allocation across different industry sectors.

**Response:** Array of sector objects with counts and total values

##### `GET /api/v1/holdings/fund/{fund_id}/top`

Get the largest positions in a fund by market value.

**Query Parameters:**

- `limit` (int, default: 10, max: 50) - Number of top holdings to return

**Response:** Array of top Holding objects ordered by value

### Stock Prices Management Endpoints

Base path: `/api/v1/stock-prices`

| Method   | Path                       | Description                               |
| -------- | -------------------------- | ----------------------------------------- |
| `GET`    | `/`                        | List stock prices with optional filtering |
| `GET`    | `/tickers`                 | Get list of all available ticker symbols  |
| `GET`    | `/{price_id}`              | Get specific stock price record by ID     |
| `POST`   | `/`                        | Create a new stock price record           |
| `PUT`    | `/{price_id}`              | Update an existing stock price record     |
| `DELETE` | `/{price_id}`              | Delete a stock price record               |
| `GET`    | `/ticker/{ticker}/latest`  | Get latest price for a ticker             |
| `GET`    | `/ticker/{ticker}/history` | Get price history for a ticker            |
| `GET`    | `/ticker/{ticker}/summary` | Get price statistics for a ticker         |
| `POST`   | `/batch/latest`            | Get latest prices for multiple tickers    |

#### Stock Prices Endpoints Details

##### `GET /api/v1/stock-prices/`

List stock price records with filtering options.

**Query Parameters:**

- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100, max: 1000) - Number of records to return
- `ticker` (string, optional) - Filter by ticker symbol
- `start_date` (date, optional) - Filter from this date
- `end_date` (date, optional) - Filter to this date

**Response:** Array of StockPrice objects

##### `GET /api/v1/stock-prices/tickers`

Get a list of all ticker symbols available in the system.

**Response:** Array of ticker strings

##### `GET /api/v1/stock-prices/{price_id}`

Get a specific stock price record.

**Path Parameters:**

- `price_id` (int, required) - Price record identifier

**Response:** StockPrice object

##### `POST /api/v1/stock-prices/`

Add a new stock price data point.

**Request Body:** StockPriceCreate schema

```json
{
  "ticker": "AAPL",
  "date": "2024-01-15",
  "open_price": 150.0,
  "high_price": 152.5,
  "low_price": 149.75,
  "close_price": 151.2,
  "volume": 45000000,
  "adjusted_close": 151.2
}
```

**Response:** Created StockPrice object

##### `PUT /api/v1/stock-prices/{price_id}`

Update an existing stock price record.

**Request Body:** StockPriceUpdate schema (partial updates)

##### `DELETE /api/v1/stock-prices/{price_id}`

Remove a stock price record.

**Response:** HTTP 204 No Content on success

##### `GET /api/v1/stock-prices/ticker/{ticker}/latest`

Get the most recent price data for a ticker.

**Path Parameters:**

- `ticker` (string, required) - Stock ticker symbol

**Response:** Latest StockPrice object for the ticker

##### `GET /api/v1/stock-prices/ticker/{ticker}/history`

Get historical price data for analysis.

**Path Parameters:**

- `ticker` (string, required) - Stock ticker symbol

**Query Parameters:**

- `days` (int, default: 30, max: 365) - Number of days of history

**Response:** StockPriceHistory object with array of price data

##### `GET /api/v1/stock-prices/ticker/{ticker}/summary`

Get statistical summary for a ticker over a time period.

**Query Parameters:**

- `days` (int, default: 30, max: 365) - Period for calculations

**Response:** Summary object with min/max/average prices, total volume, and period returns

##### `POST /api/v1/stock-prices/batch/latest`

Get latest prices for multiple tickers in a single request.

**Request Body:** Array of ticker strings (max 100)

```json
["AAPL", "GOOGL", "MSFT", "TSLA"]
```

**Response:** Array of latest StockPrice objects

## Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `201` - Created
- `204` - No Content (successful deletion)
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `422` - Unprocessable Entity (validation errors)
- `500` - Internal Server Error

Error responses include descriptive messages:

```json
{
  "detail": "Fund with id 999 not found"
}
```

## Database Schema

The system uses a PostgreSQL database with the following tables and columns:

### funds

Investment fund information and metadata.

| Column           | Type                | Constraints                 | Description                                      |
| ---------------- | ------------------- | --------------------------- | ------------------------------------------------ |
| `id`             | Integer             | Primary Key, Index          | Unique fund identifier                           |
| `name`           | String(255)         | Not Null, Unique, Index     | Fund name                                        |
| `strategy`       | Enum(fund_strategy) | Not Null                    | Investment strategy (growth, value, blend, etc.) |
| `inception_date` | Date                | Not Null                    | Fund inception date                              |
| `total_aum`      | Numeric(15,2)       | Not Null, Default: 0.00     | Total assets under management                    |
| `manager_name`   | String(255)         | Nullable                    | Fund manager name                                |
| `expense_ratio`  | Numeric(5,4)        | Default: 0.0000             | Annual expense ratio as decimal                  |
| `description`    | Text                | Nullable                    | Fund description                                 |
| `created_at`     | DateTime            | Default: now()              | Record creation timestamp                        |
| `updated_at`     | DateTime            | Default: now(), Auto-update | Record update timestamp                          |

### holdings

Individual stock positions within investment funds.

| Column           | Type          | Constraints                  | Description                          |
| ---------------- | ------------- | ---------------------------- | ------------------------------------ |
| `id`             | Integer       | Primary Key, Index           | Unique holding identifier            |
| `fund_id`        | Integer       | Foreign Key, Not Null, Index | References funds.id (CASCADE DELETE) |
| `ticker`         | String(10)    | Not Null, Index              | Stock ticker symbol                  |
| `company_name`   | String(255)   | Nullable                     | Company name                         |
| `shares`         | Numeric(15,4) | Not Null                     | Number of shares owned               |
| `purchase_price` | Numeric(10,4) | Not Null                     | Purchase price per share             |
| `purchase_date`  | Date          | Not Null                     | Date of purchase                     |
| `sector`         | String(100)   | Nullable                     | Industry sector                      |
| `market_cap`     | BigInteger    | Nullable                     | Market capitalization                |
| `created_at`     | DateTime      | Default: now()               | Record creation timestamp            |
| `updated_at`     | DateTime      | Default: now(), Auto-update  | Record update timestamp              |

### stock_prices

Historical and current stock price data for market analysis.

| Column           | Type          | Constraints        | Description                    |
| ---------------- | ------------- | ------------------ | ------------------------------ |
| `id`             | Integer       | Primary Key, Index | Unique price record identifier |
| `ticker`         | String(10)    | Not Null, Index    | Stock ticker symbol            |
| `date`           | Date          | Not Null, Index    | Price date                     |
| `open_price`     | Numeric(10,4) | Not Null, > 0      | Opening price                  |
| `high_price`     | Numeric(10,4) | Not Null, > 0      | High price of the day          |
| `low_price`      | Numeric(10,4) | Not Null, > 0      | Low price of the day           |
| `close_price`    | Numeric(10,4) | Not Null, > 0      | Closing price                  |
| `volume`         | BigInteger    | Not Null, >= 0     | Trading volume                 |
| `adjusted_close` | Numeric(10,4) | Nullable, > 0      | Adjusted closing price         |
| `created_at`     | DateTime      | Default: now()     | Record creation timestamp      |

### fund_performance

Historical fund performance metrics and NAV data.

| Column                    | Type          | Constraints                  | Description                          |
| ------------------------- | ------------- | ---------------------------- | ------------------------------------ |
| `id`                      | Integer       | Primary Key, Index           | Unique performance record identifier |
| `fund_id`                 | Integer       | Foreign Key, Not Null, Index | References funds.id (CASCADE DELETE) |
| `date`                    | Date          | Not Null, Index              | Performance date                     |
| `nav_price`               | Numeric(10,4) | Not Null, > 0                | Net Asset Value price                |
| `total_return`            | Numeric(8,4)  | Nullable                     | Total return percentage              |
| `daily_return`            | Numeric(8,4)  | Nullable                     | Daily return percentage              |
| `assets_under_management` | Numeric(15,2) | Nullable, >= 0               | AUM for this date                    |
| `shares_outstanding`      | BigInteger    | Nullable, >= 0               | Shares outstanding                   |
| `created_at`              | DateTime      | Default: now()               | Record creation timestamp            |

### peer_funds

Benchmark and competitor fund data for performance comparison.

| Column               | Type                | Constraints        | Description                   |
| -------------------- | ------------------- | ------------------ | ----------------------------- |
| `id`                 | Integer             | Primary Key, Index | Unique peer fund identifier   |
| `name`               | String(255)         | Not Null           | Peer fund name                |
| `benchmark_category` | Enum(peer_category) | Not Null, Index    | Benchmark category            |
| `total_aum`          | Numeric(15,2)       | Nullable           | Total assets under management |
| `expense_ratio`      | Numeric(5,4)        | Nullable           | Annual expense ratio          |
| `inception_date`     | Date                | Nullable           | Fund inception date           |
| `manager_company`    | String(255)         | Nullable           | Management company name       |
| `description`        | Text                | Nullable           | Fund description              |
| `created_at`         | DateTime            | Default: now()     | Record creation timestamp     |

### Enumerations

#### fund_strategy

Investment strategy types used in the `funds` table:

- `growth` - Growth-focused investments
- `value` - Value-oriented investments
- `blend` - Balanced growth and value approach
- `income` - Income-generating investments
- `sector_specific` - Sector-focused strategies
- `international` - International market exposure
- `emerging_markets` - Emerging markets focus

#### peer_category

Benchmark categories used in the `peer_funds` table:

- `large_cap_growth`, `large_cap_value` - Large cap strategies
- `mid_cap_growth`, `mid_cap_value` - Mid cap strategies
- `small_cap_growth`, `small_cap_value` - Small cap strategies
- `international_developed` - International developed markets
- `emerging_markets` - Emerging markets
- `sector_technology`, `sector_healthcare`, `sector_financial` - Sector-specific

## API Documentation

Interactive API documentation is automatically generated and available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
