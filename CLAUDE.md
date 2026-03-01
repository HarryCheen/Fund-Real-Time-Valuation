# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fund Real-Time Valuation - A fund and financial market monitoring platform with real-time data push, multi-source aggregation, and caching optimization.

**Tech Stack**: Python 3.10+, FastAPI, Vue 3 + TypeScript, SQLite, akshare, yfinance

**Deployment**: Single-port deployment (FastAPI serves both frontend and backend)

## Common Commands

```bash
# Install dependencies
pnpm run install:all

# Start development server (single port 8000, serves both frontend and backend)
pnpm run dev

# Quick start (skip cache warmup)
uv run python run_app.py --fast --reload

# Frontend-only development (Vite, port 3000 with hot reload)
pnpm run dev:web

# Backend-only development (FastAPI, port 8000)
pnpm run dev:api

# Run tests
uv run pytest tests/ -v                              # All tests
uv run pytest tests/test_file.py::test_function -v  # Single test

# Lint and type check
uv run ruff check .           # Python lint
uv run ruff check --fix .     # Auto-fix
uv run mypy .                 # Python type check
cd web && pnpm run lint      # Frontend ESLint

# Build frontend
pnpm run build:web
```

## Architecture

```
api/           # FastAPI routes and application entry
  routes/      # API endpoint handlers
    funds.py         # 基金 API
    commodities.py   # 商品 API
    indices.py       # 指数 API
    sectors.py       # 板块 API
    stocks.py        # 股票 API
    bonds.py         # 债券 API
    holidays.py      # 节假日 API
    trading_calendar.py  # 交易日历
    websocket.py     # WebSocket 实时推送
    datasource.py    # 数据源管理
    cache.py         # 缓存管理
    overview.py      # 概览数据
    sentiment.py     # 舆情数据
src/
  datasources/ # Data fetchers - implements DataSource interface
    base.py           # 数据源基类
    manager.py        # 数据源管理器
    fund_source.py    # 基金数据源
    commodity_source.py # 商品数据源
    index_source.py   # 指数数据源
    sector_source.py  # 板块数据源
    stock_source.py   # 股票数据源
    bond_source.py    # 债券数据源
    trading_calendar_source.py  # 交易日历
    cache.py          # 缓存模块
    gateway.py        # 数据网关
    fund/             # 基银子模块
      cache_strategy.py
  db/          # SQLite database DAOs
  config/      # Configuration management
  utils/       # Utilities (websocket, colors, export)
web/           # Vue 3 + TypeScript frontend
tests/         # pytest test files
docs/          # Design documentation
```

### Data Source Pattern

All data sources follow this pattern:

```python
class MyDataSource(DataSource):
    async def fetch(self, *args) -> DataSourceResult:
        try:
            data = await self._fetch(...)
            return DataSourceResult(success=True, data=data, source=self.name)
        except Exception as e:
            logger.warning(f"Fetch failed: {e}")
            return DataSourceResult(success=False, error=str(e))
```

### Key Entry Points

- `run_app.py` - Application entry point; starts FastAPI server and serves frontend
- `api/main.py` - FastAPI application instance
- `src/datasources/manager.py` - DataSourceManager orchestrates all data sources

## Configuration

Configuration files located in `~/.fund-tui/`:

- `config.yaml` - Application settings
- `funds.yaml` - Watchlist funds
- `fund_data.db` - SQLite database

## API Endpoints

### Funds

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/funds` | GET | Fund list |
| `/api/funds/{code}` | GET | Fund detail |
| `/api/funds/{code}/estimate` | GET | Fund valuation |
| `/api/funds/{code}/history` | GET | Fund history net values |
| `/api/funds/{code}/intraday` | GET | Fund intraday data |
| `/api/funds/{code}/intraday/{date}` | GET | Fund intraday by date |
| `/api/funds/watchlist` | GET/POST | Watchlist management |
| `/api/funds/watchlist/{code}` | DELETE | Remove from watchlist |
| `/api/funds/{code}/holding` | PUT | Toggle holding status |

### Bonds

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/bonds` | GET | Bond list |
| `/api/bonds/{code}` | GET | Bond detail |
| `/api/bonds/search/cbonds` | GET | Search convertible bonds |

### Stocks

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stocks` | GET | Stock quotes (batch) |
| `/api/stocks/{code}` | GET | Single stock quote |

### Commodities

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/commodities` | GET | Commodity prices |
| `/api/commodities/watchlist` | GET/POST/DELETE | Watchlist management |

### Indices & Sectors

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/indices` | GET | Global market indices |
| `/api/sectors` | GET | Industry sectors |

### News & Sentiment

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/news` | GET | Financial news |
| `/api/sentiment` | GET | Market sentiment |

### Holidays & Trading Calendar

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/holidays` | GET | Holiday list |
| `/api/holidays/{market}` | GET | Market holidays |
| `/trading-calendar/is-trading-day/{market}` | GET | Trading status |
| `/trading-calendar/calendar/{market}` | GET | Annual calendar |
| `/trading-calendar/next-trading-day/{market}` | GET | Next trading day |
| `/trading-calendar/market-status` | GET | Multi-market status |

### Cache & DataSource

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cache/stats` | GET | Cache statistics |
| `/api/datasource/statistics` | GET | DataSource statistics |
| `/api/datasource/health` | GET | DataSource health |
| `/api/datasource/sources` | GET | Registered sources |

### Health Check

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/simple` | GET | Simple health check |
| `/api/health` | GET | Detailed health check |

### WebSocket

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ws/realtime` | WebSocket | Real-time data push |
| `/ws/manager/status` | GET | WS connection status |
| `/ws/manager/broadcast` | POST | Broadcast message |

## Testing

- Test files: `tests/test_*.py`
- Use fixtures from `conftest.py`
- Async tests: `@pytest.mark.asyncio`
- Naming convention: `test_<method_name>`

## Frontend Development

For frontend-only development with hot reload:

```bash
# Terminal 1: Start backend
pnpm run dev:api

# Terminal 2: Start frontend
pnpm run dev:web
```

Frontend runs on http://localhost:3000, API requests proxied to backend.

## Code Style

### Python
- Import order: stdlib → third-party → local (absolute imports)
- Line length: 100 characters
- Type hints: Python 3.10+ style (`str | None` not `Optional[str]`)
- No bare `except:`, return `DataSourceResult(success=False, error=...)` on failure

### TypeScript/Vue
- Absolute imports: `@/components/...`
- Composition API + `<script setup>`
- TypeScript strict mode
- No `as any`, `@ts-ignore`, or `@ts-expect-error`

### Responsive Design Breakpoints

Defined in `web/src/styles/global.scss`:

```scss
--breakpoint-xs: 480px;
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
```

Use desktop-first approach with `max-width` media queries.

## Notes

- mypy ignores type stubs for: akshare, yfinance, matplotlib, pandas, numpy
- src/datasources module has relaxed mypy rules due to dynamic data structures
