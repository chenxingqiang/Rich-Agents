"""
Prior Art Researcher Agent - 先行技术研究员智能体
深度检索相关专利、技术文献，评估现有技术状态
"""

import functools
import json
import logging
from typing import Dict, Any, List, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict

from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)


def create_prior_art_researcher(llm, toolkit):
    """
    创建先行技术研究员智能体
    
    Args:
        llm: 语言模型实例
        toolkit: 专利工具包实例
    
    Returns:
        function: 先行技术研究员节点函数
    """
    
    def prior_art_researcher_node(state):
        """
        先行技术研究员节点 - 深度检索和分析先行技术
        
        Args:
            state: 专利分析状态
            
        Returns:
            dict: 更新后的状态
        """
        technology_domain = state["technology_domain"]
        innovation_topic = state["innovation_topic"]
        analysis_date = state["analysis_date"]
        
        # 获取前面智能体的分析结果
        technology_report = state.get("technology_report", "")
        innovation_opportunities = state.get("innovation_opportunities", "")
        
        # 系统提示词
        system_prompt = """你是一位专业的先行技术研究员，专门进行深度的专利检索和现有技术分析。你的任务是：

1. **全面专利检索**：
   - 进行多维度、多关键词的专利检索
   - 覆盖全球主要专利数据库
   - 检索不同时间段的专利发展
   - 分析专利族和专利引用关系

2. **现有技术分析**：
   - 识别核心先行技术和基础专利
   - 分析技术发展脉络和演进路径
   - 评估现有技术的覆盖范围和局限性
   - 识别技术空白和改进机会

3. **专利地图构建**：
   - 构建技术领域的专利地图
   - 分析主要专利权人和发明人
   - 识别核心专利和基础专利
   - 评估专利强度和价值

4. **侵权风险评估**：
   - 识别可能的侵权风险专利
   - 分析专利权利要求的覆盖范围
   - 评估专利有效性和稳定性
   - 提供规避设计建议

5. **技术发展趋势**：
   - 分析专利申请趋势和技术热点
   - 识别新兴技术方向
   - 预测技术发展路径
   - 评估技术成熟度

你需要使用专利检索工具进行全面的检索，并基于检索结果进行深入分析。

**输出格式要求**：
- 使用结构化的markdown格式
- 包含详细的检索策略和结果
- 提供专利分析表格和图表
- 包含风险评估和建议
- 在报告末尾添加关键专利清单
"""
        
        # 构建用户输入
        user_input = f"""请对以下技术领域进行全面的先行技术研究：

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**分析日期**: {analysis_date}

**技术分析背景**：
{technology_report[:800] if technology_report else "暂无技术分析背景"}

**创新机会背景**：
{innovation_opportunities[:800] if innovation_opportunities else "暂无创新机会背景"}

请进行深度的专利检索和现有技术分析。"""
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # 工具调用：进行全面的专利检索
        try:
            logger.info(f"先行技术研究员开始分析: {technology_domain} - {innovation_topic}")
            
            # 1. 多维度专利检索
            search_results = _comprehensive_patent_search(toolkit, technology_domain, innovation_topic)
            
            # 2. 专利引用分析
            citation_analysis = _analyze_patent_citations(toolkit, search_results["key_patents"])
            
            # 3. 专利族分析
            patent_family_analysis = _analyze_patent_families(toolkit, search_results["key_patents"])
            
            # 4. 竞争对手分析
            competitor_analysis = _analyze_competitors(toolkit, search_results["patents"])
            
            # 5. 技术演进分析
            technology_evolution = _analyze_technology_evolution(toolkit, search_results["patents"])
            
            # 6. 侵权风险评估
            infringement_risks = _assess_infringement_risks(toolkit, search_results["high_risk_patents"])
            
            # 整理先行技术分析数据
            prior_art_data = {
                "search_results": search_results,
                "citation_analysis": citation_analysis,
                "patent_families": patent_family_analysis,
                "competitors": competitor_analysis,
                "technology_evolution": technology_evolution,
                "infringement_risks": infringement_risks
            }
            
            # 增强用户输入
            enhanced_user_input = f"""{user_input}

**先行技术研究数据**：

1. **专利检索结果**：
   - 总专利数：{search_results['total_patents']}
   - 核心专利数：{len(search_results['key_patents'])}
   - 高风险专利数：{len(search_results['high_risk_patents'])}
   - 检索策略：{json.dumps(search_results['search_strategy'], ensure_ascii=False, indent=2)}

2. **专利引用分析**：
   {json.dumps(citation_analysis, ensure_ascii=False, indent=2)}

3. **专利族分析**：
   {json.dumps(patent_family_analysis, ensure_ascii=False, indent=2)}

4. **竞争对手分析**：
   {json.dumps(competitor_analysis, ensure_ascii=False, indent=2)}

5. **技术演进分析**：
   {json.dumps(technology_evolution, ensure_ascii=False, indent=2)}

6. **侵权风险评估**：
   {json.dumps(infringement_risks, ensure_ascii=False, indent=2)}

请基于以上数据进行深入的先行技术分析。"""
            
            messages[1]["content"] = enhanced_user_input
            
        except Exception as e:
            logger.error(f"先行技术研究员数据获取失败: {str(e)}")
            error_msg = f"\n\n**注意**: 先行技术数据获取失败({str(e)})，将基于领域知识进行分析。"
            messages[1]["content"] += error_msg
            prior_art_data = {}
        
        # 调用LLM进行先行技术分析
        try:
            result = llm.invoke(messages)
            
            # 生成先行技术报告
            prior_art_report = result.content
            
            # 提取关键信息
            key_patents = prior_art_data.get("search_results", {}).get("key_patents", [])
            similar_patents = prior_art_data.get("search_results", {}).get("similar_patents", [])
            
            # 更新状态
            updated_state = {
                "messages": [result],
                "prior_art_report": prior_art_report,
                "sender": "Prior Art Researcher",
                "patent_search_results": prior_art_data.get("search_results", {}).get("patents", []),
                "similar_patents": similar_patents,
                "patent_citations": prior_art_data.get("citation_analysis", {}),
                "infringement_risk": prior_art_data.get("infringement_risks", {}),
                "competitive_landscape": prior_art_data.get("competitors", {})
            }
            
            logger.info(f"先行技术研究员分析完成，分析了 {len(key_patents)} 个核心专利")
            return updated_state
            
        except Exception as e:
            logger.error(f"先行技术研究员LLM调用失败: {str(e)}")
            
            # 生成错误报告
            error_report = f"""# 先行技术研究报告

## ❌ 研究失败

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**分析日期**: {analysis_date}

**错误信息**: {str(e)}

**建议**: 请检查LLM配置或稍后重试。"""
            
            return {
                "messages": [AIMessage(content=error_report)],
                "prior_art_report": error_report,
                "sender": "Prior Art Researcher",
                "patent_search_results": [],
                "similar_patents": [],
                "patent_citations": {},
                "infringement_risk": {},
                "competitive_landscape": {}
            }
    
    return functools.partial(prior_art_researcher_node, name="Prior Art Researcher")


def _comprehensive_patent_search(toolkit, technology_domain: str, innovation_topic: str) -> Dict[str, Any]:
    """
    进行全面的专利检索
    
    Args:
        toolkit: 专利工具包
        technology_domain: 技术领域
        innovation_topic: 创新主题
        
    Returns:
        Dict: 检索结果
    """
    search_results = {
        "patents": [],
        "key_patents": [],
        "high_risk_patents": [],
        "similar_patents": [],
        "total_patents": 0,
        "search_strategy": []
    }
    
    try:
        # 1. 基础关键词搜索
        base_query = f"{technology_domain} {innovation_topic}"
        base_results = toolkit.search_google_patents(query=base_query, num=50)
        
        search_results["patents"].extend(base_results.get("patents", []))
        search_results["search_strategy"].append({
            "query": base_query,
            "results": len(base_results.get("patents", []))
        })
        
        # 2. 扩展关键词搜索
        extended_queries = _generate_extended_queries(technology_domain, innovation_topic)
        
        for query in extended_queries:
            extended_results = toolkit.search_google_patents(query=query, num=30)
            search_results["patents"].extend(extended_results.get("patents", []))
            search_results["search_strategy"].append({
                "query": query,
                "results": len(extended_results.get("patents", []))
            })
        
        # 3. 去重和分类
        unique_patents = _deduplicate_patents(search_results["patents"])
        search_results["patents"] = unique_patents
        search_results["total_patents"] = len(unique_patents)
        
        # 4. 识别核心专利
        search_results["key_patents"] = _identify_key_patents(unique_patents)
        
        # 5. 识别高风险专利
        search_results["high_risk_patents"] = _identify_high_risk_patents(unique_patents)
        
        # 6. 寻找相似专利
        if search_results["key_patents"]:
            first_key_patent = search_results["key_patents"][0]
            similar_patents = toolkit.search_similar_patents(
                first_key_patent.get("patent_id", ""), 
                threshold=0.7
            )
            search_results["similar_patents"] = similar_patents
        
        return search_results
        
    except Exception as e:
        logger.error(f"全面专利检索失败: {str(e)}")
        return search_results


def _generate_extended_queries(technology_domain: str, innovation_topic: str) -> List[str]:
    """生成扩展的检索查询"""
    queries = []
    
    # 基于技术领域的扩展
    domain_extensions = {
        "人工智能": ["AI", "machine learning", "deep learning", "neural network"],
        "生物技术": ["biotechnology", "genetic engineering", "bioengineering"],
        "新能源": ["renewable energy", "clean energy", "sustainable energy"],
        "区块链": ["blockchain", "distributed ledger", "cryptocurrency"],
        "物联网": ["IoT", "Internet of Things", "connected devices"],
        "量子计算": ["quantum computing", "quantum algorithm", "quantum information"]
    }
    
    # 添加领域扩展查询
    for domain, extensions in domain_extensions.items():
        if domain in technology_domain:
            for ext in extensions:
                queries.append(f"{ext} {innovation_topic}")
    
    # 添加通用技术术语组合
    technical_terms = ["method", "system", "apparatus", "device", "process"]
    for term in technical_terms:
        queries.append(f"{innovation_topic} {term}")
    
    return queries[:5]  # 限制查询数量


def _deduplicate_patents(patents: List[Dict]) -> List[Dict]:
    """去除重复专利"""
    seen_ids = set()
    unique_patents = []
    
    for patent in patents:
        patent_id = patent.get("patent_id", "")
        publication_number = patent.get("publication_number", "")
        
        # 使用专利ID或公开号作为唯一标识
        identifier = patent_id or publication_number
        
        if identifier and identifier not in seen_ids:
            seen_ids.add(identifier)
            unique_patents.append(patent)
    
    return unique_patents


def _identify_key_patents(patents: List[Dict]) -> List[Dict]:
    """识别核心专利"""
    key_patents = []
    
    for patent in patents:
        # 基于多个因素评估专利重要性
        importance_score = 0
        
        # 1. 发布日期（较新的专利更重要）
        pub_date = patent.get("publication_date", "")
        if pub_date:
            try:
                pub_year = int(pub_date[:4])
                current_year = datetime.now().year
                if current_year - pub_year <= 5:
                    importance_score += 2
                elif current_year - pub_year <= 10:
                    importance_score += 1
            except:
                pass
        
        # 2. 受让人（知名公司的专利更重要）
        assignee = patent.get("assignee", "").lower()
        important_assignees = ["google", "microsoft", "apple", "ibm", "samsung", "intel", "qualcomm"]
        if any(company in assignee for company in important_assignees):
            importance_score += 2
        
        # 3. 标题相关性
        title = patent.get("title", "").lower()
        if len(title) > 50:  # 详细的标题通常更重要
            importance_score += 1
        
        # 4. 专利状态
        if patent.get("status") == "GRANT":
            importance_score += 1
        
        # 添加评分
        patent["importance_score"] = importance_score
        
        # 选择高分专利作为核心专利
        if importance_score >= 3:
            key_patents.append(patent)
    
    # 按重要性排序并返回前20个
    key_patents.sort(key=lambda x: x.get("importance_score", 0), reverse=True)
    return key_patents[:20]


def _identify_high_risk_patents(patents: List[Dict]) -> List[Dict]:
    """识别高风险专利"""
    high_risk_patents = []
    
    for patent in patents:
        risk_score = 0
        
        # 1. 权利要求范围广泛
        title = patent.get("title", "").lower()
        snippet = patent.get("snippet", "").lower()
        
        broad_terms = ["system", "method", "apparatus", "device", "process"]
        if any(term in title for term in broad_terms):
            risk_score += 1
        
        # 2. 授权专利风险更高
        if patent.get("status") == "GRANT":
            risk_score += 2
        
        # 3. 近期专利风险更高
        pub_date = patent.get("publication_date", "")
        if pub_date:
            try:
                pub_year = int(pub_date[:4])
                current_year = datetime.now().year
                if current_year - pub_year <= 3:
                    risk_score += 2
            except:
                pass
        
        # 4. 大公司专利风险更高
        assignee = patent.get("assignee", "").lower()
        major_companies = ["google", "microsoft", "apple", "ibm", "samsung"]
        if any(company in assignee for company in major_companies):
            risk_score += 1
        
        patent["risk_score"] = risk_score
        
        if risk_score >= 4:
            high_risk_patents.append(patent)
    
    # 按风险排序
    high_risk_patents.sort(key=lambda x: x.get("risk_score", 0), reverse=True)
    return high_risk_patents[:15]


def _analyze_patent_citations(toolkit, key_patents: List[Dict]) -> Dict[str, Any]:
    """分析专利引用关系"""
    citation_analysis = {
        "total_citations": 0,
        "avg_citations": 0,
        "citation_network": {},
        "most_cited_patents": []
    }
    
    try:
        citation_counts = []
        
        for patent in key_patents[:10]:  # 限制分析数量
            patent_id = patent.get("patent_id", "")
            if patent_id and hasattr(toolkit, 'get_patent_citations'):
                try:
                    citations = toolkit.get_patent_citations(patent_id)
                    cited_by_count = len(citations.get("cited_by", []))
                    citation_counts.append(cited_by_count)
                    
                    patent["citation_count"] = cited_by_count
                    citation_analysis["citation_network"][patent_id] = citations
                    
                except Exception as e:
                    logger.warning(f"获取专利引用失败 {patent_id}: {str(e)}")
        
        if citation_counts:
            citation_analysis["total_citations"] = sum(citation_counts)
            citation_analysis["avg_citations"] = sum(citation_counts) / len(citation_counts)
            
            # 找出被引用最多的专利
            patents_with_citations = [p for p in key_patents if "citation_count" in p]
            patents_with_citations.sort(key=lambda x: x.get("citation_count", 0), reverse=True)
            citation_analysis["most_cited_patents"] = patents_with_citations[:5]
        
        return citation_analysis
        
    except Exception as e:
        logger.error(f"专利引用分析失败: {str(e)}")
        return citation_analysis


def _analyze_patent_families(toolkit, key_patents: List[Dict]) -> Dict[str, Any]:
    """分析专利族"""
    family_analysis = {
        "family_count": 0,
        "families": {},
        "largest_family": None
    }
    
    try:
        # 简化的专利族分析（基于受让人和发明人）
        families = defaultdict(list)
        
        for patent in key_patents:
            assignee = patent.get("assignee", "")
            inventor = patent.get("inventor", "")
            
            # 使用受让人作为族群标识
            if assignee:
                family_key = assignee
                families[family_key].append(patent)
        
        family_analysis["family_count"] = len(families)
        family_analysis["families"] = dict(families)
        
        # 找出最大的专利族
        if families:
            largest_family_key = max(families.keys(), key=lambda k: len(families[k]))
            family_analysis["largest_family"] = {
                "assignee": largest_family_key,
                "patent_count": len(families[largest_family_key]),
                "patents": families[largest_family_key]
            }
        
        return family_analysis
        
    except Exception as e:
        logger.error(f"专利族分析失败: {str(e)}")
        return family_analysis


def _analyze_competitors(toolkit, patents: List[Dict]) -> Dict[str, Any]:
    """分析竞争对手"""
    competitor_analysis = {
        "top_assignees": [],
        "top_inventors": [],
        "market_leaders": [],
        "emerging_players": []
    }
    
    try:
        # 统计受让人
        assignee_counts = defaultdict(int)
        inventor_counts = defaultdict(int)
        
        for patent in patents:
            assignee = patent.get("assignee", "").strip()
            inventor = patent.get("inventor", "").strip()
            
            if assignee:
                assignee_counts[assignee] += 1
            if inventor:
                inventor_counts[inventor] += 1
        
        # 排序并获取前10
        top_assignees = sorted(assignee_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_inventors = sorted(inventor_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        competitor_analysis["top_assignees"] = [
            {"name": name, "patent_count": count} for name, count in top_assignees
        ]
        competitor_analysis["top_inventors"] = [
            {"name": name, "patent_count": count} for name, count in top_inventors
        ]
        
        # 识别市场领导者（专利数量超过5个的受让人）
        market_leaders = [item for item in competitor_analysis["top_assignees"] if item["patent_count"] >= 5]
        competitor_analysis["market_leaders"] = market_leaders
        
        # 识别新兴参与者（专利数量在2-4个的受让人）
        emerging_players = [item for item in competitor_analysis["top_assignees"] 
                          if 2 <= item["patent_count"] <= 4]
        competitor_analysis["emerging_players"] = emerging_players
        
        return competitor_analysis
        
    except Exception as e:
        logger.error(f"竞争对手分析失败: {str(e)}")
        return competitor_analysis


def _analyze_technology_evolution(toolkit, patents: List[Dict]) -> Dict[str, Any]:
    """分析技术演进"""
    evolution_analysis = {
        "timeline": [],
        "key_milestones": [],
        "trend_analysis": {}
    }
    
    try:
        # 按年份分组专利
        yearly_patents = defaultdict(list)
        
        for patent in patents:
            pub_date = patent.get("publication_date", "")
            if pub_date:
                try:
                    year = int(pub_date[:4])
                    yearly_patents[year].append(patent)
                except:
                    continue
        
        # 构建时间线
        for year in sorted(yearly_patents.keys()):
            patents_in_year = yearly_patents[year]
            evolution_analysis["timeline"].append({
                "year": year,
                "patent_count": len(patents_in_year),
                "key_patents": patents_in_year[:3]  # 取前3个专利
            })
        
        # 识别关键里程碑（专利数量突增的年份）
        timeline = evolution_analysis["timeline"]
        for i in range(1, len(timeline)):
            current_count = timeline[i]["patent_count"]
            previous_count = timeline[i-1]["patent_count"]
            
            if current_count > previous_count * 1.5:  # 增长超过50%
                evolution_analysis["key_milestones"].append({
                    "year": timeline[i]["year"],
                    "description": f"专利数量从{previous_count}增长到{current_count}",
                    "growth_rate": (current_count - previous_count) / previous_count
                })
        
        # 趋势分析
        if len(timeline) >= 3:
            recent_years = timeline[-3:]
            total_recent = sum(item["patent_count"] for item in recent_years)
            avg_recent = total_recent / len(recent_years)
            
            evolution_analysis["trend_analysis"] = {
                "recent_activity": "high" if avg_recent > 5 else "moderate" if avg_recent > 2 else "low",
                "avg_patents_per_year": avg_recent,
                "total_years_analyzed": len(timeline)
            }
        
        return evolution_analysis
        
    except Exception as e:
        logger.error(f"技术演进分析失败: {str(e)}")
        return evolution_analysis


def _assess_infringement_risks(toolkit, high_risk_patents: List[Dict]) -> Dict[str, Any]:
    """评估侵权风险"""
    risk_assessment = {
        "overall_risk_level": "low",
        "high_risk_patents": [],
        "risk_factors": [],
        "mitigation_strategies": []
    }
    
    try:
        if not high_risk_patents:
            return risk_assessment
        
        # 分析高风险专利
        critical_patents = []
        
        for patent in high_risk_patents:
            patent_risk = {
                "patent_id": patent.get("patent_id", ""),
                "title": patent.get("title", ""),
                "assignee": patent.get("assignee", ""),
                "risk_score": patent.get("risk_score", 0),
                "risk_factors": []
            }
            
            # 识别具体风险因素
            if patent.get("status") == "GRANT":
                patent_risk["risk_factors"].append("已授权专利")
            
            if "system" in patent.get("title", "").lower():
                patent_risk["risk_factors"].append("系统性专利，覆盖范围广")
            
            pub_date = patent.get("publication_date", "")
            if pub_date:
                try:
                    pub_year = int(pub_date[:4])
                    current_year = datetime.now().year
                    if current_year - pub_year <= 3:
                        patent_risk["risk_factors"].append("近期专利，保护期长")
                except:
                    pass
            
            critical_patents.append(patent_risk)
        
        risk_assessment["high_risk_patents"] = critical_patents
        
        # 评估整体风险等级
        if len(critical_patents) >= 5:
            risk_assessment["overall_risk_level"] = "high"
        elif len(critical_patents) >= 2:
            risk_assessment["overall_risk_level"] = "medium"
        
        # 生成风险缓解策略
        risk_assessment["mitigation_strategies"] = [
            "进行详细的专利权利要求分析",
            "寻找现有技术进行专利无效挑战",
            "设计规避方案避免侵权",
            "考虑专利许可或交叉许可",
            "监控专利状态变化"
        ]
        
        return risk_assessment
        
    except Exception as e:
        logger.error(f"侵权风险评估失败: {str(e)}")
        return risk_assessment


def validate_prior_art_research(research_report: str) -> Dict[str, Any]:
    """
    验证先行技术研究报告的质量
    
    Args:
        research_report: 先行技术研究报告
        
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
        "专利检索",
        "现有技术",
        "技术发展",
        "竞争对手",
        "侵权风险",
        "专利地图"
    ]
    
    for element in required_elements:
        if element not in research_report:
            validation_result["missing_elements"].append(element)
            validation_result["quality_score"] -= 12
    
    # 检查报告长度
    if len(research_report) < 1200:
        validation_result["suggestions"].append("报告内容过短，建议增加详细分析")
        validation_result["quality_score"] -= 15
    
    # 检查数据支撑
    if research_report.count("专利") < 5:
        validation_result["suggestions"].append("专利数据不足，建议增加更多专利分析")
        validation_result["quality_score"] -= 10
    
    # 检查表格和图表
    if "表格" not in research_report and "|" not in research_report:
        validation_result["suggestions"].append("缺少表格展示，建议添加专利清单表格")
        validation_result["quality_score"] -= 10
    
    # 检查风险评估
    if "风险" not in research_report:
        validation_result["suggestions"].append("缺少风险评估，建议添加侵权风险分析")
        validation_result["quality_score"] -= 15
    
    # 判断是否有效
    if validation_result["quality_score"] < 70:
        validation_result["is_valid"] = False
    
    return validation_result


# 测试函数
def test_prior_art_researcher():
    """测试先行技术研究员功能"""
    print("🧪 测试先行技术研究员...")
    
    # 测试专利去重
    test_patents = [
        {"patent_id": "US123456", "title": "Test Patent 1"},
        {"patent_id": "US123456", "title": "Test Patent 1"},  # 重复
        {"patent_id": "US789012", "title": "Test Patent 2"},
    ]
    
    unique_patents = _deduplicate_patents(test_patents)
    print(f"✅ 专利去重测试: {len(test_patents)} -> {len(unique_patents)}")
    
    # 测试核心专利识别
    test_patents_with_data = [
        {
            "patent_id": "US123456",
            "title": "Advanced AI System for Medical Diagnosis",
            "assignee": "Google Inc.",
            "publication_date": "2023-01-15",
            "status": "GRANT"
        },
        {
            "patent_id": "US789012", 
            "title": "Simple Method",
            "assignee": "Small Company",
            "publication_date": "2010-01-15",
            "status": "APPLICATION"
        }
    ]
    
    key_patents = _identify_key_patents(test_patents_with_data)
    print(f"✅ 核心专利识别: {len(key_patents)} 个核心专利")
    
    # 测试报告验证
    test_report = """# 先行技术研究报告

## 专利检索结果
进行了全面的专利检索...

## 现有技术分析
分析了相关的现有技术...

## 技术发展趋势
技术发展呈现上升趋势...

## 竞争对手分析
主要竞争对手包括...

## 侵权风险评估
识别了多个高风险专利...

## 专利地图
构建了技术专利地图...

| 专利ID | 标题 | 受让人 | 风险等级 |
|--------|------|--------|----------|
| US123456 | Test Patent | Google | High |
"""
    
    validation = validate_prior_art_research(test_report)
    print(f"✅ 报告验证: 质量分数 {validation['quality_score']}/100")
    
    if validation["missing_elements"]:
        print(f"⚠️ 缺失元素: {validation['missing_elements']}")
    
    if validation["suggestions"]:
        print(f"💡 改进建议: {validation['suggestions']}")
    
    print("🎉 先行技术研究员测试完成！")


if __name__ == "__main__":
    test_prior_art_researcher() 