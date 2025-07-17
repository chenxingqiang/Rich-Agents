"""
Google Patents API Integration Utils
Google专利API集成工具 - 基于SerpApi实现全球专利检索
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import requests

# 尝试导入SerpApi
try:
    from serpapi import GoogleSearch
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False
    GoogleSearch = None

logger = logging.getLogger(__name__)


class GooglePatentsAPI:
    """Google Patents API客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化Google Patents API客户端
        
        Args:
            api_key: SerpApi API密钥，如果为None则从环境变量获取
        """
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY环境变量未设置或api_key参数为空")
        
        if not SERPAPI_AVAILABLE:
            raise ImportError("SerpApi库未安装，请运行: pip install google-search-results")
        
        self.base_params = {
            "engine": "google_patents",
            "api_key": self.api_key
        }
        
        # API调用统计
        self.api_calls_count = 0
        self.last_call_time = None
        self.rate_limit_delay = 1.0  # 秒
        
        logger.info("Google Patents API客户端初始化成功")
    
    def _rate_limit_check(self) -> None:
        """检查API调用频率限制"""
        if self.last_call_time:
            elapsed = time.time() - self.last_call_time
            if elapsed < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - elapsed
                logger.debug(f"API频率限制，等待 {sleep_time:.2f} 秒")
                time.sleep(sleep_time)
        
        self.last_call_time = time.time()
        self.api_calls_count += 1
    
    def search_patents(
        self,
        query: str,
        page: int = 1,
        num: int = 20,
        sort: str = "relevance",
        country: Optional[str] = None,
        status: Optional[str] = None,
        inventor: Optional[str] = None,
        assignee: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        搜索专利
        
        Args:
            query: 搜索查询词，支持高级语法
            page: 页码，默认1
            num: 每页结果数，10-100
            sort: 排序方式，'new'/'old'/'relevance'
            country: 国家代码过滤，如'US,CN,EP'
            status: 专利状态，'GRANT'/'APPLICATION'
            inventor: 发明人姓名
            assignee: 受让人名称
            before: 最大日期，格式'priority:20221231'
            after: 最小日期，格式'priority:20221231'
            **kwargs: 其他参数
        
        Returns:
            Dict: 搜索结果
        """
        self._rate_limit_check()
        
        # 构建搜索参数
        params = self.base_params.copy()
        params.update({
            "q": query,
            "page": page,
            "num": min(max(num, 10), 100),  # 限制在10-100之间
        })
        
        # 添加可选参数
        if sort in ["new", "old"]:
            params["sort"] = sort
        if country:
            params["country"] = country
        if status:
            params["status"] = status
        if inventor:
            params["inventor"] = inventor
        if assignee:
            params["assignee"] = assignee
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        
        # 添加其他参数
        params.update(kwargs)
        
        try:
            logger.info(f"搜索专利: {query[:50]}...")
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # 处理搜索结果
            processed_results = self._process_search_results(results)
            
            logger.info(f"搜索完成，找到 {len(processed_results.get('patents', []))} 个结果")
            return processed_results
            
        except Exception as e:
            logger.error(f"专利搜索失败: {str(e)}")
            return {
                "error": str(e),
                "patents": [],
                "summary": {},
                "total_results": 0
            }
    
    def _process_search_results(self, raw_results: Dict) -> Dict[str, Any]:
        """处理原始搜索结果"""
        processed = {
            "patents": [],
            "summary": raw_results.get("summary", {}),
            "total_results": 0,
            "search_metadata": raw_results.get("search_metadata", {})
        }
        
        organic_results = raw_results.get("organic_results", [])
        processed["total_results"] = len(organic_results)
        
        for result in organic_results:
            patent_info = {
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "patent_id": result.get("patent_id", ""),
                "publication_number": result.get("publication_number", ""),
                "publication_date": result.get("publication_date", ""),
                "priority_date": result.get("priority_date", ""),
                "filing_date": result.get("filing_date", ""),
                "grant_date": result.get("grant_date", ""),
                "inventor": result.get("inventor", ""),
                "assignee": result.get("assignee", ""),
                "language": result.get("language", ""),
                "country_status": result.get("country_status", {}),
                "patent_link": result.get("patent_link", ""),
                "pdf": result.get("pdf", ""),
                "thumbnail": result.get("thumbnail", ""),
                "figures": result.get("figures", []),
                "cpc": result.get("cpc", ""),
                "cpc_description": result.get("cpc_description", ""),
                "is_scholar": result.get("is_scholar", False),
                "position": result.get("position", 0),
                "rank": result.get("rank", 0)
            }
            processed["patents"].append(patent_info)
        
        return processed
    
    def get_patent_details(self, patent_id: str) -> Dict[str, Any]:
        """
        获取专利详细信息
        
        Args:
            patent_id: 专利ID
        
        Returns:
            Dict: 专利详细信息
        """
        # 使用专利ID进行精确搜索
        results = self.search_patents(f'patent_id:"{patent_id}"', num=1)
        
        if results.get("patents"):
            return results["patents"][0]
        else:
            return {
                "error": f"未找到专利ID: {patent_id}",
                "patent_id": patent_id
            }
    
    def search_similar_patents(
        self,
        reference_patent: str,
        threshold: float = 0.8,
        max_results: int = 20
    ) -> List[Dict]:
        """
        搜索相似专利
        
        Args:
            reference_patent: 参考专利ID或关键词
            threshold: 相似度阈值
            max_results: 最大结果数
        
        Returns:
            List[Dict]: 相似专利列表
        """
        try:
            # 如果是专利ID，先获取详细信息
            if ":" in reference_patent or len(reference_patent) > 20:
                # 直接使用作为搜索查询
                query = reference_patent
            else:
                # 获取专利详情，提取关键词
                patent_details = self.get_patent_details(reference_patent)
                if "error" in patent_details:
                    return []
                
                # 构建搜索查询
                title = patent_details.get("title", "")
                snippet = patent_details.get("snippet", "")
                query = f"{title} {snippet}"[:200]  # 限制长度
            
            # 搜索相似专利
            results = self.search_patents(query, num=max_results)
            
            # 过滤和排序结果
            similar_patents = []
            for patent in results.get("patents", []):
                # 简单的相似度评分（基于标题和摘要）
                similarity_score = self._calculate_similarity(
                    reference_patent, patent
                )
                
                if similarity_score >= threshold:
                    patent["similarity_score"] = similarity_score
                    similar_patents.append(patent)
            
            # 按相似度排序
            similar_patents.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return similar_patents
            
        except Exception as e:
            logger.error(f"相似专利搜索失败: {str(e)}")
            return []
    
    def _calculate_similarity(self, reference: str, patent: Dict) -> float:
        """
        计算专利相似度（简化版本）
        
        Args:
            reference: 参考文本
            patent: 专利信息
        
        Returns:
            float: 相似度分数 (0-1)
        """
        # 这里使用简单的文本匹配，实际应用中可以使用更复杂的NLP方法
        try:
            ref_words = set(reference.lower().split())
            patent_text = f"{patent.get('title', '')} {patent.get('snippet', '')}"
            patent_words = set(patent_text.lower().split())
            
            if not ref_words or not patent_words:
                return 0.0
            
            intersection = len(ref_words & patent_words)
            union = len(ref_words | patent_words)
            
            return intersection / union if union > 0 else 0.0
            
        except Exception:
            return 0.0
    
    def search_by_inventor(self, inventor_name: str, limit: int = 50) -> List[Dict]:
        """
        按发明人搜索专利
        
        Args:
            inventor_name: 发明人姓名
            limit: 结果限制
        
        Returns:
            List[Dict]: 专利列表
        """
        results = self.search_patents(
            query="",
            inventor=inventor_name,
            num=limit
        )
        return results.get("patents", [])
    
    def search_by_assignee(self, assignee_name: str, limit: int = 50) -> List[Dict]:
        """
        按受让人搜索专利
        
        Args:
            assignee_name: 受让人名称
            limit: 结果限制
        
        Returns:
            List[Dict]: 专利列表
        """
        results = self.search_patents(
            query="",
            assignee=assignee_name,
            num=limit
        )
        return results.get("patents", [])
    
    def search_by_date_range(
        self,
        query: str,
        start_date: str,
        end_date: str,
        date_type: str = "publication"
    ) -> List[Dict]:
        """
        按日期范围搜索专利
        
        Args:
            query: 搜索查询
            start_date: 开始日期 YYYYMMDD
            end_date: 结束日期 YYYYMMDD
            date_type: 日期类型 'publication'/'priority'/'filing'
        
        Returns:
            List[Dict]: 专利列表
        """
        results = self.search_patents(
            query=query,
            after=f"{date_type}:{start_date}",
            before=f"{date_type}:{end_date}"
        )
        return results.get("patents", [])
    
    def get_patent_trends(
        self,
        technology_field: str,
        years: int = 5
    ) -> Dict[str, Any]:
        """
        获取专利技术趋势
        
        Args:
            technology_field: 技术领域
            years: 分析年数
        
        Returns:
            Dict: 趋势分析结果
        """
        end_year = datetime.now().year
        start_year = end_year - years
        
        trends = {
            "technology_field": technology_field,
            "time_range": f"{start_year}-{end_year}",
            "yearly_data": [],
            "total_patents": 0,
            "top_assignees": [],
            "top_inventors": []
        }
        
        try:
            # 按年份获取专利数据
            for year in range(start_year, end_year + 1):
                year_start = f"{year}0101"
                year_end = f"{year}1231"
                
                year_results = self.search_by_date_range(
                    query=technology_field,
                    start_date=year_start,
                    end_date=year_end,
                    date_type="publication"
                )
                
                year_data = {
                    "year": year,
                    "patent_count": len(year_results),
                    "patents": year_results
                }
                trends["yearly_data"].append(year_data)
                trends["total_patents"] += len(year_results)
                
                # 短暂延迟避免API限制
                time.sleep(0.5)
            
            # 分析顶级受让人和发明人
            all_patents = []
            for year_data in trends["yearly_data"]:
                all_patents.extend(year_data["patents"])
            
            trends["top_assignees"] = self._analyze_top_entities(
                all_patents, "assignee"
            )
            trends["top_inventors"] = self._analyze_top_entities(
                all_patents, "inventor"
            )
            
            return trends
            
        except Exception as e:
            logger.error(f"专利趋势分析失败: {str(e)}")
            trends["error"] = str(e)
            return trends
    
    def _analyze_top_entities(
        self,
        patents: List[Dict],
        entity_type: str,
        top_k: int = 10
    ) -> List[Dict]:
        """分析顶级实体（受让人或发明人）"""
        entity_counts = {}
        
        for patent in patents:
            entity = patent.get(entity_type, "").strip()
            if entity:
                entity_counts[entity] = entity_counts.get(entity, 0) + 1
        
        # 排序并返回前K个
        sorted_entities = sorted(
            entity_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {"name": entity, "count": count}
            for entity, count in sorted_entities[:top_k]
        ]
    
    def get_api_usage_stats(self) -> Dict[str, Any]:
        """获取API使用统计"""
        return {
            "total_calls": self.api_calls_count,
            "last_call_time": self.last_call_time,
            "rate_limit_delay": self.rate_limit_delay
        }


# 便捷函数
def search_patents(query: str, **kwargs) -> Dict[str, Any]:
    """
    便捷的专利搜索函数
    
    Args:
        query: 搜索查询
        **kwargs: 其他参数
    
    Returns:
        Dict: 搜索结果
    """
    try:
        api = GooglePatentsAPI()
        return api.search_patents(query, **kwargs)
    except Exception as e:
        logger.error(f"专利搜索失败: {str(e)}")
        return {"error": str(e), "patents": []}


def get_patent_by_id(patent_id: str) -> Dict[str, Any]:
    """
    通过ID获取专利详情
    
    Args:
        patent_id: 专利ID
    
    Returns:
        Dict: 专利详情
    """
    try:
        api = GooglePatentsAPI()
        return api.get_patent_details(patent_id)
    except Exception as e:
        logger.error(f"获取专利详情失败: {str(e)}")
        return {"error": str(e), "patent_id": patent_id}


def analyze_patent_landscape(
    technology_field: str,
    years: int = 3
) -> Dict[str, Any]:
    """
    分析专利技术地图
    
    Args:
        technology_field: 技术领域
        years: 分析年数
    
    Returns:
        Dict: 技术地图分析结果
    """
    try:
        api = GooglePatentsAPI()
        return api.get_patent_trends(technology_field, years)
    except Exception as e:
        logger.error(f"专利地图分析失败: {str(e)}")
        return {"error": str(e), "technology_field": technology_field}


# 测试函数
def test_google_patents_api():
    """测试Google Patents API功能"""
    print("🧪 测试Google Patents API...")
    
    try:
        # 测试基本搜索
        results = search_patents("artificial intelligence", num=5)
        print(f"✅ 基本搜索测试: 找到 {len(results.get('patents', []))} 个结果")
        
        # 测试按受让人搜索
        if results.get("patents"):
            first_patent = results["patents"][0]
            print(f"✅ 第一个专利: {first_patent.get('title', 'N/A')}")
        
        # 测试趋势分析
        trends = analyze_patent_landscape("machine learning", years=2)
        print(f"✅ 趋势分析测试: 总计 {trends.get('total_patents', 0)} 个专利")
        
        print("🎉 Google Patents API测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    test_google_patents_api() 