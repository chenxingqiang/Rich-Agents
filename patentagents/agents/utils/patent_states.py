"""
Patent State Management System
专利状态管理系统 - 定义专利分析过程中的各种状态
"""

from typing import Annotated, Dict, List, Optional, Any
try:
    from typing_extensions import TypedDict
except ImportError:
    from typing import TypedDict
from langgraph.graph import MessagesState


class PatentDebateState(TypedDict):
    """专利辩论状态"""
    participants: List[str]  # 参与者列表
    arguments: List[Dict[str, Any]]  # 论证列表
    current_round: int  # 当前轮次
    consensus_reached: bool  # 是否达成共识
    final_decision: Optional[str]  # 最终决策


class PatentValidationState(TypedDict):
    """专利验证状态"""
    validation_type: str  # 验证类型
    criteria: List[str]  # 验证标准
    results: Dict[str, Any]  # 验证结果
    confidence_score: float  # 置信度分数
    recommendations: List[str]  # 建议列表


class PatentState(MessagesState):
    """
    专利分析状态管理
    继承自MessagesState，支持消息传递和状态跟踪
    """
    
    # 基础信息
    technology_domain: Annotated[str, "技术领域，如：人工智能、生物技术、新能源"]
    innovation_topic: Annotated[str, "创新主题，具体的技术方向或产品"]
    analysis_date: Annotated[str, "分析日期，格式：YYYY-MM-DD"]
    analysis_type: Annotated[str, "分析类型：discovery/validation/analysis/writing"]
    
    # 发送者信息
    sender: Annotated[str, "发送当前消息的智能体名称"]
    
    # 分析阶段输出
    technology_report: Annotated[str, "技术分析师的技术领域分析报告"]
    innovation_opportunities: Annotated[str, "创新发现师的创新机会识别报告"]
    prior_art_report: Annotated[str, "先行技术研究员的现有技术状态报告"]
    market_intelligence: Annotated[str, "市场情报分析师的商业价值评估报告"]
    
    # 研究阶段输出
    innovation_advocacy: Annotated[str, "创新推进研究员的优势论证分析"]
    risk_assessment: Annotated[str, "风险评估研究员的风险识别报告"]
    patent_strategy: Annotated[str, "专利策略管理员的策略建议"]
    
    # 辩论状态
    innovation_debate_state: Annotated[
        PatentDebateState, "创新推进vs风险评估的辩论状态"
    ]
    validation_debate_state: Annotated[
        PatentValidationState, "专利验证过程的状态跟踪"
    ]
    
    # 执行阶段输出
    patent_draft: Annotated[str, "专利撰写员生成的专利申请草稿"]
    quality_assessment: Annotated[str, "质量评估师的质量评估报告"]
    final_patent_application: Annotated[str, "最终的专利申请文档"]
    
    # 专利数据
    patent_search_results: Annotated[List[Dict], "专利检索结果列表"]
    similar_patents: Annotated[List[Dict], "相似专利列表"]
    patent_citations: Annotated[List[Dict], "专利引用关系"]
    patent_classifications: Annotated[List[str], "专利分类代码"]
    
    # 技术文献数据
    literature_results: Annotated[List[Dict], "技术文献检索结果"]
    research_trends: Annotated[Dict[str, Any], "研究趋势分析"]
    
    # 市场数据
    market_analysis: Annotated[Dict[str, Any], "市场分析数据"]
    competitive_landscape: Annotated[Dict[str, Any], "竞争格局分析"]
    
    # 验证结果
    novelty_assessment: Annotated[Dict[str, Any], "新颖性评估结果"]
    inventiveness_assessment: Annotated[Dict[str, Any], "创造性评估结果"]
    utility_assessment: Annotated[Dict[str, Any], "实用性评估结果"]
    
    # 风险评估
    infringement_risk: Annotated[Dict[str, Any], "侵权风险评估"]
    grant_probability: Annotated[float, "授权概率预测"]
    commercial_potential: Annotated[Dict[str, Any], "商业化潜力评估"]


class PatentAnalysisContext:
    """专利分析上下文管理器"""
    
    def __init__(self):
        self.current_state: Optional[PatentState] = None
        self.history: List[PatentState] = []
        self.metadata: Dict[str, Any] = {}
    
    def update_state(self, state: PatentState) -> None:
        """更新当前状态"""
        if self.current_state:
            self.history.append(self.current_state)
        self.current_state = state
    
    def get_state_history(self) -> List[PatentState]:
        """获取状态历史"""
        return self.history.copy()
    
    def get_current_state(self) -> Optional[PatentState]:
        """获取当前状态"""
        return self.current_state
    
    def set_metadata(self, key: str, value: Any) -> None:
        """设置元数据"""
        self.metadata[key] = value
    
    def get_metadata(self, key: str) -> Any:
        """获取元数据"""
        return self.metadata.get(key)


def create_initial_patent_state(
    technology_domain: str,
    innovation_topic: str,
    analysis_type: str = "discovery"
) -> PatentState:
    """
    创建初始专利分析状态
    
    Args:
        technology_domain: 技术领域
        innovation_topic: 创新主题
        analysis_type: 分析类型
    
    Returns:
        PatentState: 初始化的专利状态
    """
    from datetime import datetime
    
    return PatentState(
        messages=[],
        technology_domain=technology_domain,
        innovation_topic=innovation_topic,
        analysis_date=datetime.now().strftime("%Y-%m-%d"),
        analysis_type=analysis_type,
        sender="system",
        
        # 初始化空状态
        technology_report="",
        innovation_opportunities="",
        prior_art_report="",
        market_intelligence="",
        
        innovation_advocacy="",
        risk_assessment="",
        patent_strategy="",
        
        patent_draft="",
        quality_assessment="",
        final_patent_application="",
        
        # 初始化空数据
        patent_search_results=[],
        similar_patents=[],
        patent_citations=[],
        patent_classifications=[],
        
        literature_results=[],
        research_trends={},
        
        market_analysis={},
        competitive_landscape={},
        
        novelty_assessment={},
        inventiveness_assessment={},
        utility_assessment={},
        
        infringement_risk={},
        grant_probability=0.0,
        commercial_potential={},
        
        # 初始化辩论状态
        innovation_debate_state=PatentDebateState(
            participants=[],
            arguments=[],
            current_round=0,
            consensus_reached=False,
            final_decision=None
        ),
        validation_debate_state=PatentValidationState(
            validation_type="",
            criteria=[],
            results={},
            confidence_score=0.0,
            recommendations=[]
        )
    )


def validate_patent_state(state: PatentState) -> Dict[str, Any]:
    """
    验证专利状态的完整性和有效性
    
    Args:
        state: 要验证的专利状态
    
    Returns:
        Dict: 验证结果，包含是否有效和错误信息
    """
    errors = []
    warnings = []
    
    # 必填字段验证
    required_fields = [
        "technology_domain",
        "innovation_topic", 
        "analysis_date",
        "analysis_type"
    ]
    
    for field in required_fields:
        if not getattr(state, field, None):
            errors.append(f"必填字段 '{field}' 为空")
    
    # 分析类型验证
    valid_analysis_types = ["discovery", "validation", "analysis", "writing"]
    if state.analysis_type not in valid_analysis_types:
        errors.append(f"分析类型 '{state.analysis_type}' 无效，应为: {valid_analysis_types}")
    
    # 日期格式验证
    try:
        from datetime import datetime
        datetime.strptime(state.analysis_date, "%Y-%m-%d")
    except ValueError:
        errors.append(f"日期格式 '{state.analysis_date}' 无效，应为 YYYY-MM-DD")
    
    # 数据完整性检查
    if state.analysis_type == "discovery":
        if not state.technology_report and not state.innovation_opportunities:
            warnings.append("发现阶段缺少技术分析或创新机会报告")
    
    elif state.analysis_type == "validation":
        if not state.prior_art_report:
            warnings.append("验证阶段缺少先行技术报告")
    
    elif state.analysis_type == "writing":
        if not state.patent_draft:
            warnings.append("撰写阶段缺少专利草稿")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "score": max(0, 100 - len(errors) * 25 - len(warnings) * 5)
    } 