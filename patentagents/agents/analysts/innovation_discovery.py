"""
Innovation Discovery Analyst Agent - 创新发现师智能体
从最新技术动态、学术论文、行业报告中发现潜在创新点
"""

import functools
import json
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta

from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)


def create_innovation_discovery_analyst(llm, toolkit):
    """
    创建创新发现师智能体
    
    Args:
        llm: 语言模型实例
        toolkit: 专利工具包实例
    
    Returns:
        function: 创新发现师节点函数
    """
    
    def innovation_discovery_node(state):
        """
        创新发现师节点 - 发现技术创新机会
        
        Args:
            state: 专利分析状态
            
        Returns:
            dict: 更新后的状态
        """
        technology_domain = state["technology_domain"]
        innovation_topic = state["innovation_topic"]
        analysis_date = state["analysis_date"]
        
        # 获取技术分析师的报告作为背景
        technology_report = state.get("technology_report", "")
        
        # 系统提示词
        system_prompt = """你是一位专业的创新发现师，专门从技术动态、学术研究和行业发展中发现创新机会。你的任务是：

1. **技术空白识别**：
   - 分析现有技术的覆盖情况
   - 识别技术发展的空白点和薄弱环节
   - 发现未被充分开发的技术方向
   - 评估技术空白的创新潜力

2. **新兴技术发现**：
   - 识别正在兴起的技术趋势
   - 分析技术融合和交叉创新机会
   - 发现前沿技术的应用场景
   - 预测技术突破的可能方向

3. **创新机会评估**：
   - 评估创新机会的技术可行性
   - 分析市场需求和商业价值
   - 识别创新的竞争优势
   - 评估实现难度和风险

4. **跨领域创新**：
   - 发现不同技术领域的融合点
   - 识别跨行业的技术应用机会
   - 分析技术迁移的创新潜力
   - 探索新的技术组合方式

你需要基于专利数据、技术趋势和领域知识进行深入分析，确保发现的创新机会具有实际价值和可行性。

**输出格式要求**：
- 使用结构化的markdown格式
- 每个创新机会包含详细描述和评估
- 提供创新机会的优先级排序
- 包含实现路径和建议
- 在报告末尾添加创新机会汇总表格
"""
        
        # 构建用户输入
        user_input = f"""请基于以下信息发现技术创新机会：

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**分析日期**: {analysis_date}

**技术分析背景**：
{technology_report[:1000] if technology_report else "暂无技术分析背景"}

请深入分析并发现具有价值的创新机会。"""
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # 工具调用：获取创新发现数据
        try:
            logger.info(f"创新发现师开始分析: {technology_domain} - {innovation_topic}")
            
            # 1. 识别技术空白
            existing_patents = []
            if hasattr(toolkit, 'search_google_patents'):
                search_results = toolkit.search_google_patents(
                    query=f"{technology_domain} {innovation_topic}",
                    num=100,
                    sort="new"
                )
                existing_patents = [p.get('patent_id', '') for p in search_results.get('patents', [])]
            
            technology_gaps = toolkit.identify_technology_gaps(
                field=technology_domain,
                existing_patents=existing_patents
            )
            
            # 2. 发现跨领域创新机会
            related_domains = _extract_related_domains(technology_domain)
            cross_domain_innovations = toolkit.cross_domain_innovation_discovery(
                domains=[technology_domain] + related_domains
            )
            
            # 3. 分析新兴技术趋势
            emerging_trends = toolkit.discover_emerging_technologies(
                news_sources=["tech_news", "research_papers"],
                time_window=90
            )
            
            # 4. 获取研究前沿信息
            research_frontiers = toolkit.analyze_research_frontiers(
                literature_corpus=[]  # 这里可以添加文献数据
            )
            
            # 整理创新发现数据
            innovation_data = {
                "technology_gaps": technology_gaps,
                "cross_domain_innovations": cross_domain_innovations,
                "emerging_trends": emerging_trends,
                "research_frontiers": research_frontiers,
                "existing_patents_count": len(existing_patents)
            }
            
            # 增强用户输入
            enhanced_user_input = f"""{user_input}

**创新发现数据**：

1. **技术空白分析**：
   - 发现技术空白：{len(technology_gaps)} 个
   - 详细信息：{json.dumps(technology_gaps, ensure_ascii=False, indent=2)}

2. **跨领域创新机会**：
   - 发现跨领域机会：{len(cross_domain_innovations)} 个
   - 详细信息：{json.dumps(cross_domain_innovations, ensure_ascii=False, indent=2)}

3. **新兴技术趋势**：
   - 发现新兴趋势：{len(emerging_trends)} 个
   - 详细信息：{json.dumps(emerging_trends, ensure_ascii=False, indent=2)}

4. **研究前沿分析**：
   {json.dumps(research_frontiers, ensure_ascii=False, indent=2)}

5. **现有专利覆盖**：
   - 相关专利数量：{innovation_data['existing_patents_count']} 个

请基于以上数据进行深入的创新机会分析。"""
            
            messages[1]["content"] = enhanced_user_input
            
        except Exception as e:
            logger.error(f"创新发现师数据获取失败: {str(e)}")
            error_msg = f"\n\n**注意**: 创新发现数据获取失败({str(e)})，将基于领域知识进行分析。"
            messages[1]["content"] += error_msg
            innovation_data = {}
        
        # 调用LLM进行创新发现分析
        try:
            result = llm.invoke(messages)
            
            # 生成创新机会报告
            innovation_opportunities = result.content
            
            # 提取创新机会列表
            innovation_list = _extract_innovation_opportunities(innovation_opportunities)
            
            # 更新状态
            updated_state = {
                "messages": [result],
                "innovation_opportunities": innovation_opportunities,
                "sender": "Innovation Discovery Analyst",
                "innovation_list": innovation_list,
                "technology_gaps": innovation_data.get("technology_gaps", []),
                "cross_domain_innovations": innovation_data.get("cross_domain_innovations", [])
            }
            
            logger.info(f"创新发现师分析完成，发现 {len(innovation_list)} 个创新机会")
            return updated_state
            
        except Exception as e:
            logger.error(f"创新发现师LLM调用失败: {str(e)}")
            
            # 生成错误报告
            error_report = f"""# 创新发现报告

## ❌ 创新发现失败

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**分析日期**: {analysis_date}

**错误信息**: {str(e)}

**建议**: 请检查LLM配置或稍后重试。"""
            
            return {
                "messages": [AIMessage(content=error_report)],
                "innovation_opportunities": error_report,
                "sender": "Innovation Discovery Analyst",
                "innovation_list": [],
                "technology_gaps": [],
                "cross_domain_innovations": []
            }
    
    return functools.partial(innovation_discovery_node, name="Innovation Discovery Analyst")


def _extract_related_domains(technology_domain: str) -> List[str]:
    """
    提取相关技术领域
    
    Args:
        technology_domain: 主要技术领域
        
    Returns:
        List[str]: 相关技术领域列表
    """
    domain_mappings = {
        "人工智能": ["机器学习", "深度学习", "计算机视觉", "自然语言处理", "机器人技术"],
        "生物技术": ["基因工程", "蛋白质工程", "细胞治疗", "药物发现", "生物信息学"],
        "新能源": ["太阳能", "风能", "储能技术", "电池技术", "燃料电池"],
        "区块链": ["加密货币", "智能合约", "分布式系统", "数字身份", "去中心化应用"],
        "物联网": ["传感器技术", "边缘计算", "5G通信", "智能家居", "工业互联网"],
        "量子计算": ["量子算法", "量子通信", "量子密码", "量子传感", "量子材料"]
    }
    
    # 查找相关领域
    for domain, related in domain_mappings.items():
        if domain in technology_domain:
            return related[:3]  # 返回前3个相关领域
    
    # 如果没有找到精确匹配，返回通用相关领域
    return ["软件工程", "材料科学", "电子工程"]


def _extract_innovation_opportunities(report: str) -> List[Dict[str, Any]]:
    """
    从报告中提取创新机会列表
    
    Args:
        report: 创新发现报告
        
    Returns:
        List[Dict]: 创新机会列表
    """
    opportunities = []
    
    # 简化的提取逻辑，实际应用中可以使用更复杂的NLP方法
    lines = report.split('\n')
    current_opportunity = {}
    
    for line in lines:
        line = line.strip()
        
        # 检测创新机会标题
        if line.startswith('##') and ('机会' in line or '创新' in line):
            if current_opportunity:
                opportunities.append(current_opportunity)
            current_opportunity = {
                'title': line.replace('##', '').strip(),
                'description': '',
                'priority': 'medium',
                'feasibility': 'unknown'
            }
        
        # 收集描述信息
        elif current_opportunity and line and not line.startswith('#'):
            current_opportunity['description'] += line + ' '
        
        # 检测优先级和可行性
        if '高优先级' in line or '高价值' in line:
            if current_opportunity:
                current_opportunity['priority'] = 'high'
        
        if '可行性高' in line or '容易实现' in line:
            if current_opportunity:
                current_opportunity['feasibility'] = 'high'
    
    # 添加最后一个机会
    if current_opportunity:
        opportunities.append(current_opportunity)
    
    return opportunities


def create_innovation_discovery_with_validation(llm, toolkit):
    """
    创建带验证的创新发现师智能体
    
    Args:
        llm: 语言模型实例
        toolkit: 专利工具包实例
    
    Returns:
        function: 创新发现师节点函数
    """
    
    def innovation_discovery_with_validation_node(state):
        """带验证的创新发现师节点"""
        
        # 调用基础创新发现师
        base_analyst = create_innovation_discovery_analyst(llm, toolkit)
        result = base_analyst(state)
        
        # 验证创新机会质量
        if result.get("innovation_opportunities"):
            validation_result = validate_innovation_opportunities(
                result["innovation_opportunities"]
            )
            
            result["innovation_validation"] = validation_result
            
            # 如果质量不合格，记录警告
            if not validation_result["is_valid"]:
                logger.warning(f"创新发现质量不合格: {validation_result['issues']}")
        
        return result
    
    return functools.partial(innovation_discovery_with_validation_node, name="Innovation Discovery Analyst")


def validate_innovation_opportunities(opportunities_report: str) -> Dict[str, Any]:
    """
    验证创新机会报告的质量
    
    Args:
        opportunities_report: 创新机会报告
        
    Returns:
        dict: 验证结果
    """
    validation_result = {
        "is_valid": True,
        "quality_score": 100,
        "issues": [],
        "suggestions": []
    }
    
    # 检查报告长度
    if len(opportunities_report) < 800:
        validation_result["issues"].append("报告内容过短")
        validation_result["quality_score"] -= 20
    
    # 检查创新机会数量
    opportunity_count = opportunities_report.count("##")
    if opportunity_count < 3:
        validation_result["issues"].append("创新机会数量不足")
        validation_result["quality_score"] -= 15
    
    # 检查必要元素
    required_elements = ["技术空白", "创新机会", "可行性", "优先级"]
    for element in required_elements:
        if element not in opportunities_report:
            validation_result["issues"].append(f"缺少{element}分析")
            validation_result["quality_score"] -= 10
    
    # 检查数据支撑
    if "专利" not in opportunities_report and "数据" not in opportunities_report:
        validation_result["issues"].append("缺少数据支撑")
        validation_result["quality_score"] -= 15
    
    # 检查创新性
    if "创新" not in opportunities_report:
        validation_result["issues"].append("缺少创新性分析")
        validation_result["quality_score"] -= 10
    
    # 判断是否有效
    if validation_result["quality_score"] < 70:
        validation_result["is_valid"] = False
    
    # 生成改进建议
    if validation_result["issues"]:
        validation_result["suggestions"] = [
            "增加更多创新机会的详细分析",
            "提供更多数据支撑和案例",
            "加强可行性和优先级评估",
            "增加跨领域创新的探索"
        ]
    
    return validation_result


def prioritize_innovation_opportunities(opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    对创新机会进行优先级排序
    
    Args:
        opportunities: 创新机会列表
        
    Returns:
        List[Dict]: 排序后的创新机会列表
    """
    # 定义优先级权重
    priority_weights = {
        'high': 3,
        'medium': 2,
        'low': 1
    }
    
    feasibility_weights = {
        'high': 3,
        'medium': 2,
        'low': 1,
        'unknown': 1
    }
    
    # 计算综合分数
    for opportunity in opportunities:
        priority_score = priority_weights.get(opportunity.get('priority', 'medium'), 2)
        feasibility_score = feasibility_weights.get(opportunity.get('feasibility', 'unknown'), 1)
        
        # 综合评分
        opportunity['score'] = priority_score * feasibility_score
        
        # 添加描述长度作为质量指标
        description_length = len(opportunity.get('description', ''))
        if description_length > 200:
            opportunity['score'] += 1
    
    # 按分数排序
    return sorted(opportunities, key=lambda x: x.get('score', 0), reverse=True)


# 测试函数
def test_innovation_discovery():
    """测试创新发现师功能"""
    print("🧪 测试创新发现师...")
    
    # 模拟测试数据
    test_opportunities = [
        {
            "title": "AI驱动的药物发现",
            "description": "利用人工智能技术加速药物发现过程",
            "priority": "high",
            "feasibility": "medium"
        },
        {
            "title": "量子计算优化算法",
            "description": "开发量子计算环境下的优化算法",
            "priority": "medium",
            "feasibility": "low"
        }
    ]
    
    # 测试优先级排序
    prioritized = prioritize_innovation_opportunities(test_opportunities)
    print(f"✅ 优先级排序: {len(prioritized)} 个机会")
    
    for i, opp in enumerate(prioritized, 1):
        print(f"  {i}. {opp['title']} (分数: {opp['score']})")
    
    # 测试报告验证
    test_report = """# 创新发现报告

## 技术空白分析
发现多个技术空白...

## 创新机会1: AI药物发现
高优先级机会，可行性高...

## 创新机会2: 量子算法
中等优先级机会...

## 创新机会3: 生物计算
新兴领域机会...
"""
    
    validation = validate_innovation_opportunities(test_report)
    print(f"✅ 报告验证: 质量分数 {validation['quality_score']}/100")
    
    if validation["issues"]:
        print(f"⚠️ 发现问题: {validation['issues']}")
    
    print("🎉 创新发现师测试完成！")


if __name__ == "__main__":
    test_innovation_discovery() 