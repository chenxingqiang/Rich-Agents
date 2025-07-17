"""
Technology Analyst Agent - 技术分析师智能体
负责分析目标技术领域的发展趋势、技术成熟度、市场需求
"""

import functools
import json
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)


def create_technology_analyst(llm, toolkit):
    """
    创建技术分析师智能体
    
    Args:
        llm: 语言模型实例
        toolkit: 专利工具包实例
    
    Returns:
        function: 技术分析师节点函数
    """
    
    def technology_analyst_node(state):
        """
        技术分析师节点 - 分析技术领域和发展趋势
        
        Args:
            state: 专利分析状态
            
        Returns:
            dict: 更新后的状态
        """
        technology_domain = state["technology_domain"]
        innovation_topic = state["innovation_topic"]
        analysis_date = state["analysis_date"]
        
        # 系统提示词
        system_prompt = """你是一位专业的技术分析师，专门分析技术领域的发展趋势、技术成熟度和市场需求。你的任务是：

1. **技术领域分析**：
   - 分析技术领域的发展历程和现状
   - 识别关键技术要素和核心技术路径
   - 评估技术成熟度和发展阶段
   - 预测技术发展趋势和未来方向

2. **市场需求分析**：
   - 分析市场对该技术的需求程度
   - 识别主要应用场景和目标用户
   - 评估商业化潜力和市场规模
   - 分析竞争格局和主要参与者

3. **技术机会识别**：
   - 识别技术创新机会和空白点
   - 分析技术融合和跨领域应用
   - 评估技术风险和挑战
   - 提出技术发展建议

你需要使用专利检索工具获取相关技术数据，并基于数据进行深入分析。请确保分析结果准确、全面、具有前瞻性。

**输出格式要求**：
- 使用结构化的markdown格式
- 包含数据支撑和具体案例
- 提供明确的结论和建议
- 在报告末尾添加关键信息汇总表格
"""
        
        # 用户输入
        user_input = f"""请对以下技术领域进行全面分析：

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**分析日期**: {analysis_date}

请使用专利检索工具获取相关数据，并提供详细的技术分析报告。"""
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # 工具调用：搜索相关专利
        try:
            logger.info(f"技术分析师开始分析: {technology_domain} - {innovation_topic}")
            
            # 1. 搜索该技术领域的专利
            patent_search_results = toolkit.search_google_patents(
                query=f"{technology_domain} {innovation_topic}",
                num=50,
                sort="new"
            )
            
            # 2. 分析专利趋势
            patent_trends = toolkit.analyze_patent_trends(
                technology_field=technology_domain,
                time_range=(
                    (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d"),
                    datetime.now().strftime("%Y-%m-%d")
                )
            )
            
            # 3. 生成技术地图
            patent_landscape = toolkit.generate_patent_landscape(technology_domain)
            
            # 整理数据用于分析
            analysis_data = {
                "recent_patents": patent_search_results.get("patents", [])[:20],
                "patent_trends": patent_trends,
                "patent_landscape": patent_landscape,
                "total_patents": patent_search_results.get("total_results", 0),
                "search_summary": patent_search_results.get("summary", {})
            }
            
            # 添加数据到用户消息
            enhanced_user_input = f"""{user_input}

**专利数据分析结果**：

1. **专利检索结果**：
   - 找到相关专利：{analysis_data['total_patents']} 个
   - 近期专利数量：{len(analysis_data['recent_patents'])} 个
   - 主要受让人：{json.dumps(analysis_data.get('search_summary', {}).get('assignee', [])[:5], ensure_ascii=False, indent=2)}

2. **专利趋势数据**：
   {json.dumps(analysis_data['patent_trends'], ensure_ascii=False, indent=2)}

3. **技术地图数据**：
   {json.dumps(analysis_data['patent_landscape'], ensure_ascii=False, indent=2)}

4. **近期重要专利**：
   {json.dumps([{
       'title': p.get('title', ''),
       'assignee': p.get('assignee', ''),
       'publication_date': p.get('publication_date', ''),
       'patent_id': p.get('patent_id', '')
   } for p in analysis_data['recent_patents'][:10]], ensure_ascii=False, indent=2)}

请基于以上数据进行深入的技术分析。"""
            
            messages[1]["content"] = enhanced_user_input
            
        except Exception as e:
            logger.error(f"技术分析师数据获取失败: {str(e)}")
            error_msg = f"\n\n**注意**: 专利数据获取失败({str(e)})，将基于领域知识进行分析。"
            messages[1]["content"] += error_msg
        
        # 调用LLM进行分析
        try:
            result = llm.invoke(messages)
            
            # 生成技术分析报告
            technology_report = result.content
            
            # 更新状态
            updated_state = {
                "messages": [result],
                "technology_report": technology_report,
                "sender": "Technology Analyst",
                "patent_search_results": analysis_data.get("recent_patents", []),
                "research_trends": analysis_data.get("patent_trends", {})
            }
            
            logger.info("技术分析师分析完成")
            return updated_state
            
        except Exception as e:
            logger.error(f"技术分析师LLM调用失败: {str(e)}")
            
            # 生成错误报告
            error_report = f"""# 技术分析报告

## ❌ 分析失败

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**分析日期**: {analysis_date}

**错误信息**: {str(e)}

**建议**: 请检查LLM配置或稍后重试。"""
            
            return {
                "messages": [AIMessage(content=error_report)],
                "technology_report": error_report,
                "sender": "Technology Analyst",
                "patent_search_results": [],
                "research_trends": {}
            }
    
    return functools.partial(technology_analyst_node, name="Technology Analyst")


def create_technology_analyst_with_memory(llm, toolkit, memory):
    """
    创建带记忆的技术分析师智能体
    
    Args:
        llm: 语言模型实例
        toolkit: 专利工具包实例
        memory: 记忆系统实例
    
    Returns:
        function: 技术分析师节点函数
    """
    
    def technology_analyst_with_memory_node(state):
        """带记忆的技术分析师节点"""
        technology_domain = state["technology_domain"]
        innovation_topic = state["innovation_topic"]
        
        # 检索相关记忆
        query = f"{technology_domain} {innovation_topic}"
        past_memories = memory.get_memories(query, n_matches=3)
        
        # 构建记忆上下文
        memory_context = ""
        if past_memories:
            memory_context = "\n\n**历史分析记忆**：\n"
            for i, memory_item in enumerate(past_memories, 1):
                memory_context += f"{i}. {memory_item.get('content', '')}\n"
        
        # 调用基础技术分析师
        base_analyst = create_technology_analyst(llm, toolkit)
        result = base_analyst(state)
        
        # 如果分析成功，保存到记忆
        if result.get("technology_report") and "❌ 分析失败" not in result["technology_report"]:
            try:
                memory.save_memory(
                    content=result["technology_report"][:500],  # 截取前500字符
                    metadata={
                        "type": "technology_analysis",
                        "domain": technology_domain,
                        "topic": innovation_topic,
                        "date": state["analysis_date"]
                    }
                )
                logger.info("技术分析结果已保存到记忆")
            except Exception as e:
                logger.error(f"保存技术分析记忆失败: {str(e)}")
        
        return result
    
    return functools.partial(technology_analyst_with_memory_node, name="Technology Analyst")


def validate_technology_analysis(analysis_report: str) -> Dict[str, Any]:
    """
    验证技术分析报告的质量
    
    Args:
        analysis_report: 技术分析报告
        
    Returns:
        dict: 验证结果
    """
    validation_result = {
        "is_valid": True,
        "quality_score": 100,
        "missing_elements": [],
        "suggestions": []
    }
    
    # 检查必需元素
    required_elements = [
        "技术领域分析",
        "市场需求",
        "技术趋势",
        "发展建议",
        "结论"
    ]
    
    for element in required_elements:
        if element not in analysis_report:
            validation_result["missing_elements"].append(element)
            validation_result["quality_score"] -= 15
    
    # 检查报告长度
    if len(analysis_report) < 500:
        validation_result["suggestions"].append("报告内容过短，建议增加详细分析")
        validation_result["quality_score"] -= 10
    
    # 检查数据支撑
    if "专利" not in analysis_report and "数据" not in analysis_report:
        validation_result["suggestions"].append("缺少数据支撑，建议添加专利数据分析")
        validation_result["quality_score"] -= 20
    
    # 检查结构化程度
    if analysis_report.count("#") < 3:
        validation_result["suggestions"].append("报告结构不够清晰，建议使用更多标题")
        validation_result["quality_score"] -= 10
    
    # 判断是否有效
    if validation_result["quality_score"] < 60:
        validation_result["is_valid"] = False
    
    return validation_result


# 测试函数
def test_technology_analyst():
    """测试技术分析师功能"""
    print("🧪 测试技术分析师...")
    
    # 模拟测试数据
    test_report = """# 技术分析报告

## 技术领域分析
人工智能技术正在快速发展...

## 市场需求
市场对AI技术需求旺盛...

## 技术趋势
深度学习、神经网络等技术趋势...

## 发展建议
建议关注新兴技术...

## 结论
该技术领域具有良好的发展前景...
"""
    
    # 验证报告质量
    validation = validate_technology_analysis(test_report)
    print(f"✅ 报告验证: 质量分数 {validation['quality_score']}/100")
    
    if validation["missing_elements"]:
        print(f"⚠️ 缺失元素: {validation['missing_elements']}")
    
    if validation["suggestions"]:
        print(f"💡 改进建议: {validation['suggestions']}")
    
    print("🎉 技术分析师测试完成！")


if __name__ == "__main__":
    test_technology_analyst() 