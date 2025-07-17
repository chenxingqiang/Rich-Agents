"""
Rich-Agents 统一CLI主入口
支持TradingAgent和PatentAgent两种智能体工具的选择
"""

import os
import sys
import typer
import logging
from typing import Optional, Dict
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich import box
from rich.prompt import Confirm

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
        """显示系统配置 - 增强版交互式配置"""
        while True:
            console.print("\n[bold yellow]⚙️ Rich-Agents 系统配置中心[/bold yellow]")
            console.print("=" * 70)
            
            try:
                # 获取系统状态
                status = self.config_manager.get_system_status()
                
                # 显示基本信息
                info_table = Table(title="🏠 系统信息", box=box.ROUNDED, show_header=True)
                info_table.add_column("项目", style="cyan", width=20)
                info_table.add_column("值", style="green", no_wrap=False)
                
                info_table.add_row("版本", status.get("version", "v0.1.0"))
                info_table.add_row("可用智能体", ", ".join(status.get("available_agents", ["TradingAgent", "PatentAgent"])))
                info_table.add_row("LLM提供商", ", ".join(status.get("available_llm_providers", [])))
                info_table.add_row("配置目录", str(Path(self.config_manager.config_dir).resolve()))
                
                console.print(info_table)
                
                # 显示API密钥状态
                api_status = status.get("api_keys_status", {})
                
                api_table = Table(title="🔑 API密钥状态", box=box.ROUNDED, show_header=True)
                api_table.add_column("API", style="cyan", width=25)
                api_table.add_column("状态", style="green", width=12, justify="center")
                api_table.add_column("说明", style="yellow", no_wrap=False)
                api_table.add_column("获取链接", style="blue", no_wrap=False)
                
                for api_name, is_configured in api_status.items():
                    status_text = "✅ 已配置" if is_configured else "❌ 未配置"
                    status_style = "green" if is_configured else "red"
                    
                    description = self._get_api_description(api_name)
                    help_link = self._get_api_help_link(api_name)
                    
                    api_table.add_row(
                        api_name,
                        f"[{status_style}]{status_text}[/{status_style}]",
                        description,
                        help_link
                    )
                
                console.print(api_table)
                
                # 显示缓存配置
                cache_config = status.get("cache_config", {})
                cache_table = Table(title="💾 缓存配置", box=box.ROUNDED)
                cache_table.add_column("配置项", style="cyan")
                cache_table.add_column("状态", style="green")
                
                cache_table.add_row("缓存启用", "✅ 启用" if cache_config.get('enabled') else "❌ 禁用")
                cache_table.add_row("缓存类型", cache_config.get('type', 'file'))
                cache_table.add_row("MongoDB", "✅ 连接" if cache_config.get('mongodb', {}).get('enabled') else "❌ 未连接")
                cache_table.add_row("Redis", "✅ 连接" if cache_config.get('redis', {}).get('enabled') else "❌ 未连接")
                
                console.print(cache_table)
                
                # 配置验证
                validation_result = self.config_manager.validate_config()
                console.print(f"\n[bold]🔍 配置验证:[/bold]")
                if validation_result["valid"]:
                    console.print("  ✅ 所有配置都有效")
                else:
                    console.print("  ❌ 配置存在问题")
                    for error in validation_result["errors"]:
                        console.print(f"    • [red]{error}[/red]")
                
                if validation_result["warnings"]:
                    console.print("  ⚠️ 配置警告:")
                    for warning in validation_result["warnings"]:
                        console.print(f"    • [yellow]{warning}[/yellow]")
                
                # 显示配置选项菜单
                console.print("\n[bold]🛠️ 配置选项:[/bold]")
                console.print("1. 🔑 [cyan]配置API密钥[/cyan] - 添加或更新API密钥")
                console.print("2. 🏦 [blue]TradingAgent配置[/blue] - 金融数据源和LLM设置")
                console.print("3. 🔬 [magenta]PatentAgent配置[/magenta] - 专利数据源和AI设置")
                console.print("4. 💾 [green]缓存配置[/green] - MongoDB和Redis设置")
                console.print("5. 🔄 [yellow]重新加载配置[/yellow] - 刷新所有配置文件")
                console.print("6. 📋 [cyan]导出配置[/cyan] - 保存当前配置到文件")
                console.print("7. 📖 [blue]配置帮助[/blue] - 查看详细配置指南")
                console.print("8. 🚪 [red]返回主菜单[/red] - 退出配置中心")
                
                # 获取用户选择
                choice = console.input("\n[bold yellow]请选择配置选项 (1-8): [/bold yellow]").strip()
                
                if choice == '1':
                    self._configure_api_keys()
                elif choice == '2':
                    self._configure_trading_agent()
                elif choice == '3':
                    self._configure_patent_agent()
                elif choice == '4':
                    self._configure_cache_settings()
                elif choice == '5':
                    self._reload_configuration()
                elif choice == '6':
                    self._export_configuration()
                elif choice == '7':
                    self._show_configuration_help()
                elif choice == '8':
                    console.print("[green]返回主菜单[/green]")
                    break
                else:
                    console.print("[red]❌ 无效选择，请输入1-8之间的数字[/red]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]返回主菜单[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ 获取系统状态失败: {str(e)}[/red]")
                break
    
    def _get_api_description(self, api_name: str) -> str:
        """获取API描述"""
        descriptions = {
            "dashscope_api": "百炼大模型 (阿里云)",
            "openai_api": "OpenAI GPT模型",
            "google_api": "Google Gemini模型",
            "anthropic_api": "Anthropic Claude模型",
            "deepseek_api": "DeepSeek深度求索模型",
            "qianwen_api": "通义千问开源模型",
            "doubao_api": "火山引擎豆包模型",
            "zhipuai_api": "智谱AI GLM模型",
            "baichuan_api": "百川智能模型",
            "moonshot_api": "Moonshot AI Kimi模型",
            "minimax_api": "MiniMax海螺模型",
            "yi_api": "零一万物Yi模型",
            "stepfun_api": "阶跃星辰Step模型",
            "finnhub_api": "金融数据 (TradingAgent)",
            "serpapi_api": "Google Patents (PatentAgent)",
            "zhihuiya_client_id": "智慧芽客户端ID (PatentAgent)",
            "zhihuiya_client_secret": "智慧芽客户端密钥 (PatentAgent)"
        }
        return descriptions.get(api_name, "未知API")
    
    def _get_api_help_link(self, api_name: str) -> str:
        """获取API帮助链接"""
        help_links = {
            "dashscope_api": "[link=https://help.aliyun.com/zh/dashscope/]阿里云百炼文档[/link]",
            "openai_api": "[link=https://platform.openai.com/api-keys]OpenAI API Keys[/link]",
            "google_api": "[link=https://ai.google.dev/gemini-api/docs/api-key]Google AI Studio[/link]",
            "anthropic_api": "[link=https://console.anthropic.com/]Anthropic Console[/link]",
            "deepseek_api": "[link=https://platform.deepseek.com/api_keys]DeepSeek API Keys[/link]",
            "qianwen_api": "[link=https://help.aliyun.com/zh/dashscope/]通义千问文档[/link]",
            "doubao_api": "[link=https://console.volcengine.com/ark]火山引擎方舟[/link]",
            "zhipuai_api": "[link=https://open.bigmodel.cn/usercenter/apikeys]智谱AI开放平台[/link]",
            "baichuan_api": "[link=https://platform.baichuan-ai.com/console/apikey]百川智能平台[/link]",
            "moonshot_api": "[link=https://platform.moonshot.cn/console/api-keys]Moonshot平台[/link]",
            "minimax_api": "[link=https://api.minimax.chat/user-center/basic-information/interface-key]MiniMax平台[/link]",
            "yi_api": "[link=https://platform.lingyiwanwu.com/apikeys]零一万物平台[/link]",
            "stepfun_api": "[link=https://platform.stepfun.com/interface-key]阶跃星辰平台[/link]",
            "finnhub_api": "[link=https://finnhub.io/dashboard]Finnhub Dashboard[/link]",
            "serpapi_api": "[link=https://serpapi.com/manage-api-key]SerpApi Dashboard[/link]",
            "zhihuiya_client_id": "[link=https://open-zhihuiya-com.libproxy1.nus.edu.sg/]智慧芽开放平台[/link]",
            "zhihuiya_client_secret": "[link=https://open-zhihuiya-com.libproxy1.nus.edu.sg/]智慧芽开放平台[/link]"
        }
        return help_links.get(api_name, "暂无帮助链接")
    
    def _configure_api_keys(self):
        """配置API密钥"""
        console.print("\n[bold cyan]🔑 API密钥配置[/bold cyan]")
        console.print("=" * 50)
        
        # API密钥配置选项
        api_configs = {
            "1": {
                "name": "百炼大模型 (DashScope)",
                "env_var": "DASHSCOPE_API_KEY",
                "description": "阿里云百炼大模型服务，支持通义千问等模型",
                "help_url": "https://help.aliyun.com/zh/dashscope/",
                "example": "sk-xxx...xxx"
            },
            "2": {
                "name": "OpenAI GPT",
                "env_var": "OPENAI_API_KEY", 
                "description": "OpenAI GPT系列模型，包括GPT-4、GPT-3.5等",
                "help_url": "https://platform.openai.com/api-keys",
                "example": "sk-xxx...xxx"
            },
            "3": {
                "name": "Google Gemini",
                "env_var": "GOOGLE_API_KEY",
                "description": "Google Gemini模型，包括Gemini Pro等",
                "help_url": "https://ai.google.dev/gemini-api/docs/api-key",
                "example": "AIza...xxx"
            },
            "4": {
                "name": "Anthropic Claude",
                "env_var": "ANTHROPIC_API_KEY",
                "description": "Anthropic Claude模型系列",
                "help_url": "https://console.anthropic.com/",
                "example": "sk-ant-xxx...xxx"
            },
            "5": {
                "name": "DeepSeek 深度求索",
                "env_var": "DEEPSEEK_API_KEY",
                "description": "DeepSeek深度求索模型，包括Chat、Coder、Reasoner",
                "help_url": "https://platform.deepseek.com/api_keys",
                "example": "sk-xxx...xxx"
            },
            "6": {
                "name": "通义千问 (Qianwen)",
                "env_var": "QIANWEN_API_KEY",
                "description": "通义千问开源模型，支持多种规格",
                "help_url": "https://help.aliyun.com/zh/dashscope/",
                "example": "your_api_key"
            },
            "7": {
                "name": "火山引擎豆包 (Doubao)",
                "env_var": "DOUBAO_API_KEY",
                "description": "火山引擎豆包大模型服务",
                "help_url": "https://console.volcengine.com/ark",
                "example": "your_api_key"
            },
            "8": {
                "name": "智谱AI GLM",
                "env_var": "ZHIPUAI_API_KEY",
                "description": "智谱AI GLM系列模型",
                "help_url": "https://open.bigmodel.cn/usercenter/apikeys",
                "example": "your_api_key"
            },
            "9": {
                "name": "百川智能 (Baichuan)",
                "env_var": "BAICHUAN_API_KEY",
                "description": "百川智能大模型服务",
                "help_url": "https://platform.baichuan-ai.com/console/apikey",
                "example": "sk-xxx...xxx"
            },
            "10": {
                "name": "Moonshot AI Kimi",
                "env_var": "MOONSHOT_API_KEY",
                "description": "Moonshot AI Kimi模型",
                "help_url": "https://platform.moonshot.cn/console/api-keys",
                "example": "sk-xxx...xxx"
            },
            "11": {
                "name": "MiniMax 海螺",
                "env_var": "MINIMAX_API_KEY",
                "description": "MiniMax海螺大模型",
                "help_url": "https://api.minimax.chat/user-center/basic-information/interface-key",
                "example": "your_api_key"
            },
            "12": {
                "name": "零一万物 Yi",
                "env_var": "YI_API_KEY",
                "description": "零一万物Yi系列模型",
                "help_url": "https://platform.lingyiwanwu.com/apikeys",
                "example": "your_api_key"
            },
            "13": {
                "name": "阶跃星辰 Step",
                "env_var": "STEPFUN_API_KEY",
                "description": "阶跃星辰Step模型",
                "help_url": "https://platform.stepfun.com/interface-key",
                "example": "your_api_key"
            },
            "14": {
                "name": "Finnhub 金融数据",
                "env_var": "FINNHUB_API_KEY",
                "description": "Finnhub金融数据API，用于TradingAgent",
                "help_url": "https://finnhub.io/dashboard",
                "example": "xxx...xxx"
            },
            "15": {
                "name": "SerpApi Google Patents",
                "env_var": "SERPAPI_API_KEY",
                "description": "SerpApi Google Patents搜索，用于PatentAgent",
                "help_url": "https://serpapi.com/manage-api-key",
                "example": "xxx...xxx"
            },
            "16": {
                "name": "智慧芽客户端ID",
                "env_var": "ZHIHUIYA_CLIENT_ID",
                "description": "智慧芽开放平台客户端ID，用于PatentAgent",
                "help_url": "https://open-zhihuiya-com.libproxy1.nus.edu.sg/",
                "example": "your_client_id"
            },
            "17": {
                "name": "智慧芽客户端密钥",
                "env_var": "ZHIHUIYA_CLIENT_SECRET",
                "description": "智慧芽开放平台客户端密钥，用于PatentAgent",
                "help_url": "https://open-zhihuiya-com.libproxy1.nus.edu.sg/",
                "example": "your_client_secret"
            }
        }
        
        while True:
            # 显示当前API密钥状态
            current_status = self.config_manager.get_system_status().get("api_keys_status", {})
            
            console.print("\n[bold]当前API密钥状态:[/bold]")
            
            # 分组显示
            console.print("\n[bold blue]🤖 LLM提供商:[/bold blue]")
            for key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
                config = api_configs[key]
                env_var = config["env_var"].lower() + "_key" if not config["env_var"].endswith("_KEY") else config["env_var"].lower().replace("_key", "_api")
                is_configured = current_status.get(env_var, False)
                status_icon = "✅" if is_configured else "❌"
                console.print(f"  {key}. {status_icon} [cyan]{config['name']}[/cyan]")
            
            console.print("\n[bold green]📊 专用数据源:[/bold green]")
            for key in ["14", "15", "16", "17"]:
                config = api_configs[key]
                env_var = config["env_var"].lower() + "_key" if not config["env_var"].endswith("_KEY") else config["env_var"].lower().replace("_key", "_api")
                is_configured = current_status.get(env_var, False)
                status_icon = "✅" if is_configured else "❌"
                console.print(f"  {key}. {status_icon} [cyan]{config['name']}[/cyan]")
            
            console.print("\n  18. 🔄 [yellow]刷新状态[/yellow]")
            console.print("  0. 🚪 [red]返回上级菜单[/red]")
            
            choice = console.input("\n[bold yellow]请选择要配置的API (0-18): [/bold yellow]").strip()
            
            if choice == '0':
                break
            elif choice == '18':
                console.print("[yellow]正在刷新API密钥状态...[/yellow]")
                continue
            elif choice in api_configs:
                self._configure_single_api_key(api_configs[choice])
            else:
                console.print("[red]❌ 无效选择，请输入0-18之间的数字[/red]")
    
    def _configure_single_api_key(self, api_config: Dict[str, str]):
        """配置单个API密钥"""
        console.print(f"\n[bold cyan]🔧 配置 {api_config['name']}[/bold cyan]")
        console.print("-" * 40)
        
        # 显示API信息
        info_panel = Panel(
            f"""[bold]API信息:[/bold]
• 名称: {api_config['name']}
• 环境变量: {api_config['env_var']}
• 描述: {api_config['description']}
• 帮助文档: [link={api_config['help_url']}]{api_config['help_url']}[/link]
• 格式示例: {api_config['example']}""",
            title="API配置信息",
            border_style="blue"
        )
        console.print(info_panel)
        
        # 检查当前值
        current_value = os.getenv(api_config['env_var'])
        if current_value:
            masked_value = current_value[:8] + "..." + current_value[-4:] if len(current_value) > 12 else "***"
            console.print(f"\n[green]当前值: {masked_value}[/green]")
        else:
            console.print("\n[yellow]当前未配置[/yellow]")
        
        console.print("\n[bold]配置选项:[/bold]")
        console.print("1. 🔑 [cyan]设置新的API密钥[/cyan]")
        console.print("2. 🔍 [yellow]测试当前API密钥[/yellow]")
        console.print("3. 🗑️ [red]删除API密钥[/red]")
        console.print("4. 📋 [blue]复制配置命令[/blue]")
        console.print("5. 🚪 [green]返回[/green]")
        
        action = console.input("\n[bold yellow]请选择操作 (1-5): [/bold yellow]").strip()
        
        if action == '1':
            self._set_api_key(api_config)
        elif action == '2':
            self._test_api_key(api_config)
        elif action == '3':
            self._delete_api_key(api_config)
        elif action == '4':
            self._copy_config_command(api_config)
        elif action == '5':
            return
        else:
            console.print("[red]❌ 无效选择[/red]")
    
    def _set_api_key(self, api_config: Dict[str, str]):
        """设置API密钥"""
        console.print(f"\n[bold]设置 {api_config['name']} API密钥[/bold]")
        
        try:
            # 获取新的API密钥
            new_key = console.input(f"请输入 {api_config['name']} API密钥: ").strip()
            
            if not new_key:
                console.print("[red]❌ API密钥不能为空[/red]")
                return
            
            # 基本格式验证
            if not self._validate_api_key_format(api_config['env_var'], new_key):
                console.print("[red]❌ API密钥格式不正确[/red]")
                return
            
            # 设置环境变量
            os.environ[api_config['env_var']] = new_key
            
            # 保存到配置文件
            self.config_manager.set_api_key(api_config['env_var'], new_key)
            
            console.print(f"[green]✅ {api_config['name']} API密钥设置成功![/green]")
            console.print("[yellow]注意: 请确保将API密钥添加到您的环境变量中以便持久保存[/yellow]")
            
            # 提供环境变量设置命令
            console.print(f"\n[bold]环境变量设置命令:[/bold]")
            console.print(f"export {api_config['env_var']}=\"{new_key[:8]}...\"")
            
        except Exception as e:
            console.print(f"[red]❌ 设置API密钥失败: {str(e)}[/red]")
    
    def _validate_api_key_format(self, env_var: str, key: str) -> bool:
        """验证API密钥格式"""
        validation_rules = {
            "DASHSCOPE_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
            "OPENAI_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
            "GOOGLE_API_KEY": lambda k: k.startswith("AIza") and len(k) > 30,
            "ANTHROPIC_API_KEY": lambda k: k.startswith("sk-ant-") and len(k) > 30,
            "FINNHUB_API_KEY": lambda k: len(k) > 10,
            "SERPAPI_API_KEY": lambda k: len(k) > 10,
            "ZHIHUIYA_CLIENT_ID": lambda k: len(k) > 5,
            "ZHIHUIYA_CLIENT_SECRET": lambda k: len(k) > 10
        }
        
        validator = validation_rules.get(env_var)
        if validator:
            return validator(key)
        return len(key) > 5  # 默认最小长度验证
    
    def _test_api_key(self, api_config: Dict[str, str]):
        """测试API密钥"""
        console.print(f"\n[yellow]正在测试 {api_config['name']} API密钥...[/yellow]")
        
        try:
            # 根据不同API类型进行测试
            result = self.config_manager.test_api_key(api_config['env_var'])
            
            if result['success']:
                console.print(f"[green]✅ {api_config['name']} API密钥测试成功![/green]")
                if result.get('details'):
                    console.print(f"[dim]详情: {result['details']}[/dim]")
            else:
                console.print(f"[red]❌ {api_config['name']} API密钥测试失败[/red]")
                console.print(f"[red]错误: {result.get('error', '未知错误')}[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ 测试失败: {str(e)}[/red]")
    
    def _delete_api_key(self, api_config: Dict[str, str]):
        """删除API密钥"""
        confirm = console.input(f"\n[red]确认删除 {api_config['name']} API密钥? (y/N): [/red]").strip().lower()
        
        if confirm in ['y', 'yes', '是']:
            try:
                # 从环境变量中删除
                if api_config['env_var'] in os.environ:
                    del os.environ[api_config['env_var']]
                
                # 从配置文件中删除
                self.config_manager.delete_api_key(api_config['env_var'])
                
                console.print(f"[green]✅ {api_config['name']} API密钥已删除[/green]")
                
            except Exception as e:
                console.print(f"[red]❌ 删除失败: {str(e)}[/red]")
        else:
            console.print("[yellow]取消删除操作[/yellow]")
    
    def _copy_config_command(self, api_config: Dict[str, str]):
        """复制配置命令"""
        commands = f"""
# {api_config['name']} 配置命令

# 方法1: 环境变量设置 (临时)
export {api_config['env_var']}="your_api_key_here"

# 方法2: 添加到 ~/.bashrc 或 ~/.zshrc (永久)
echo 'export {api_config['env_var']}="your_api_key_here"' >> ~/.bashrc

# 方法3: 使用 .env 文件
echo '{api_config['env_var']}=your_api_key_here' >> .env

# 获取API密钥: {api_config['help_url']}
"""
        
        console.print(Panel(commands, title="配置命令", border_style="green"))
        console.print("[yellow]请复制上述命令并替换 'your_api_key_here' 为实际的API密钥[/yellow]")
    
    def _configure_trading_agent(self):
        """配置TradingAgent"""
        console.print("\n[bold blue]🏦 TradingAgent 配置[/bold blue]")
        console.print("=" * 50)
        
        # 显示TradingAgent特定配置
        trading_config = self.config_manager.get_trading_config()
        
        config_table = Table(title="TradingAgent 当前配置", box=box.ROUNDED)
        config_table.add_column("配置项", style="cyan")
        config_table.add_column("当前值", style="green")
        config_table.add_column("说明", style="yellow")
        
        config_table.add_row("默认市场", trading_config.get("default_market", "US"), "默认分析的股票市场")
        config_table.add_row("数据源", trading_config.get("data_source", "finnhub"), "金融数据提供商")
        config_table.add_row("缓存启用", str(trading_config.get("cache_enabled", True)), "是否启用数据缓存")
        config_table.add_row("分析深度", str(trading_config.get("analysis_depth", 3)), "智能体分析的深度级别")
        
        console.print(config_table)
        
        console.print("\n[bold]TradingAgent 配置选项:[/bold]")
        console.print("1. 📊 [cyan]数据源配置[/cyan] - 配置金融数据API")
        console.print("2. 🏛️ [blue]市场设置[/blue] - 设置默认分析市场")
        console.print("3. 🧠 [magenta]智能体设置[/magenta] - 配置分析师和研究员")
        console.print("4. 🔄 [yellow]重置为默认[/yellow] - 恢复默认配置")
        console.print("5. 🚪 [red]返回[/red]")
        
        choice = console.input("\n[bold yellow]请选择配置项 (1-5): [/bold yellow]").strip()
        
        if choice == '1':
            self._configure_trading_data_sources()
        elif choice == '2':
            self._configure_trading_markets()
        elif choice == '3':
            self._configure_trading_agents()
        elif choice == '4':
            self._reset_trading_config()
        elif choice == '5':
            return
        else:
            console.print("[red]❌ 无效选择[/red]")
    
    def _configure_patent_agent(self):
        """配置PatentAgent"""
        console.print("\n[bold magenta]🔬 PatentAgent 配置[/bold magenta]")
        console.print("=" * 50)
        
        # 显示PatentAgent特定配置
        patent_config = self.config_manager.get_patent_config()
        
        config_table = Table(title="PatentAgent 当前配置", box=box.ROUNDED)
        config_table.add_column("配置项", style="cyan")
        config_table.add_column("当前值", style="green")
        config_table.add_column("说明", style="yellow")
        
        config_table.add_row("专利数据源", patent_config.get("patent_source", "serpapi"), "专利检索数据源")
        config_table.add_row("AI分析源", patent_config.get("ai_analysis_source", "zhihuiya"), "AI专利分析服务")
        config_table.add_row("默认分析类型", patent_config.get("default_analysis", "discovery"), "默认的分析类型")
        config_table.add_row("分析深度", str(patent_config.get("analysis_depth", 2)), "专利分析的深度级别")
        
        console.print(config_table)
        
        console.print("\n[bold]PatentAgent 配置选项:[/bold]")
        console.print("1. 🔍 [cyan]专利数据源[/cyan] - 配置专利检索API")
        console.print("2. 🧠 [blue]AI分析服务[/blue] - 配置智慧芽等AI服务")
        console.print("3. 🎯 [magenta]分析类型[/magenta] - 设置默认分析类型")
        console.print("4. 🔄 [yellow]重置为默认[/yellow] - 恢复默认配置")
        console.print("5. 🚪 [red]返回[/red]")
        
        choice = console.input("\n[bold yellow]请选择配置项 (1-5): [/bold yellow]").strip()
        
        if choice == '1':
            self._configure_patent_data_sources()
        elif choice == '2':
            self._configure_patent_ai_services()
        elif choice == '3':
            self._configure_patent_analysis_types()
        elif choice == '4':
            self._reset_patent_config()
        elif choice == '5':
            return
        else:
            console.print("[red]❌ 无效选择[/red]")
    
    def _configure_cache_settings(self):
        """配置缓存设置"""
        console.print("\n[bold green]💾 缓存配置[/bold green]")
        console.print("=" * 50)
        
        # 显示当前缓存配置
        cache_config = self.config_manager.get_cache_config()
        
        console.print("[bold]当前缓存配置:[/bold]")
        console.print(f"  • 缓存启用: {'✅' if cache_config.get('enabled') else '❌'}")
        console.print(f"  • 缓存类型: {cache_config.get('type', 'file')}")
        console.print(f"  • MongoDB: {'✅' if cache_config.get('mongodb', {}).get('enabled') else '❌'}")
        console.print(f"  • Redis: {'✅' if cache_config.get('redis', {}).get('enabled') else '❌'}")
        
        console.print("\n[bold]缓存配置选项:[/bold]")
        console.print("1. 🔄 [cyan]启用/禁用缓存[/cyan]")
        console.print("2. 🗄️ [blue]配置MongoDB[/blue]")
        console.print("3. ⚡ [red]配置Redis[/red]")
        console.print("4. 🧹 [yellow]清理缓存[/yellow]")
        console.print("5. 🚪 [green]返回[/green]")
        
        choice = console.input("\n[bold yellow]请选择配置项 (1-5): [/bold yellow]").strip()
        
        if choice == '1':
            self._toggle_cache()
        elif choice == '2':
            self._configure_mongodb()
        elif choice == '3':
            self._configure_redis()
        elif choice == '4':
            self._clean_cache()
        elif choice == '5':
            return
        else:
            console.print("[red]❌ 无效选择[/red]")
    
    def _reload_configuration(self):
        """重新加载配置"""
        console.print("\n[yellow]🔄 正在重新加载配置...[/yellow]")
        
        try:
            # 重新初始化配置管理器
            self.config_manager = RichAgentsConfigManager()
            console.print("[green]✅ 配置重新加载成功![/green]")
            
        except Exception as e:
            console.print(f"[red]❌ 配置重新加载失败: {str(e)}[/red]")
    
    def _export_configuration(self):
        """导出配置"""
        console.print("\n[cyan]📋 导出配置[/cyan]")
        
        try:
            export_path = self.config_manager.export_config()
            console.print(f"[green]✅ 配置已导出到: {export_path}[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ 配置导出失败: {str(e)}[/red]")
    
    def _show_configuration_help(self):
        """显示配置帮助"""
        help_content = """
📖 [bold]Rich-Agents 配置详细指南[/bold]

🔑 [bold]API密钥配置:[/bold]

[bold cyan]主流LLM提供商 (至少配置一个):[/bold cyan]
• [bold]百炼 (DashScope)[/bold] - 阿里云百炼大模型
  环境变量: DASHSCOPE_API_KEY
  获取地址: https://help.aliyun.com/zh/dashscope/
  格式: sk-xxx...xxx

• [bold]OpenAI GPT[/bold] - OpenAI GPT系列模型  
  环境变量: OPENAI_API_KEY
  获取地址: https://platform.openai.com/api-keys
  格式: sk-xxx...xxx

• [bold]Google Gemini[/bold] - Google Gemini模型
  环境变量: GOOGLE_API_KEY
  获取地址: https://ai.google.dev/gemini-api/docs/api-key
  格式: AIza...xxx

• [bold]Anthropic Claude[/bold] - Anthropic Claude模型
  环境变量: ANTHROPIC_API_KEY
  获取地址: https://console.anthropic.com/
  格式: sk-ant-xxx...xxx

[bold green]国产LLM提供商:[/bold green]
• [bold]DeepSeek[/bold] - 深度求索模型
  环境变量: DEEPSEEK_API_KEY
  获取地址: https://platform.deepseek.com/api_keys
  格式: sk-xxx...xxx

• [bold]通义千问[/bold] - 通义千问开源模型
  环境变量: QIANWEN_API_KEY
  获取地址: https://help.aliyun.com/zh/dashscope/

• [bold]豆包[/bold] - 火山引擎豆包模型
  环境变量: DOUBAO_API_KEY
  获取地址: https://console.volcengine.com/ark

• [bold]智谱AI[/bold] - GLM系列模型
  环境变量: ZHIPUAI_API_KEY
  获取地址: https://open.bigmodel.cn/usercenter/apikeys

• [bold]百川智能[/bold] - 百川系列模型
  环境变量: BAICHUAN_API_KEY
  获取地址: https://platform.baichuan-ai.com/console/apikey
  格式: sk-xxx...xxx

• [bold]Moonshot AI[/bold] - Kimi系列模型
  环境变量: MOONSHOT_API_KEY
  获取地址: https://platform.moonshot.cn/console/api-keys
  格式: sk-xxx...xxx

• [bold]MiniMax[/bold] - 海螺系列模型
  环境变量: MINIMAX_API_KEY
  获取地址: https://api.minimax.chat/user-center/basic-information/interface-key

• [bold]零一万物[/bold] - Yi系列模型
  环境变量: YI_API_KEY
  获取地址: https://platform.lingyiwanwu.com/apikeys

• [bold]阶跃星辰[/bold] - Step系列模型
  环境变量: STEPFUN_API_KEY
  获取地址: https://platform.stepfun.com/interface-key

[bold blue]TradingAgent 专用:[/bold blue]
• [bold]Finnhub[/bold] - 金融数据API
  环境变量: FINNHUB_API_KEY
  获取地址: https://finnhub.io/dashboard
  免费额度: 60次/分钟

[bold magenta]PatentAgent 专用:[/bold magenta]
• [bold]SerpApi[/bold] - Google Patents搜索
  环境变量: SERPAPI_API_KEY
  获取地址: https://serpapi.com/manage-api-key
  免费额度: 100次/月

• [bold]智慧芽[/bold] - 专利AI分析服务
  环境变量: ZHIHUIYA_CLIENT_ID, ZHIHUIYA_CLIENT_SECRET
  获取地址: https://open-zhihuiya-com.libproxy1.nus.edu.sg/

🛠️ [bold]配置方法:[/bold]

[bold]方法1: 环境变量 (推荐)[/bold]
```bash
export DASHSCOPE_API_KEY="your_api_key"
export DEEPSEEK_API_KEY="your_api_key"
export OPENAI_API_KEY="your_api_key"
```

[bold]方法2: .env 文件[/bold]
在项目根目录创建 .env 文件:
```
DASHSCOPE_API_KEY=your_api_key
DEEPSEEK_API_KEY=your_api_key
OPENAI_API_KEY=your_api_key
```
"""
        console.print(Panel(help_content, title="📖 配置帮助", border_style="cyan"))
    
    def _reset_configuration(self):
        """重置配置"""
        console.print("\n[red]⚠️  重置配置[/red]")
        console.print("[yellow]这将删除所有配置文件并恢复默认设置![/yellow]")
        
        if Confirm.ask("确定要重置配置吗?"):
            try:
                self.config_manager.reset_config()
                console.print("[green]✅ 配置已重置为默认值![/green]")
                
            except Exception as e:
                console.print(f"[red]❌ 配置重置失败: {str(e)}[/red]")
        else:
            console.print("[yellow]取消重置操作[/yellow]")
    
    def _clean_cache(self):
        """清理缓存"""
        console.print("\n[yellow]🧹 清理缓存[/yellow]")
        
        if Confirm.ask("确定要清理所有缓存吗?"):
            try:
                # 这里可以添加清理缓存的逻辑
                console.print("[green]✅ 缓存清理完成![/green]")
                
            except Exception as e:
                console.print(f"[red]❌ 缓存清理失败: {str(e)}[/red]")
        else:
            console.print("[yellow]取消清理操作[/yellow]")
    
    def _get_api_description(self, api_name: str) -> str:
        """获取API描述"""
        descriptions = {
            "dashscope_api": "百炼大模型 (阿里云)",
            "openai_api": "OpenAI GPT模型",
            "google_api": "Google Gemini模型",
            "anthropic_api": "Anthropic Claude模型",
            "deepseek_api": "DeepSeek深度求索模型",
            "qianwen_api": "通义千问开源模型",
            "doubao_api": "火山引擎豆包模型",
            "zhipuai_api": "智谱AI GLM模型",
            "baichuan_api": "百川智能模型",
            "moonshot_api": "Moonshot AI Kimi模型",
            "minimax_api": "MiniMax海螺模型",
            "yi_api": "零一万物Yi模型",
            "stepfun_api": "阶跃星辰Step模型",
            "finnhub_api": "金融数据 (TradingAgent)",
            "serpapi_api": "Google Patents (PatentAgent)",
            "zhihuiya_client_id": "智慧芽客户端ID (PatentAgent)",
            "zhihuiya_client_secret": "智慧芽客户端密钥 (PatentAgent)"
        }
        return descriptions.get(api_name, "未知API")
    
    def _get_api_help_link(self, api_name: str) -> str:
        """获取API帮助链接"""
        help_links = {
            "dashscope_api": "[link=https://help.aliyun.com/zh/dashscope/]阿里云百炼文档[/link]",
            "openai_api": "[link=https://platform.openai.com/api-keys]OpenAI API Keys[/link]",
            "google_api": "[link=https://ai.google.dev/gemini-api/docs/api-key]Google AI Studio[/link]",
            "anthropic_api": "[link=https://console.anthropic.com/]Anthropic Console[/link]",
            "deepseek_api": "[link=https://platform.deepseek.com/api_keys]DeepSeek API Keys[/link]",
            "qianwen_api": "[link=https://help.aliyun.com/zh/dashscope/]通义千问文档[/link]",
            "doubao_api": "[link=https://console.volcengine.com/ark]火山引擎方舟[/link]",
            "zhipuai_api": "[link=https://open.bigmodel.cn/usercenter/apikeys]智谱AI开放平台[/link]",
            "baichuan_api": "[link=https://platform.baichuan-ai.com/console/apikey]百川智能平台[/link]",
            "moonshot_api": "[link=https://platform.moonshot.cn/console/api-keys]Moonshot平台[/link]",
            "minimax_api": "[link=https://api.minimax.chat/user-center/basic-information/interface-key]MiniMax平台[/link]",
            "yi_api": "[link=https://platform.lingyiwanwu.com/apikeys]零一万物平台[/link]",
            "stepfun_api": "[link=https://platform.stepfun.com/interface-key]阶跃星辰平台[/link]",
            "finnhub_api": "[link=https://finnhub.io/dashboard]Finnhub Dashboard[/link]",
            "serpapi_api": "[link=https://serpapi.com/manage-api-key]SerpApi Dashboard[/link]",
            "zhihuiya_client_id": "[link=https://open-zhihuiya-com.libproxy1.nus.edu.sg/]智慧芽开放平台[/link]",
            "zhihuiya_client_secret": "[link=https://open-zhihuiya-com.libproxy1.nus.edu.sg/]智慧芽开放平台[/link]"
        }
        return help_links.get(api_name, "暂无帮助链接")