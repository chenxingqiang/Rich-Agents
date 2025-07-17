"""
Patent Agents Graph - 专利智能体图
定义专利分析的完整工作流程和智能体协作逻辑
"""

import logging
from typing import Dict, Any, List, Literal
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from ..agents.utils.patent_states import PatentState, create_initial_patent_state
from ..agents.utils.patent_utils import PatentToolkit
from ..agents.analysts.technology_analyst import create_technology_analyst
from ..agents.analysts.innovation_discovery import create_innovation_discovery_analyst
from ..agents.analysts.prior_art_researcher import create_prior_art_researcher
from ..agents.writers.patent_writer import create_patent_writer

logger = logging.getLogger(__name__)


class PatentAgentsGraph:
    """
    专利智能体图 - 管理专利分析的完整工作流程
    """
    
    def __init__(self, llm, config: Dict[str, Any] = None):
        """
        初始化专利智能体图
        
        Args:
            llm: 语言模型实例
            config: 配置字典
        """
        self.llm = llm
        self.config = config or {}
        
        # 初始化专利工具包
        self.toolkit = PatentToolkit(config)
        
        # 创建智能体
        self.technology_analyst = create_technology_analyst(llm, self.toolkit)
        self.innovation_discovery = create_innovation_discovery_analyst(llm, self.toolkit)
        self.prior_art_researcher = create_prior_art_researcher(llm, self.toolkit)
        self.patent_writer = create_patent_writer(llm, self.toolkit)
        
        # 构建工作流程图
        self.graph = self._build_graph()
        
        logger.info("专利智能体图初始化完成")
    
    def _build_graph(self) -> StateGraph:
        """构建专利分析工作流程图"""
        
        # 创建状态图
        workflow = StateGraph(PatentState)
        
        # 添加智能体节点
        workflow.add_node("technology_analyst", self.technology_analyst)
        workflow.add_node("innovation_discovery", self.innovation_discovery)
        workflow.add_node("prior_art_researcher", self.prior_art_researcher)
        workflow.add_node("patent_writer", self.patent_writer)
        
        # 添加决策节点
        workflow.add_node("analysis_router", self._analysis_router)
        workflow.add_node("quality_checker", self._quality_checker)
        workflow.add_node("final_reviewer", self._final_reviewer)
        
        # 定义工作流程
        workflow.set_entry_point("technology_analyst")
        
        # 技术分析师 -> 创新发现师
        workflow.add_edge("technology_analyst", "innovation_discovery")
        
        # 创新发现师 -> 先行技术研究员
        workflow.add_edge("innovation_discovery", "prior_art_researcher")
        
        # 先行技术研究员 -> 分析路由器
        workflow.add_edge("prior_art_researcher", "analysis_router")
        
        # 分析路由器的条件路由
        workflow.add_conditional_edges(
            "analysis_router",
            self._should_continue_analysis,
            {
                "continue": "technology_analyst",  # 需要更多分析
                "proceed": "patent_writer",       # 继续专利撰写
                "end": END                        # 结束分析
            }
        )
        
        # 专利撰写员 -> 质量检查器
        workflow.add_edge("patent_writer", "quality_checker")
        
        # 质量检查器的条件路由
        workflow.add_conditional_edges(
            "quality_checker",
            self._should_revise_patent,
            {
                "revise": "patent_writer",        # 需要修改专利
                "review": "final_reviewer",       # 进入最终审查
                "approve": END                    # 直接通过
            }
        )
        
        # 最终审查器 -> 结束
        workflow.add_edge("final_reviewer", END)
        
        # 编译图
        return workflow.compile()
    
    def _analysis_router(self, state: PatentState) -> Dict[str, Any]:
        """分析路由器 - 决定是否需要更多分析"""
        
        # 检查分析完整性
        analysis_completeness = self._check_analysis_completeness(state)
        
        router_decision = {
            "messages": [{"role": "system", "content": f"分析路由器决策: {analysis_completeness['decision']}"}],
            "sender": "Analysis Router",
            "analysis_completeness": analysis_completeness
        }
        
        logger.info(f"分析路由器决策: {analysis_completeness['decision']}")
        return router_decision
    
    def _quality_checker(self, state: PatentState) -> Dict[str, Any]:
        """质量检查器 - 检查专利草稿质量"""
        
        patent_draft = state.get("patent_draft", "")
        
        # 使用工具包验证专利格式
        format_validation = self.toolkit.validate_patent_format(patent_draft)
        
        # 进行质量评估
        quality_assessment = self._assess_patent_quality(state)
        
        quality_result = {
            "messages": [{"role": "system", "content": f"质量检查结果: {quality_assessment['decision']}"}],
            "sender": "Quality Checker",
            "quality_assessment": quality_assessment,
            "format_validation": format_validation
        }
        
        logger.info(f"质量检查结果: {quality_assessment['decision']}")
        return quality_result
    
    def _final_reviewer(self, state: PatentState) -> Dict[str, Any]:
        """最终审查器 - 生成最终专利申请"""
        
        # 整合所有分析结果
        final_report = self._generate_final_report(state)
        
        # 生成最终专利申请
        final_patent_application = self._finalize_patent_application(state)
        
        final_result = {
            "messages": [{"role": "system", "content": "最终审查完成"}],
            "sender": "Final Reviewer",
            "final_patent_application": final_patent_application,
            "final_report": final_report
        }
        
        logger.info("最终审查完成")
        return final_result
    
    def _should_continue_analysis(self, state: PatentState) -> Literal["continue", "proceed", "end"]:
        """决定是否继续分析"""
        
        analysis_completeness = state.get("analysis_completeness", {})
        
        if analysis_completeness.get("score", 0) < 60:
            return "continue"  # 需要更多分析
        elif analysis_completeness.get("score", 0) < 80:
            return "proceed"   # 可以继续专利撰写
        else:
            return "end"       # 分析已足够完整
    
    def _should_revise_patent(self, state: PatentState) -> Literal["revise", "review", "approve"]:
        """决定是否需要修改专利"""
        
        quality_assessment = state.get("quality_assessment", {})
        
        if quality_assessment.get("score", 0) < 50:
            return "revise"    # 需要重新撰写
        elif quality_assessment.get("score", 0) < 80:
            return "review"    # 需要最终审查
        else:
            return "approve"   # 直接通过
    
    def _check_analysis_completeness(self, state: PatentState) -> Dict[str, Any]:
        """检查分析完整性"""
        
        completeness = {
            "score": 0,
            "decision": "continue",
            "missing_elements": [],
            "quality_issues": []
        }
        
        # 检查必要的分析报告
        required_reports = [
            ("technology_report", "技术分析报告"),
            ("innovation_opportunities", "创新机会报告"),
            ("prior_art_report", "先行技术报告")
        ]
        
        for field, name in required_reports:
            report = state.get(field, "")
            if report and len(report) > 500:
                completeness["score"] += 30
            else:
                completeness["missing_elements"].append(name)
        
        # 检查数据完整性
        if state.get("patent_search_results"):
            completeness["score"] += 10
        else:
            completeness["quality_issues"].append("缺少专利检索数据")
        
        # 决定下一步行动
        if completeness["score"] >= 80:
            completeness["decision"] = "proceed"
        elif completeness["score"] >= 60:
            completeness["decision"] = "proceed"
        else:
            completeness["decision"] = "continue"
        
        return completeness
    
    def _assess_patent_quality(self, state: PatentState) -> Dict[str, Any]:
        """评估专利质量"""
        
        quality = {
            "score": 0,
            "decision": "revise",
            "strengths": [],
            "weaknesses": []
        }
        
        patent_draft = state.get("patent_draft", "")
        
        # 检查专利草稿长度
        if len(patent_draft) > 2000:
            quality["score"] += 20
            quality["strengths"].append("专利文档内容充实")
        else:
            quality["weaknesses"].append("专利文档内容过短")
        
        # 检查必要章节
        required_sections = ["发明名称", "技术领域", "背景技术", "发明内容", "权利要求书"]
        present_sections = sum(1 for section in required_sections if section in patent_draft)
        
        quality["score"] += present_sections * 10
        
        if present_sections == len(required_sections):
            quality["strengths"].append("包含所有必要章节")
        else:
            quality["weaknesses"].append(f"缺少 {len(required_sections) - present_sections} 个必要章节")
        
        # 检查权利要求
        claims_count = len(state.get("patent_claims", []))
        if claims_count >= 3:
            quality["score"] += 15
            quality["strengths"].append("权利要求数量充足")
        else:
            quality["weaknesses"].append("权利要求数量不足")
        
        # 检查技术描述质量
        if "实施例" in patent_draft:
            quality["score"] += 10
            quality["strengths"].append("包含具体实施例")
        else:
            quality["weaknesses"].append("缺少具体实施例")
        
        # 决定下一步行动
        if quality["score"] >= 80:
            quality["decision"] = "approve"
        elif quality["score"] >= 60:
            quality["decision"] = "review"
        else:
            quality["decision"] = "revise"
        
        return quality
    
    def _generate_final_report(self, state: PatentState) -> str:
        """生成最终分析报告"""
        
        report_sections = []
        
        # 添加执行摘要
        report_sections.append("# 专利分析最终报告")
        report_sections.append(f"**技术领域**: {state.get('technology_domain', 'N/A')}")
        report_sections.append(f"**创新主题**: {state.get('innovation_topic', 'N/A')}")
        report_sections.append(f"**分析日期**: {state.get('analysis_date', 'N/A')}")
        
        # 添加分析结果摘要
        report_sections.append("\n## 分析结果摘要")
        
        if state.get("technology_report"):
            report_sections.append("### 技术分析")
            report_sections.append(state["technology_report"][:500] + "...")
        
        if state.get("innovation_opportunities"):
            report_sections.append("### 创新机会")
            report_sections.append(state["innovation_opportunities"][:500] + "...")
        
        if state.get("prior_art_report"):
            report_sections.append("### 先行技术")
            report_sections.append(state["prior_art_report"][:500] + "...")
        
        # 添加专利草稿摘要
        if state.get("patent_draft"):
            report_sections.append("### 专利申请")
            report_sections.append("专利申请文档已完成，包含完整的技术描述和权利要求。")
        
        # 添加质量评估
        quality_assessment = state.get("quality_assessment", {})
        if quality_assessment:
            report_sections.append(f"### 质量评估")
            report_sections.append(f"**质量分数**: {quality_assessment.get('score', 0)}/100")
            report_sections.append(f"**优势**: {', '.join(quality_assessment.get('strengths', []))}")
            report_sections.append(f"**建议**: {', '.join(quality_assessment.get('weaknesses', []))}")
        
        return "\n".join(report_sections)
    
    def _finalize_patent_application(self, state: PatentState) -> str:
        """生成最终专利申请文档"""
        
        patent_draft = state.get("patent_draft", "")
        
        # 添加标准化的头部信息
        header = f"""专利申请文档
申请日期: {state.get('analysis_date', datetime.now().strftime('%Y-%m-%d'))}
技术领域: {state.get('technology_domain', 'N/A')}
申请人: [待填写]
发明人: [待填写]

{'='*50}

"""
        
        # 添加尾部信息
        footer = f"""

{'='*50}

本专利申请文档由PatentAgent智能体系统生成
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
分析质量: {state.get('quality_assessment', {}).get('score', 0)}/100
"""
        
        return header + patent_draft + footer
    
    def run_analysis(
        self,
        technology_domain: str,
        innovation_topic: str,
        analysis_type: str = "discovery"
    ) -> Dict[str, Any]:
        """
        运行专利分析
        
        Args:
            technology_domain: 技术领域
            innovation_topic: 创新主题
            analysis_type: 分析类型
            
        Returns:
            Dict: 分析结果
        """
        
        # 创建初始状态
        initial_state = create_initial_patent_state(
            technology_domain=technology_domain,
            innovation_topic=innovation_topic,
            analysis_type=analysis_type
        )
        
        logger.info(f"开始专利分析: {technology_domain} - {innovation_topic}")
        
        try:
            # 运行工作流程
            result = self.graph.invoke(initial_state)
            
            logger.info("专利分析完成")
            return {
                "success": True,
                "result": result,
                "final_report": result.get("final_report", ""),
                "patent_application": result.get("final_patent_application", ""),
                "analysis_summary": self._create_analysis_summary(result)
            }
            
        except Exception as e:
            logger.error(f"专利分析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    def _create_analysis_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """创建分析摘要"""
        
        summary = {
            "technology_domain": result.get("technology_domain", ""),
            "innovation_topic": result.get("innovation_topic", ""),
            "analysis_date": result.get("analysis_date", ""),
            "reports_generated": [],
            "patent_claims_count": len(result.get("patent_claims", [])),
            "quality_score": result.get("quality_assessment", {}).get("score", 0),
            "key_findings": []
        }
        
        # 统计生成的报告
        report_fields = [
            ("technology_report", "技术分析报告"),
            ("innovation_opportunities", "创新机会报告"),
            ("prior_art_report", "先行技术报告"),
            ("patent_draft", "专利申请草稿")
        ]
        
        for field, name in report_fields:
            if result.get(field):
                summary["reports_generated"].append(name)
        
        # 提取关键发现
        if result.get("innovation_list"):
            summary["key_findings"].append(f"发现 {len(result['innovation_list'])} 个创新机会")
        
        if result.get("patent_search_results"):
            summary["key_findings"].append(f"分析了 {len(result['patent_search_results'])} 个相关专利")
        
        if result.get("infringement_risk"):
            risk_level = result["infringement_risk"].get("overall_risk_level", "low")
            summary["key_findings"].append(f"侵权风险等级: {risk_level}")
        
        return summary
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """获取工作流程状态"""
        
        return {
            "toolkit_status": self.toolkit.get_toolkit_status(),
            "available_agents": [
                "Technology Analyst",
                "Innovation Discovery Analyst", 
                "Prior Art Researcher",
                "Patent Writer"
            ],
            "workflow_nodes": [
                "technology_analyst",
                "innovation_discovery", 
                "prior_art_researcher",
                "patent_writer",
                "analysis_router",
                "quality_checker",
                "final_reviewer"
            ],
            "configuration": self.config
        }


# 便捷函数
def create_patent_agents_graph(llm, config: Dict[str, Any] = None) -> PatentAgentsGraph:
    """创建专利智能体图实例"""
    return PatentAgentsGraph(llm, config)


def run_patent_analysis(
    llm,
    technology_domain: str,
    innovation_topic: str,
    config: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    运行专利分析的便捷函数
    
    Args:
        llm: 语言模型实例
        technology_domain: 技术领域
        innovation_topic: 创新主题
        config: 配置字典
        
    Returns:
        Dict: 分析结果
    """
    
    graph = create_patent_agents_graph(llm, config)
    return graph.run_analysis(technology_domain, innovation_topic)


# 测试函数
def test_patent_graph():
    """测试专利智能体图功能"""
    print("🧪 测试专利智能体图...")
    
    try:
        # 模拟LLM（实际使用时需要真实的LLM）
        class MockLLM:
            def invoke(self, messages):
                class MockResult:
                    content = "模拟的分析结果"
                return MockResult()
        
        mock_llm = MockLLM()
        
        # 创建专利智能体图
        graph = create_patent_agents_graph(mock_llm)
        
        # 检查状态
        status = graph.get_workflow_status()
        print(f"✅ 工作流程状态: {len(status['available_agents'])} 个智能体")
        print(f"✅ 工作流程节点: {len(status['workflow_nodes'])} 个节点")
        
        # 创建测试状态
        test_state = create_initial_patent_state(
            technology_domain="人工智能",
            innovation_topic="图像识别",
            analysis_type="discovery"
        )
        
        # 测试分析完整性检查
        completeness = graph._check_analysis_completeness(test_state)
        print(f"✅ 分析完整性检查: {completeness['score']}/100")
        
        print("🎉 专利智能体图测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    test_patent_graph() 