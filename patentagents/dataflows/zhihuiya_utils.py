"""
智慧芽专利数据平台API集成工具
ZhiHuiYa Patent API Integration Utils
"""

import os
import json
import time
import logging
import base64
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import requests
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class ZhiHuiYaAPI:
    """智慧芽专利数据平台API客户端"""
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        base_url: str = "https://open-zhihuiya-com.libproxy1.nus.edu.sg"
    ):
        """
        初始化智慧芽API客户端
        
        Args:
            client_id: 客户端ID，如果为None则从环境变量获取
            client_secret: 客户端密钥，如果为None则从环境变量获取
            base_url: API基础URL
        """
        self.client_id = client_id or os.getenv("ZHIHUIYA_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("ZHIHUIYA_CLIENT_SECRET")
        self.base_url = base_url
        
        if not self.client_id or not self.client_secret:
            raise ValueError("ZHIHUIYA_CLIENT_ID和ZHIHUIYA_CLIENT_SECRET环境变量未设置")
        
        # 认证相关
        self.access_token = None
        self.token_expires_at = None
        self.token_type = "BearerToken"
        
        # API调用统计
        self.api_calls_count = 0
        self.last_call_time = None
        self.rate_limit_delay = 0.5  # 秒
        
        # 获取访问令牌
        self._get_access_token()
        
        logger.info("智慧芽API客户端初始化成功")
    
    def _get_access_token(self) -> None:
        """获取访问令牌"""
        try:
            # 构建认证头
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_string.encode('utf-8')
            auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {auth_b64}"
            }
            
            data = {
                "grant_type": "client_credentials"
            }
            
            response = requests.post(
                f"{self.base_url}/oauth/token",
                headers=headers,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("token")
                self.token_type = token_data.get("token_type", "BearerToken")
                expires_in = token_data.get("expires_in", 1800)  # 默认30分钟
                
                # 计算过期时间
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                
                logger.info("智慧芽访问令牌获取成功")
            else:
                raise Exception(f"获取访问令牌失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"获取智慧芽访问令牌失败: {str(e)}")
            raise
    
    def _ensure_valid_token(self) -> None:
        """确保访问令牌有效"""
        if not self.access_token or not self.token_expires_at:
            self._get_access_token()
            return
        
        # 检查令牌是否即将过期
        if datetime.now() >= self.token_expires_at:
            logger.info("访问令牌即将过期，重新获取")
            self._get_access_token()
    
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
    
    def _make_api_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        发起API请求
        
        Args:
            endpoint: API端点
            method: HTTP方法
            params: URL参数
            data: 请求数据
            timeout: 超时时间
        
        Returns:
            Dict: API响应
        """
        self._ensure_valid_token()
        self._rate_limit_check()
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # 添加apikey参数
        if params is None:
            params = {}
        params["apikey"] = self.client_id
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, params=params, json=data, timeout=timeout)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            # 检查响应状态
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"API请求失败: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {"error": error_msg, "status_code": response.status_code}
                
        except requests.exceptions.RequestException as e:
            error_msg = f"API请求异常: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def search_patents(
        self,
        keywords: str,
        page: int = 1,
        page_size: int = 20,
        sort_field: str = "relevance",
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        搜索专利
        
        Args:
            keywords: 搜索关键词
            page: 页码
            page_size: 每页结果数
            sort_field: 排序字段
            filters: 筛选条件
        
        Returns:
            Dict: 搜索结果
        """
        params = {
            "q": keywords,
            "page": page,
            "page_size": min(max(page_size, 1), 100),
            "sort": sort_field
        }
        
        if filters:
            params.update(filters)
        
        logger.info(f"搜索专利: {keywords[:50]}...")
        
        result = self._make_api_request("/api/v1/patents/search", "GET", params)
        
        if "error" not in result:
            logger.info(f"搜索完成，找到 {result.get('total', 0)} 个结果")
        
        return result
    
    def get_patent_details(self, patent_id: str) -> Dict[str, Any]:
        """
        获取专利详细信息
        
        Args:
            patent_id: 专利ID
        
        Returns:
            Dict: 专利详细信息
        """
        logger.info(f"获取专利详情: {patent_id}")
        
        result = self._make_api_request(f"/api/v1/patents/{patent_id}")
        
        return result
    
    def extract_patent_core_invention(self, patent_text: str) -> Dict[str, Any]:
        """
        使用AI31提取专利核心发明点
        
        Args:
            patent_text: 专利文本内容
        
        Returns:
            Dict: 核心发明点分析结果
        """
        data = {
            "text": patent_text,
            "ai_model": "AI31",
            "task": "core_invention_extraction"
        }
        
        logger.info("使用AI31提取专利核心发明点...")
        
        result = self._make_api_request("/api/v1/ai/analyze", "POST", data=data)
        
        return result
    
    def analyze_patent_feasibility(self, patent_content: str) -> Dict[str, Any]:
        """
        使用AI40进行专利可行性分析
        
        Args:
            patent_content: 专利内容
        
        Returns:
            Dict: 可行性分析结果
        """
        data = {
            "content": patent_content,
            "ai_model": "AI40",
            "task": "feasibility_analysis"
        }
        
        logger.info("使用AI40进行专利可行性分析...")
        
        result = self._make_api_request("/api/v1/ai/analyze", "POST", data=data)
        
        return result
    
    def compare_patent_similarity(
        self,
        patent_a: str,
        patent_b: str,
        comparison_type: str = "full"
    ) -> Dict[str, Any]:
        """
        使用AI30进行专利相似度比对
        
        Args:
            patent_a: 专利A的内容
            patent_b: 专利B的内容
            comparison_type: 比较类型 'full'/'claims'/'abstract'
        
        Returns:
            Dict: 相似度分析结果
        """
        data = {
            "patent_a": patent_a,
            "patent_b": patent_b,
            "ai_model": "AI30",
            "task": "similarity_comparison",
            "comparison_type": comparison_type
        }
        
        logger.info("使用AI30进行专利相似度比对...")
        
        result = self._make_api_request("/api/v1/ai/compare", "POST", data=data)
        
        return result
    
    def translate_patent_text(
        self,
        text: str,
        target_language: str,
        source_language: str = "auto"
    ) -> Dict[str, Any]:
        """
        使用AI61进行专利文档翻译
        
        Args:
            text: 要翻译的文本
            target_language: 目标语言 'zh'/'en'/'ja'/'ko'等
            source_language: 源语言，'auto'为自动检测
        
        Returns:
            Dict: 翻译结果
        """
        data = {
            "text": text,
            "ai_model": "AI61",
            "task": "translation",
            "target_language": target_language,
            "source_language": source_language
        }
        
        logger.info(f"使用AI61翻译文本到{target_language}...")
        
        result = self._make_api_request("/api/v1/ai/translate", "POST", data=data)
        
        return result
    
    def extract_drug_ddt_info(self, patent_text: str) -> Dict[str, Any]:
        """
        使用AI01提取药物DDT信息（药物、适应症、靶点）
        
        Args:
            patent_text: 专利文本
        
        Returns:
            Dict: DDT信息提取结果
        """
        data = {
            "text": patent_text,
            "ai_model": "AI01",
            "task": "drug_ddt_extraction"
        }
        
        logger.info("使用AI01提取药物DDT信息...")
        
        result = self._make_api_request("/api/v1/ai/extract", "POST", data=data)
        
        return result
    
    def search_similar_patents(
        self,
        reference_patent_id: str,
        similarity_threshold: float = 0.7,
        max_results: int = 50
    ) -> List[Dict]:
        """
        搜索相似专利
        
        Args:
            reference_patent_id: 参考专利ID
            similarity_threshold: 相似度阈值
            max_results: 最大结果数
        
        Returns:
            List[Dict]: 相似专利列表
        """
        params = {
            "reference_patent": reference_patent_id,
            "threshold": similarity_threshold,
            "limit": max_results
        }
        
        logger.info(f"搜索相似专利: {reference_patent_id}")
        
        result = self._make_api_request("/api/v1/patents/similar", "GET", params)
        
        return result.get("similar_patents", [])
    
    def get_patent_citations(self, patent_id: str) -> Dict[str, Any]:
        """
        获取专利引用关系
        
        Args:
            patent_id: 专利ID
        
        Returns:
            Dict: 引用关系数据
        """
        logger.info(f"获取专利引用关系: {patent_id}")
        
        result = self._make_api_request(f"/api/v1/patents/{patent_id}/citations")
        
        return result
    
    def analyze_patent_landscape(
        self,
        technology_field: str,
        date_range: Tuple[str, str] = None,
        geographical_scope: List[str] = None
    ) -> Dict[str, Any]:
        """
        分析专利技术地图
        
        Args:
            technology_field: 技术领域
            date_range: 日期范围 (start_date, end_date)
            geographical_scope: 地理范围 ['CN', 'US', 'EP']
        
        Returns:
            Dict: 技术地图分析结果
        """
        params = {
            "field": technology_field
        }
        
        if date_range:
            params["start_date"] = date_range[0]
            params["end_date"] = date_range[1]
        
        if geographical_scope:
            params["countries"] = ",".join(geographical_scope)
        
        logger.info(f"分析专利技术地图: {technology_field}")
        
        result = self._make_api_request("/api/v1/analytics/landscape", "GET", params)
        
        return result
    
    def get_patent_trends(
        self,
        technology_keywords: List[str],
        years: int = 5
    ) -> Dict[str, Any]:
        """
        获取专利技术趋势
        
        Args:
            technology_keywords: 技术关键词列表
            years: 分析年数
        
        Returns:
            Dict: 趋势分析结果
        """
        params = {
            "keywords": ",".join(technology_keywords),
            "years": years
        }
        
        logger.info(f"获取专利技术趋势: {technology_keywords}")
        
        result = self._make_api_request("/api/v1/analytics/trends", "GET", params)
        
        return result
    
    def validate_patent_novelty(
        self,
        patent_content: str,
        search_scope: str = "global"
    ) -> Dict[str, Any]:
        """
        验证专利新颖性
        
        Args:
            patent_content: 专利内容
            search_scope: 搜索范围 'global'/'china'/'us'/'europe'
        
        Returns:
            Dict: 新颖性验证结果
        """
        data = {
            "content": patent_content,
            "scope": search_scope,
            "task": "novelty_validation"
        }
        
        logger.info("验证专利新颖性...")
        
        result = self._make_api_request("/api/v1/validation/novelty", "POST", data=data)
        
        return result
    
    def assess_patent_value(self, patent_id: str) -> Dict[str, Any]:
        """
        评估专利价值
        
        Args:
            patent_id: 专利ID
        
        Returns:
            Dict: 价值评估结果
        """
        logger.info(f"评估专利价值: {patent_id}")
        
        result = self._make_api_request(f"/api/v1/valuation/{patent_id}")
        
        return result
    
    def get_api_usage_stats(self) -> Dict[str, Any]:
        """获取API使用统计"""
        return {
            "total_calls": self.api_calls_count,
            "last_call_time": self.last_call_time,
            "rate_limit_delay": self.rate_limit_delay,
            "token_expires_at": self.token_expires_at.isoformat() if self.token_expires_at else None
        }


# 便捷函数
def search_patents_zhihuiya(keywords: str, **kwargs) -> Dict[str, Any]:
    """
    便捷的智慧芽专利搜索函数
    
    Args:
        keywords: 搜索关键词
        **kwargs: 其他参数
    
    Returns:
        Dict: 搜索结果
    """
    try:
        api = ZhiHuiYaAPI()
        return api.search_patents(keywords, **kwargs)
    except Exception as e:
        logger.error(f"智慧芽专利搜索失败: {str(e)}")
        return {"error": str(e), "results": []}


def analyze_patent_with_ai(patent_text: str, analysis_type: str = "core_invention") -> Dict[str, Any]:
    """
    使用智慧芽AI分析专利
    
    Args:
        patent_text: 专利文本
        analysis_type: 分析类型 'core_invention'/'feasibility'/'ddt_extraction'
    
    Returns:
        Dict: 分析结果
    """
    try:
        api = ZhiHuiYaAPI()
        
        if analysis_type == "core_invention":
            return api.extract_patent_core_invention(patent_text)
        elif analysis_type == "feasibility":
            return api.analyze_patent_feasibility(patent_text)
        elif analysis_type == "ddt_extraction":
            return api.extract_drug_ddt_info(patent_text)
        else:
            return {"error": f"不支持的分析类型: {analysis_type}"}
            
    except Exception as e:
        logger.error(f"智慧芽AI分析失败: {str(e)}")
        return {"error": str(e)}


def compare_patents_similarity(patent_a: str, patent_b: str) -> Dict[str, Any]:
    """
    比较两个专利的相似度
    
    Args:
        patent_a: 专利A内容
        patent_b: 专利B内容
    
    Returns:
        Dict: 相似度分析结果
    """
    try:
        api = ZhiHuiYaAPI()
        return api.compare_patent_similarity(patent_a, patent_b)
    except Exception as e:
        logger.error(f"专利相似度比较失败: {str(e)}")
        return {"error": str(e)}


def translate_patent_document(text: str, target_language: str = "zh") -> Dict[str, Any]:
    """
    翻译专利文档
    
    Args:
        text: 要翻译的文本
        target_language: 目标语言
    
    Returns:
        Dict: 翻译结果
    """
    try:
        api = ZhiHuiYaAPI()
        return api.translate_patent_text(text, target_language)
    except Exception as e:
        logger.error(f"专利文档翻译失败: {str(e)}")
        return {"error": str(e)}


def validate_patent_novelty(patent_content: str) -> Dict[str, Any]:
    """
    验证专利新颖性
    
    Args:
        patent_content: 专利内容
    
    Returns:
        Dict: 新颖性验证结果
    """
    try:
        api = ZhiHuiYaAPI()
        return api.validate_patent_novelty(patent_content)
    except Exception as e:
        logger.error(f"专利新颖性验证失败: {str(e)}")
        return {"error": str(e)}


# 测试函数
def test_zhihuiya_api():
    """测试智慧芽API功能"""
    print("🧪 测试智慧芽API...")
    
    try:
        # 测试基本搜索
        results = search_patents_zhihuiya("人工智能", page_size=5)
        print(f"✅ 基本搜索测试: {results.get('total', 0)} 个结果")
        
        # 测试AI分析
        test_text = "一种基于深度学习的图像识别方法"
        ai_result = analyze_patent_with_ai(test_text, "core_invention")
        print(f"✅ AI分析测试: {ai_result.get('status', 'N/A')}")
        
        # 测试翻译
        translation_result = translate_patent_document("artificial intelligence", "zh")
        print(f"✅ 翻译测试: {translation_result.get('status', 'N/A')}")
        
        print("🎉 智慧芽API测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    test_zhihuiya_api() 