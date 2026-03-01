# Fund Real-Time Valuation

> 基金实时估值与行情监控 Web 应用

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3.4+-42b883.svg)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178c6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个功能完整的基金与金融市场行情监控平台，支持实时数据推送、多数据源聚合、缓存优化。

## 功能特性

### 核心功能
- **基金估值监控** - 实时追踪基金净值、估算涨跌幅，支持自选基金
- **全球指数行情** - 美股、港股、A股、日经、英国富时等主要市场指数
- **大宗商品** - 黄金、白银、原油、铜等商品实时价格
- **板块轮动** - A股行业板块涨跌排行与资金流向
- **股票行情** - 个股实时价格与盘口数据
- **债券市场** - 国债、企业债收益率曲线
- **财经新闻** - 聚合多方财经资讯
- **舆情分析** - 市场情绪指标与热点追踪

### 技术特性
- **实时推送** - WebSocket 长连接，支持数据实时更新
- **智能缓存** - 多级缓存策略，减少 API 调用
- **多数据源** - 支持 akshare、yfinance 等多个数据源
- **交易日历** - 全球 10+ 市场交易/休市日查询
- **单端口部署** - 前后端统一通过 FastAPI 服务

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI, Pydantic, SQLite, async/await |
| 前端 | Vue 3, TypeScript, Pinia, Vite |
| 数据 | akshare, yfinance |
| 工具 | pnpm, ruff, mypy, pytest |

## 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- pnpm 8+

### 安装与启动

```bash
# 1. 安装依赖（前端 + 后端）
pnpm run install:all

# 2. 启动开发服务器（前后端统一端口 8000）
pnpm run dev

# 3. 访问 http://localhost:8000
```

### 单独启动

```bash
# 后端独立开发（端口 8000）
pnpm run dev:api

# 前端独立开发（端口 3000，热更新）
pnpm run dev:web
```

### 快速启动（跳过缓存预热）

```bash
uv run python run_app.py --fast --reload
```

## 项目结构

```
Fund-Real-Time-Valuation/
├── run_app.py                 # 应用入口
├── pyproject.toml            # Python 项目配置
├── package.json              # pnpm 工作空间配置
│
├── api/                      # FastAPI 后端
│   ├── main.py               # 应用实例
│   ├── dependencies.py       # 依赖注入
│   ├── models.py             # 数据模型
│   └── routes/               # API 路由
│       ├── funds.py          # 基金 API
│       ├── commodities.py   # 商品 API
│       ├── indices.py        # 指数 API
│       ├── sectors.py        # 板块 API
│       ├── stocks.py         # 股票 API
│       ├── bonds.py          # 债券 API
│       ├── news.py           # 新闻 API
│       ├── sentiment.py      # 舆情 API
│       ├── trading_calendar.py  # 交易日历
│       ├── holidays.py       # 节假日
│       ├── websocket.py      # WebSocket
│       ├── datasource.py     # 数据源管理
│       ├── cache.py          # 缓存管理
│       └── overview.py       # 概览数据
│
├── src/                      # Python 源码
│   ├── datasources/          # 数据源层
│   │   ├── base.py           # 数据源基类
│   │   ├── manager.py        # 数据源管理器
│   │   ├── fund_source.py    # 基金数据源
│   │   ├── commodity_source.py # 商品数据源
│   │   ├── index_source.py   # 指数数据源
│   │   ├── sector_source.py  # 板块数据源
│   │   ├── stock_source.py   # 股票数据源
│   │   ├── bond_source.py    # 债券数据源
│   │   ├── trading_calendar_source.py # 交易日历
│   │   ├── cache.py          # 缓存模块
│   │   ├── gateway.py        # 数据网关
│   │   └── fund/             # 基金子模块
│   │       └── cache_strategy.py
│   ├── db/                   # 数据库层
│   ├── config/               # 配置管理
│   └── utils/                # 工具模块
│
├── web/                      # Vue 3 前端
│   ├── src/
│   │   ├── views/            # 页面视图
│   │   │   ├── HomeView.vue
│   │   │   ├── FundsView.vue
│   │   │   ├── CommoditiesView.vue
│   │   │   ├── IndicesView.vue
│   │   │   ├── SectorsView.vue
│   │   │   ├── StocksView.vue
│   │   │   ├── BondsView.vue
│   │   │   ├── NewsView.vue
│   │   │   └── SettingsView.vue
│   │   ├── components/       # 组件
│   │   ├── stores/           # Pinia 状态
│   │   ├── api/              # API 调用
│   │   └── styles/           # 样式
│   └── package.json
│
└── tests/                    # 测试
```

## 开发命令

```bash
# 安装依赖
pnpm run install:all

# 运行测试
uv run pytest tests/ -v

# Python 代码检查
uv run ruff check .              # 检查
uv run ruff check --fix .        # 自动修复
uv run mypy .                    # 类型检查

# 前端代码检查
cd web && pnpm run lint

# 构建前端
pnpm run build:web
```

## API 接口

### 基金

```bash
# 基金列表
GET /api/funds

# 基金详情
GET /api/funds/{code}

# 基金估值
GET /api/funds/{code}/estimate

# 基金历史净值
GET /api/funds/{code}/history?period=近一年

# 基金日内分时数据
GET /api/funds/{code}/intraday

# 按日期获取日内分时数据
GET /api/funds/{code}/intraday/{date}

# 自选管理
POST   /api/funds/watchlist    # 添加自选
DELETE /api/funds/watchlist/{code}  # 删除自选

# 持仓管理
PUT /api/funds/{code}/holding?holding=true  # 标记/取消持有
```

### 债券

```bash
# 债券列表
GET /api/bonds?bond_type=cbond

# 单个债券详情
GET /api/bonds/{code}?market=sh

# 可转债搜索
GET /api/bonds/search/cbonds?keyword=110
```

### 股票

```bash
# 股票行情（批量）
GET /api/stocks?codes=sh600000,sz000001,AAPL

# 单个股票详情
GET /api/stocks/{code}
```

### 商品

```bash
# 商品行情
GET /api/commodities

# 关注列表
GET    /api/commodities/watchlist
POST   /api/commodities/watchlist
DELETE /api/commodities/watchlist
```

### 指数

```bash
# 全球市场指数
GET /api/indices
```

### 板块

```bash
# 行业板块
GET /api/sectors
```

### 新闻

```bash
# 财经新闻
GET /api/news
```

### 舆情

```bash
# 舆情数据
GET /api/sentiment
```

### 节假日

```bash
# 节假日列表
GET /api/holidays?market=china&year=2025

# 指定市场节假日
GET /api/holidays/{market}?year=2025
```

### 交易日历

```bash
# 判断是否为交易日
GET /trading-calendar/is-trading-day/{market}

# 获取年度交易日历
GET /trading-calendar/calendar/{market}?year=2025

# 获取下一个交易日
GET /trading-calendar/next-trading-day/{market}

# 获取多市场状态
GET /trading-calendar/market-status?markets=china,usa,comex
```

**支持的市场**: `china`, `hk`, `usa`, `japan`, `uk`, `germany`, `france`, `sge`, `comex`, `cme`, `lbma`

### 缓存与数据源

```bash
# 缓存统计
GET /api/cache/stats

# 数据源统计
GET /api/datasource/statistics

# 数据源健康状态
GET /api/datasource/health

# 已注册数据源列表
GET /api/datasource/sources
```

### 健康检查

```bash
# 简单健康检查
GET /api/health/simple

# 详细健康检查
GET /api/health
```

### WebSocket

```bash
# 实时数据推送
WS /ws/realtime

# WebSocket 管理状态
GET /ws/manager/status

# 广播消息
POST /ws/manager/broadcast
```

## 配置

配置文件位置: `~/.fund-tui/`

| 文件 | 说明 |
|------|------|
| `config.yaml` | 应用配置 |
| `funds.yaml` | 自选基金列表 |
| `fund_data.db` | SQLite 数据库 |

## 部署

### 生产构建

```bash
# 构建前端资源
pnpm run build:web

# 启动应用（单端口）
pnpm run dev
```

### Docker（可选）

```dockerfile
FROM python:3.10-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv sync --frozen
COPY . .
EXPOSE 8000
CMD ["uv", "run", "python", "run_app.py"]
```

## 许可证

[MIT](LICENSE)
