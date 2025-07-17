"""
Patent Toolkit - 专利工具包
集成多个专利API和分析工具的统一接口
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 导入专利API工具
from ...dataflows.google_patents_utils import GooglePatentsAPI
from ...dataflows.zhihuiya_utils import ZhiHuiYaAPI

logger = logging.getLogger(__name__)


class PatentToolkit:
    """
    专利工具包 - 统一的专利分析工具接口
    集成Google Patents API和智慧芽API的所有功能
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化专利工具包
        
        Args:
            config: 配置字典，包含API密钥等信息
        """
        self.config = config or {}
        
        # 初始化API客户端
        self.google_api = None
        self.zhihuiya_api = None
        
        # 尝试初始化Google Patents API
        try:
            self.google_api = GooglePatentsAPI()
            logger.info("Google Patents API初始化成功")
        except Exception as e:
            logger.warning(f"Google Patents API初始化失败: {str(e)}")
        
        # 尝试初始化智慧芽API
        try:
            self.zhihuiya_api = ZhiHuiYaAPI()
            logger.info("智慧芽API初始化成功")
        except Exception as e:
            logger.warning(f"智慧芽API初始化失败: {str(e)}")
        
        # 线程池用于并行处理
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        logger.info("专利工具包初始化完成")
    
    # ============ Google Patents API 专利检索工具 ============
    
    def search_google_patents(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        使用Google Patents API进行专利检索
        
        Args:
            query: 搜索查询词，支持高级语法如 "(Coffee) OR (Tea)"
            **kwargs: 其他搜索参数
        
        Returns:
            Dict: 包含专利结果、摘要统计等信息
        """
        if not self.google_api:
            return {"error": "Google Patents API未初始化", "patents": []}
        
        try:
            return self.google_api.search_patents(query, **kwargs)
        except Exception as e:
            logger.error(f"Google专利搜索失败: {str(e)}")
            return {"error": str(e), "patents": []}
    
    def get_patent_details(self, patent_id: str) -> Dict[str, Any]:
        """获取专利详细信息，包括PDF链接、图像、引用等"""
        if not self.google_api:
            return {"error": "Google Patents API未初始化", "patent_id": patent_id}
        
        try:
            return self.google_api.get_patent_details(patent_id)
        except Exception as e:
            logger.error(f"获取专利详情失败: {str(e)}")
            return {"error": str(e), "patent_id": patent_id}
    
    def search_similar_patents(self, patent_id: str, threshold: float = 0.8) -> List[Dict]:
        """基于专利ID搜索相似专利"""
        if not self.google_api:
            return []
        
        try:
            return self.google_api.search_similar_patents(patent_id, threshold)
        except Exception as e:
            logger.error(f"相似专利搜索失败: {str(e)}")
            return []
    
    # ============ 智慧芽专利数据工具 ============
    
    def search_zhihuiya_patents(self, keywords: str, **filters) -> Dict[str, Any]:
        """使用智慧芽API进行专利检索"""
        if not self.zhihuiya_api:
            return {"error": "智慧芽API未初始化", "results": []}
        
        try:
            return self.zhihuiya_api.search_patents(keywords, **filters)
        except Exception as e:
            logger.error(f"智慧芽专利搜索失败: {str(e)}")
            return {"error": str(e), "results": []}
    
    def extract_patent_core_invention(self, patent_text: str) -> Dict[str, Any]:
        """使用智慧芽AI31提取专利核心发明点"""
        if not self.zhihuiya_api:
            return {"error": "智慧芽API未初始化"}
        
        try:
            return self.zhihuiya_api.extract_patent_core_invention(patent_text)
        except Exception as e:
            logger.error(f"提取专利核心发明点失败: {str(e)}")
            return {"error": str(e)}
    
    def analyze_patent_feasibility(self, patent_content: str) -> Dict[str, Any]:
        """使用智慧芽AI40进行专利可行性分析"""
        if not self.zhihuiya_api:
            return {"error": "智慧芽API未初始化"}
        
        try:
            return self.zhihuiya_api.analyze_patent_feasibility(patent_content)
        except Exception as e:
            logger.error(f"专利可行性分析失败: {str(e)}")
            return {"error": str(e)}
    
    def compare_patent_similarity(self, patent_a: str, patent_b: str) -> Dict[str, Any]:
        """使用智慧芽AI30进行专利相似度比对"""
        if not self.zhihuiya_api:
            return {"error": "智慧芽API未初始化"}
        
        try:
            return self.zhihuiya_api.compare_patent_similarity(patent_a, patent_b)
        except Exception as e:
            logger.error(f"专利相似度比对失败: {str(e)}")
            return {"error": str(e)}
    
    def translate_patent_text(self, text: str, target_lang: str) -> str:
        """使用智慧芽AI61进行专利文档翻译"""
        if not self.zhihuiya_api:
            return f"翻译失败: 智慧芽API未初始化"
        
        try:
            result = self.zhihuiya_api.translate_patent_text(text, target_lang)
            return result.get("translated_text", text)
        except Exception as e:
            logger.error(f"专利文档翻译失败: {str(e)}")
            return f"翻译失败: {str(e)}"
    
    # ============ 传统专利数据库接口 ============
    
    def search_uspto_patents(self, keywords: str, classification: str = "") -> List[Dict]:
        """USPTO专利检索"""
        # 使用Google Patents API作为备选
        if self.google_api:
            results = self.google_api.search_patents(
                keywords, 
                country="US", 
                status="GRANT"
            )
            return results.get("patents", [])
        return []
    
    def search_epo_patents(self, keywords: str, ipc_class: str = "") -> List[Dict]:
        """EPO专利检索"""
        # 使用Google Patents API作为备选
        if self.google_api:
            results = self.google_api.search_patents(
                keywords, 
                country="EP"
            )
            return results.get("patents", [])
        return []
    
    # ============ 文献检索工具 ============
    
    def search_ieee_papers(self, keywords: str, year_range: Tuple[int, int] = None) -> List[Dict]:
        """IEEE学术文献检索"""
        # TODO: 实现IEEE API集成
        logger.warning("IEEE API集成尚未实现")
        return []
    
    def search_arxiv_papers(self, keywords: str, categories: List[str] = None) -> List[Dict]:
        """arXiv预印本论文检索"""
        # TODO: 实现arXiv API集成
        logger.warning("arXiv API集成尚未实现")
        return []
    
    def search_google_scholar(self, query: str, citation_threshold: int = 10) -> List[Dict]:
        """Google Scholar学术搜索"""
        # TODO: 实现Google Scholar API集成
        logger.warning("Google Scholar API集成尚未实现")
        return []
    
    # ============ 技术分析工具 ============
    
    def analyze_patent_trends(
        self, 
        technology_field: str, 
        time_range: Tuple[str, str] = None
    ) -> Dict[str, Any]:
        """分析专利技术趋势"""
        results = {}
        
        # 使用Google Patents API获取趋势数据
        if self.google_api:
            try:
                google_trends = self.google_api.get_patent_trends(technology_field)
                results["google_trends"] = google_trends
            except Exception as e:
                logger.error(f"Google专利趋势分析失败: {str(e)}")
        
        # 使用智慧芽API获取趋势数据
        if self.zhihuiya_api:
            try:
                zhihuiya_trends = self.zhihuiya_api.get_patent_trends([technology_field])
                results["zhihuiya_trends"] = zhihuiya_trends
            except Exception as e:
                logger.error(f"智慧芽专利趋势分析失败: {str(e)}")
        
        return results
    
    def generate_patent_landscape(self, technology_area: str) -> Dict[str, Any]:
        """生成专利技术地图"""
        if self.zhihuiya_api:
            try:
                return self.zhihuiya_api.analyze_patent_landscape(technology_area)
            except Exception as e:
                logger.error(f"专利技术地图生成失败: {str(e)}")
                return {"error": str(e)}
        
        return {"error": "智慧芽API未初始化"}
    
    def assess_patent_strength(self, patent_id: str) -> Dict[str, Any]:
        """评估专利强度和价值"""
        if self.zhihuiya_api:
            try:
                return self.zhihuiya_api.assess_patent_value(patent_id)
            except Exception as e:
                logger.error(f"专利强度评估失败: {str(e)}")
                return {"error": str(e)}
        
        return {"error": "智慧芽API未初始化"}
    
    def build_patent_citation_network(self, patent_ids: List[str]) -> Dict[str, Any]:
        """构建专利引用网络图"""
        citation_network = {
            "nodes": [],
            "edges": [],
            "statistics": {}
        }
        
        if not self.zhihuiya_api:
            return {"error": "智慧芽API未初始化"}
        
        try:
            for patent_id in patent_ids:
                citations = self.zhihuiya_api.get_patent_citations(patent_id)
                
                # 添加节点
                citation_network["nodes"].append({
                    "id": patent_id,
                    "citations": citations
                })
                
                # 添加边（引用关系）
                for citation in citations.get("cited_by", []):
                    citation_network["edges"].append({
                        "source": patent_id,
                        "target": citation.get("patent_id", ""),
                        "type": "cited_by"
                    })
                
                for citation in citations.get("cites", []):
                    citation_network["edges"].append({
                        "source": patent_id,
                        "target": citation.get("patent_id", ""),
                        "type": "cites"
                    })
            
            # 计算网络统计信息
            citation_network["statistics"] = {
                "total_nodes": len(citation_network["nodes"]),
                "total_edges": len(citation_network["edges"]),
                "avg_citations": sum(len(node["citations"].get("cited_by", [])) 
                                   for node in citation_network["nodes"]) / len(patent_ids)
            }
            
            return citation_network
            
        except Exception as e:
            logger.error(f"构建专利引用网络失败: {str(e)}")
            return {"error": str(e)}
    
    # ============ 创新发现工具 ============
    
    def identify_technology_gaps(self, field: str, existing_patents: List[str]) -> List[Dict]:
        """识别技术空白领域"""
        gaps = []
        
        try:
            # 使用Google Patents API搜索该领域的专利
            if self.google_api:
                search_results = self.google_api.search_patents(field, num=100)
                all_patents = search_results.get("patents", [])
                
                # 分析专利分布和空白
                # 这里使用简化的分析方法
                patent_keywords = {}
                for patent in all_patents:
                    title = patent.get("title", "").lower()
                    words = title.split()
                    for word in words:
                        if len(word) > 3:  # 过滤短词
                            patent_keywords[word] = patent_keywords.get(word, 0) + 1
                
                # 识别关键词覆盖不足的领域
                low_coverage_keywords = [
                    word for word, count in patent_keywords.items() 
                    if count < 5  # 阈值可调整
                ]
                
                for keyword in low_coverage_keywords[:10]:  # 取前10个
                    gaps.append({
                        "keyword": keyword,
                        "coverage": patent_keywords[keyword],
                        "potential": "high" if patent_keywords[keyword] < 2 else "medium"
                    })
            
            return gaps
            
        except Exception as e:
            logger.error(f"识别技术空白失败: {str(e)}")
            return []
    
    def discover_emerging_technologies(
        self, 
        news_sources: List[str], 
        time_window: int = 30
    ) -> List[Dict]:
        """发现新兴技术趋势"""
        # TODO: 实现新闻源分析和技术趋势发现
        logger.warning("新兴技术发现功能尚未实现")
        return []
    
    def analyze_research_frontiers(self, literature_corpus: List[Dict]) -> Dict[str, Any]:
        """分析研究前沿"""
        # TODO: 实现文献分析和研究前沿识别
        logger.warning("研究前沿分析功能尚未实现")
        return {}
    
    def cross_domain_innovation_discovery(self, domains: List[str]) -> List[Dict]:
        """跨领域创新机会发现"""
        innovations = []
        
        if not self.google_api:
            return innovations
        
        try:
            # 为每个领域搜索专利
            domain_patents = {}
            for domain in domains:
                results = self.google_api.search_patents(domain, num=50)
                domain_patents[domain] = results.get("patents", [])
            
            # 寻找跨领域的技术交叉点
            for i, domain_a in enumerate(domains):
                for j, domain_b in enumerate(domains[i+1:], i+1):
                    # 分析两个领域的专利交集
                    patents_a = domain_patents[domain_a]
                    patents_b = domain_patents[domain_b]
                    
                    # 寻找共同的发明人或受让人
                    common_inventors = set()
                    common_assignees = set()
                    
                    for patent_a in patents_a:
                        for patent_b in patents_b:
                            if patent_a.get("inventor") == patent_b.get("inventor"):
                                common_inventors.add(patent_a.get("inventor"))
                            if patent_a.get("assignee") == patent_b.get("assignee"):
                                common_assignees.add(patent_a.get("assignee"))
                    
                    if common_inventors or common_assignees:
                        innovations.append({
                            "domain_a": domain_a,
                            "domain_b": domain_b,
                            "common_inventors": list(common_inventors),
                            "common_assignees": list(common_assignees),
                            "innovation_potential": "high"
                        })
            
            return innovations
            
        except Exception as e:
            logger.error(f"跨领域创新发现失败: {str(e)}")
            return []
    
    # ============ 专利撰写工具 ============
    
    def generate_patent_claims(self, technical_description: str) -> List[str]:
        """生成专利权利要求"""
        if not self.zhihuiya_api:
            return ["智慧芽API未初始化，无法生成权利要求"]
        
        try:
            # 使用智慧芽AI分析技术描述
            core_invention = self.zhihuiya_api.extract_patent_core_invention(technical_description)
            
            # 基于核心发明点生成权利要求
            claims = []
            
            # 独立权利要求
            main_claim = f"1. 一种{technical_description}，其特征在于："
            claims.append(main_claim)
            
            # 从属权利要求（基于AI分析结果）
            if "core_points" in core_invention:
                for i, point in enumerate(core_invention["core_points"][:5], 2):
                    dependent_claim = f"{i}. 根据权利要求1所述的方法，其特征在于：{point}"
                    claims.append(dependent_claim)
            
            return claims
            
        except Exception as e:
            logger.error(f"生成专利权利要求失败: {str(e)}")
            return [f"权利要求生成失败: {str(e)}"]
    
    def create_patent_drawings(self, technical_specs: Dict) -> List[str]:
        """创建专利附图"""
        # TODO: 实现专利附图生成
        logger.warning("专利附图生成功能尚未实现")
        return []
    
    def format_patent_application(self, content_sections: Dict) -> str:
        """格式化专利申请文档"""
        sections = [
            "发明名称",
            "技术领域", 
            "背景技术",
            "发明内容",
            "附图说明",
            "具体实施方式",
            "权利要求书",
            "说明书摘要"
        ]
        
        formatted_doc = ""
        
        for section in sections:
            if section in content_sections:
                formatted_doc += f"\n{section}\n"
                formatted_doc += "=" * len(section) + "\n"
                formatted_doc += content_sections[section] + "\n"
        
        return formatted_doc
    
    def validate_patent_format(self, patent_draft: str) -> Dict[str, Any]:
        """验证专利文档格式和完整性"""
        required_sections = [
            "发明名称", "技术领域", "背景技术", "发明内容", 
            "权利要求书", "说明书摘要"
        ]
        
        validation_result = {
            "is_valid": True,
            "missing_sections": [],
            "warnings": [],
            "score": 100
        }
        
        for section in required_sections:
            if section not in patent_draft:
                validation_result["missing_sections"].append(section)
                validation_result["is_valid"] = False
                validation_result["score"] -= 15
        
        # 检查文档长度
        if len(patent_draft) < 1000:
            validation_result["warnings"].append("文档过短，可能缺少详细描述")
            validation_result["score"] -= 10
        
        return validation_result
    
    # ============ 专利价值评估工具 ============
    
    def evaluate_patent_commercial_value(self, patent_id: str) -> Dict[str, Any]:
        """评估专利商业价值"""
        if self.zhihuiya_api:
            try:
                return self.zhihuiya_api.assess_patent_value(patent_id)
            except Exception as e:
                logger.error(f"专利商业价值评估失败: {str(e)}")
                return {"error": str(e)}
        
        return {"error": "智慧芽API未初始化"}
    
    def assess_infringement_risk(
        self, 
        patent_content: str, 
        existing_patents: List[str]
    ) -> Dict[str, Any]:
        """评估专利侵权风险"""
        risk_assessment = {
            "overall_risk": "low",
            "risk_factors": [],
            "similar_patents": [],
            "recommendations": []
        }
        
        if not self.zhihuiya_api:
            return {"error": "智慧芽API未初始化"}
        
        try:
            # 检查与现有专利的相似度
            high_similarity_count = 0
            
            for existing_patent in existing_patents:
                similarity_result = self.zhihuiya_api.compare_patent_similarity(
                    patent_content, existing_patent
                )
                
                similarity_score = similarity_result.get("similarity_score", 0)
                
                if similarity_score > 0.8:
                    high_similarity_count += 1
                    risk_assessment["similar_patents"].append({
                        "patent": existing_patent,
                        "similarity": similarity_score
                    })
            
            # 评估风险等级
            if high_similarity_count > 2:
                risk_assessment["overall_risk"] = "high"
                risk_assessment["recommendations"].append("建议重新设计技术方案")
            elif high_similarity_count > 0:
                risk_assessment["overall_risk"] = "medium"
                risk_assessment["recommendations"].append("建议进行更详细的侵权分析")
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"专利侵权风险评估失败: {str(e)}")
            return {"error": str(e)}
    
    def predict_patent_grant_probability(self, patent_application: str) -> float:
        """预测专利授权概率"""
        if not self.zhihuiya_api:
            return 0.0
        
        try:
            # 使用智慧芽可行性分析
            feasibility = self.zhihuiya_api.analyze_patent_feasibility(patent_application)
            
            # 基于可行性分析结果计算授权概率
            feasibility_score = feasibility.get("feasibility_score", 0.5)
            
            # 简化的概率计算
            grant_probability = min(max(feasibility_score, 0.1), 0.9)
            
            return grant_probability
            
        except Exception as e:
            logger.error(f"专利授权概率预测失败: {str(e)}")
            return 0.0
    
    # ============ 工具管理和统计 ============
    
    def get_toolkit_status(self) -> Dict[str, Any]:
        """获取工具包状态"""
        status = {
            "google_api_available": self.google_api is not None,
            "zhihuiya_api_available": self.zhihuiya_api is not None,
            "total_apis": 0,
            "api_usage": {}
        }
        
        if self.google_api:
            status["total_apis"] += 1
            status["api_usage"]["google"] = self.google_api.get_api_usage_stats()
        
        if self.zhihuiya_api:
            status["total_apis"] += 1
            status["api_usage"]["zhihuiya"] = self.zhihuiya_api.get_api_usage_stats()
        
        return status
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)


# 便捷函数
def create_patent_toolkit(config: Optional[Dict] = None) -> PatentToolkit:
    """创建专利工具包实例"""
    return PatentToolkit(config)


# 测试函数
def test_patent_toolkit():
    """测试专利工具包功能"""
    print("🧪 测试专利工具包...")
    
    try:
        toolkit = PatentToolkit()
        
        # 测试状态检查
        status = toolkit.get_toolkit_status()
        print(f"✅ 工具包状态: {status['total_apis']} 个API可用")
        
        # 测试专利搜索
        if status["google_api_available"]:
            results = toolkit.search_google_patents("artificial intelligence", num=3)
            print(f"✅ Google专利搜索: {len(results.get('patents', []))} 个结果")
        
        # 测试智慧芽功能
        if status["zhihuiya_api_available"]:
            test_text = "一种基于人工智能的图像识别方法"
            ai_result = toolkit.extract_patent_core_invention(test_text)
            print(f"✅ 智慧芽AI分析: {ai_result.get('status', 'N/A')}")
        
        # 测试专利撰写
        claims = toolkit.generate_patent_claims("图像识别方法")
        print(f"✅ 权利要求生成: {len(claims)} 条")
        
        print("🎉 专利工具包测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    test_patent_toolkit() 