# AGENTS.md

**Generated:** 2026-02-04
**Module:** tests - Test Suite

## OVERVIEW

pytest test suite for datasources, database, API, and utility components.

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Test fixtures | `conftest.py` | Path setup, common fixtures |
| Datasource tests | `test_datasources.py` | Data source tests |
| Database tests | `test_database.py` | SQLite CRUD tests |
| Manager tests | `test_manager.py` | Data source manager tests |
| Gateway tests | `test_gateway.py`, `test_gateway_models.py` | Data gateway tests |
| Hot backup tests | `test_hot_backup.py` | Hot backup tests |
| Health tests | `test_datasource_health.py` | Health check tests |
| Cache tests | `test_cache.py`, `test_dual_cache.py`, `test_cache_strategy.py` | Caching tests |
| Cache cleaner tests | `test_cache_cleaner.py` | Cache cleanup tests |
| Cache warmer tests | `test_cache_warmer.py` | Cache preload tests |
| Fund tests | `test_qdii_fund.py` | QDII fund tests |
| Bond tests | `test_bond_source.py` | Bond source tests |
| Stock tests | `test_stock_source.py` | Stock source tests |
| Index tests | `test_index_source.py` | Index source tests |
| Commodity tests | `test_akshare_commodity.py`, `test_commodity_repo.py` | Commodity tests |
| Sector tests | `test_akshare_sector.py` | Sector tests |
| Sentiment tests | `test_akshare_sentiment.py` | Sentiment tests |
| Calendar tests | `test_trading_calendar.py` | Trading calendar tests |
| Config tests | `test_config.py`, `test_commodities_config.py` | Configuration tests |
| API tests | `test_api_models.py`, `test_api_routes.py` | API tests |
| Utility tests | `test_colors.py`, `test_export.py`, `test_log_buffer.py` | Utility tests |
| Unified models tests | `test_unified_models.py` | Unified models tests |
| Circuit breaker tests | `test_circuit_breaker.py` | Circuit breaker tests |
| Aggregator tests | `test_aggregator.py` | Aggregator tests |
| Datasource base tests | `test_datasource_base.py` | Base class tests |

## CONVENTIONS

### Test Structure
- `tests/test_*.py` naming
- Use `pytest` for testing
- Class-based test groups: `class TestClassName:`

### Path Setup
- `conftest.py` sets up sys.path for imports:
  ```python
  PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  sys.path.insert(0, PROJECT_ROOT)
  sys.path.insert(0, SRC_ROOT)
  ```

### Mock Patterns
- Use `unittest.mock` for mocking
- Async tests: `pytest.mark.asyncio` (if async test framework available)
- Mock HTTP responses for data source tests

### Test Naming
- `test_<method_name>` for method tests
- `test_<feature>` for feature tests

## ANTI-PATTERNS

- **Don't hardcode paths**: Use conftest.py path setup
- **Don't skip import setup**: Tests need sys.path configured

## NOTES

- **pytest version**: Specified in requirements.txt (check actual version)
- **Async testing**: If using pytest-asyncio, mark with `@pytest.mark.asyncio`
- **Test data**: May use fixtures for sample fund/commodity data
