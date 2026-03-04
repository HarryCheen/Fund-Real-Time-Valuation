"""
板块数据接口稳定性测试脚本

测试 akshare 中各板块接口在非交易时间的可用性和稳定性：
1. stock_board_industry_spot_em() - 东方财富实时行情（当前使用）
2. stock_board_concept_spot_em() - 同上
3. stock_board_industry_name_em() - 行业板块列表（可能更稳定）
4. stock_board_concept_name_em() - 概念板块列表（可能更稳定）
5. stock_fund_flow_industry() - 资金流向
6. stock_fund_flow_concept() - 资金流向
7. EastMoney 直连 API

运行时间: 非交易时间（测试稳定性）
"""

import asyncio
import time
from datetime import datetime
from typing import Any

import httpx


def print_separator(title: str) -> None:
    """打印分隔符"""
    print(f"\n{'=' * 70}")
    print(f" {title}")
    print("=" * 70)


def print_result(name: str, success: bool, data: Any = None, error: str = None) -> None:
    """打印测试结果"""
    status = "✅ 可用" if success else "❌ 失败"
    print(f"\n[{status}] {name}")
    if success and data is not None:
        if isinstance(data, dict):
            print(f"   数据: {data.get('count', len(data))} 条" if "sectors" in data or "items" in data else f"   数据: {data}")
        elif hasattr(data, "__len__"):
            print(f"   数据: {len(data)} 条")
    elif error:
        print(f"   错误: {error}")


class SectorStabilityTester:
    """板块接口稳定性测试器"""

    def __init__(self):
        self.results: dict[str, dict] = {}

    async def test_spot_em_industry(self) -> dict:
        """测试行业板块实时行情接口"""
        start = time.time()
        try:
            import akshare as ak

            df = ak.stock_board_industry_spot_em()
            elapsed = time.time() - start

            if df is not None and not df.empty:
                return {
                    "success": True,
                    "data": {"count": len(df), "columns": list(df.columns)},
                    "elapsed": elapsed,
                }
            return {"success": False, "error": "返回空数据", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_spot_em_concept(self) -> dict:
        """测试概念板块实时行情接口"""
        start = time.time()
        try:
            import akshare as ak

            df = ak.stock_board_concept_spot_em()
            elapsed = time.time() - start

            if df is not None and not df.empty:
                return {
                    "success": True,
                    "data": {"count": len(df), "columns": list(df.columns)},
                    "elapsed": elapsed,
                }
            return {"success": False, "error": "返回空数据", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_name_em_industry(self) -> dict:
        """测试行业板块名称列表接口"""
        start = time.time()
        try:
            import akshare as ak

            df = ak.stock_board_industry_name_em()
            elapsed = time.time() - start

            if df is not None and not df.empty:
                return {
                    "success": True,
                    "data": {"count": len(df), "columns": list(df.columns)},
                    "elapsed": elapsed,
                }
            return {"success": False, "error": "返回空数据", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_name_em_concept(self) -> dict:
        """测试概念板块名称列表接口"""
        start = time.time()
        try:
            import akshare as ak

            df = ak.stock_board_concept_name_em()
            elapsed = time.time() - start

            if df is not None and not df.empty:
                return {
                    "success": True,
                    "data": {"count": len(df), "columns": list(df.columns)},
                    "elapsed": elapsed,
                }
            return {"success": False, "error": "返回空数据", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_fund_flow_industry(self) -> dict:
        """测试行业资金流向接口"""
        start = time.time()
        try:
            import akshare as ak

            df = ak.stock_fund_flow_industry(symbol="即时")
            elapsed = time.time() - start

            if df is not None and not df.empty:
                return {
                    "success": True,
                    "data": {"count": len(df), "columns": list(df.columns)},
                    "elapsed": elapsed,
                }
            return {"success": False, "error": "返回空数据", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_fund_flow_concept(self) -> dict:
        """测试概念资金流向接口"""
        start = time.time()
        try:
            import akshare as ak

            df = ak.stock_fund_flow_concept(symbol="即时")
            elapsed = time.time() - start

            if df is not None and not df.empty:
                return {
                    "success": True,
                    "data": {"count": len(df), "columns": list(df.columns)},
                    "elapsed": elapsed,
                }
            return {"success": False, "error": "返回空数据", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_eastmoney_direct_industry(self) -> dict:
        """测试东方财富直连 API - 行业板块"""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    "https://push2.eastmoney.com/api/qt/clist/get",
                    params={
                        "cb": "",
                        "fid": "f2",
                        "po": "1",
                        "pz": "10",
                        "pn": "1",
                        "fltt": "2",
                        "invt": "2",
                        "ut": "8dec03ba335b81bf4ebdf7b29ec27d15",
                        "fs": "m:90+t:2",
                    },
                )
                elapsed = time.time() - start
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data") and data["data"].get("diff"):
                        return {
                            "success": True,
                            "data": {"count": len(data["data"]["diff"])},
                            "elapsed": elapsed,
                        }
            return {"success": False, "error": "返回数据为空", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_eastmoney_direct_concept(self) -> dict:
        """测试东方财富直连 API - 概念板块"""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    "https://push2.eastmoney.com/api/qt/clist/get",
                    params={
                        "cb": "",
                        "fid": "f2",
                        "po": "1",
                        "pz": "10",
                        "pn": "1",
                        "fltt": "2",
                        "invt": "2",
                        "ut": "8dec03ba335b81bf4ebdf7b29ec27d15",
                        "fs": "m:90+t:3",
                    },
                )
                elapsed = time.time() - start
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data") and data["data"].get("diff"):
                        return {
                            "success": True,
                            "data": {"count": len(data["data"]["diff"])},
                            "elapsed": elapsed,
                        }
            return {"success": False, "error": "返回数据为空", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_eastmoney_fund_flow_direct(self) -> dict:
        """测试东方财富直连 API - 资金流向"""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # 按主力净流入排序
                response = await client.get(
                    "https://push2.eastmoney.com/api/qt/clist/get",
                    params={
                        "cb": "",
                        "fid": "f62",  # 主力净流入
                        "po": "1",
                        "pz": "10",
                        "pn": "1",
                        "fltt": "2",
                        "invt": "2",
                        "ut": "8dec03ba335b81bf4ebdf7b29ec27d15",
                        "fs": "m:90+t:2",
                        "fields": "f12,f14,f2,f3,f62,f184",
                    },
                )
                elapsed = time.time() - start
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data") and data["data"].get("diff"):
                        return {
                            "success": True,
                            "data": {"count": len(data["data"]["diff"])},
                            "elapsed": elapsed,
                        }
            return {"success": False, "error": "返回数据为空", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def test_board_hist_industry(self) -> dict:
        """测试行业板块历史数据接口"""
        start = time.time()
        try:
            import akshare as ak

            df = ak.stock_board_industry_hist_em(symbol="银行", period="daily", adjust="qfq")
            elapsed = time.time() - start

            if df is not None and not df.empty:
                return {
                    "success": True,
                    "data": {"count": len(df), "columns": list(df.columns)},
                    "elapsed": elapsed,
                }
            return {"success": False, "error": "返回空数据", "elapsed": elapsed}
        except Exception as e:
            return {"success": False, "error": str(e), "elapsed": time.time() - start}

    async def run_all_tests(self) -> dict:
        """运行所有测试"""
        tests = [
            ("stock_board_industry_spot_em (行业实时)", self.test_spot_em_industry),
            ("stock_board_concept_spot_em (概念实时)", self.test_spot_em_concept),
            ("stock_board_industry_name_em (行业列表)", self.test_name_em_industry),
            ("stock_board_concept_name_em (概念列表)", self.test_name_em_concept),
            ("stock_fund_flow_industry (行业资金)", self.test_fund_flow_industry),
            ("stock_fund_flow_concept (概念资金)", self.test_fund_flow_concept),
            ("EastMoney直连API-行业", self.test_eastmoney_direct_industry),
            ("EastMoney直连API-概念", self.test_eastmoney_direct_concept),
            ("EastMoney直连API-资金流向", self.test_eastmoney_fund_flow_direct),
            ("stock_board_industry_hist (行业历史)", self.test_board_hist_industry),
        ]

        results = {}
        for name, test_func in tests:
            print(f"\n正在测试: {name}...")
            result = await test_func()
            results[name] = result
            print_result(name, result.get("success"), result.get("data"), result.get("error"))
            if result.get("elapsed"):
                print(f"   耗时: {result['elapsed']:.2f}s")
            # 短暂延迟避免请求过快
            await asyncio.sleep(0.5)

        return results


def analyze_results(results: dict) -> dict:
    """分析测试结果"""
    analysis = {
        "total": len(results),
        "success": 0,
        "failed": 0,
        "by_category": {
            "spot_em": {"total": 0, "success": 0},
            "name_em": {"total": 0, "success": 0},
            "fund_flow": {"total": 0, "success": 0},
            "direct_api": {"total": 0, "success": 0},
            "hist": {"total": 0, "success": 0},
        },
        "recommendations": [],
    }

    for name, result in results.items():
        if result.get("success"):
            analysis["success"] += 1
        else:
            analysis["failed"] += 1

        # 分类统计
        if "spot_em" in name:
            cat = "spot_em"
        elif "name_em" in name:
            cat = "name_em"
        elif "fund_flow" in name:
            cat = "fund_flow"
        elif "直连" in name or "direct" in name:
            cat = "direct_api"
        elif "hist" in name:
            cat = "hist"
        else:
            cat = "other"

        analysis["by_category"][cat]["total"] += 1
        if result.get("success"):
            analysis["by_category"][cat]["success"] += 1

    return analysis


def print_analysis(analysis: dict) -> None:
    """打印分析结果"""
    print_separator("测试结果分析")

    print(f"\n总计: {analysis['success']}/{analysis['total']} 个接口可用")
    print(f"  ✅ 成功: {analysis['success']}")
    print(f"  ❌ 失败: {analysis['failed']}")

    print("\n按类别统计:")
    for cat, stats in analysis["by_category"].items():
        if stats["total"] > 0:
            success_rate = stats["success"] / stats["total"] * 100
            status = "✅" if success_rate > 0 else "❌"
            print(f"  {status} {cat}: {stats['success']}/{stats['total']} ({success_rate:.0f}%)")


def generate_recommendations(results: dict, analysis: dict) -> list:
    """生成推荐方案"""
    recommendations = []

    # 检查各类别的稳定性
    spot_em_success = analysis["by_category"]["spot_em"]["success"]
    spot_em_total = analysis["by_category"]["spot_em"]["total"]

    name_em_success = analysis["by_category"]["name_em"]["success"]

    fund_flow_success = analysis["by_category"]["fund_flow"]["success"]

    direct_api_success = analysis["by_category"]["direct_api"]["success"]

    # 生成推荐
    if name_em_success > 0 and spot_em_success == 0:
        recommendations.append({
            "type": "primary",
            "title": "使用 name_em 接口作为主要数据源",
            "description": "spot_em 接口在非交易时间不稳定，建议使用 name_em 接口作为主要数据源",
            "implementation": "修改 EastMoneySectorSource 使用 stock_board_industry_name_em() 和 stock_board_concept_name_em()"
        })

    if direct_api_success > 0:
        recommendations.append({
            "type": "backup",
            "title": "使用 EastMoney 直连 API 作为备用",
            "description": "直连 API 稳定性较高，可作为备用数据源",
            "implementation": "EastMoneyDirectSource 已经实现，可以直接使用"
        })

    if fund_flow_success > 0:
        recommendations.append({
            "type": "enhancement",
            "title": "资金流向接口稳定",
            "description": "stock_fund_flow_industry/concept 接口在非交易时间可用",
            "implementation": "FundFlowSource 已经实现，可以用于获取资金流向数据"
        })

    if spot_em_success < spot_em_total and spot_em_success > 0:
        recommendations.append({
            "type": "fallback",
            "title": "添加 spot_em 的 fallback 机制",
            "description": "spot_em 接口部分时间可用，添加缓存和 fallback 机制",
            "implementation": "在 EastMoneySectorSource 中添加缓存策略，失败时回退到其他接口"
        })

    return recommendations


async def main():
    """主函数"""
    print("=" * 70)
    print(" 板块数据接口稳定性测试")
    print(f" 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" 当前状态: {'非交易时间' if datetime.now().hour < 9 or datetime.now().hour >= 15 else '交易时间'}")
    print("=" * 70)

    # 检查 akshare 版本
    try:
        import akshare as ak

        print(f"\nakshare 版本: {ak.__version__}")
    except ImportError:
        print("\n❌ akshare 未安装，请运行: pip install akshare")
        return

    # 运行测试
    tester = SectorStabilityTester()
    results = await tester.run_all_tests()

    # 分析结果
    analysis = analyze_results(results)

    # 打印分析
    print_analysis(analysis)

    # 生成推荐
    recommendations = generate_recommendations(results, analysis)

    # 打印推荐
    print_separator("解决方案建议")

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. [{rec['type'].upper()}] {rec['title']}")
        print(f"   {rec['description']}")
        print(f"   实现: {rec['implementation']}")

    if not recommendations:
        print("\n所有接口均正常运行，无需特别处理。")

    # 打印最终报告
    print_separator("最终报告")

    print("\n📊 接口稳定性排名:")
    sorted_results = sorted(
        [(name, r) for name, r in results.items()],
        key=lambda x: (not x[1].get("success"), -x[1].get("elapsed", 999))
    )

    for i, (name, result) in enumerate(sorted_results, 1):
        status = "✅" if result.get("success") else "❌"
        elapsed = f"{result.get('elapsed', 0):.2f}s" if result.get("elapsed") else ""
        print(f"  {i}. {status} {name} {elapsed}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
