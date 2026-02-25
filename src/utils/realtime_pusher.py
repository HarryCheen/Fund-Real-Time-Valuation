"""
实时数据推送器模块

定时获取数据并通过 WebSocket 推送到前端。
支持智能 Diff 只推送变化数据。
支持交易时段检测，在非交易时段降低推送频率。
"""

import asyncio
import logging

from src.datasources.manager import DataSourceManager, DataSourceType
from src.datasources.trading_calendar_source import Market, TradingCalendarSource
from src.utils.websocket_manager import WebSocketManager, get_websocket_manager

logger = logging.getLogger(__name__)

# 交易时段推送间隔（秒）
TRADING_FUND_INTERVAL = 30
TRADING_COMMODITY_INTERVAL = 15
TRADING_INDEX_INTERVAL = 15

# 非交易时段推送间隔（秒）
NON_TRADING_FUND_INTERVAL = 120
NON_TRADING_COMMODITY_INTERVAL = 60
NON_TRADING_INDEX_INTERVAL = 60


class RealtimePusher:
    """实时数据推送器"""

    def __init__(
        self,
        data_source_manager: DataSourceManager | None = None,
        websocket_manager: WebSocketManager | None = None,
    ):
        self._data_manager = data_source_manager
        self._ws_manager = websocket_manager
        self._running = False
        self._tasks: list[asyncio.Task] = []

        self._last_fund_data: list[dict] | None = None
        self._last_commodity_data: list[dict] | None = None
        self._last_index_data: list[dict] | None = None

        self._trading_calendar = TradingCalendarSource()

    @property
    def data_manager(self) -> DataSourceManager:
        if self._data_manager is None:
            from api.dependencies import get_data_source_manager

            self._data_manager = get_data_source_manager()
        return self._data_manager

    @property
    def ws_manager(self) -> WebSocketManager:
        if self._ws_manager is None:
            self._ws_manager = get_websocket_manager()
        return self._ws_manager

    def _has_subscribers(self, subscription: str) -> bool:
        subscriptions = self.ws_manager.get_subscriptions_info()
        return subscriptions.get(subscription, 0) > 0

    def _is_trading_hours(self, market: Market = Market.CHINA) -> bool:
        try:
            result = self._trading_calendar.is_within_trading_hours(market)
            return result.get("status") == "open"
        except Exception as e:
            logger.warning(f"检查交易时段失败: {e}")
            return False

    def _get_intervals(self) -> tuple[int, int, int]:
        is_trading = self._is_trading_hours(Market.CHINA)
        if is_trading:
            return TRADING_FUND_INTERVAL, TRADING_COMMODITY_INTERVAL, TRADING_INDEX_INTERVAL
        return NON_TRADING_FUND_INTERVAL, NON_TRADING_COMMODITY_INTERVAL, NON_TRADING_INDEX_INTERVAL

    def _diff_data(
        self, data_type: str, old_data: list[dict], new_data: list[dict]
    ) -> list[dict] | None:
        if not old_data:
            return new_data

        old_dict = {item.get("code") or item.get("symbol"): item for item in old_data}
        new_dict = {item.get("code") or item.get("symbol"): item for item in new_data}

        old_keys = set(old_dict.keys())
        new_keys = set(new_dict.keys())

        if old_keys != new_keys:
            return new_data

        changed_items = []
        for key in new_keys:
            old_item = old_dict[key]
            new_item = new_dict[key]
            for field, value in new_item.items():
                if field not in old_item or old_item[field] != value:
                    changed_items.append(new_item)
                    break

        return changed_items if changed_items else None

    async def _push_funds_loop(self):
        fund_interval, _, _ = self._get_intervals()
        while self._running:
            try:
                if not self._has_subscribers("funds"):
                    await asyncio.sleep(5)
                    continue

                result = await self.data_manager.fetch(DataSourceType.FUND)
                if result.success and result.data:
                    new_data = result.data if isinstance(result.data, list) else [result.data]

                    if self._last_fund_data is not None:
                        diff_data = self._diff_data("funds", self._last_fund_data, new_data)
                        if diff_data is None:
                            logger.debug("基金数据无变化，跳过推送")
                            self._last_fund_data = new_data
                            await asyncio.sleep(fund_interval)
                            continue

                        await self.ws_manager.broadcast_to_subscription(
                            subscription="funds",
                            message_type="fund_update",
                            data=diff_data,
                        )
                        logger.debug(f"推送 {len(diff_data)} 条变化基金数据")
                    else:
                        await self.ws_manager.broadcast_to_subscription(
                            subscription="funds",
                            message_type="fund_update",
                            data=new_data,
                        )
                        logger.debug(f"首次推送 {len(new_data)} 条基金数据")

                    self._last_fund_data = new_data
                else:
                    logger.warning(f"获取基金数据失败: {result.error}")

            except Exception as e:
                logger.error(f"基金推送循环异常: {e}")

            await asyncio.sleep(fund_interval)

    async def _push_commodities_loop(self):
        _, commodity_interval, _ = self._get_intervals()
        while self._running:
            try:
                if not self._has_subscribers("commodities"):
                    await asyncio.sleep(5)
                    continue

                result = await self.data_manager.fetch(DataSourceType.COMMODITY)
                if result.success and result.data:
                    new_data = result.data if isinstance(result.data, list) else [result.data]

                    if self._last_commodity_data is not None:
                        diff_data = self._diff_data(
                            "commodities", self._last_commodity_data, new_data
                        )
                        if diff_data is None:
                            logger.debug("商品数据无变化，跳过推送")
                            self._last_commodity_data = new_data
                            await asyncio.sleep(commodity_interval)
                            continue

                        await self.ws_manager.broadcast_to_subscription(
                            subscription="commodities",
                            message_type="commodity_update",
                            data=diff_data,
                        )
                        logger.debug(f"推送 {len(diff_data)} 条变化商品数据")
                    else:
                        await self.ws_manager.broadcast_to_subscription(
                            subscription="commodities",
                            message_type="commodity_update",
                            data=new_data,
                        )
                        logger.debug(f"首次推送 {len(new_data)} 条商品数据")

                    self._last_commodity_data = new_data
                else:
                    logger.warning(f"获取商品数据失败: {result.error}")

            except Exception as e:
                logger.error(f"商品推送循环异常: {e}")

            await asyncio.sleep(commodity_interval)

    async def _push_indices_loop(self):
        _, _, index_interval = self._get_intervals()
        while self._running:
            try:
                if not self._has_subscribers("indices"):
                    await asyncio.sleep(5)
                    continue

                result = await self.data_manager.fetch(DataSourceType.STOCK)
                if result.success and result.data:
                    new_data = result.data if isinstance(result.data, list) else [result.data]

                    if self._last_index_data is not None:
                        diff_data = self._diff_data("indices", self._last_index_data, new_data)
                        if diff_data is None:
                            logger.debug("指数数据无变化，跳过推送")
                            self._last_index_data = new_data
                            await asyncio.sleep(index_interval)
                            continue

                        await self.ws_manager.broadcast_to_subscription(
                            subscription="indices",
                            message_type="index_update",
                            data=diff_data,
                        )
                        logger.debug(f"推送 {len(diff_data)} 条变化指数数据")
                    else:
                        await self.ws_manager.broadcast_to_subscription(
                            subscription="indices",
                            message_type="index_update",
                            data=new_data,
                        )
                        logger.debug(f"首次推送 {len(new_data)} 条指数数据")

                    self._last_index_data = new_data
                else:
                    logger.warning(f"获取指数数据失败: {result.error}")

            except Exception as e:
                logger.error(f"指数推送循环异常: {e}")

            await asyncio.sleep(index_interval)

    async def start(self):
        if self._running:
            logger.warning("推送器已在运行中")
            return

        self._running = True
        logger.info("启动实时数据推送器")

        self._tasks = [
            asyncio.create_task(self._push_funds_loop()),
            asyncio.create_task(self._push_commodities_loop()),
            asyncio.create_task(self._push_indices_loop()),
        ]

        logger.info(f"已启动 {len(self._tasks)} 个推送任务")

    async def stop(self):
        if not self._running:
            logger.warning("推送器未在运行")
            return

        self._running = False
        logger.info("停止实时数据推送器")

        for task in self._tasks:
            task.cancel()

        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

        self._tasks = []
        logger.info("实时数据推送器已停止")


_pusher: RealtimePusher | None = None


def get_realtime_pusher() -> RealtimePusher:
    global _pusher
    if _pusher is None:
        _pusher = RealtimePusher()
    return _pusher


async def start_realtime_pusher():
    pusher = get_realtime_pusher()
    await pusher.start()


async def stop_realtime_pusher():
    if _pusher is not None:
        await _pusher.stop()
