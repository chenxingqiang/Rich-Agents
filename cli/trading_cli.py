"""
TradingAgent CLI适配器
将现有的TradingAgent功能集成到Rich-Agents统一框架中
"""

import os
import sys
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# 导入Rich-Agents共享组件
from shared.config.rich_agents_config_manager import RichAgentsConfigManager
from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter

# 导入现有的TradingAgent组件
try:
    from cli.main import run_analysis as run_trading_analysis
except ImportError:
    # 如果原CLI不可用，设置为None
    run_trading_analysis = None

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

logger = logging.getLogger(__name__)


class TradingAgentCLI:
    """TradingAgent CLI适配器"""
    
    def __init__(self, config_manager: Optional[RichAgentsConfigManager] = None):
        """
        初始化TradingAgent CLI
        
        Args:
            config_manager: Rich-Agents配置管理器实例
        """
        self.config_manager = config_manager or RichAgentsConfigManager()
        self.trading_config = self.config_manager.get_trading_config()
        
        logger.info("TradingAgent CLI适配器初始化完成")
    
    def run(self):
        """运行TradingAgent分析"""
        try:
            from rich.console import Console
            console = Console()
            
            console.print("[bold blue]🏦 TradingAgent - 多智能体金融交易分析框架[/bold blue]")
            console.print("[dim]正在启动金融交易智能体团队...[/dim]\n")
            
            # 验证API密钥配置
            validation_result = self.config_manager.validate_config("trading")
            if not validation_result["valid"]:
                console.print("[red]❌ 配置验证失败:[/red]")
                for error in validation_result["errors"]:
                    console.print(f"  • [red]{error}[/red]")
                console.print("\n[yellow]请检查API密钥配置后重试[/yellow]")
                return
            
            if validation_result["warnings"]:
                console.print("[yellow]⚠️ 配置警告:[/yellow]")
                for warning in validation_result["warnings"]:
                    console.print(f"  • [yellow]{warning}[/yellow]")
                console.print()
            
            # 调用原有的TradingAgent分析流程
            console.print("[green]✅ 配置验证通过，启动TradingAgent分析流程[/green]\n")
            
            # 使用原有的run_analysis函数
            if run_trading_analysis is not None:
                run_trading_analysis()
            else:
                console.print("[yellow]⚠️ 原TradingAgent CLI不可用，启动基础模式[/yellow]")
                self._run_basic_trading_mode(console)
            
        except ImportError as e:
            console.print(f"[red]❌ 导入TradingAgent模块失败: {str(e)}[/red]")
            console.print("[yellow]请确保TradingAgent依赖已正确安装[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ TradingAgent运行失败: {str(e)}[/red]")
            logger.error(f"TradingAgent运行失败: {str(e)}")
    
    def create_trading_graph(self, analysts: list, config: Dict[str, Any]) -> TradingAgentsGraph:
        """
        创建TradingAgent图实例
        
        Args:
            analysts: 分析师列表
            config: 配置字典
            
        Returns:
            TradingAgentsGraph实例
        """
        try:
            # 使用Rich-Agents的统一配置创建TradingAgent
            merged_config = DEFAULT_CONFIG.copy()
            merged_config.update(config)
            
            # 创建TradingAgent图
            graph = TradingAgentsGraph(
                analysts=analysts,
                config=merged_config,
                debug=config.get("debug", True)
            )
            
            return graph
            
        except Exception as e:
            logger.error(f"创建TradingAgent图失败: {str(e)}")
            raise
    
    def run_custom_analysis(self, ticker: str, date: str, **kwargs) -> Dict[str, Any]:
        """
        运行自定义分析
        
        Args:
            ticker: 股票代码
            date: 分析日期
            **kwargs: 其他参数
            
        Returns:
            分析结果
        """
        try:
            # 准备配置
            config = self.trading_config.copy()
            config.update(kwargs)
            
            # 设置分析师
            analysts = config.get("analysts", ["market", "social", "news", "fundamentals"])
            
            # 创建TradingAgent图
            graph = self.create_trading_graph(analysts, config)
            
            # 运行分析
            state, decision = graph.propagate(ticker, date)
            
            return {
                "success": True,
                "ticker": ticker,
                "date": date,
                "state": state,
                "decision": decision
            }
            
        except Exception as e:
            logger.error(f"自定义分析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_supported_markets(self) -> Dict[str, Any]:
        """获取支持的市场"""
        return self.trading_config.get("markets", {})
    
    def get_available_analysts(self) -> list:
        """获取可用的分析师"""
        return self.trading_config.get("analysts", ["market", "social", "news", "fundamentals"])
    
    def _run_basic_trading_mode(self, console):
        """运行基础交易模式"""
        console.print("[bold]TradingAgent 基础模式[/bold]")
        console.print()
        
        # 显示可用功能
        console.print("可用功能:")
        console.print("1. 📊 股票基础分析")
        console.print("2. 📈 市场趋势分析")
        console.print("3. 🔧 系统状态检查")
        console.print("4. 🚪 返回主菜单")
        
        while True:
            try:
                choice = console.input("\n[bold yellow]请选择功能 (1-4): [/bold yellow]").strip()
                
                if choice == '1':
                    self._basic_stock_analysis(console)
                elif choice == '2':
                    self._basic_market_analysis(console)
                elif choice == '3':
                    self._trading_system_status(console)
                elif choice == '4':
                    console.print("[green]返回主菜单[/green]")
                    break
                else:
                    console.print("[red]❌ 无效选择，请输入1-4之间的数字[/red]")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]返回主菜单[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ 操作失败: {str(e)}[/red]")
    
    def _basic_stock_analysis(self, console):
        """基础股票分析"""
        console.print("\n[bold cyan]📊 股票基础分析[/bold cyan]")
        
        try:
            ticker = console.input("请输入股票代码 (如 AAPL, TSLA): ").strip().upper()
            if not ticker:
                console.print("[red]❌ 股票代码不能为空[/red]")
                return
            
            console.print(f"\n[yellow]正在分析股票: {ticker}[/yellow]")
            
            # 模拟基础分析
            analysis_result = f"""
股票分析报告: {ticker}

基础信息:
• 股票代码: {ticker}
• 分析时间: 当前时间
• 分析类型: 基础模式

技术指标:
• 建议进行完整的技术分析
• 需要配置相关API密钥获取实时数据

风险提示:
• 此为基础模式演示
• 实际投资请谨慎决策
• 建议使用完整的TradingAgent功能

注: 配置API密钥后可获得详细的多智能体分析报告。
"""
            
            console.print("\n[green]✅ 基础分析完成![/green]")
            console.print(analysis_result)
            
        except Exception as e:
            console.print(f"[red]❌ 股票分析失败: {str(e)}[/red]")
    
    def _basic_market_analysis(self, console):
        """基础市场分析"""
        console.print("\n[bold cyan]📈 市场趋势分析[/bold cyan]")
        
        try:
            market = console.input("请选择市场 (US/CN): ").strip().upper()
            if market not in ['US', 'CN']:
                console.print("[red]❌ 请输入 US (美股) 或 CN (A股)[/red]")
                return
            
            console.print(f"\n[yellow]正在分析{market}市场趋势...[/yellow]")
            
            market_name = "美股市场" if market == "US" else "中国A股市场"
            
            analysis_result = f"""
{market_name}趋势分析:

市场概况:
• 市场类型: {market_name}
• 分析模式: 基础模式
• 数据来源: 模拟数据

趋势分析:
• 当前市场情绪: 需要实时数据分析
• 主要指数表现: 需要配置数据源
• 行业热点: 需要新闻和社交媒体分析

投资建议:
• 建议使用完整的TradingAgent功能
• 配置相关API密钥获取实时数据
• 进行多智能体协作分析

注: 此为基础模式演示，实际分析需要完整配置。
"""
            
            console.print("\n[green]✅ 市场分析完成![/green]")
            console.print(analysis_result)
            
        except Exception as e:
            console.print(f"[red]❌ 市场分析失败: {str(e)}[/red]")
    
    def _trading_system_status(self, console):
        """交易系统状态检查"""
        console.print("\n[bold cyan]🔧 TradingAgent系统状态检查[/bold cyan]")
        
        try:
            # 检查API密钥状态
            api_status = self.config_manager.check_api_keys("trading")
            
            console.print("\n[bold]API密钥状态:[/bold]")
            for api_name, is_configured in api_status.items():
                if "finnhub" in api_name or any(llm in api_name for llm in ["dashscope", "openai", "google", "anthropic"]):
                    status_text = "✅ 已配置" if is_configured else "❌ 未配置"
                    console.print(f"  • {api_name}: {status_text}")
            
            # 检查市场支持
            markets = self.get_supported_markets()
            console.print("\n[bold]支持的市场:[/bold]")
            for market, config in markets.items():
                status = "✅ 启用" if config.get("enabled") else "❌ 禁用"
                console.print(f"  • {market}: {status}")
            
            # 检查分析师
            analysts = self.get_available_analysts()
            console.print(f"\n[bold]可用分析师:[/bold]")
            console.print(f"  • {', '.join(analysts)}")
            
        except Exception as e:
            console.print(f"[red]❌ 状态检查失败: {str(e)}[/red]")
    
    def validate_trading_config(self) -> Dict[str, Any]:
        """验证TradingAgent配置"""
        return self.config_manager.validate_config("trading") 