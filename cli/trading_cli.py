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
from cli.main import run_analysis as run_trading_analysis
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
            run_trading_analysis()
            
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
    
    def validate_trading_config(self) -> Dict[str, Any]:
        """验证TradingAgent配置"""
        return self.config_manager.validate_config("trading") 