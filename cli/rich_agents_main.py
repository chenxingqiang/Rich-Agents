"""
Rich-Agents 统一CLI主入口
支持TradingAgent和PatentAgent两种智能体工具的选择
"""

import os
import sys
import typer
import logging
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich import box

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入共享组件
from shared.config.rich_agents_config_manager import RichAgentsConfigManager
from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter

# 导入子CLI
from cli.trading_cli import TradingAgentCLI
from cli.patent_cli import PatentAgentCLI

console = Console()
logger = logging.getLogger(__name__)

# 创建typer应用
app = typer.Typer(
    name="Rich-Agents",
    help="Rich-Agents: 多智能体AI工具集 - 支持金融交易分析和专利智能体",
    add_completion=True,
)


class RichAgentsCLI:
    """Rich-Agents统一CLI类"""
    
    def __init__(self):
        """初始化Rich-Agents CLI"""
        try:
            self.config_manager = RichAgentsConfigManager()
            
            # 初始化子CLI
            self.trading_cli = None
            self.patent_cli = None
            
            logger.info("Rich-Agents CLI初始化完成")
        except Exception as e:
            console.print(f"[red]❌ 初始化失败: {str(e)}[/red]")
            logger.error(f"Rich-Agents CLI初始化失败: {str(e)}")
    
    def show_welcome(self):
        """显示欢迎界面"""
        welcome_text = """
╔═══════════════════════════════════════════════════════════════════╗
║                        Rich-Agents                                ║
║                    多智能体AI工具集                                 ║
║                                                                   ║
║  🏦 TradingAgent  |  🔬 PatentAgent  |  ⚙️ 系统配置              ║
║                                                                   ║
║            将AI技术深度应用于专业领域                              ║
╚═══════════════════════════════════════════════════════════════════╝

[bold green]欢迎使用Rich-Agents！[/bold green]

Rich-Agents是一个统一的多智能体AI工具集，目前支持两个专业领域：

🏦 [bold blue]TradingAgent[/bold blue] - 多智能体金融交易分析框架
   • 市场分析师、情绪分析师、新闻分析师、基本面分析师
   • 多智能体协作研究和辩论
   • 风险管理和投资组合管理
   • 支持美股和A股市场

🔬 [bold cyan]PatentAgent[/bold cyan] - 专利发现、验证、分析与撰写系统
   • 技术创新发现和专利机会识别
   • 专利可行性验证和风险评估
   • 专利价值分析和商业价值评估
   • 专利申请文档撰写和质量评估

请选择您需要的智能体工具：

1. 🏦 [bold blue]TradingAgent[/bold blue] - 启动金融交易分析工具
2. 🔬 [bold cyan]PatentAgent[/bold cyan] - 启动专利智能体工具
3. ⚙️ [bold yellow]系统配置[/bold yellow] - 配置管理和状态检查
4. 📖 [bold green]帮助信息[/bold green] - 查看详细使用说明
5. 🚪 [bold red]退出系统[/bold red]

"""
        console.print(Panel(welcome_text, border_style="green", padding=(1, 2)))
    
    def get_user_choice(self) -> str:
        """获取用户选择"""
        while True:
            try:
                choice = console.input("[bold yellow]请输入您的选择 (1-5): [/bold yellow]").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    return choice
                else:
                    console.print("[red]❌ 无效选择，请输入1-5之间的数字[/red]")
            except KeyboardInterrupt:
                console.print("\n\n[yellow]👋 感谢使用Rich-Agents！[/yellow]")
                sys.exit(0)
            except Exception as e:
                console.print(f"[red]❌ 输入错误: {str(e)}[/red]")
    
    def run_trading_agent(self):
        """运行TradingAgent"""
        try:
            if self.trading_cli is None:
                from cli.trading_cli import TradingAgentCLI
                self.trading_cli = TradingAgentCLI(self.config_manager)
            
            console.print("\n[bold blue]🏦 启动TradingAgent - 金融交易分析工具[/bold blue]")
            console.print("[dim]正在初始化交易智能体...[/dim]")
            
            self.trading_cli.run()
            
        except ImportError as e:
            console.print(f"[red]❌ 无法导入TradingAgent模块: {str(e)}[/red]")
            console.print("[yellow]请确保已正确安装TradingAgent相关依赖[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ TradingAgent运行失败: {str(e)}[/red]")
            logger.error(f"TradingAgent运行失败: {str(e)}")
    
    def run_patent_agent(self):
        """运行PatentAgent"""
        try:
            if self.patent_cli is None:
                from cli.patent_cli import PatentAgentCLI
                self.patent_cli = PatentAgentCLI(self.config_manager)
            
            console.print("\n[bold cyan]🔬 启动PatentAgent - 专利智能体工具[/bold cyan]")
            console.print("[dim]正在初始化专利智能体...[/dim]")
            
            self.patent_cli.run()
            
        except ImportError as e:
            console.print(f"[red]❌ 无法导入PatentAgent模块: {str(e)}[/red]")
            console.print("[yellow]请确保已正确安装PatentAgent相关依赖[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ PatentAgent运行失败: {str(e)}[/red]")
            logger.error(f"PatentAgent运行失败: {str(e)}")
    
    def show_system_config(self):
        """显示系统配置"""
        console.print("\n[bold yellow]⚙️ 系统配置和状态检查[/bold yellow]")
        console.print("=" * 60)
        
        try:
            # 获取系统状态
            status = self.config_manager.get_system_status()
            
            # 显示基本信息
            info_table = Table(title="系统信息", box=box.ROUNDED)
            info_table.add_column("项目", style="cyan")
            info_table.add_column("值", style="green")
            
            info_table.add_row("版本", status.get("version", "unknown"))
            info_table.add_row("可用智能体", ", ".join(status.get("available_agents", [])))
            info_table.add_row("LLM提供商", ", ".join(status.get("available_llm_providers", [])))
            
            console.print(info_table)
            
            # 显示API密钥状态
            api_status = status.get("api_keys_status", {})
            
            api_table = Table(title="API密钥状态", box=box.ROUNDED)
            api_table.add_column("API", style="cyan")
            api_table.add_column("状态", style="green")
            api_table.add_column("说明", style="yellow")
            
            for api_name, is_configured in api_status.items():
                status_text = "✅ 已配置" if is_configured else "❌ 未配置"
                status_style = "green" if is_configured else "red"
                
                description = self._get_api_description(api_name)
                
                api_table.add_row(
                    api_name,
                    f"[{status_style}]{status_text}[/{status_style}]",
                    description
                )
            
            console.print(api_table)
            
            # 显示缓存配置
            cache_config = status.get("cache_config", {})
            console.print(f"\n[bold]缓存配置:[/bold]")
            console.print(f"  • 缓存启用: {'✅' if cache_config.get('enabled') else '❌'}")
            console.print(f"  • 缓存类型: {cache_config.get('type', 'unknown')}")
            console.print(f"  • MongoDB: {'✅' if cache_config.get('mongodb', {}).get('enabled') else '❌'}")
            console.print(f"  • Redis: {'✅' if cache_config.get('redis', {}).get('enabled') else '❌'}")
            
            # 配置验证
            validation_result = self.config_manager.validate_config()
            console.print(f"\n[bold]配置验证:[/bold]")
            if validation_result["valid"]:
                console.print("  ✅ 配置有效")
            else:
                console.print("  ❌ 配置存在问题")
                for error in validation_result["errors"]:
                    console.print(f"    • [red]{error}[/red]")
            
            if validation_result["warnings"]:
                console.print("  ⚠️ 警告:")
                for warning in validation_result["warnings"]:
                    console.print(f"    • [yellow]{warning}[/yellow]")
            
        except Exception as e:
            console.print(f"[red]❌ 获取系统状态失败: {str(e)}[/red]")
        
        console.print("\n" + "=" * 60)
    
    def _get_api_description(self, api_name: str) -> str:
        """获取API描述"""
        descriptions = {
            "dashscope_api": "百炼大模型 (阿里云)",
            "openai_api": "OpenAI GPT模型",
            "google_api": "Google Gemini模型",
            "anthropic_api": "Anthropic Claude模型",
            "finnhub_api": "金融数据 (TradingAgent)",
            "serpapi_api": "Google Patents (PatentAgent)",
            "zhihuiya_client_id": "智慧芽客户端ID (PatentAgent)",
            "zhihuiya_client_secret": "智慧芽客户端密钥 (PatentAgent)"
        }
        return descriptions.get(api_name, "未知API")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
📖 [bold]Rich-Agents 使用指南[/bold]

🎯 [bold]主要功能:[/bold]

🏦 [bold blue]TradingAgent - 金融交易分析[/bold blue]
   • 多智能体协作分析 (市场、情绪、新闻、基本面)
   • 支持美股和A股市场
   • 风险管理和投资组合管理
   • 实时数据分析和交易决策

🔬 [bold cyan]PatentAgent - 专利智能体[/bold cyan]
   • 技术创新发现和机会识别
   • 专利可行性验证和风险评估  
   • 专利价值分析和商业评估
   • 专利申请文档撰写

🔧 [bold]系统要求:[/bold]
   • Python 3.10+
   • 配置相关API密钥
   • 稳定的网络连接

📝 [bold]使用流程:[/bold]
   1. 选择智能体工具 (TradingAgent 或 PatentAgent)
   2. 根据提示输入分析参数
   3. 系统自动进行多智能体协作分析
   4. 查看分析结果和建议
   5. 可选择保存结果到本地文件

🔑 [bold]API配置:[/bold]
   请在环境变量中设置以下API密钥:
   
   [bold]LLM提供商:[/bold]
   • DASHSCOPE_API_KEY - 百炼大模型API密钥
   • OPENAI_API_KEY - OpenAI API密钥  
   • GOOGLE_API_KEY - Google API密钥
   • ANTHROPIC_API_KEY - Anthropic API密钥
   
   [bold]TradingAgent专用:[/bold]
   • FINNHUB_API_KEY - 金融数据API密钥
   
   [bold]PatentAgent专用:[/bold]
   • SERPAPI_API_KEY - Google Patents检索API密钥
   • ZHIHUIYA_CLIENT_ID - 智慧芽客户端ID
   • ZHIHUIYA_CLIENT_SECRET - 智慧芽客户端密钥

📞 [bold]技术支持:[/bold]
   如遇问题，请检查:
   1. API密钥是否正确配置
   2. 网络连接是否正常
   3. 依赖库是否完整安装
   4. 系统日志中的错误信息

🌟 [bold]最佳实践:[/bold]
   • 确保API密钥有效且有足够配额
   • 定期检查系统状态和配置
   • 保存重要的分析结果
   • 合理设置分析参数

"""
        console.print(Panel(help_text, border_style="blue", padding=(1, 2)))
    
    def run(self):
        """运行主循环"""
        try:
            while True:
                self.show_welcome()
                choice = self.get_user_choice()
                
                if choice == '1':  # TradingAgent
                    self.run_trading_agent()
                elif choice == '2':  # PatentAgent
                    self.run_patent_agent()
                elif choice == '3':  # 系统配置
                    self.show_system_config()
                elif choice == '4':  # 帮助信息
                    self.show_help()
                elif choice == '5':  # 退出系统
                    console.print("\n[yellow]👋 感谢使用Rich-Agents！[/yellow]")
                    break
                
                # 询问是否继续
                if choice in ['1', '2']:
                    while True:
                        try:
                            continue_choice = console.input(
                                "\n[bold yellow]🔄 是否继续使用Rich-Agents? (y/n): [/bold yellow]"
                            ).strip().lower()
                            
                            if continue_choice in ['y', 'yes', '是', 'Y']:
                                break
                            elif continue_choice in ['n', 'no', '否', 'N']:
                                console.print("\n[yellow]👋 感谢使用Rich-Agents！[/yellow]")
                                return
                            else:
                                console.print("[red]❌ 请输入 y(是) 或 n(否)[/red]")
                        except KeyboardInterrupt:
                            console.print("\n\n[yellow]👋 感谢使用Rich-Agents！[/yellow]")
                            return
                
        except KeyboardInterrupt:
            console.print("\n\n[yellow]👋 感谢使用Rich-Agents！[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ 系统错误: {str(e)}[/red]")
            logger.error(f"Rich-Agents CLI运行错误: {str(e)}")


# Typer命令行接口
@app.command()
def main(
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="直接启动指定智能体 (trading/patent)"),
    config_dir: Optional[str] = typer.Option(None, "--config", "-c", help="配置文件目录"),
    debug: bool = typer.Option(False, "--debug", "-d", help="启用调试模式")
):
    """
    Rich-Agents 统一CLI入口
    
    支持TradingAgent和PatentAgent两种智能体工具
    """
    # 配置日志
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    try:
        cli = RichAgentsCLI()
        
        # 如果指定了智能体类型，直接启动
        if agent:
            if agent.lower() == "trading":
                cli.run_trading_agent()
            elif agent.lower() == "patent":
                cli.run_patent_agent()
            else:
                console.print(f"[red]❌ 不支持的智能体类型: {agent}[/red]")
                console.print("[yellow]支持的类型: trading, patent[/yellow]")
                return
        else:
            # 否则启动交互式界面
            cli.run()
            
    except Exception as e:
        console.print(f"[red]❌ 启动失败: {str(e)}[/red]")
        logger.error(f"Rich-Agents CLI启动失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app() 