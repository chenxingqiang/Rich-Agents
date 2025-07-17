"""
Rich-Agents 主入口文件
可以直接运行TradingAgent或者启动Rich-Agents统一CLI
"""

# 保持原有的TradingAgent单独使用方式
def run_trading_agent_example():
    """运行TradingAgent示例"""
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG

    # Create a custom config
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"  # Use a different model
    config["backend_url"] = "https://generativelanguage.googleapis.com/v1"  # Use a different backend
    config["deep_think_llm"] = "gemini-2.0-flash"  # Use a different model
    config["quick_think_llm"] = "gemini-2.0-flash"  # Use a different model
    config["max_debate_rounds"] = 1  # Increase debate rounds
    config["online_tools"] = True  # Increase debate rounds

    # Initialize with custom config
    ta = TradingAgentsGraph(debug=True, config=config)

    # forward propagate
    _, decision = ta.propagate("NVDA", "2024-05-10")
    print(decision)

    # Memorize mistakes and reflect
    # ta.reflect_and_remember(1000) # parameter is the position returns


def run_rich_agents_cli():
    """运行Rich-Agents统一CLI"""
    try:
        # 尝试使用完整版CLI (需要typer)
        from cli.rich_agents_main import app
        app()
    except ImportError:
        # 如果typer不可用，使用简化版CLI
        from cli.rich_agents_simple import main
        main()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--trading-example":
        # 运行TradingAgent示例
        print("运行TradingAgent示例...")
        run_trading_agent_example()
    else:
        # 运行Rich-Agents统一CLI
        print("启动Rich-Agents统一CLI...")
        run_rich_agents_cli()
