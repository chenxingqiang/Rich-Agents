"""
PatentAgent CLI适配器
将PatentAgent功能集成到Rich-Agents统一框架中
"""

import os
import sys
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# 导入Rich-Agents共享组件
from shared.config.rich_agents_config_manager import RichAgentsConfigManager
from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter

logger = logging.getLogger(__name__)


class PatentAgentCLI:
    """PatentAgent CLI适配器"""
    
    def __init__(self, config_manager: Optional[RichAgentsConfigManager] = None):
        """
        初始化PatentAgent CLI
        
        Args:
            config_manager: Rich-Agents配置管理器实例
        """
        self.config_manager = config_manager or RichAgentsConfigManager()
        self.patent_config = self.config_manager.get_patent_config()
        
        logger.info("PatentAgent CLI适配器初始化完成")
    
    def run(self):
        """运行PatentAgent分析"""
        try:
            from rich.console import Console
            console = Console()
            
            console.print("[bold cyan]🔬 PatentAgent - 专利发现、验证、分析与撰写系统[/bold cyan]")
            console.print("[dim]正在启动专利智能体团队...[/dim]\n")
            
            # 验证API密钥配置
            validation_result = self.config_manager.validate_config("patent")
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
            
            # 检查PatentAgent模块是否可用
            try:
                # 尝试导入PatentAgent CLI
                from patentagents.cli.main import PatentAgentCLI as OriginalPatentCLI
                
                console.print("[green]✅ 配置验证通过，启动PatentAgent分析流程[/green]\n")
                
                # 创建并运行原始PatentAgent CLI
                patent_cli = OriginalPatentCLI()
                patent_cli.run()
                
            except ImportError:
                # 如果PatentAgent模块不可用，提供基础功能
                console.print("[yellow]⚠️ PatentAgent完整模块不可用，启动基础模式[/yellow]\n")
                self._run_basic_mode(console)
                
        except Exception as e:
            console.print(f"[red]❌ PatentAgent运行失败: {str(e)}[/red]")
            logger.error(f"PatentAgent运行失败: {str(e)}")
    
    def _run_basic_mode(self, console):
        """运行基础模式"""
        console.print("[bold]PatentAgent 基础模式[/bold]")
        console.print()
        
        # 显示可用功能
        console.print("可用功能:")
        console.print("1. 🔍 技术领域分析")
        console.print("2. 📊 专利检索模拟")
        console.print("3. ✍️ 专利申请草稿生成")
        console.print("4. 🔧 系统状态检查")
        console.print("5. 🚪 返回主菜单")
        
        while True:
            try:
                choice = console.input("\n[bold yellow]请选择功能 (1-5): [/bold yellow]").strip()
                
                if choice == '1':
                    self._technology_analysis(console)
                elif choice == '2':
                    self._patent_search_simulation(console)
                elif choice == '3':
                    self._patent_draft_generation(console)
                elif choice == '4':
                    self._system_status_check(console)
                elif choice == '5':
                    console.print("[green]返回主菜单[/green]")
                    break
                else:
                    console.print("[red]❌ 无效选择，请输入1-5之间的数字[/red]")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]返回主菜单[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ 操作失败: {str(e)}[/red]")
    
    def _technology_analysis(self, console):
        """技术领域分析"""
        console.print("\n[bold cyan]🔍 技术领域分析[/bold cyan]")
        
        try:
            # 获取技术领域
            domain = console.input("请输入技术领域 (如: 人工智能, 生物技术): ").strip()
            if not domain:
                console.print("[red]❌ 技术领域不能为空[/red]")
                return
            
            # 获取具体方向
            topic = console.input("请输入具体技术方向 (如: 机器学习, 基因编辑): ").strip()
            if not topic:
                console.print("[red]❌ 技术方向不能为空[/red]")
                return
            
            console.print(f"\n[yellow]正在分析技术领域: {domain} - {topic}[/yellow]")
            
            # 使用LLM进行技术分析
            analysis_result = self._perform_technology_analysis(domain, topic)
            
            if analysis_result["success"]:
                console.print("\n[green]✅ 技术分析完成![/green]")
                console.print("\n[bold]分析结果:[/bold]")
                console.print(analysis_result["analysis"])
            else:
                console.print(f"\n[red]❌ 分析失败: {analysis_result['error']}[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ 技术分析失败: {str(e)}[/red]")
    
    def _patent_search_simulation(self, console):
        """专利检索模拟"""
        console.print("\n[bold cyan]📊 专利检索模拟[/bold cyan]")
        
        try:
            keywords = console.input("请输入检索关键词: ").strip()
            if not keywords:
                console.print("[red]❌ 检索关键词不能为空[/red]")
                return
            
            console.print(f"\n[yellow]正在检索专利: {keywords}[/yellow]")
            
            # 模拟专利检索
            search_result = self._simulate_patent_search(keywords)
            
            console.print("\n[green]✅ 检索完成![/green]")
            console.print(f"\n[bold]检索结果:[/bold]")
            console.print(f"找到相关专利: {search_result['count']} 件")
            console.print(f"主要技术领域: {', '.join(search_result['domains'])}")
            console.print(f"关键申请人: {', '.join(search_result['applicants'])}")
            
        except Exception as e:
            console.print(f"[red]❌ 专利检索失败: {str(e)}[/red]")
    
    def _patent_draft_generation(self, console):
        """专利申请草稿生成"""
        console.print("\n[bold cyan]✍️ 专利申请草稿生成[/bold cyan]")
        
        try:
            invention_title = console.input("请输入发明名称: ").strip()
            if not invention_title:
                console.print("[red]❌ 发明名称不能为空[/red]")
                return
            
            technical_field = console.input("请输入技术领域: ").strip()
            if not technical_field:
                console.print("[red]❌ 技术领域不能为空[/red]")
                return
            
            console.print(f"\n[yellow]正在生成专利申请草稿: {invention_title}[/yellow]")
            
            # 生成专利草稿
            draft_result = self._generate_patent_draft(invention_title, technical_field)
            
            if draft_result["success"]:
                console.print("\n[green]✅ 专利草稿生成完成![/green]")
                console.print("\n[bold]专利申请草稿:[/bold]")
                console.print(draft_result["draft"])
            else:
                console.print(f"\n[red]❌ 生成失败: {draft_result['error']}[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ 草稿生成失败: {str(e)}[/red]")
    
    def _system_status_check(self, console):
        """系统状态检查"""
        console.print("\n[bold cyan]🔧 PatentAgent系统状态检查[/bold cyan]")
        
        try:
            # 检查API密钥状态
            api_status = self.config_manager.check_api_keys("patent")
            
            console.print("\n[bold]API密钥状态:[/bold]")
            for api_name, is_configured in api_status.items():
                if "serpapi" in api_name or "zhihuiya" in api_name:
                    status_text = "✅ 已配置" if is_configured else "❌ 未配置"
                    console.print(f"  • {api_name}: {status_text}")
            
            # 检查LLM状态
            console.print("\n[bold]LLM提供商状态:[/bold]")
            llm_providers = self.config_manager.get_available_llm_providers()
            for provider in llm_providers:
                api_key = self.config_manager.get_api_key(provider)
                status = "✅ 可用" if api_key else "❌ 未配置"
                console.print(f"  • {provider}: {status}")
            
            # 检查PatentAgent模块
            console.print("\n[bold]PatentAgent模块状态:[/bold]")
            try:
                import patentagents
                console.print("  • PatentAgent模块: ✅ 已安装")
            except ImportError:
                console.print("  • PatentAgent模块: ❌ 未安装")
            
        except Exception as e:
            console.print(f"[red]❌ 状态检查失败: {str(e)}[/red]")
    
    def _perform_technology_analysis(self, domain: str, topic: str) -> Dict[str, Any]:
        """执行技术分析"""
        try:
            # 尝试使用可用的LLM进行分析
            available_providers = self.config_manager.get_available_llm_providers()
            
            for provider in available_providers:
                api_key = self.config_manager.get_api_key(provider)
                if api_key:
                    try:
                        model = self.config_manager.get_default_model(provider)
                        llm = UnifiedLLMAdapter(provider, model, api_key)
                        
                        prompt = f"""
请对以下技术领域进行分析:

技术领域: {domain}
具体方向: {topic}

请从以下角度进行分析:
1. 技术现状和发展趋势
2. 主要技术挑战
3. 潜在创新机会
4. 商业应用前景
5. 专利布局建议

请提供详细的分析报告。
"""
                        
                        analysis = llm.invoke(prompt)
                        return {
                            "success": True,
                            "analysis": analysis,
                            "provider": provider,
                            "model": model
                        }
                        
                    except Exception as e:
                        logger.warning(f"使用{provider}分析失败: {str(e)}")
                        continue
            
            # 如果所有LLM都不可用，返回模拟结果
            return {
                "success": True,
                "analysis": f"""
技术领域分析报告: {domain} - {topic}

1. 技术现状:
   • 该技术领域正处于快速发展阶段
   • 具有较强的创新活力和市场潜力
   • 需要进一步的技术突破

2. 发展趋势:
   • 技术标准化程度逐步提高
   • 产业化应用不断拓展
   • 国际竞争日趋激烈

3. 创新机会:
   • 核心算法优化
   • 应用场景扩展
   • 跨领域技术融合

4. 商业前景:
   • 市场需求持续增长
   • 产业链逐步完善
   • 投资热度较高

5. 专利建议:
   • 重点关注核心技术专利布局
   • 加强国际专利申请
   • 构建专利组合优势

注: 此为基础分析模式生成的报告，建议配置LLM API密钥以获得更详细的分析。
""",
                "provider": "simulation",
                "model": "basic"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _simulate_patent_search(self, keywords: str) -> Dict[str, Any]:
        """模拟专利检索"""
        import random
        
        # 模拟检索结果
        count = random.randint(50, 500)
        domains = random.sample([
            "人工智能", "机器学习", "深度学习", "计算机视觉", 
            "自然语言处理", "物联网", "区块链", "量子计算"
        ], 3)
        applicants = random.sample([
            "Google Inc", "Microsoft Corp", "Apple Inc", "IBM Corp",
            "华为技术有限公司", "腾讯科技", "百度在线", "阿里巴巴"
        ], 4)
        
        return {
            "count": count,
            "domains": domains,
            "applicants": applicants,
            "keywords": keywords
        }
    
    def _generate_patent_draft(self, invention_title: str, technical_field: str) -> Dict[str, Any]:
        """生成专利申请草稿"""
        try:
            # 尝试使用LLM生成草稿
            available_providers = self.config_manager.get_available_llm_providers()
            
            for provider in available_providers:
                api_key = self.config_manager.get_api_key(provider)
                if api_key:
                    try:
                        model = self.config_manager.get_default_model(provider)
                        llm = UnifiedLLMAdapter(provider, model, api_key)
                        
                        prompt = f"""
请为以下发明生成专利申请草稿:

发明名称: {invention_title}
技术领域: {technical_field}

请包含以下部分:
1. 技术领域
2. 背景技术
3. 发明内容
4. 技术方案
5. 有益效果
6. 权利要求书(至少包含1个独立权利要求和2个从属权利要求)

请确保格式符合专利申请要求。
"""
                        
                        draft = llm.invoke(prompt)
                        return {
                            "success": True,
                            "draft": draft,
                            "provider": provider,
                            "model": model
                        }
                        
                    except Exception as e:
                        logger.warning(f"使用{provider}生成草稿失败: {str(e)}")
                        continue
            
            # 如果LLM不可用，生成基础草稿
            return {
                "success": True,
                "draft": f"""
专利申请草稿

发明名称: {invention_title}

1. 技术领域
本发明涉及{technical_field}技术领域，特别涉及一种{invention_title}。

2. 背景技术
现有技术中，{technical_field}存在以下问题:
- 技术效率有待提高
- 实现成本较高
- 应用范围有限

3. 发明内容
本发明提供一种{invention_title}，旨在解决上述技术问题。

技术方案:
通过采用创新的技术手段，实现{invention_title}的改进设计。

4. 有益效果
本发明具有以下有益效果:
- 提高了技术效率
- 降低了实现成本
- 扩大了应用范围

5. 权利要求书

权利要求1: 一种{invention_title}，其特征在于，包括...

权利要求2: 根据权利要求1所述的{invention_title}，其特征在于，进一步包括...

权利要求3: 根据权利要求1或2所述的{invention_title}，其特征在于，所述...

注: 此为基础模式生成的草稿，建议配置LLM API密钥以获得更详细的专利申请文档。
""",
                "provider": "simulation",
                "model": "basic"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_supported_analysis_types(self) -> list:
        """获取支持的分析类型"""
        return self.patent_config.get("analysis_types", ["discovery", "validation", "analysis", "writing"])
    
    def get_available_agents(self) -> Dict[str, Any]:
        """获取可用的智能体"""
        return self.patent_config.get("agents", {})
    
    def validate_patent_config(self) -> Dict[str, Any]:
        """验证PatentAgent配置"""
        return self.config_manager.validate_config("patent") 