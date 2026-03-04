#!/usr/bin/env python3
"""测试 akshare 资金流向接口的可用性和稳定性。

测试接口:
1. stock_fund_flow_industry - 行业资金流向
2. stock_fund_flow_concept - 概念资金流向

注意: 这两个接口依赖 py_mini_racer 库来执行 JavaScript 代码，
当前环境存在 mini-racer 版本兼容性问题。
"""

import inspect

import httpx


def check_akshare_api_signature() -> dict:
    """检查 akshare API 签名."""
    result = {}
    try:
        import akshare as ak

        # 检查 stock_fund_flow_industry 签名
        func = ak.stock_fund_flow_industry
        sig = inspect.signature(func)
        doc = func.__doc__ or ""
        result["industry"] = {
            "signature": str(sig),
            "doc": doc[:500],
            "source": inspect.getfile(func),
        }

        # 检查 stock_fund_flow_concept 签名
        func = ak.stock_fund_flow_concept
        sig = inspect.signature(func)
        doc = func.__doc__ or ""
        result["concept"] = {
            "signature": str(sig),
            "doc": doc[:500],
            "source": inspect.getfile(func),
        }

        result["akshare_version"] = ak.__version__ if hasattr(ak, "__version__") else "unknown"
    except Exception as e:
        result["error"] = str(e)

    return result


def check_mini_racer() -> dict:
    """检查 mini_racer/py_mini_racer 库状态."""
    result = {}

    # 检查 py_mini_racer
    try:
        import py_mini_racer

        result["py_mini_racer_path"] = py_mini_racer.__file__

        # 尝试初始化 MiniRacer
        try:
            from py_mini_racer import MiniRacer

            mr = MiniRacer()
            test_result = mr.eval("1 + 1")
            result["py_mini_racer_working"] = True
            result["test_result"] = test_result
        except Exception as e:
            result["py_mini_racer_working"] = False
            result["py_mini_racer_error"] = str(e)

    except ImportError as e:
        result["py_mini_racer_installed"] = False
        result["error"] = str(e)

    # 检查 mini_racer (使用 find_spec 检查)
    import importlib.util
    if importlib.util.find_spec("mini_racer") is not None:
        result["mini_racer_installed"] = True

    # 检查动态库符号
    import os
    import subprocess

    lib_path = os.path.join(
        os.path.dirname(result.get("py_mini_racer_path", "")),
        "libmini_racer.dylib",
    )
    if os.path.exists(lib_path):
        result["lib_path"] = lib_path
        try:
            nm_result = subprocess.run(
                ["nm", "-g", lib_path],
                capture_output=True,
                text=True,
            )
            symbols = [
                line.split()[-1]
                for line in nm_result.stdout.split("\n")
                if " T _mr" in line
            ]
            result["exported_mr_symbols"] = symbols[:10]

            # 检查关键符号
            result["has_mr_eval"] = "_mr_eval" in symbols
            result["has_mr_eval_context"] = "_mr_eval_context" in symbols
        except Exception as e:
            result["nm_error"] = str(e)

    return result


def test_akshare_fund_flow() -> dict:
    """测试 akshare 资金流向接口."""
    result = {
        "industry": {"success": False, "error": None},
        "concept": {"success": False, "error": None},
    }

    try:
        import akshare as ak

        # 测试行业资金流向
        try:
            df = ak.stock_fund_flow_industry(symbol="即时")
            result["industry"]["success"] = True
            result["industry"]["columns"] = df.columns.tolist()
            result["industry"]["row_count"] = len(df)
            result["industry"]["sample_data"] = df.head(3).to_dict("records")
        except Exception as e:
            result["industry"]["error"] = str(e)

        # 测试概念资金流向
        try:
            df = ak.stock_fund_flow_concept(symbol="即时")
            result["concept"]["success"] = True
            result["concept"]["columns"] = df.columns.tolist()
            result["concept"]["row_count"] = len(df)
            result["concept"]["sample_data"] = df.head(3).to_dict("records")
        except Exception as e:
            result["concept"]["error"] = str(e)

    except ImportError as e:
        result["import_error"] = str(e)

    return result


def test_ths_api_directly() -> dict:
    """直接测试同花顺 API（绕过 akshare）."""
    result = {
        "industry": {"success": False, "error": None},
        "concept": {"success": False, "error": None},
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    # 测试同花顺行业资金流向页面
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(
                "https://data.10jqka.com.cn/funds/hyzjl/",
                headers=headers,
            )
            result["industry"]["status_code"] = resp.status_code
            result["industry"]["content_length"] = len(resp.text)
            result["industry"]["success"] = resp.status_code == 200
    except Exception as e:
        result["industry"]["error"] = str(e)

    # 测试同花顺概念资金流向页面
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(
                "https://data.10jqka.com.cn/funds/gnzjl/",
                headers=headers,
            )
            result["concept"]["status_code"] = resp.status_code
            result["concept"]["content_length"] = len(resp.text)
            result["concept"]["success"] = resp.status_code == 200
    except Exception as e:
        result["concept"]["error"] = str(e)

    return result


def test_eastmoney_api() -> dict:
    """测试东方财富 API（项目已使用的替代方案）."""
    result = {"success": False, "error": None, "data": None}

    try:
        with httpx.Client(timeout=10) as client:
            # 东方财富行业板块资金流向 API
            resp = client.get(
                "https://push2.eastmoney.com/api/qt/clist/get",
                params={
                    "cb": "",
                    "fid": "f62",  # 按主力净流入排序
                    "po": "1",  # 降序
                    "pz": "10",  # 获取10条
                    "pn": "1",
                    "fltt": "2",
                    "invt": "2",
                    "ut": "8dec03ba335b81bf4ebdf7b29ec27d15",
                    "fs": "m:90+t:2",  # 行业板块
                    "fields": "f12,f14,f2,f3,f62,f184",
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Referer": "https://quote.eastmoney.com/",
                },
            )

            if resp.status_code == 200:
                data = resp.json()
                if data.get("data") and data["data"].get("diff"):
                    result["success"] = True
                    result["count"] = len(data["data"]["diff"])
                    result["sample"] = [
                        {
                            "code": item.get("f12"),
                            "name": item.get("f14"),
                            "change_pct": item.get("f3"),
                            "main_inflow": item.get("f62"),
                        }
                        for item in data["data"]["diff"][:3]
                    ]
                else:
                    result["error"] = "No data in response"
            else:
                result["error"] = f"HTTP {resp.status_code}"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    """运行所有测试."""
    print("=" * 70)
    print("akshare 资金流向接口测试报告")
    print("=" * 70)

    # 1. 检查 API 签名
    print("\n1. 检查 akshare API 签名...")
    api_info = check_akshare_api_signature()
    if "error" in api_info:
        print(f"   错误: {api_info['error']}")
    else:
        print(f"   akshare 版本: {api_info.get('akshare_version')}")
        for name in ["industry", "concept"]:
            if name in api_info:
                print(f"\n   stock_fund_flow_{name}:")
                print(f"     签名: {api_info[name]['signature']}")
                print(f"     源码位置: {api_info[name]['source']}")

    # 2. 检查 mini_racer 状态
    print("\n" + "=" * 70)
    print("2. 检查 mini_racer/py_mini_racer 库状态...")
    racer_info = check_mini_racer()
    print(f"   py_mini_racer 路径: {racer_info.get('py_mini_racer_path')}")
    print(f"   py_mini_racer 工作正常: {racer_info.get('py_mini_racer_working')}")
    if not racer_info.get("py_mini_racer_working"):
        print(f"   错误: {racer_info.get('py_mini_racer_error')}")
    print(f"   导出的 mr_* 符号: {racer_info.get('exported_mr_symbols', [])[:5]}")
    print(f"   有 mr_eval: {racer_info.get('has_mr_eval')}")
    print(f"   有 mr_eval_context: {racer_info.get('has_mr_eval_context')}")

    # 3. 测试 akshare 接口
    print("\n" + "=" * 70)
    print("3. 测试 akshare 资金流向接口...")
    akshare_result = test_akshare_fund_flow()
    for name in ["industry", "concept"]:
        r = akshare_result.get(name, {})
        status = "成功" if r.get("success") else f"失败: {r.get('error')}"
        print(f"   stock_fund_flow_{name}: {status}")
        if r.get("success"):
            print(f"     行数: {r.get('row_count')}")
            print(f"     列名: {r.get('columns')}")

    # 4. 直接测试同花顺 API
    print("\n" + "=" * 70)
    print("4. 直接测试同花顺 API (绕过 akshare)...")
    ths_result = test_ths_api_directly()
    for name in ["industry", "concept"]:
        r = ths_result.get(name, {})
        status = "成功" if r.get("success") else f"失败: {r.get('error')}"
        print(f"   同花顺{name}资金流向页面: {status}")
        if r.get("success"):
            print(f"     状态码: {r.get('status_code')}")
            print(f"     内容长度: {r.get('content_length')} bytes")

    # 5. 测试东方财富 API
    print("\n" + "=" * 70)
    print("5. 测试东方财富 API (项目替代方案)...")
    em_result = test_eastmoney_api()
    if em_result.get("success"):
        print("   状态: 成功")
        print(f"   获取数据: {em_result.get('count')} 条")
        print("   示例数据:")
        for item in em_result.get("sample", []):
            print(f"     {item.get('name')}: 涨跌幅 {item.get('change_pct')}%")
    else:
        print(f"   状态: 失败 - {em_result.get('error')}")

    # 汇总
    print("\n" + "=" * 70)
    print("测试结论汇总")
    print("=" * 70)
    print("""
问题分析:
---------
akshare 的 stock_fund_flow_industry 和 stock_fund_flow_concept 接口依赖
py_mini_racer 库来执行 JavaScript 代码（用于解密同花顺的 API）。

当前环境存在的问题:
- 安装的 mini-racer 0.14.1 版本导出的符号是 mr_eval, mr_init_context 等
- 但 py_mini_racer 0.6.0 期望的符号是 mr_eval_context
- 这是 mini-racer 包和 py_mini_racer 包之间的版本不兼容问题

解决方案:
---------
1. 项目已实现 EastMoneyDirectSource 数据源，可以直接获取资金流向数据
   (位于 src/datasources/sector_source.py)
   
2. 东方财富 API 提供相同的数据，接口稳定，无需 JavaScript 解密

3. 如需使用 akshare 接口，需要:
   - 降级 mini-racer 到兼容版本
   - 或者等待 akshare 更新以适配新版 mini-racer API

建议:
-----
使用项目已有的 EastMoneyDirectSource 数据源获取资金流向数据，
该数据源直接访问东方财富 API，无需依赖 py_mini_racer。
""")


if __name__ == "__main__":
    main()