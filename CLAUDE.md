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
  routes/      # API endpoint handlers (funds, commodities, indices, sectors, etc.)
src/
  datasources/ # Data fetchers (akshare, yfinance, etc.) - implements DataSource interface
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

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/funds` | GET | Fund list |
| `/api/funds/{code}/estimate` | GET | Fund valuation |
| `/api/commodities` | GET | Commodity prices |
| `/api/indices` | GET | Global market indices |
| `/api/sectors` | GET | Industry sectors |
| `/api/stocks` | GET | Stock quotes |
| `/api/bonds` | GET | Bond yields |
| `/api/news` | GET | Financial news |
| `/api/sentiment` | GET | Market sentiment |
| `/trading-calendar/is-trading-day/{market}` | GET | Trading status |
| `/api/ws` | WebSocket | Real-time data push |

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
