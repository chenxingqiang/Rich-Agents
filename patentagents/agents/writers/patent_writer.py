"""
Patent Writer Agent - 专利撰写员智能体
基于分析结果，撰写高质量的专利申请文档
"""

import functools
import json
import logging
import re
from typing import Dict, Any, List, Tuple
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)


def create_patent_writer(llm, toolkit):
    """
    创建专利撰写员智能体
    
    Args:
        llm: 语言模型实例
        toolkit: 专利工具包实例
    
    Returns:
        function: 专利撰写员节点函数
    """
    
    def patent_writer_node(state):
        """
        专利撰写员节点 - 撰写专利申请文档
        
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
        prior_art_report = state.get("prior_art_report", "")
        
        # 系统提示词
        system_prompt = """你是一位专业的专利撰写员，专门撰写高质量的专利申请文档。你的任务是：

1. **专利申请文档撰写**：
   - 撰写完整的专利申请文档
   - 确保符合专利局的格式要求
   - 包含所有必要的技术描述
   - 保证技术描述的准确性和完整性

2. **权利要求书撰写**：
   - 撰写清晰、准确的权利要求
   - 包含独立权利要求和从属权利要求
   - 确保权利要求的层次结构合理
   - 避免权利要求过于宽泛或狭窄

3. **技术描述优化**：
   - 提供详细的技术背景描述
   - 说明发明的技术问题和解决方案
   - 描述发明的技术效果和优势
   - 包含具体的实施例和应用场景

4. **附图说明**：
   - 设计合适的专利附图
   - 提供详细的附图说明
   - 确保附图与技术描述一致
   - 突出发明的关键技术特征

5. **专利格式规范**：
   - 遵循专利申请的标准格式
   - 确保各部分内容完整
   - 使用专业的专利术语
   - 避免歧义和模糊表达

你需要基于技术分析、创新机会和先行技术研究结果，撰写一份完整、专业的专利申请文档。

**输出格式要求**：
- 严格按照专利申请文档格式
- 包含所有必要的章节
- 使用专业的专利术语
- 确保技术描述的逻辑性和完整性
- 提供详细的权利要求书
"""
        
        # 构建用户输入
        user_input = f"""请基于以下分析结果撰写专利申请文档：

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**申请日期**: {analysis_date}

**技术分析背景**：
{technology_report[:1000] if technology_report else "暂无技术分析背景"}

**创新机会分析**：
{innovation_opportunities[:1000] if innovation_opportunities else "暂无创新机会分析"}

**先行技术研究**：
{prior_art_report[:1000] if prior_art_report else "暂无先行技术研究"}

请撰写一份完整的专利申请文档，包括发明名称、技术领域、背景技术、发明内容、权利要求书、说明书摘要等所有必要部分。"""
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # 工具调用：辅助专利撰写
        try:
            logger.info(f"专利撰写员开始撰写: {technology_domain} - {innovation_topic}")
            
            # 1. 提取核心技术描述
            core_invention = _extract_core_invention(
                technology_report, innovation_opportunities, prior_art_report
            )
            
            # 2. 生成权利要求草稿
            claims_draft = toolkit.generate_patent_claims(core_invention["description"])
            
            # 3. 分析现有技术以避免冲突
            prior_art_analysis = _analyze_prior_art_for_writing(
                state.get("patent_search_results", []),
                state.get("similar_patents", [])
            )
            
            # 4. 生成技术效果描述
            technical_effects = _generate_technical_effects(core_invention)
            
            # 5. 创建附图说明
            drawing_descriptions = _create_drawing_descriptions(core_invention)
            
            # 整理撰写辅助数据
            writing_data = {
                "core_invention": core_invention,
                "claims_draft": claims_draft,
                "prior_art_analysis": prior_art_analysis,
                "technical_effects": technical_effects,
                "drawing_descriptions": drawing_descriptions
            }
            
            # 增强用户输入
            enhanced_user_input = f"""{user_input}

**专利撰写辅助数据**：

1. **核心发明提取**：
   - 技术问题：{core_invention['problem']}
   - 解决方案：{core_invention['solution']}
   - 技术效果：{core_invention['effect']}
   - 核心描述：{core_invention['description']}

2. **权利要求草稿**：
   {json.dumps(claims_draft, ensure_ascii=False, indent=2)}

3. **先行技术分析**：
   {json.dumps(prior_art_analysis, ensure_ascii=False, indent=2)}

4. **技术效果描述**：
   {json.dumps(technical_effects, ensure_ascii=False, indent=2)}

5. **附图说明**：
   {json.dumps(drawing_descriptions, ensure_ascii=False, indent=2)}

请基于以上数据撰写完整的专利申请文档。"""
            
            messages[1]["content"] = enhanced_user_input
            
        except Exception as e:
            logger.error(f"专利撰写员数据准备失败: {str(e)}")
            error_msg = f"\n\n**注意**: 撰写辅助数据准备失败({str(e)})，将基于分析结果进行撰写。"
            messages[1]["content"] += error_msg
            writing_data = {}
        
        # 调用LLM进行专利撰写
        try:
            result = llm.invoke(messages)
            
            # 生成专利申请草稿
            patent_draft = result.content
            
            # 格式化专利文档
            formatted_patent = _format_patent_document(patent_draft)
            
            # 验证专利格式
            format_validation = toolkit.validate_patent_format(formatted_patent)
            
            # 提取权利要求
            extracted_claims = _extract_claims_from_draft(formatted_patent)
            
            # 更新状态
            updated_state = {
                "messages": [result],
                "patent_draft": formatted_patent,
                "sender": "Patent Writer",
                "patent_claims": extracted_claims,
                "format_validation": format_validation,
                "writing_data": writing_data
            }
            
            logger.info(f"专利撰写员撰写完成，包含 {len(extracted_claims)} 条权利要求")
            return updated_state
            
        except Exception as e:
            logger.error(f"专利撰写员LLM调用失败: {str(e)}")
            
            # 生成错误报告
            error_report = f"""# 专利申请文档

## ❌ 撰写失败

**技术领域**: {technology_domain}
**具体方向**: {innovation_topic}
**申请日期**: {analysis_date}

**错误信息**: {str(e)}

**建议**: 请检查LLM配置或稍后重试。"""
            
            return {
                "messages": [AIMessage(content=error_report)],
                "patent_draft": error_report,
                "sender": "Patent Writer",
                "patent_claims": [],
                "format_validation": {"is_valid": False, "errors": [str(e)]},
                "writing_data": {}
            }
    
    return functools.partial(patent_writer_node, name="Patent Writer")


def _extract_core_invention(
    technology_report: str, 
    innovation_opportunities: str, 
    prior_art_report: str
) -> Dict[str, str]:
    """
    从分析报告中提取核心发明要素
    
    Args:
        technology_report: 技术分析报告
        innovation_opportunities: 创新机会报告
        prior_art_report: 先行技术报告
        
    Returns:
        Dict: 核心发明要素
    """
    core_invention = {
        "problem": "",
        "solution": "",
        "effect": "",
        "description": ""
    }
    
    try:
        # 从技术报告中提取技术问题
        if "问题" in technology_report or "挑战" in technology_report:
            problem_section = _extract_section_content(technology_report, ["问题", "挑战", "困难"])
            core_invention["problem"] = problem_section[:200] if problem_section else "现有技术存在局限性"
        
        # 从创新机会中提取解决方案
        if "解决" in innovation_opportunities or "方案" in innovation_opportunities:
            solution_section = _extract_section_content(innovation_opportunities, ["解决", "方案", "方法"])
            core_invention["solution"] = solution_section[:300] if solution_section else "提供创新的技术解决方案"
        
        # 从各报告中提取技术效果
        effect_keywords = ["效果", "优势", "改进", "提升"]
        for report in [technology_report, innovation_opportunities, prior_art_report]:
            if any(keyword in report for keyword in effect_keywords):
                effect_section = _extract_section_content(report, effect_keywords)
                if effect_section:
                    core_invention["effect"] = effect_section[:200]
                    break
        
        if not core_invention["effect"]:
            core_invention["effect"] = "提高技术性能和实用性"
        
        # 综合生成核心描述
        core_invention["description"] = f"""
        本发明涉及{core_invention['problem']}的技术问题，
        通过{core_invention['solution']}的技术方案，
        实现了{core_invention['effect']}的技术效果。
        """.strip()
        
        return core_invention
        
    except Exception as e:
        logger.error(f"提取核心发明失败: {str(e)}")
        return {
            "problem": "现有技术存在技术局限性",
            "solution": "提供创新的技术解决方案",
            "effect": "提高技术性能和实用性",
            "description": "本发明提供了一种创新的技术解决方案"
        }


def _extract_section_content(text: str, keywords: List[str]) -> str:
    """从文本中提取包含关键词的段落内容"""
    lines = text.split('\n')
    relevant_content = []
    
    for line in lines:
        if any(keyword in line for keyword in keywords):
            # 找到相关行，提取周围内容
            start_idx = max(0, lines.index(line) - 1)
            end_idx = min(len(lines), lines.index(line) + 3)
            relevant_content.extend(lines[start_idx:end_idx])
    
    return ' '.join(relevant_content).strip()


def _analyze_prior_art_for_writing(
    patent_search_results: List[Dict], 
    similar_patents: List[Dict]
) -> Dict[str, Any]:
    """分析先行技术以辅助专利撰写"""
    analysis = {
        "key_prior_art": [],
        "differentiation_points": [],
        "avoidance_strategies": []
    }
    
    try:
        # 识别关键先行技术
        all_patents = patent_search_results + similar_patents
        
        for patent in all_patents[:10]:  # 限制分析数量
            if patent.get("importance_score", 0) > 2 or patent.get("similarity_score", 0) > 0.7:
                analysis["key_prior_art"].append({
                    "patent_id": patent.get("patent_id", ""),
                    "title": patent.get("title", ""),
                    "key_features": patent.get("snippet", "")[:100],
                    "assignee": patent.get("assignee", "")
                })
        
        # 生成区别点
        analysis["differentiation_points"] = [
            "技术实现方式的创新",
            "应用场景的扩展",
            "性能参数的优化",
            "系统架构的改进",
            "算法效率的提升"
        ]
        
        # 生成规避策略
        analysis["avoidance_strategies"] = [
            "强调技术方案的独特性",
            "突出技术效果的差异",
            "详细描述实施细节",
            "提供多种实施方式",
            "明确技术范围界限"
        ]
        
        return analysis
        
    except Exception as e:
        logger.error(f"先行技术分析失败: {str(e)}")
        return analysis


def _generate_technical_effects(core_invention: Dict[str, str]) -> List[str]:
    """生成技术效果描述"""
    effects = []
    
    # 基于核心发明生成技术效果
    solution = core_invention.get("solution", "")
    
    # 通用技术效果模板
    effect_templates = [
        "提高了系统的处理效率",
        "增强了技术方案的稳定性",
        "降低了实施成本和复杂度",
        "扩展了应用场景的适用性",
        "改善了用户体验和便利性"
    ]
    
    # 根据解决方案内容选择合适的效果
    if "AI" in solution or "人工智能" in solution:
        effects.extend([
            "提高了智能算法的准确性",
            "增强了机器学习模型的泛化能力",
            "优化了数据处理和分析效率"
        ])
    elif "系统" in solution or "方法" in solution:
        effects.extend([
            "提高了系统的整体性能",
            "简化了操作流程和步骤",
            "增强了系统的可扩展性"
        ])
    else:
        effects.extend(effect_templates[:3])
    
    return effects


def _create_drawing_descriptions(core_invention: Dict[str, str]) -> List[Dict[str, str]]:
    """创建附图说明"""
    drawings = []
    
    # 基于核心发明生成附图说明
    description = core_invention.get("description", "")
    
    # 通用附图模板
    drawing_templates = [
        {
            "figure_num": "图1",
            "title": "系统整体架构图",
            "description": "示出了本发明技术方案的整体架构和主要组成部分"
        },
        {
            "figure_num": "图2", 
            "title": "技术流程图",
            "description": "示出了本发明技术方案的具体实施流程和步骤"
        },
        {
            "figure_num": "图3",
            "title": "关键组件示意图",
            "description": "示出了本发明中关键技术组件的结构和连接关系"
        }
    ]
    
    # 根据技术领域调整附图
    if "AI" in description or "算法" in description:
        drawing_templates[1]["title"] = "算法流程图"
        drawing_templates[1]["description"] = "示出了本发明智能算法的处理流程和决策逻辑"
    
    drawings.extend(drawing_templates)
    
    return drawings


def _format_patent_document(patent_draft: str) -> str:
    """格式化专利文档"""
    try:
        # 确保文档包含标准章节
        required_sections = [
            "发明名称",
            "技术领域", 
            "背景技术",
            "发明内容",
            "附图说明",
            "具体实施方式",
            "权利要求书",
            "说明书摘要"
        ]
        
        formatted_doc = patent_draft
        
        # 检查并添加缺失的章节
        for section in required_sections:
            if section not in formatted_doc:
                # 添加章节标题
                section_content = f"\n\n{section}\n{'=' * len(section)}\n\n[待完善的{section}内容]\n"
                
                # 插入到合适位置
                if section == "说明书摘要":
                    formatted_doc += section_content
                else:
                    # 插入到文档中间
                    formatted_doc += section_content
        
        # 统一格式
        formatted_doc = _standardize_format(formatted_doc)
        
        return formatted_doc
        
    except Exception as e:
        logger.error(f"格式化专利文档失败: {str(e)}")
        return patent_draft


def _standardize_format(text: str) -> str:
    """标准化文档格式"""
    # 统一标题格式
    text = re.sub(r'^#+\s*([^\n]+)', r'\1\n' + '=' * 20, text, flags=re.MULTILINE)
    
    # 统一段落间距
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 统一编号格式
    text = re.sub(r'^\d+\.', lambda m: f"[{m.group().rstrip('.')}]", text, flags=re.MULTILINE)
    
    return text.strip()


def _extract_claims_from_draft(patent_draft: str) -> List[str]:
    """从专利草稿中提取权利要求"""
    claims = []
    
    try:
        # 查找权利要求书章节
        claims_section_start = patent_draft.find("权利要求书")
        if claims_section_start == -1:
            claims_section_start = patent_draft.find("权利要求")
        
        if claims_section_start != -1:
            # 提取权利要求书内容
            claims_content = patent_draft[claims_section_start:]
            
            # 查找下一个章节的开始
            next_section = claims_content.find("\n\n", 100)  # 跳过标题
            if next_section != -1:
                claims_content = claims_content[:next_section]
            
            # 提取各项权利要求
            claim_pattern = r'(\d+)\.\s*([^0-9]+?)(?=\d+\.|$)'
            matches = re.findall(claim_pattern, claims_content, re.DOTALL)
            
            for match in matches:
                claim_num, claim_text = match
                claims.append(f"{claim_num}. {claim_text.strip()}")
        
        return claims
        
    except Exception as e:
        logger.error(f"提取权利要求失败: {str(e)}")
        return []


def create_patent_writer_with_validation(llm, toolkit):
    """
    创建带验证的专利撰写员智能体
    
    Args:
        llm: 语言模型实例
        toolkit: 专利工具包实例
    
    Returns:
        function: 专利撰写员节点函数
    """
    
    def patent_writer_with_validation_node(state):
        """带验证的专利撰写员节点"""
        
        # 调用基础专利撰写员
        base_writer = create_patent_writer(llm, toolkit)
        result = base_writer(state)
        
        # 验证专利草稿质量
        if result.get("patent_draft"):
            validation_result = validate_patent_draft(result["patent_draft"])
            result["draft_validation"] = validation_result
            
            # 如果质量不合格，记录警告
            if not validation_result["is_valid"]:
                logger.warning(f"专利草稿质量不合格: {validation_result['issues']}")
                
                # 尝试改进草稿
                if validation_result["quality_score"] > 50:
                    improved_draft = _improve_patent_draft(
                        result["patent_draft"], 
                        validation_result["suggestions"]
                    )
                    result["patent_draft"] = improved_draft
                    result["improvement_applied"] = True
        
        return result
    
    return functools.partial(patent_writer_with_validation_node, name="Patent Writer")


def _improve_patent_draft(draft: str, suggestions: List[str]) -> str:
    """改进专利草稿"""
    improved_draft = draft
    
    try:
        # 根据建议进行改进
        for suggestion in suggestions:
            if "权利要求" in suggestion:
                # 改进权利要求
                improved_draft = _improve_claims_section(improved_draft)
            elif "技术描述" in suggestion:
                # 改进技术描述
                improved_draft = _improve_technical_description(improved_draft)
            elif "格式" in suggestion:
                # 改进格式
                improved_draft = _standardize_format(improved_draft)
        
        return improved_draft
        
    except Exception as e:
        logger.error(f"改进专利草稿失败: {str(e)}")
        return draft


def _improve_claims_section(draft: str) -> str:
    """改进权利要求章节"""
    # 简化的改进逻辑
    if "权利要求书" in draft:
        # 确保权利要求格式正确
        draft = re.sub(
            r'(\d+)\s*[.。]\s*',
            r'\1. ',
            draft
        )
    
    return draft


def _improve_technical_description(draft: str) -> str:
    """改进技术描述"""
    # 简化的改进逻辑
    if "具体实施方式" in draft:
        # 确保有详细的技术描述
        if draft.count("实施例") < 2:
            draft = draft.replace(
                "具体实施方式",
                "具体实施方式\n\n实施例1：\n[详细实施例描述]\n\n实施例2：\n[另一实施例描述]\n"
            )
    
    return draft


def validate_patent_draft(patent_draft: str) -> Dict[str, Any]:
    """
    验证专利草稿的质量
    
    Args:
        patent_draft: 专利草稿
        
    Returns:
        dict: 验证结果
    """
    validation_result = {
        "is_valid": True,
        "quality_score": 100,
        "issues": [],
        "suggestions": []
    }
    
    # 检查必需章节
    required_sections = [
        "发明名称", "技术领域", "背景技术", "发明内容", 
        "权利要求书", "说明书摘要"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in patent_draft:
            missing_sections.append(section)
            validation_result["quality_score"] -= 15
    
    if missing_sections:
        validation_result["issues"].append(f"缺少必需章节: {missing_sections}")
        validation_result["suggestions"].append("添加缺失的专利文档章节")
    
    # 检查权利要求
    claims_count = len(re.findall(r'\d+\.\s+', patent_draft))
    if claims_count < 3:
        validation_result["issues"].append("权利要求数量不足")
        validation_result["quality_score"] -= 20
        validation_result["suggestions"].append("增加更多权利要求")
    
    # 检查文档长度
    if len(patent_draft) < 2000:
        validation_result["issues"].append("文档内容过短")
        validation_result["quality_score"] -= 15
        validation_result["suggestions"].append("增加详细的技术描述")
    
    # 检查技术描述
    if "实施例" not in patent_draft:
        validation_result["issues"].append("缺少具体实施例")
        validation_result["quality_score"] -= 10
        validation_result["suggestions"].append("添加具体的实施例描述")
    
    # 检查专业术语
    if patent_draft.count("本发明") < 3:
        validation_result["issues"].append("专业术语使用不足")
        validation_result["quality_score"] -= 5
        validation_result["suggestions"].append("使用更多专业的专利术语")
    
    # 判断是否有效
    if validation_result["quality_score"] < 60:
        validation_result["is_valid"] = False
    
    return validation_result


def analyze_patent_claims(claims: List[str]) -> Dict[str, Any]:
    """
    分析专利权利要求
    
    Args:
        claims: 权利要求列表
        
    Returns:
        dict: 分析结果
    """
    analysis = {
        "total_claims": len(claims),
        "independent_claims": 0,
        "dependent_claims": 0,
        "claim_types": {},
        "coverage_analysis": {}
    }
    
    try:
        for claim in claims:
            # 识别独立权利要求和从属权利要求
            if "根据权利要求" in claim:
                analysis["dependent_claims"] += 1
            else:
                analysis["independent_claims"] += 1
            
            # 识别权利要求类型
            if "方法" in claim or "步骤" in claim:
                analysis["claim_types"]["method"] = analysis["claim_types"].get("method", 0) + 1
            elif "系统" in claim or "装置" in claim:
                analysis["claim_types"]["system"] = analysis["claim_types"].get("system", 0) + 1
            elif "产品" in claim or "组合物" in claim:
                analysis["claim_types"]["product"] = analysis["claim_types"].get("product", 0) + 1
        
        # 覆盖范围分析
        analysis["coverage_analysis"] = {
            "has_method_claims": "method" in analysis["claim_types"],
            "has_system_claims": "system" in analysis["claim_types"],
            "has_product_claims": "product" in analysis["claim_types"],
            "claim_diversity": len(analysis["claim_types"])
        }
        
        return analysis
        
    except Exception as e:
        logger.error(f"权利要求分析失败: {str(e)}")
        return analysis


# 测试函数
def test_patent_writer():
    """测试专利撰写员功能"""
    print("🧪 测试专利撰写员...")
    
    # 测试核心发明提取
    test_tech_report = """
    ## 技术问题
    现有的图像识别技术存在准确率低的问题。
    
    ## 技术挑战
    处理复杂场景下的图像识别困难。
    """
    
    test_innovation = """
    ## 解决方案
    采用深度学习算法提高识别准确率。
    
    ## 技术方法
    使用卷积神经网络进行特征提取。
    """
    
    core_invention = _extract_core_invention(test_tech_report, test_innovation, "")
    print(f"✅ 核心发明提取: {core_invention['problem'][:30]}...")
    
    # 测试权利要求提取
    test_draft = """
    权利要求书
    
    1. 一种图像识别方法，其特征在于包括以下步骤：
       获取图像数据；
       使用神经网络处理图像。
    
    2. 根据权利要求1所述的方法，其特征在于：
       所述神经网络为卷积神经网络。
    
    说明书摘要
    本发明提供了一种图像识别方法。
    """
    
    claims = _extract_claims_from_draft(test_draft)
    print(f"✅ 权利要求提取: {len(claims)} 条权利要求")
    
    # 测试权利要求分析
    analysis = analyze_patent_claims(claims)
    print(f"✅ 权利要求分析: {analysis['independent_claims']} 独立 + {analysis['dependent_claims']} 从属")
    
    # 测试专利草稿验证
    validation = validate_patent_draft(test_draft)
    print(f"✅ 草稿验证: 质量分数 {validation['quality_score']}/100")
    
    if validation["issues"]:
        print(f"⚠️ 发现问题: {validation['issues']}")
    
    if validation["suggestions"]:
        print(f"💡 改进建议: {validation['suggestions']}")
    
    print("🎉 专利撰写员测试完成！")


if __name__ == "__main__":
    test_patent_writer() 