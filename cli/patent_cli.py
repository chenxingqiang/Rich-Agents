"""
PatentAgent CLI适配器
将PatentAgent功能集成到Rich-Agents统一框架中，保持与TradingAgent一致的交互风格
"""

import os
import sys
import logging
import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.spinner import Spinner
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.rule import Rule

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
        self.console = Console()
        
        logger.info("PatentAgent CLI适配器初始化完成")
    
    def show_welcome(self):
        """显示欢迎界面 - 与TradingAgent保持一致的风格"""
        try:
            # 读取ASCII艺术欢迎界面
            welcome_file = Path(__file__).parent / "static" / "patent_welcome.txt"
            if welcome_file.exists():
                with open(welcome_file, "r", encoding="utf-8") as f:
                    welcome_ascii = f.read()
            else:
                welcome_ascii = "PatentAgent"

            # 创建欢迎界面内容 - 模仿TradingAgent的格式
            welcome_content = f"{welcome_ascii}\n"
            welcome_content += "[bold cyan]PatentAgent: 专利发现、验证、分析与撰写系统 - CLI[/bold cyan]\n\n"
            welcome_content += "[bold]Workflow Steps:[/bold]\n"
            welcome_content += "I. 技术分析 → II. 创新发现 → III. 先行技术研究 → IV. 专利撰写 → V. 质量评估\n\n"
            welcome_content += (
                "[dim]Built by [Tauric Research](https://github.com/TauricResearch)[/dim]"
            )

            # 创建并居中显示欢迎框 - 与TradingAgent一致
            welcome_box = Panel(
                welcome_content,
                border_style="cyan",  # 使用cyan作为PatentAgent的主题色
                padding=(1, 2),
                title="Welcome to PatentAgent",
                subtitle="专利发现、验证、分析与撰写系统",
            )
            self.console.print(Align.center(welcome_box))
            self.console.print()  # 添加空行
            
        except Exception as e:
            logger.error(f"显示欢迎界面失败: {str(e)}")
            self.console.print("[red]❌ 欢迎界面加载失败[/red]")

    def create_question_box(self, title: str, prompt: str, default: str = None) -> Panel:
        """创建问题框 - 与TradingAgent保持一致的风格"""
        box_content = f"[bold]{title}[/bold]\n"
        box_content += f"[dim]{prompt}[/dim]"
        if default:
            box_content += f"\n[dim]Default: {default}[/dim]"
        return Panel(box_content, border_style="blue", padding=(1, 2))

    def get_user_selections(self) -> Dict[str, str]:
        """获取用户选择 - 模仿TradingAgent的分步骤收集方式"""
        
        # 显示欢迎界面
        self.show_welcome()
        
        # Step 1: 分析类型选择
        self.console.print(
            self.create_question_box(
                "Step 1: 选择分析类型", 
                "选择您需要的专利分析类型", 
                ""
            )
        )
        analysis_type = self._select_analysis_type()
        
        # Step 2: 技术领域
        self.console.print(
            self.create_question_box(
                "Step 2: 技术领域", 
                "输入您要分析的技术领域", 
                "人工智能"
            )
        )
        technology_domain = self._get_technology_domain()
        
        # Step 3: 技术方向
        self.console.print(
            self.create_question_box(
                "Step 3: 技术方向", 
                f"输入{technology_domain}领域的具体技术方向", 
                "机器学习"
            )
        )
        technology_direction = self._get_technology_direction(technology_domain)
        
        # Step 4: 创新主题
        self.console.print(
            self.create_question_box(
                "Step 4: 创新主题", 
                "描述您的具体创新想法或技术方案", 
                ""
            )
        )
        innovation_topic = self._get_innovation_topic()
        
        # Step 5: 分析深度
        self.console.print(
            self.create_question_box(
                "Step 5: 分析深度", 
                "选择分析的详细程度", 
                "标准分析"
            )
        )
        analysis_depth = self._select_analysis_depth()
        
        return {
            "analysis_type": analysis_type,
            "technology_domain": technology_domain,
            "technology_direction": technology_direction,
            "innovation_topic": innovation_topic,
            "analysis_depth": analysis_depth,
            "analysis_date": datetime.datetime.now().strftime("%Y-%m-%d")
        }

    def _select_analysis_type(self) -> str:
        """选择分析类型"""
        analysis_types = {
            "1": {"name": "技术创新发现", "value": "discovery", "desc": "发现技术领域的创新机会"},
            "2": {"name": "专利可行性验证", "value": "validation", "desc": "验证专利申请的可行性"},
            "3": {"name": "专利价值分析", "value": "analysis", "desc": "分析专利的技术和商业价值"},
            "4": {"name": "专利申请撰写", "value": "writing", "desc": "撰写完整的专利申请文档"}
        }
        
        self.console.print("[bold]可用的分析类型:[/bold]")
        for key, value in analysis_types.items():
            self.console.print(f"  {key}. [cyan]{value['name']}[/cyan] - {value['desc']}")
        
        while True:
            try:
                choice = self.console.input("\n[bold yellow]请选择分析类型 (1-4): [/bold yellow]").strip()
                if choice in analysis_types:
                    selected = analysis_types[choice]
                    self.console.print(f"[green]✓ 已选择: {selected['name']}[/green]\n")
                    return selected["value"]
                else:
                    self.console.print("[red]❌ 无效选择，请输入1-4之间的数字[/red]")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]用户取消操作[/yellow]")
                sys.exit(0)

    def _get_technology_domain(self) -> str:
        """获取技术领域"""
        self.console.print("[bold]技术领域示例:[/bold]")
        domains = [
            "人工智能", "生物技术", "新能源", "区块链", 
            "物联网", "量子计算", "新材料", "医疗器械"
        ]
        
        for i, domain in enumerate(domains, 1):
            self.console.print(f"  {i}. [cyan]{domain}[/cyan]")
        
        while True:
            try:
                domain = self.console.input("\n[bold yellow]请输入技术领域: [/bold yellow]").strip()
                if domain:
                    self.console.print(f"[green]✓ 技术领域: {domain}[/green]\n")
                    return domain
                else:
                    self.console.print("[red]❌ 技术领域不能为空[/red]")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]用户取消操作[/yellow]")
                sys.exit(0)

    def _get_technology_direction(self, domain: str) -> str:
        """获取技术方向"""
        # 根据技术领域提供建议
        suggestions = self._get_domain_suggestions(domain)
        
        if suggestions:
            self.console.print(f"[bold]{domain} 领域的技术方向示例:[/bold]")
            for suggestion in suggestions[:6]:  # 显示前6个建议
                self.console.print(f"  • [cyan]{suggestion}[/cyan]")
        
        while True:
            try:
                direction = self.console.input("\n[bold yellow]请输入技术方向: [/bold yellow]").strip()
                if direction:
                    self.console.print(f"[green]✓ 技术方向: {direction}[/green]\n")
                    return direction
                else:
                    self.console.print("[red]❌ 技术方向不能为空[/red]")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]用户取消操作[/yellow]")
                sys.exit(0)

    def _get_innovation_topic(self) -> str:
        """获取创新主题"""
        self.console.print("[bold]创新主题示例:[/bold]")
        self.console.print("  • 基于深度学习的图像识别优化算法")
        self.console.print("  • 新型锂电池正极材料及其制备方法")
        self.console.print("  • 分布式区块链数据存储系统")
        self.console.print("  • 智能物联网设备安全认证方法")
        
        while True:
            try:
                topic = self.console.input("\n[bold yellow]请描述您的创新主题: [/bold yellow]").strip()
                if topic:
                    self.console.print(f"[green]✓ 创新主题: {topic}[/green]\n")
                    return topic
                else:
                    self.console.print("[red]❌ 创新主题不能为空[/red]")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]用户取消操作[/yellow]")
                sys.exit(0)

    def _select_analysis_depth(self) -> str:
        """选择分析深度"""
        depths = {
            "1": {"name": "快速分析", "value": "quick", "desc": "基础分析，快速获得结果"},
            "2": {"name": "标准分析", "value": "standard", "desc": "全面分析，平衡深度和速度"},
            "3": {"name": "深度分析", "value": "deep", "desc": "详细分析，最全面的结果"}
        }
        
        self.console.print("[bold]分析深度选项:[/bold]")
        for key, value in depths.items():
            self.console.print(f"  {key}. [cyan]{value['name']}[/cyan] - {value['desc']}")
        
        while True:
            try:
                choice = self.console.input("\n[bold yellow]请选择分析深度 (1-3, 默认2): [/bold yellow]").strip()
                if not choice:
                    choice = "2"  # 默认选择
                
                if choice in depths:
                    selected = depths[choice]
                    self.console.print(f"[green]✓ 分析深度: {selected['name']}[/green]\n")
                    return selected["value"]
                else:
                    self.console.print("[red]❌ 无效选择，请输入1-3之间的数字[/red]")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]用户取消操作[/yellow]")
                sys.exit(0)

    def _get_domain_suggestions(self, domain: str) -> list:
        """根据技术领域获取建议"""
        suggestions_map = {
            "人工智能": ["机器学习", "深度学习", "计算机视觉", "自然语言处理", "强化学习", "神经网络"],
            "生物技术": ["基因工程", "生物制药", "细胞治疗", "蛋白质工程", "生物传感器", "发酵技术"],
            "新能源": ["太阳能电池", "风力发电", "储能技术", "燃料电池", "电动汽车", "能源管理"],
            "区块链": ["分布式账本", "智能合约", "加密货币", "去中心化应用", "共识算法", "数字身份"],
            "物联网": ["传感器网络", "边缘计算", "智能家居", "工业物联网", "车联网", "无线通信"],
            "量子计算": ["量子算法", "量子通信", "量子密码", "量子纠错", "量子模拟", "量子传感"],
            "新材料": ["纳米材料", "复合材料", "智能材料", "生物材料", "超导材料", "功能材料"],
            "医疗器械": ["医学影像", "手术机器人", "植入式设备", "诊断设备", "康复设备", "远程医疗"]
        }
        
        # 模糊匹配
        for key, suggestions in suggestions_map.items():
            if key in domain or domain in key:
                return suggestions
        
        return ["请根据您的具体需求输入"]

    def run_patent_analysis(self, selections: Dict[str, str]):
        """运行专利分析 - 使用与TradingAgent类似的实时显示"""
        try:
            # 创建布局 - 模仿TradingAgent的布局结构
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=8),
                Layout(name="progress", size=12),
                Layout(name="messages", ratio=1),
                Layout(name="footer", size=6),
            )
            
            # 更新显示
            self._update_patent_display(layout, selections)
            
            # 模拟分析过程
            with Live(layout, console=self.console, refresh_per_second=2) as live:
                self._simulate_patent_analysis(layout, selections, live)
            
            # 显示完成信息
            self._show_analysis_complete(selections)
            
        except Exception as e:
            self.console.print(f"[red]❌ 专利分析失败: {str(e)}[/red]")
            logger.error(f"专利分析失败: {str(e)}")

    def _update_patent_display(self, layout, selections):
        """更新专利分析显示"""
        # Header
        layout["header"].update(
            Panel(
                "[bold cyan]PatentAgent 专利分析进行中[/bold cyan]\n"
                "[dim]© [Tauric Research](https://github.com/TauricResearch)[/dim]",
                title="PatentAgent Analysis",
                border_style="cyan",
                padding=(1, 2),
                expand=True,
            )
        )
        
        # Progress - 显示智能体团队状态
        progress_table = Table(
            show_header=True,
            header_style="bold magenta",
            show_footer=False,
            box=box.SIMPLE_HEAD,
            expand=True,
        )
        progress_table.add_column("团队", style="cyan", justify="center", width=20)
        progress_table.add_column("智能体", style="green", justify="center", width=25)
        progress_table.add_column("状态", style="yellow", justify="center", width=20)
        
        # 专利智能体团队
        teams = {
            "分析师团队": ["技术分析师", "创新发现师", "先行技术研究员", "市场情报分析师"],
            "研究团队": ["创新推进研究员", "风险评估研究员", "专利策略管理员"],
            "执行团队": ["专利撰写员", "质量评估师"],
        }
        
        for team, agents in teams.items():
            for i, agent in enumerate(agents):
                team_name = team if i == 0 else ""
                status = "pending"  # 初始状态
                status_cell = f"[yellow]{status}[/yellow]"
                progress_table.add_row(team_name, agent, status_cell)
            
            # 添加分隔线
            progress_table.add_row("─" * 20, "─" * 25, "─" * 20, style="dim")
        
        layout["progress"].update(
            Panel(progress_table, title="智能体状态", border_style="cyan", padding=(1, 2))
        )
        
        # Messages
        messages_table = Table(
            show_header=True,
            header_style="bold magenta",
            show_footer=False,
            expand=True,
            box=box.MINIMAL,
        )
        messages_table.add_column("时间", style="cyan", width=8, justify="center")
        messages_table.add_column("类型", style="green", width=12, justify="center")
        messages_table.add_column("内容", style="white", no_wrap=False, ratio=1)
        
        # 添加初始消息
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        messages_table.add_row(current_time, "系统", f"开始{selections['analysis_type']}分析")
        messages_table.add_row(current_time, "配置", f"技术领域: {selections['technology_domain']}")
        messages_table.add_row(current_time, "配置", f"技术方向: {selections['technology_direction']}")
        
        layout["messages"].update(
            Panel(messages_table, title="分析日志", border_style="cyan", padding=(1, 2))
        )
        
        # Footer - 显示分析参数
        footer_content = f"分析类型: {selections['analysis_type']} | "
        footer_content += f"技术领域: {selections['technology_domain']} | "
        footer_content += f"分析深度: {selections['analysis_depth']} | "
        footer_content += f"日期: {selections['analysis_date']}"
        
        layout["footer"].update(
            Panel(footer_content, border_style="grey50", padding=(0, 2))
        )

    def _simulate_patent_analysis(self, layout, selections, live):
        """模拟专利分析过程"""
        import time
        
        # 模拟分析步骤
        steps = [
            ("技术分析师", "分析技术领域发展趋势"),
            ("创新发现师", "识别创新机会和技术空白"),
            ("先行技术研究员", "检索相关专利和文献"),
            ("市场情报分析师", "评估商业价值和市场前景"),
            ("创新推进研究员", "论证技术优势和可行性"),
            ("风险评估研究员", "识别技术风险和专利风险"),
            ("专利策略管理员", "制定专利申请策略"),
            ("专利撰写员", "撰写专利申请文档"),
            ("质量评估师", "评估专利申请质量"),
        ]
        
        for i, (agent, task) in enumerate(steps):
            time.sleep(2)  # 模拟处理时间
            
            # 这里可以添加实际的分析逻辑
            self.console.print(f"[dim]正在执行: {agent} - {task}[/dim]")

    def _show_analysis_complete(self, selections):
        """显示分析完成信息"""
        complete_content = f"""
[bold green]✅ 专利分析完成！[/bold green]

[bold]分析结果摘要:[/bold]
• 分析类型: {selections['analysis_type']}
• 技术领域: {selections['technology_domain']}
• 技术方向: {selections['technology_direction']}
• 创新主题: {selections['innovation_topic']}
• 分析深度: {selections['analysis_depth']}

[bold]主要发现:[/bold]
• 技术可行性: 高
• 专利风险: 中等
• 商业价值: 有潜力
• 建议行动: 继续深入研究

[bold cyan]感谢使用PatentAgent！[/bold cyan]
"""
        
        complete_box = Panel(
            complete_content,
            border_style="green",
            padding=(1, 2),
            title="分析完成",
        )
        
        self.console.print(complete_box)

    def run(self):
        """运行PatentAgent分析 - 主入口"""
        try:
            self.console.print("[bold cyan]🔬 PatentAgent - 专利发现、验证、分析与撰写系统[/bold cyan]")
            self.console.print("[dim]正在启动专利智能体团队...[/dim]\n")
            
            # 验证API密钥配置
            validation_result = self.config_manager.validate_config("patent")
            if not validation_result["valid"]:
                self.console.print("[red]❌ 配置验证失败:[/red]")
                for error in validation_result["errors"]:
                    self.console.print(f"  • [red]{error}[/red]")
                self.console.print("\n[yellow]请检查API密钥配置后重试[/yellow]")
                return
            
            if validation_result["warnings"]:
                self.console.print("[yellow]⚠️ 配置警告:[/yellow]")
                for warning in validation_result["warnings"]:
                    self.console.print(f"  • [yellow]{warning}[/yellow]")
                self.console.print()
            
            self.console.print("[green]✅ 配置验证通过，启动PatentAgent分析流程[/green]\n")
            
            # 获取用户选择 - 使用与TradingAgent一致的分步骤方式
            selections = self.get_user_selections()
            
            # 运行分析
            self.run_patent_analysis(selections)
            
        except Exception as e:
            self.console.print(f"[red]❌ PatentAgent运行失败: {str(e)}[/red]")
            logger.error(f"PatentAgent运行失败: {str(e)}")


def main():
    """PatentAgent CLI主函数"""
    try:
        cli = PatentAgentCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n👋 感谢使用PatentAgent！")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")


if __name__ == "__main__":
    main() 