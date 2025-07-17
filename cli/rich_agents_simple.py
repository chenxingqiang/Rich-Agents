#!/usr/bin/env python3
"""
Rich-Agents 简化CLI入口
不依赖typer，使用标准库实现基本功能
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None

# 导入共享组件
from shared.config.rich_agents_config_manager import RichAgentsConfigManager
from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter

# 导入子CLI (可选)
try:
    from cli.trading_cli import TradingAgentCLI
    TRADING_CLI_AVAILABLE = True
except ImportError:
    TradingAgentCLI = None
    TRADING_CLI_AVAILABLE = False

from cli.patent_cli import PatentAgentCLI


def print_message(message: str, style: str = "normal"):
    """统一的消息输出函数"""
    if RICH_AVAILABLE and console:
        if style == "error":
            console.print(f"[red]❌ {message}[/red]")
        elif style == "success":
            console.print(f"[green]✅ {message}[/green]")
        elif style == "warning":
            console.print(f"[yellow]⚠️ {message}[/yellow]")
        elif style == "info":
            console.print(f"[blue]ℹ️ {message}[/blue]")
        else:
            console.print(message)
    else:
        if style == "error":
            print(f"❌ {message}")
        elif style == "success":
            print(f"✅ {message}")
        elif style == "warning":
            print(f"⚠️ {message}")
        elif style == "info":
            print(f"ℹ️ {message}")
        else:
            print(message)


class RichAgentsSimpleCLI:
    """Rich-Agents简化CLI类"""
    
    def __init__(self):
        """初始化Rich-Agents CLI"""
        try:
            self.config_manager = RichAgentsConfigManager()
            
            # 初始化子CLI
            self.trading_cli = None
            self.patent_cli = None
            
            print_message("Rich-Agents CLI初始化完成", "success")
        except Exception as e:
            print_message(f"初始化失败: {str(e)}", "error")
            sys.exit(1)
    
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

欢迎使用Rich-Agents！

Rich-Agents是一个统一的多智能体AI工具集，目前支持两个专业领域：

🏦 TradingAgent - 多智能体金融交易分析框架
   • 市场分析师、情绪分析师、新闻分析师、基本面分析师
   • 多智能体协作研究和辩论
   • 风险管理和投资组合管理
   • 支持美股和A股市场

🔬 PatentAgent - 专利发现、验证、分析与撰写系统
   • 技术创新发现和专利机会识别
   • 专利可行性验证和风险评估
   • 专利价值分析和商业价值评估
   • 专利申请文档撰写和质量评估

请选择您需要的智能体工具：

1. 🏦 TradingAgent - 启动金融交易分析工具
2. 🔬 PatentAgent - 启动专利智能体工具
3. ⚙️ 系统配置 - 配置管理和状态检查
4. 📖 帮助信息 - 查看详细使用说明
5. 🚪 退出系统

"""
        if RICH_AVAILABLE:
            console.print(Panel(welcome_text, border_style="green", padding=(1, 2)))
        else:
            print(welcome_text)
    
    def get_user_choice(self) -> str:
        """获取用户选择"""
        while True:
            try:
                choice = input("请输入您的选择 (1-5): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    return choice
                else:
                    print_message("无效选择，请输入1-5之间的数字", "error")
            except KeyboardInterrupt:
                print_message("\n\n感谢使用Rich-Agents！", "info")
                sys.exit(0)
            except Exception as e:
                print_message(f"输入错误: {str(e)}", "error")
    
    def run_trading_agent(self):
        """运行TradingAgent"""
        if not TRADING_CLI_AVAILABLE:
            print_message("TradingAgent CLI不可用，缺少必要依赖", "error")
            print_message("请安装完整的TradingAgent依赖包", "warning")
            self._show_trading_basic_info()
            return
            
        try:
            if self.trading_cli is None:
                self.trading_cli = TradingAgentCLI(self.config_manager)
            
            print_message("🏦 启动TradingAgent - 金融交易分析工具", "info")
            print_message("正在初始化交易智能体...", "info")
            
            self.trading_cli.run()
            
        except ImportError as e:
            print_message(f"无法导入TradingAgent模块: {str(e)}", "error")
            print_message("请确保已正确安装TradingAgent相关依赖", "warning")
        except Exception as e:
            print_message(f"TradingAgent运行失败: {str(e)}", "error")
    
    def run_patent_agent(self):
        """运行PatentAgent"""
        try:
            if self.patent_cli is None:
                self.patent_cli = PatentAgentCLI(self.config_manager)
            
            print_message("🔬 启动PatentAgent - 专利智能体工具", "info")
            print_message("正在初始化专利智能体...", "info")
            
            self.patent_cli.run()
            
        except ImportError as e:
            print_message(f"无法导入PatentAgent模块: {str(e)}", "error")
            print_message("请确保已正确安装PatentAgent相关依赖", "warning")
        except Exception as e:
            print_message(f"PatentAgent运行失败: {str(e)}", "error")
    
    def show_system_config(self):
        """显示系统配置"""
        while True:
            print_message("⚙️ Rich-Agents 系统配置中心", "info")
            print("=" * 60)
            
            try:
                # 获取系统状态
                status = self.config_manager.get_system_status()
                
                # 显示基本信息
                print("\n🏠 系统信息:")
                print(f"  版本: {status.get('version', 'v0.1.0')}")
                print(f"  可用智能体: {', '.join(status.get('available_agents', ['TradingAgent', 'PatentAgent']))}")
                print(f"  LLM提供商: {', '.join(status.get('available_llm_providers', []))}")
                print(f"  配置目录: {self.config_manager.config_dir}")
                
                # 显示API密钥状态
                api_status = status.get("api_keys_status", {})
                print("\n🔑 API密钥状态:")
                for api_name, is_configured in api_status.items():
                    status_text = "✅ 已配置" if is_configured else "❌ 未配置"
                    description = self._get_api_description(api_name)
                    print(f"  {api_name}: {status_text} - {description}")
                
                # 显示缓存配置
                cache_config = status.get("cache_config", {})
                print("\n💾 缓存配置:")
                print(f"  缓存启用: {'✅ 启用' if cache_config.get('enabled') else '❌ 禁用'}")
                print(f"  缓存类型: {cache_config.get('type', 'file')}")
                print(f"  MongoDB: {'✅ 连接' if cache_config.get('mongodb', {}).get('enabled') else '❌ 未连接'}")
                print(f"  Redis: {'✅ 连接' if cache_config.get('redis', {}).get('enabled') else '❌ 未连接'}")
                
                # 配置验证
                validation_result = self.config_manager.validate_config()
                print("\n🔍 配置验证:")
                if validation_result["valid"]:
                    print("  ✅ 所有配置都有效")
                else:
                    print("  ❌ 配置存在问题")
                    for error in validation_result["errors"]:
                        print(f"    • {error}")
                
                if validation_result["warnings"]:
                    print("  ⚠️ 配置警告:")
                    for warning in validation_result["warnings"]:
                        print(f"    • {warning}")
                
                # 显示配置选项菜单
                print("\n🛠️ 配置选项:")
                print("1. 🔑 配置API密钥 - 添加或更新API密钥")
                print("2. 🏦 TradingAgent配置 - 金融数据源和LLM设置")
                print("3. 🔬 PatentAgent配置 - 专利数据源和AI设置")
                print("4. 💾 缓存配置 - MongoDB和Redis设置")
                print("5. 🔄 重新加载配置 - 刷新所有配置文件")
                print("6. 📋 导出配置 - 保存当前配置到文件")
                print("7. 📖 配置帮助 - 查看详细配置指南")
                print("8. 🚪 返回主菜单 - 退出配置中心")
                
                # 获取用户选择
                choice = input("\n请选择配置选项 (1-8): ").strip()
                
                if choice == '1':
                    self._configure_api_keys_simple()
                elif choice == '2':
                    self._configure_trading_agent_simple()
                elif choice == '3':
                    self._configure_patent_agent_simple()
                elif choice == '4':
                    self._configure_cache_settings_simple()
                elif choice == '5':
                    self._reload_configuration_simple()
                elif choice == '6':
                    self._export_configuration_simple()
                elif choice == '7':
                    self._show_configuration_help_simple()
                elif choice == '8':
                    print_message("返回主菜单", "info")
                    break
                else:
                    print_message("无效选择，请输入1-8之间的数字", "error")
                
            except KeyboardInterrupt:
                print_message("\n返回主菜单", "info")
                break
            except Exception as e:
                print_message(f"获取系统状态失败: {str(e)}", "error")
                break
    
    def _configure_api_keys_simple(self):
        """配置API密钥 - 简化版"""
        print_message("🔑 API密钥配置", "info")
        print("=" * 40)
        
        # API密钥配置选项
        api_configs = {
            "1": {"name": "百炼大模型 (DashScope)", "env_var": "DASHSCOPE_API_KEY"},
            "2": {"name": "OpenAI GPT", "env_var": "OPENAI_API_KEY"},
            "3": {"name": "Google Gemini", "env_var": "GOOGLE_API_KEY"},
            "4": {"name": "Anthropic Claude", "env_var": "ANTHROPIC_API_KEY"},
            "5": {"name": "DeepSeek 深度求索", "env_var": "DEEPSEEK_API_KEY"},
            "6": {"name": "通义千问 (Qianwen)", "env_var": "QIANWEN_API_KEY"},
            "7": {"name": "火山引擎豆包 (Doubao)", "env_var": "DOUBAO_API_KEY"},
            "8": {"name": "智谱AI GLM", "env_var": "ZHIPUAI_API_KEY"},
            "9": {"name": "百川智能 (Baichuan)", "env_var": "BAICHUAN_API_KEY"},
            "10": {"name": "Moonshot AI Kimi", "env_var": "MOONSHOT_API_KEY"},
            "11": {"name": "MiniMax 海螺", "env_var": "MINIMAX_API_KEY"},
            "12": {"name": "零一万物 Yi", "env_var": "YI_API_KEY"},
            "13": {"name": "阶跃星辰 Step", "env_var": "STEPFUN_API_KEY"},
            "14": {"name": "Finnhub 金融数据", "env_var": "FINNHUB_API_KEY"},
            "15": {"name": "SerpApi Google Patents", "env_var": "SERPAPI_API_KEY"},
            "16": {"name": "智慧芽客户端ID", "env_var": "ZHIHUIYA_CLIENT_ID"},
            "17": {"name": "智慧芽客户端密钥", "env_var": "ZHIHUIYA_CLIENT_SECRET"}
        }
        
        while True:
            # 显示当前API密钥状态
            current_status = self.config_manager.get_system_status().get("api_keys_status", {})
            
            print("\n当前API密钥状态:")
            
            # 分组显示
            print("\n🤖 LLM提供商:")
            for key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
                config = api_configs[key]
                env_var = config["env_var"].lower() + "_key" if not config["env_var"].endswith("_KEY") else config["env_var"].lower().replace("_key", "_api")
                is_configured = current_status.get(env_var, False)
                status_icon = "✅" if is_configured else "❌"
                print(f"  {key}. {status_icon} {config['name']}")
            
            print("\n📊 专用数据源:")
            for key in ["14", "15", "16", "17"]:
                config = api_configs[key]
                env_var = config["env_var"].lower() + "_key" if not config["env_var"].endswith("_KEY") else config["env_var"].lower().replace("_key", "_api")
                is_configured = current_status.get(env_var, False)
                status_icon = "✅" if is_configured else "❌"
                print(f"  {key}. {status_icon} {config['name']}")
            
            print("\n  18. 🔄 刷新状态")
            print("  0. 🚪 返回上级菜单")
            
            choice = input("\n请选择要配置的API (0-18): ").strip()
            
            if choice == '0':
                break
            elif choice == '18':
                print_message("正在刷新API密钥状态...", "info")
                continue
            elif choice in api_configs:
                self._configure_single_api_key_simple(api_configs[choice])
            else:
                print_message("无效选择，请输入0-18之间的数字", "error")
    
    def _configure_single_api_key_simple(self, api_config):
        """配置单个API密钥 - 简化版"""
        print(f"\n🔧 配置 {api_config['name']}")
        print("-" * 30)
        
        # 检查当前值
        current_value = os.getenv(api_config['env_var'])
        if current_value:
            masked_value = current_value[:8] + "..." + current_value[-4:] if len(current_value) > 12 else "***"
            print(f"当前值: {masked_value}")
        else:
            print("当前未配置")
        
        print("\n配置选项:")
        print("1. 🔑 设置新的API密钥")
        print("2. 🔍 测试当前API密钥")
        print("3. 🗑️ 删除API密钥")
        print("4. 🚪 返回")
        
        action = input("\n请选择操作 (1-4): ").strip()
        
        if action == '1':
            self._set_api_key_simple(api_config)
        elif action == '2':
            self._test_api_key_simple(api_config)
        elif action == '3':
            self._delete_api_key_simple(api_config)
        elif action == '4':
            return
        else:
            print_message("无效选择", "error")
    
    def _set_api_key_simple(self, api_config):
        """设置API密钥 - 简化版"""
        print(f"\n设置 {api_config['name']} API密钥")
        
        try:
            new_key = input(f"请输入 {api_config['name']} API密钥: ").strip()
            
            if not new_key:
                print_message("API密钥不能为空", "error")
                return
            
            # 设置环境变量
            os.environ[api_config['env_var']] = new_key
            
            # 保存到配置文件
            self.config_manager.set_api_key(api_config['env_var'], new_key)
            
            print_message(f"{api_config['name']} API密钥设置成功!", "success")
            print_message("注意: 请确保将API密钥添加到您的环境变量中以便持久保存", "warning")
            
            # 提供环境变量设置命令
            print(f"\n环境变量设置命令:")
            print(f"export {api_config['env_var']}=\"{new_key[:8]}...\"")
            
        except Exception as e:
            print_message(f"设置API密钥失败: {str(e)}", "error")
    
    def _test_api_key_simple(self, api_config):
        """测试API密钥 - 简化版"""
        print(f"\n正在测试 {api_config['name']} API密钥...")
        
        try:
            result = self.config_manager.test_api_key(api_config['env_var'])
            
            if result['success']:
                print_message(f"{api_config['name']} API密钥测试成功!", "success")
                if result.get('details'):
                    print(f"详情: {result['details']}")
            else:
                print_message(f"{api_config['name']} API密钥测试失败", "error")
                print_message(f"错误: {result.get('error', '未知错误')}", "error")
                
        except Exception as e:
            print_message(f"测试失败: {str(e)}", "error")
    
    def _delete_api_key_simple(self, api_config):
        """删除API密钥 - 简化版"""
        confirm = input(f"\n确认删除 {api_config['name']} API密钥? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes', '是']:
            try:
                # 从环境变量中删除
                if api_config['env_var'] in os.environ:
                    del os.environ[api_config['env_var']]
                
                # 从配置文件中删除
                self.config_manager.delete_api_key(api_config['env_var'])
                
                print_message(f"{api_config['name']} API密钥已删除", "success")
                
            except Exception as e:
                print_message(f"删除失败: {str(e)}", "error")
        else:
            print_message("取消删除操作", "info")
    
    def _configure_trading_agent_simple(self):
        """配置TradingAgent - 简化版"""
        print_message("🏦 TradingAgent 配置", "info")
        print("=" * 40)
        
        trading_config = self.config_manager.get_trading_config()
        
        print("TradingAgent 当前配置:")
        print(f"  默认市场: {trading_config.get('default_market', 'US')}")
        print(f"  数据源: {trading_config.get('data_source', 'finnhub')}")
        print(f"  缓存启用: {trading_config.get('cache_enabled', True)}")
        print(f"  分析深度: {trading_config.get('analysis_depth', 3)}")
        
        print("\nTradingAgent 配置选项:")
        print("1. 📊 数据源配置 (开发中)")
        print("2. 🏛️ 市场设置 (开发中)")
        print("3. 🧠 智能体设置 (开发中)")
        print("4. 🚪 返回")
        
        choice = input("\n请选择配置项 (1-4): ").strip()
        
        if choice in ['1', '2', '3']:
            print_message("该功能正在开发中，敬请期待...", "info")
        elif choice == '4':
            return
        else:
            print_message("无效选择", "error")
    
    def _configure_patent_agent_simple(self):
        """配置PatentAgent - 简化版"""
        print_message("🔬 PatentAgent 配置", "info")
        print("=" * 40)
        
        patent_config = self.config_manager.get_patent_config()
        
        print("PatentAgent 当前配置:")
        print(f"  专利数据源: {patent_config.get('patent_source', 'serpapi')}")
        print(f"  AI分析源: {patent_config.get('ai_analysis_source', 'zhihuiya')}")
        print(f"  默认分析类型: {patent_config.get('default_analysis', 'discovery')}")
        print(f"  分析深度: {patent_config.get('analysis_depth', 2)}")
        
        print("\nPatentAgent 配置选项:")
        print("1. 🔍 专利数据源 (开发中)")
        print("2. 🧠 AI分析服务 (开发中)")
        print("3. 🎯 分析类型 (开发中)")
        print("4. 🚪 返回")
        
        choice = input("\n请选择配置项 (1-4): ").strip()
        
        if choice in ['1', '2', '3']:
            print_message("该功能正在开发中，敬请期待...", "info")
        elif choice == '4':
            return
        else:
            print_message("无效选择", "error")
    
    def _configure_cache_settings_simple(self):
        """配置缓存设置 - 简化版"""
        print_message("💾 缓存配置", "info")
        print("=" * 40)
        
        cache_config = self.config_manager.get_cache_config()
        
        print("当前缓存配置:")
        print(f"  缓存启用: {'✅' if cache_config.get('enabled') else '❌'}")
        print(f"  缓存类型: {cache_config.get('type', 'file')}")
        print(f"  MongoDB: {'✅' if cache_config.get('mongodb', {}).get('enabled') else '❌'}")
        print(f"  Redis: {'✅' if cache_config.get('redis', {}).get('enabled') else '❌'}")
        
        print("\n缓存配置选项:")
        print("1. 🔄 启用/禁用缓存 (开发中)")
        print("2. 🗄️ 配置MongoDB (开发中)")
        print("3. ⚡ 配置Redis (开发中)")
        print("4. 🧹 清理缓存 (开发中)")
        print("5. 🚪 返回")
        
        choice = input("\n请选择配置项 (1-5): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            print_message("该功能正在开发中，敬请期待...", "info")
        elif choice == '5':
            return
        else:
            print_message("无效选择", "error")
    
    def _reload_configuration_simple(self):
        """重新加载配置 - 简化版"""
        print_message("🔄 正在重新加载配置...", "info")
        
        try:
            # 重新初始化配置管理器
            self.config_manager = RichAgentsConfigManager()
            print_message("配置重新加载成功!", "success")
            
        except Exception as e:
            print_message(f"配置重新加载失败: {str(e)}", "error")
    
    def _export_configuration_simple(self):
        """导出配置 - 简化版"""
        print_message("📋 导出配置", "info")
        
        try:
            export_path = self.config_manager.export_config()
            print_message(f"配置已导出到: {export_path}", "success")
            
        except Exception as e:
            print_message(f"配置导出失败: {str(e)}", "error")
    
    def _show_configuration_help_simple(self):
        """显示配置帮助 - 简化版"""
        help_text = """
📖 Rich-Agents 配置详细指南

🔑 API密钥配置:

LLM提供商 (至少配置一个):
• 百炼 (DashScope) - 阿里云百炼大模型
  环境变量: DASHSCOPE_API_KEY
  获取地址: https://help.aliyun.com/zh/dashscope/

• OpenAI GPT - OpenAI GPT系列模型  
  环境变量: OPENAI_API_KEY
  获取地址: https://platform.openai.com/api-keys

• Google Gemini - Google Gemini模型
  环境变量: GOOGLE_API_KEY
  获取地址: https://ai.google.dev/gemini-api/docs/api-key

• Anthropic Claude - Anthropic Claude模型
  环境变量: ANTHROPIC_API_KEY
  获取地址: https://console.anthropic.com/

TradingAgent 专用:
• Finnhub - 金融数据API
  环境变量: FINNHUB_API_KEY
  获取地址: https://finnhub.io/dashboard

PatentAgent 专用:
• SerpApi - Google Patents搜索
  环境变量: SERPAPI_API_KEY
  获取地址: https://serpapi.com/manage-api-key

• 智慧芽 - 专利AI分析服务
  环境变量: ZHIHUIYA_CLIENT_ID, ZHIHUIYA_CLIENT_SECRET
  获取地址: https://open-zhihuiya-com.libproxy1.nus.edu.sg/

🛠️ 配置方法:

方法1: 环境变量 (推荐)
export DASHSCOPE_API_KEY="your_api_key"
export OPENAI_API_KEY="your_api_key"

方法2: .env 文件
在项目根目录创建 .env 文件:
DASHSCOPE_API_KEY=your_api_key
OPENAI_API_KEY=your_api_key

方法3: 系统配置界面
使用Rich-Agents配置中心直接设置

💡 最佳实践:
• 至少配置一个LLM提供商
• TradingAgent需要Finnhub API
• PatentAgent需要SerpApi和智慧芽API
• 定期检查API配额使用情况
• 保护好您的API密钥安全

📞 技术支持:
如需帮助，请访问:
• GitHub Issues: https://github.com/TauricResearch/TradingAgents/issues
• 文档: https://github.com/TauricResearch/TradingAgents/wiki
"""
        
        print(help_text)
    
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
    
    def _show_trading_basic_info(self):
        """显示TradingAgent基础信息"""
        info_text = """
🏦 TradingAgent - 多智能体金融交易分析框架

TradingAgent是一个强大的多智能体金融分析系统，包含：

📊 核心分析师团队:
  • 市场分析师 (Market Analyst) - 分析市场趋势和技术指标
  • 情绪分析师 (Social Media Analyst) - 分析社交媒体情绪
  • 新闻分析师 (News Analyst) - 分析财经新闻影响
  • 基本面分析师 (Fundamentals Analyst) - 分析公司基本面

🔬 智能体研究团队:
  • 多头研究员 (Bull Researcher) - 看涨观点论证
  • 空头研究员 (Bear Researcher) - 看跌观点论证
  • 研究管理员 (Research Manager) - 协调研究方向

⚖️ 风险管理:
  • 风险管理员 (Risk Manager) - 评估投资风险
  • 投资组合管理 - 优化资产配置

🌍 市场支持:
  • 美股市场 (US Stock Market)
  • 中国A股市场 (China Stock Market)

📈 主要功能:
  • 多智能体协作分析
  • 实时市场数据获取
  • 技术指标计算
  • 风险评估和建议
  • 投资决策支持

🔧 安装完整版本:
  pip install langchain-openai typer
  
然后重新运行Rich-Agents即可使用完整的TradingAgent功能。
"""
        
        if RICH_AVAILABLE:
            console.print(Panel(info_text, border_style="cyan", padding=(1, 2)))
        else:
            print(info_text)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
📖 Rich-Agents 使用指南

🎯 主要功能:

🏦 TradingAgent - 金融交易分析
   • 多智能体协作分析 (市场、情绪、新闻、基本面)
   • 支持美股和A股市场
   • 风险管理和投资组合管理
   • 实时数据分析和交易决策

🔬 PatentAgent - 专利智能体
   • 技术创新发现和机会识别
   • 专利可行性验证和风险评估  
   • 专利价值分析和商业评估
   • 专利申请文档撰写

🔧 系统要求:
   • Python 3.10+
   • 配置相关API密钥
   • 稳定的网络连接

📝 使用流程:
   1. 选择智能体工具 (TradingAgent 或 PatentAgent)
   2. 根据提示输入分析参数
   3. 系统自动进行多智能体协作分析
   4. 查看分析结果和建议
   5. 可选择保存结果到本地文件

🔑 API配置:
   请在环境变量中设置以下API密钥:
   
   LLM提供商:
   • DASHSCOPE_API_KEY - 百炼大模型API密钥
   • OPENAI_API_KEY - OpenAI API密钥  
   • GOOGLE_API_KEY - Google API密钥
   • ANTHROPIC_API_KEY - Anthropic API密钥
   
   TradingAgent专用:
   • FINNHUB_API_KEY - 金融数据API密钥
   
   PatentAgent专用:
   • SERPAPI_API_KEY - Google Patents检索API密钥
   • ZHIHUIYA_CLIENT_ID - 智慧芽客户端ID
   • ZHIHUIYA_CLIENT_SECRET - 智慧芽客户端密钥

📞 技术支持:
   如遇问题，请检查:
   1. API密钥是否正确配置
   2. 网络连接是否正常
   3. 依赖库是否完整安装
   4. 系统日志中的错误信息

🌟 最佳实践:
   • 确保API密钥有效且有足够配额
   • 定期检查系统状态和配置
   • 保存重要的分析结果
   • 合理设置分析参数

"""
        if RICH_AVAILABLE:
            console.print(Panel(help_text, border_style="blue", padding=(1, 2)))
        else:
            print(help_text)
    
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
                    print_message("感谢使用Rich-Agents！", "info")
                    break
                
                # 询问是否继续
                if choice in ['1', '2']:
                    while True:
                        try:
                            continue_choice = input("\n🔄 是否继续使用Rich-Agents? (y/n): ").strip().lower()
                            
                            if continue_choice in ['y', 'yes', '是']:
                                break
                            elif continue_choice in ['n', 'no', '否']:
                                print_message("感谢使用Rich-Agents！", "info")
                                return
                            else:
                                print_message("请输入 y(是) 或 n(否)", "error")
                        except KeyboardInterrupt:
                            print_message("\n\n感谢使用Rich-Agents！", "info")
                            return
                
        except KeyboardInterrupt:
            print_message("\n\n感谢使用Rich-Agents！", "info")
        except Exception as e:
            print_message(f"系统错误: {str(e)}", "error")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Rich-Agents: 多智能体AI工具集 - 支持金融交易分析和专利智能体"
    )
    parser.add_argument(
        "--agent", "-a", 
        choices=["trading", "patent"],
        help="直接启动指定智能体 (trading/patent)"
    )
    parser.add_argument(
        "--debug", "-d", 
        action="store_true",
        help="启用调试模式"
    )
    
    args = parser.parse_args()
    
    # 配置日志
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    try:
        cli = RichAgentsSimpleCLI()
        
        # 如果指定了智能体类型，直接启动
        if args.agent:
            if args.agent == "trading":
                cli.run_trading_agent()
            elif args.agent == "patent":
                cli.run_patent_agent()
        else:
            # 否则启动交互式界面
            cli.run()
            
    except Exception as e:
        print_message(f"启动失败: {str(e)}", "error")
        sys.exit(1)


if __name__ == "__main__":
    main() 