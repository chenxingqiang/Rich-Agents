"""
PatentAgent CLI Main - 专利智能体命令行主程序
提供用户友好的交互界面
"""

import os
import sys
import argparse
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from patentagents.graph.patent_graph import create_patent_agents_graph
from patentagents.llm_adapters.dashscope_adapter import DashScopeAdapter
from patentagents.config.config_manager import ConfigManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PatentAgentCLI:
    """专利智能体命令行界面"""
    
    def __init__(self):
        """初始化CLI"""
        self.config_manager = ConfigManager()
        self.llm = None
        self.graph = None
        
        # 加载配置
        self._load_configuration()
        
        # 初始化LLM
        self._initialize_llm()
        
        # 创建智能体图
        self._create_graph()
    
    def _load_configuration(self):
        """加载配置"""
        try:
            self.config = self.config_manager.get_config()
            logger.info("配置加载成功")
        except Exception as e:
            logger.error(f"配置加载失败: {str(e)}")
            self.config = {}
    
    def _initialize_llm(self):
        """初始化语言模型"""
        try:
            # 默认使用DashScope
            self.llm = DashScopeAdapter(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                model_name=self.config.get("model", {}).get("name", "qwen-turbo")
            )
            logger.info("LLM初始化成功")
        except Exception as e:
            logger.error(f"LLM初始化失败: {str(e)}")
            self.llm = None
    
    def _create_graph(self):
        """创建智能体图"""
        try:
            if self.llm:
                self.graph = create_patent_agents_graph(self.llm, self.config)
                logger.info("智能体图创建成功")
            else:
                logger.error("无法创建智能体图：LLM未初始化")
        except Exception as e:
            logger.error(f"智能体图创建失败: {str(e)}")
            self.graph = None
    
    def show_welcome(self):
        """显示欢迎信息"""
        welcome_text = """
╔════════════════════════════════════════════════════════════════╗
║                      PatentAgent 专利智能体                      ║
║                                                                ║
║    🔬 技术分析  |  💡 创新发现  |  📊 先行技术  |  ✍️ 专利撰写    ║
║                                                                ║
║              将AI技术深度应用于知识产权领域                      ║
╚════════════════════════════════════════════════════════════════╝

欢迎使用PatentAgent！请选择您的需求：

1. 🔍 技术创新发现 - 发现技术领域的创新机会
2. ✅ 专利可行性验证 - 验证专利申请的可行性
3. 📊 专利价值分析 - 分析专利的技术和商业价值
4. ✍️ 专利申请撰写 - 撰写完整的专利申请文档
5. 🔧 系统状态检查 - 检查系统配置和状态
6. ❓ 帮助信息 - 查看详细使用说明
7. 🚪 退出系统

"""
        print(welcome_text)
    
    def get_user_choice(self) -> str:
        """获取用户选择"""
        while True:
            try:
                choice = input("请输入您的选择 (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    return choice
                else:
                    print("❌ 无效选择，请输入1-7之间的数字")
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用PatentAgent！")
                sys.exit(0)
            except Exception as e:
                print(f"❌ 输入错误: {str(e)}")
    
    def get_technology_info(self) -> Dict[str, str]:
        """获取技术信息"""
        print("\n" + "="*50)
        print("📝 请输入技术信息")
        print("="*50)
        
        # 获取技术领域
        print("\n💡 技术领域示例:")
        print("   • 人工智能 (AI、机器学习、深度学习)")
        print("   • 生物技术 (基因工程、生物制药)")
        print("   • 新能源 (太阳能、风能、储能)")
        print("   • 区块链 (分布式账本、加密货币)")
        print("   • 物联网 (IoT、智能设备)")
        print("   • 量子计算 (量子算法、量子通信)")
        
        while True:
            technology_domain = input("\n请输入技术领域: ").strip()
            if technology_domain:
                break
            print("❌ 技术领域不能为空，请重新输入")
        
        # 获取具体方向
        print(f"\n🎯 {technology_domain} 领域的具体方向示例:")
        
        # 根据技术领域提供具体建议
        suggestions = self._get_domain_suggestions(technology_domain)
        for suggestion in suggestions:
            print(f"   • {suggestion}")
        
        while True:
            innovation_topic = input(f"\n请输入 {technology_domain} 的具体技术方向: ").strip()
            if innovation_topic:
                break
            print("❌ 技术方向不能为空，请重新输入")
        
        return {
            "technology_domain": technology_domain,
            "innovation_topic": innovation_topic
        }
    
    def _get_domain_suggestions(self, domain: str) -> list:
        """根据技术领域获取具体方向建议"""
        suggestions_map = {
            "人工智能": [
                "计算机视觉 (图像识别、目标检测)",
                "自然语言处理 (文本分析、机器翻译)",
                "机器学习 (深度学习、强化学习)",
                "语音识别 (语音合成、语音理解)"
            ],
            "生物技术": [
                "基因编辑 (CRISPR、基因治疗)",
                "生物制药 (抗体药物、疫苗)",
                "生物材料 (生物降解材料、仿生材料)",
                "生物传感器 (生物检测、诊断技术)"
            ],
            "新能源": [
                "太阳能技术 (光伏电池、太阳能电池)",
                "风能技术 (风力发电、风机设计)",
                "储能技术 (电池技术、储能系统)",
                "氢能技术 (氢燃料电池、氢气制备)"
            ],
            "区块链": [
                "加密货币 (数字货币、支付系统)",
                "智能合约 (去中心化应用、DeFi)",
                "供应链管理 (溯源系统、物流追踪)",
                "数字身份 (身份认证、隐私保护)"
            ]
        }
        
        # 模糊匹配
        for key, suggestions in suggestions_map.items():
            if key in domain or any(keyword in domain.lower() for keyword in key.lower().split()):
                return suggestions
        
        # 默认建议
        return [
            "核心算法或方法",
            "系统架构或设计",
            "设备或装置",
            "应用场景或用途"
        ]
    
    def run_patent_analysis(self, technology_domain: str, innovation_topic: str, analysis_type: str = "discovery"):
        """运行专利分析"""
        
        if not self.graph:
            print("❌ 系统未正确初始化，无法执行分析")
            return
        
        print(f"\n🚀 开始分析...")
        print(f"📍 技术领域: {technology_domain}")
        print(f"🎯 具体方向: {innovation_topic}")
        print(f"📊 分析类型: {analysis_type}")
        print("=" * 60)
        
        try:
            # 显示进度
            print("🔬 技术分析师正在分析技术领域...")
            
            # 运行分析
            result = self.graph.run_analysis(
                technology_domain=technology_domain,
                innovation_topic=innovation_topic,
                analysis_type=analysis_type
            )
            
            if result["success"]:
                print("✅ 分析完成！")
                self._display_analysis_results(result)
                
                # 询问是否保存结果
                if self._ask_save_results():
                    self._save_analysis_results(result, technology_domain, innovation_topic)
                
            else:
                print(f"❌ 分析失败: {result.get('error', '未知错误')}")
                
        except Exception as e:
            print(f"❌ 分析过程中发生错误: {str(e)}")
            logger.error(f"分析失败: {str(e)}")
    
    def _display_analysis_results(self, result: Dict[str, Any]):
        """显示分析结果"""
        print("\n" + "="*60)
        print("📋 分析结果摘要")
        print("="*60)
        
        summary = result.get("analysis_summary", {})
        
        print(f"🎯 技术领域: {summary.get('technology_domain', 'N/A')}")
        print(f"💡 创新主题: {summary.get('innovation_topic', 'N/A')}")
        print(f"📅 分析日期: {summary.get('analysis_date', 'N/A')}")
        print(f"📊 质量评分: {summary.get('quality_score', 0)}/100")
        print(f"📝 权利要求数: {summary.get('patent_claims_count', 0)}")
        
        # 显示生成的报告
        reports = summary.get("reports_generated", [])
        if reports:
            print(f"\n📄 生成的报告:")
            for i, report in enumerate(reports, 1):
                print(f"   {i}. {report}")
        
        # 显示关键发现
        findings = summary.get("key_findings", [])
        if findings:
            print(f"\n🔍 关键发现:")
            for i, finding in enumerate(findings, 1):
                print(f"   {i}. {finding}")
        
        # 显示最终报告摘要
        final_report = result.get("final_report", "")
        if final_report:
            print(f"\n📋 最终报告摘要:")
            print("-" * 40)
            # 显示报告的前500字符
            print(final_report[:500] + "..." if len(final_report) > 500 else final_report)
        
        print("\n" + "="*60)
    
    def _ask_save_results(self) -> bool:
        """询问是否保存结果"""
        while True:
            try:
                choice = input("\n💾 是否保存分析结果到文件? (y/n): ").strip().lower()
                if choice in ['y', 'yes', '是', 'Y']:
                    return True
                elif choice in ['n', 'no', '否', 'N']:
                    return False
                else:
                    print("❌ 请输入 y(是) 或 n(否)")
            except KeyboardInterrupt:
                return False
    
    def _save_analysis_results(self, result: Dict[str, Any], technology_domain: str, innovation_topic: str):
        """保存分析结果"""
        try:
            # 创建输出目录
            output_dir = "patent_analysis_results"
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"patent_analysis_{technology_domain}_{innovation_topic}_{timestamp}".replace(" ", "_")
            
            # 保存完整结果为JSON
            json_file = os.path.join(output_dir, f"{filename}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # 保存最终报告为Markdown
            if result.get("final_report"):
                md_file = os.path.join(output_dir, f"{filename}_report.md")
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(result["final_report"])
            
            # 保存专利申请文档
            if result.get("patent_application"):
                patent_file = os.path.join(output_dir, f"{filename}_patent.md")
                with open(patent_file, 'w', encoding='utf-8') as f:
                    f.write(result["patent_application"])
            
            print(f"✅ 分析结果已保存到:")
            print(f"   📁 目录: {output_dir}")
            print(f"   📄 完整结果: {json_file}")
            if result.get("final_report"):
                print(f"   📋 分析报告: {md_file}")
            if result.get("patent_application"):
                print(f"   📝 专利申请: {patent_file}")
                
        except Exception as e:
            print(f"❌ 保存结果失败: {str(e)}")
            logger.error(f"保存结果失败: {str(e)}")
    
    def show_system_status(self):
        """显示系统状态"""
        print("\n" + "="*50)
        print("🔧 系统状态检查")
        print("="*50)
        
        # 检查LLM状态
        print("🤖 语言模型状态:")
        if self.llm:
            print("   ✅ LLM已初始化")
            print(f"   📋 模型类型: {type(self.llm).__name__}")
        else:
            print("   ❌ LLM未初始化")
        
        # 检查智能体图状态
        print("\n🕸️ 智能体图状态:")
        if self.graph:
            print("   ✅ 智能体图已创建")
            status = self.graph.get_workflow_status()
            print(f"   👥 可用智能体: {len(status['available_agents'])}")
            print(f"   🔗 工作流程节点: {len(status['workflow_nodes'])}")
            
            # 显示智能体列表
            print("\n   📋 智能体列表:")
            for agent in status['available_agents']:
                print(f"      • {agent}")
                
        else:
            print("   ❌ 智能体图未创建")
        
        # 检查配置状态
        print("\n⚙️ 配置状态:")
        if self.config:
            print("   ✅ 配置已加载")
            print(f"   📊 配置项数量: {len(self.config)}")
        else:
            print("   ❌ 配置未加载")
        
        # 检查API密钥
        print("\n🔑 API密钥状态:")
        api_keys = [
            ("DASHSCOPE_API_KEY", "百炼API"),
            ("SERPAPI_API_KEY", "Google Patents API"),
            ("ZHIHUIYA_CLIENT_ID", "智慧芽客户端ID"),
            ("ZHIHUIYA_CLIENT_SECRET", "智慧芽客户端密钥")
        ]
        
        for env_var, description in api_keys:
            if os.getenv(env_var):
                print(f"   ✅ {description}: 已配置")
            else:
                print(f"   ❌ {description}: 未配置")
        
        print("\n" + "="*50)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
📖 PatentAgent 使用指南

🎯 主要功能:
1. 技术创新发现 - 自动发现技术领域的创新机会和技术空白
2. 专利可行性验证 - 深度分析专利申请的可行性和成功概率
3. 专利价值分析 - 评估专利的技术价值和商业价值
4. 专利申请撰写 - 生成符合专利局标准的专利申请文档

🔧 系统要求:
• Python 3.8+
• 配置相关API密钥 (百炼、Google Patents、智慧芽等)
• 稳定的网络连接

📝 使用流程:
1. 选择分析类型
2. 输入技术领域和具体方向
3. 系统自动进行多智能体协作分析
4. 查看分析结果和专利申请文档
5. 可选择保存结果到本地文件

🔑 API配置:
请在环境变量中设置以下API密钥:
• DASHSCOPE_API_KEY - 百炼大模型API密钥
• SERPAPI_API_KEY - Google Patents检索API密钥
• ZHIHUIYA_CLIENT_ID - 智慧芽客户端ID
• ZHIHUIYA_CLIENT_SECRET - 智慧芽客户端密钥

📞 技术支持:
如遇问题，请检查:
1. API密钥是否正确配置
2. 网络连接是否正常
3. 输入的技术领域是否明确
4. 系统日志中的错误信息

🌟 最佳实践:
• 提供具体、明确的技术领域描述
• 选择合适的分析类型
• 定期检查系统状态
• 保存重要的分析结果

"""
        print(help_text)
    
    def run(self):
        """运行CLI主循环"""
        while True:
            try:
                self.show_welcome()
                choice = self.get_user_choice()
                
                if choice == '1':  # 技术创新发现
                    tech_info = self.get_technology_info()
                    self.run_patent_analysis(
                        tech_info["technology_domain"],
                        tech_info["innovation_topic"],
                        "discovery"
                    )
                
                elif choice == '2':  # 专利可行性验证
                    tech_info = self.get_technology_info()
                    self.run_patent_analysis(
                        tech_info["technology_domain"],
                        tech_info["innovation_topic"],
                        "validation"
                    )
                
                elif choice == '3':  # 专利价值分析
                    tech_info = self.get_technology_info()
                    self.run_patent_analysis(
                        tech_info["technology_domain"],
                        tech_info["innovation_topic"],
                        "analysis"
                    )
                
                elif choice == '4':  # 专利申请撰写
                    tech_info = self.get_technology_info()
                    self.run_patent_analysis(
                        tech_info["technology_domain"],
                        tech_info["innovation_topic"],
                        "writing"
                    )
                
                elif choice == '5':  # 系统状态检查
                    self.show_system_status()
                
                elif choice == '6':  # 帮助信息
                    self.show_help()
                
                elif choice == '7':  # 退出系统
                    print("\n👋 感谢使用PatentAgent！")
                    break
                
                # 询问是否继续
                if choice in ['1', '2', '3', '4']:
                    while True:
                        try:
                            continue_choice = input("\n🔄 是否继续使用系统? (y/n): ").strip().lower()
                            if continue_choice in ['y', 'yes', '是', 'Y']:
                                break
                            elif continue_choice in ['n', 'no', '否', 'N']:
                                print("\n👋 感谢使用PatentAgent！")
                                return
                            else:
                                print("❌ 请输入 y(是) 或 n(否)")
                        except KeyboardInterrupt:
                            print("\n\n👋 感谢使用PatentAgent！")
                            return
                
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用PatentAgent！")
                break
            except Exception as e:
                print(f"❌ 系统错误: {str(e)}")
                logger.error(f"CLI运行错误: {str(e)}")


def run_patent_cli():
    """运行专利智能体CLI的入口函数"""
    try:
        cli = PatentAgentCLI()
        cli.run()
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        logger.error(f"CLI启动失败: {str(e)}")
        sys.exit(1)


def main():
    """主函数 - 支持命令行参数"""
    parser = argparse.ArgumentParser(description="PatentAgent 专利智能体系统")
    parser.add_argument(
        "--domain", 
        help="技术领域",
        type=str
    )
    parser.add_argument(
        "--topic", 
        help="具体技术方向",
        type=str
    )
    parser.add_argument(
        "--type", 
        help="分析类型 (discovery/validation/analysis/writing)",
        type=str,
        default="discovery"
    )
    parser.add_argument(
        "--config",
        help="配置文件路径",
        type=str
    )
    parser.add_argument(
        "--output",
        help="输出目录",
        type=str,
        default="patent_analysis_results"
    )
    
    args = parser.parse_args()
    
    # 如果提供了命令行参数，直接运行分析
    if args.domain and args.topic:
        try:
            cli = PatentAgentCLI()
            cli.run_patent_analysis(args.domain, args.topic, args.type)
        except Exception as e:
            print(f"❌ 命令行分析失败: {str(e)}")
            sys.exit(1)
    else:
        # 否则运行交互式CLI
        run_patent_cli()


if __name__ == "__main__":
    main() 