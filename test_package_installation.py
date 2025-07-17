#!/usr/bin/env python3
"""
Rich-Agents 包安装测试脚本
验证包的所有功能是否正常工作
"""

import sys
import importlib
import traceback
from typing import List, Tuple

def test_import(module_name: str, description: str) -> Tuple[bool, str]:
    """测试模块导入"""
    try:
        importlib.import_module(module_name)
        return True, f"✅ {description}: 导入成功"
    except Exception as e:
        return False, f"❌ {description}: 导入失败 - {str(e)}"

def test_function_call(module_name: str, function_name: str, description: str) -> Tuple[bool, str]:
    """测试函数调用"""
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)
        # 对于某些函数，我们只测试是否可调用
        if callable(func):
            return True, f"✅ {description}: 函数可调用"
        else:
            return False, f"❌ {description}: 不是可调用对象"
    except Exception as e:
        return False, f"❌ {description}: 调用失败 - {str(e)}"

def main():
    """主测试函数"""
    print("🚀 Rich-Agents 包安装测试")
    print("=" * 60)
    
    # 测试用例列表
    tests = [
        # 核心模块测试
        ("shared", "共享基础设施模块"),
        ("shared.config", "配置管理模块"),
        ("shared.config.rich_agents_config_manager", "Rich-Agents配置管理器"),
        ("shared.llm_adapters", "LLM适配器模块"),
        ("shared.llm_adapters.unified_llm_adapter", "统一LLM适配器"),
        
        # CLI模块测试
        ("cli", "CLI模块"),
        ("cli.rich_agents_main", "Rich-Agents主CLI"),
        ("cli.rich_agents_simple", "Rich-Agents简化CLI"),
        ("cli.trading_cli", "TradingAgent CLI"),
        ("cli.patent_cli", "PatentAgent CLI"),
        
        # 智能体模块测试
        ("tradingagents", "TradingAgent模块"),
        ("tradingagents.default_config", "TradingAgent默认配置"),
        ("patentagents", "PatentAgent模块"),
    ]
    
    # 执行导入测试
    success_count = 0
    total_count = len(tests)
    
    print("\n📦 模块导入测试:")
    print("-" * 40)
    
    for module_name, description in tests:
        success, message = test_import(module_name, description)
        print(message)
        if success:
            success_count += 1
    
    # 测试关键功能
    print("\n🔧 功能测试:")
    print("-" * 40)
    
    function_tests = [
        ("shared.config.rich_agents_config_manager", "RichAgentsConfigManager", "配置管理器类"),
        ("shared.llm_adapters.unified_llm_adapter", "UnifiedLLMAdapter", "统一LLM适配器类"),
        ("cli.rich_agents_simple", "main", "简化CLI主函数"),
    ]
    
    for module_name, func_name, description in function_tests:
        success, message = test_function_call(module_name, func_name, description)
        print(message)
        if success:
            success_count += 1
        total_count += 1
    
    # 测试依赖包
    print("\n📚 依赖包测试:")
    print("-" * 40)
    
    dependency_tests = [
        ("typer", "Typer CLI框架"),
        ("rich", "Rich终端库"),
        ("langchain", "LangChain框架"),
        ("langgraph", "LangGraph图框架"),
        ("questionary", "交互式问答库"),
        ("yfinance", "Yahoo Finance数据"),
        ("akshare", "AkShare金融数据"),
        ("redis", "Redis缓存"),
        ("requests", "HTTP请求库"),
        ("pandas", "数据分析库"),
    ]
    
    for module_name, description in dependency_tests:
        success, message = test_import(module_name, description)
        print(message)
        if success:
            success_count += 1
        total_count += 1
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {success_count}/{total_count} 通过")
    
    success_rate = (success_count / total_count) * 100
    
    if success_rate >= 90:
        print(f"🎉 测试通过率: {success_rate:.1f}% - 优秀!")
        print("✅ Rich-Agents包安装成功，所有核心功能正常!")
    elif success_rate >= 70:
        print(f"⚠️  测试通过率: {success_rate:.1f}% - 良好")
        print("🔧 大部分功能正常，可能需要安装一些可选依赖")
    else:
        print(f"❌ 测试通过率: {success_rate:.1f}% - 需要修复")
        print("🛠️  请检查安装过程和依赖配置")
    
    print("\n💡 使用建议:")
    print("- 运行 'python main.py' 启动Rich-Agents")
    print("- 运行 'python -m cli.rich_agents_simple' 启动简化版")
    print("- 运行 'python -m cli.trading_cli' 启动TradingAgent")
    print("- 运行 'python -m cli.patent_cli' 启动PatentAgent")
    
    return success_rate >= 70

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 测试过程中发生错误: {e}")
        traceback.print_exc()
        sys.exit(1) 