"""
akshare 接口可用性测试脚本

测试以下接口：
1. 行业板块: stock_board_industry_name_em()
2. 概念板块: stock_board_concept_name_em()
3. 资金流向相关接口
"""

from datetime import datetime


def print_separator(title: str):
    """打印分隔符"""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)


def print_dataframe_info(df, name: str):
    """打印 DataFrame 基本信息"""
    if df is None:
        print(f"  {name}: 返回 None")
        return

    if df.empty:
        print(f"  {name}: 返回空 DataFrame")
        return

    print(f"  {name}:")
    print(f"    - 行数: {len(df)}")
    print(f"    - 列数: {len(df.columns)}")
    print(f"    - 列名: {list(df.columns)}")
    print("    - 前3行数据:")
    print(df.head(3).to_string(index=False))
    print()


def test_industry_board():
    """测试行业板块接口"""
    print_separator("1. 行业板块接口测试")

    try:
        import akshare as ak

        # 行业板块列表
        print("\n[stock_board_industry_name_em] - 行业板块列表")
        df = ak.stock_board_industry_name_em()
        print_dataframe_info(df, "行业板块列表")

        return df is not None and not df.empty

    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        return False


def test_concept_board():
    """测试概念板块接口"""
    print_separator("2. 概念板块接口测试")

    try:
        import akshare as ak

        # 概念板块列表
        print("\n[stock_board_concept_name_em] - 概念板块列表")
        df = ak.stock_board_concept_name_em()
        print_dataframe_info(df, "概念板块列表")

        return df is not None and not df.empty

    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        return False


def test_fund_flow_apis():
    """测试资金流向相关接口"""
    print_separator("3. 资金流向接口测试")

    import akshare as ak

    results = {}

    # 3.1 个股资金流向
    print("\n[stock_individual_fund_flow] - 个股资金流向")
    try:
        # 需要提供股票代码
        df = ak.stock_individual_fund_flow(stock="000001", market="sh")
        print_dataframe_info(df, "个股资金流向(000001)")
        results["stock_individual_fund_flow"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_individual_fund_flow"] = False

    # 3.2 行业资金流向 (正确的函数名)
    print("\n[stock_fund_flow_industry] - 行业资金流向")
    try:
        df = ak.stock_fund_flow_industry()
        print_dataframe_info(df, "行业资金流向")
        results["stock_fund_flow_industry"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_fund_flow_industry"] = False

    # 3.3 概念资金流向 (正确的函数名)
    print("\n[stock_fund_flow_concept] - 概念资金流向")
    try:
        df = ak.stock_fund_flow_concept()
        print_dataframe_info(df, "概念资金流向")
        results["stock_fund_flow_concept"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_fund_flow_concept"] = False

    # 3.4 个股资金流向排名
    print("\n[stock_individual_fund_flow_rank] - 个股资金流向排名")
    try:
        df = ak.stock_individual_fund_flow_rank(indicator="今日")
        print_dataframe_info(df, "个股资金流向排名(今日)")
        results["stock_individual_fund_flow_rank"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_individual_fund_flow_rank"] = False

    # 3.5 大单交易
    print("\n[stock_fund_flow_big_deal] - 大单交易")
    try:
        df = ak.stock_fund_flow_big_deal()
        print_dataframe_info(df, "大单交易")
        results["stock_fund_flow_big_deal"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_fund_flow_big_deal"] = False

    return results


def test_sector_detail_apis():
    """测试板块详情接口"""
    print_separator("4. 板块详情接口测试")

    import akshare as ak

    results = {}

    # 4.1 行业板块成份股
    print("\n[stock_board_industry_cons_em] - 行业板块成份股")
    try:
        df = ak.stock_board_industry_cons_em(symbol="银行")
        print_dataframe_info(df, "银行板块成份股")
        results["stock_board_industry_cons_em"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_board_industry_cons_em"] = False

    # 4.2 概念板块成份股
    print("\n[stock_board_concept_cons_em] - 概念板块成份股")
    try:
        df = ak.stock_board_concept_cons_em(symbol="新能源")
        print_dataframe_info(df, "新能源概念成份股")
        results["stock_board_concept_cons_em"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_board_concept_cons_em"] = False

    return results


def test_additional_fund_flow_apis():
    """测试其他资金流向相关接口"""
    print_separator("5. 其他资金流向接口测试")

    import akshare as ak

    results = {}

    # 5.1 主力资金流向
    print("\n[stock_main_fund_flow] - 主力资金流向")
    try:
        df = ak.stock_main_fund_flow(symbol="强势股")
        print_dataframe_info(df, "主力资金流向(强势股)")
        results["stock_main_fund_flow"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_main_fund_flow"] = False

    # 5.2 板块资金净流入排名
    print("\n[stock_sector_fund_flow_rank] - 板块资金净流入排名")
    try:
        df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
        print_dataframe_info(df, "行业资金流排名")
        results["stock_sector_fund_flow_rank"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_sector_fund_flow_rank"] = False

    # 5.3 大盘资金流向
    print("\n[stock_market_fund_flow] - 大盘资金流向")
    try:
        df = ak.stock_market_fund_flow()
        print_dataframe_info(df, "大盘资金流向")
        results["stock_market_fund_flow"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_market_fund_flow"] = False

    # 5.4 板块资金净流入汇总
    print("\n[stock_sector_fund_flow_summary] - 板块资金净流入汇总")
    try:
        df = ak.stock_sector_fund_flow_summary()
        print_dataframe_info(df, "板块资金净流入汇总")
        results["stock_sector_fund_flow_summary"] = df is not None and not df.empty
    except Exception as e:
        print(f"  错误: {type(e).__name__}: {e}")
        results["stock_sector_fund_flow_summary"] = False

    return results


def main():
    """主测试函数"""
    print("=" * 60)
    print(" akshare 接口可用性测试")
    print(f" 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 检查 akshare 版本
    try:
        import akshare as ak

        print(f"\nakshare 版本: {ak.__version__}")
    except ImportError:
        print("\n错误: akshare 未安装，请运行 pip install akshare")
        return

    # 运行测试
    all_results = {}

    # 1. 行业板块
    all_results["行业板块"] = test_industry_board()

    # 2. 概念板块
    all_results["概念板块"] = test_concept_board()

    # 3. 资金流向
    fund_flow_results = test_fund_flow_apis()
    all_results.update(fund_flow_results)

    # 4. 板块详情
    detail_results = test_sector_detail_apis()
    all_results.update(detail_results)

    # 5. 其他资金流向
    other_results = test_additional_fund_flow_apis()
    all_results.update(other_results)

    # 打印汇总报告
    print_separator("测试结果汇总")

    print("\n接口可用性统计:")
    for name, available in all_results.items():
        status = "✅ 可用" if available else "❌ 不可用"
        print(f"  {name}: {status}")

    # 统计
    available_count = sum(1 for v in all_results.values() if v)
    total_count = len(all_results)
    print(f"\n总计: {available_count}/{total_count} 个接口可用")

    # 推荐集成建议
    print_separator("集成建议")

    print("\n建议集成的接口:")
    recommendations = []

    if all_results.get("行业板块"):
        recommendations.append({
            "name": "stock_board_industry_name_em",
            "desc": "行业板块行情",
            "priority": "高",
            "reason": "提供完整的行业板块列表和涨跌幅数据"
        })

    if all_results.get("概念板块"):
        recommendations.append({
            "name": "stock_board_concept_name_em",
            "desc": "概念板块行情",
            "priority": "高",
            "reason": "提供完整的概念板块列表和涨跌幅数据"
        })

    if all_results.get("stock_fund_flow_industry"):
        recommendations.append({
            "name": "stock_fund_flow_industry",
            "desc": "行业板块资金流向",
            "priority": "高",
            "reason": "提供行业主力资金流入流出数据"
        })

    if all_results.get("stock_fund_flow_concept"):
        recommendations.append({
            "name": "stock_fund_flow_concept",
            "desc": "概念板块资金流向",
            "priority": "高",
            "reason": "提供概念板块主力资金流入流出数据"
        })

    if all_results.get("stock_individual_fund_flow_rank"):
        recommendations.append({
            "name": "stock_individual_fund_flow_rank",
            "desc": "个股资金流向排名",
            "priority": "中",
            "reason": "提供个股主力资金排名数据"
        })

    if all_results.get("stock_board_industry_cons_em"):
        recommendations.append({
            "name": "stock_board_industry_cons_em",
            "desc": "行业板块成份股",
            "priority": "中",
            "reason": "获取行业板块内个股列表"
        })

    if all_results.get("stock_board_concept_cons_em"):
        recommendations.append({
            "name": "stock_board_concept_cons_em",
            "desc": "概念板块成份股",
            "priority": "中",
            "reason": "获取概念板块内个股列表"
        })

    if all_results.get("stock_market_fund_flow"):
        recommendations.append({
            "name": "stock_market_fund_flow",
            "desc": "大盘资金流向",
            "priority": "中",
            "reason": "提供大盘整体资金流向数据"
        })

    for rec in recommendations:
        print(f"\n  [{rec['priority']}级] {rec['name']}")
        print(f"    描述: {rec['desc']}")
        print(f"    原因: {rec['reason']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()