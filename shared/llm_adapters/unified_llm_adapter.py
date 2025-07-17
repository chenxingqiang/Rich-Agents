"""
Rich-Agents 统一LLM适配器
支持OpenAI、DashScope、Google、Anthropic等多个LLM提供商
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMAdapterInterface(ABC):
    """LLM适配器接口"""
    
    @abstractmethod
    def invoke(self, messages: Union[str, List[Dict[str, str]]], **kwargs) -> str:
        """调用LLM"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """获取模型名称"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """获取提供商名称"""
        pass


class UnifiedLLMAdapter:
    """
    统一LLM适配器
    支持多个LLM提供商的统一接口
    """
    
    def __init__(self, provider: str, model: str, api_key: Optional[str] = None, **kwargs):
        """
        初始化统一LLM适配器
        
        Args:
            provider: LLM提供商名称 ('openai', 'dashscope', 'google', 'anthropic')
            model: 模型名称
            api_key: API密钥，如果不提供则从环境变量获取
            **kwargs: 其他参数
        """
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key
        self.kwargs = kwargs
        
        # 如果没有提供API密钥，尝试从环境变量获取
        if not self.api_key:
            self.api_key = self._get_api_key_from_env()
        
        if not self.api_key:
            raise ValueError(f"未找到{provider}的API密钥")
        
        # 创建底层适配器
        self.adapter = self._create_adapter()
        
        logger.info(f"初始化LLM适配器: {provider}/{model}")
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """从环境变量获取API密钥"""
        env_map = {
            "openai": "OPENAI_API_KEY",
            "dashscope": "DASHSCOPE_API_KEY",
            "google": "GOOGLE_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY"
        }
        
        env_var = env_map.get(self.provider)
        if env_var:
            return os.getenv(env_var)
        return None
    
    def _get_available_models(self) -> Dict[str, List[str]]:
        """获取可用模型列表"""
        models = {}
        
        # 检查各个提供商的API密钥
        if os.getenv("DASHSCOPE_API_KEY"):
            models["dashscope"] = ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"]
        
        if os.getenv("OPENAI_API_KEY"):
            models["openai"] = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"]
        
        if os.getenv("GOOGLE_API_KEY"):
            models["google"] = ["gemini-pro", "gemini-pro-vision", "gemini-2.0-flash", "gemini-1.5-pro"]
        
        if os.getenv("ANTHROPIC_API_KEY"):
            models["anthropic"] = ["claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet", "claude-3-opus"]
        
        if os.getenv("DEEPSEEK_API_KEY"):
            models["deepseek"] = ["deepseek-chat", "deepseek-coder", "deepseek-reasoner"]
        
        if os.getenv("QIANWEN_API_KEY"):
            models["qianwen"] = ["qwen2.5-72b-instruct", "qwen2.5-32b-instruct", "qwen2.5-14b-instruct", "qwen2.5-7b-instruct"]
        
        if os.getenv("DOUBAO_API_KEY"):
            models["doubao"] = ["doubao-pro-32k", "doubao-pro-4k", "doubao-lite-32k", "doubao-lite-4k"]
        
        if os.getenv("ZHIPUAI_API_KEY"):
            models["zhipuai"] = ["glm-4", "glm-4-plus", "glm-4-0520", "glm-4-air", "glm-4-airx", "glm-4-flash"]
        
        if os.getenv("BAICHUAN_API_KEY"):
            models["baichuan"] = ["baichuan2-turbo", "baichuan2-turbo-192k", "baichuan3-turbo", "baichuan3-turbo-128k"]
        
        if os.getenv("MOONSHOT_API_KEY"):
            models["moonshot"] = ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
        
        if os.getenv("MINIMAX_API_KEY"):
            models["minimax"] = ["abab6.5s-chat", "abab6.5-chat", "abab5.5s-chat", "abab5.5-chat"]
        
        if os.getenv("YI_API_KEY"):
            models["yi"] = ["yi-34b-chat-0205", "yi-34b-chat-200k", "yi-6b-chat", "yi-large"]
        
        if os.getenv("STEPFUN_API_KEY"):
            models["stepfun"] = ["step-1v-8k", "step-1v-32k", "step-2-16k"]
        
        return models
    
    def _create_adapter(self):
        """根据提供商创建相应的适配器"""
        try:
            if self.provider == "dashscope":
                from langchain_community.llms import Tongyi
                self.llm = Tongyi(
                    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
                    model_name=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096)
                )
            elif self.provider == "openai":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    openai_api_key=os.getenv("OPENAI_API_KEY"),
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "google":
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_output_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                self.llm = ChatAnthropic(
                    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "deepseek":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("DEEPSEEK_API_KEY"),
                    base_url="https://api.deepseek.com",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "qianwen":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("QIANWEN_API_KEY"),
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "doubao":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("DOUBAO_API_KEY"),
                    base_url="https://ark.cn-beijing.volces.com/api/v3",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "zhipuai":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("ZHIPUAI_API_KEY"),
                    base_url="https://open.bigmodel.cn/api/paas/v4",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "baichuan":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("BAICHUAN_API_KEY"),
                    base_url="https://api.baichuan-ai.com/v1",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "moonshot":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("MOONSHOT_API_KEY"),
                    base_url="https://api.moonshot.cn/v1",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "minimax":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("MINIMAX_API_KEY"),
                    base_url="https://api.minimax.chat/v1",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "yi":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("YI_API_KEY"),
                    base_url="https://api.lingyiwanwu.com/v1",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            elif self.provider == "stepfun":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=os.getenv("STEPFUN_API_KEY"),
                    base_url="https://api.stepfun.com/v1",
                    model=self.model,
                    temperature=self.kwargs.get("temperature", 0.7),
                    max_tokens=self.kwargs.get("max_tokens", 4096),
                    **{k: v for k, v in self.kwargs.items() if k not in ["temperature", "max_tokens"]}
                )
            else:
                raise ValueError(f"不支持的LLM提供商: {self.provider}")
                
            logger.info(f"成功创建{self.provider}适配器，模型: {self.model}")
            
        except Exception as e:
            logger.error(f"创建{self.provider}适配器失败: {str(e)}")
            raise
    
    def invoke(self, messages: Union[str, List[Dict[str, str]]], **kwargs) -> str:
        """
        统一调用接口
        
        Args:
            messages: 消息内容，可以是字符串或消息列表
            **kwargs: 其他参数
            
        Returns:
            LLM响应字符串
        """
        try:
            # 统一消息格式
            if isinstance(messages, str):
                if self.provider == "dashscope":
                    # DashScope可能需要特殊处理
                    response = self.adapter.invoke(messages, **kwargs)
                else:
                    from langchain_core.messages import HumanMessage
                    formatted_messages = [HumanMessage(content=messages)]
                    response = self.adapter.invoke(formatted_messages, **kwargs)
            else:
                # 假设是标准的消息格式
                if self.provider == "dashscope":
                    # 转换为字符串格式
                    content = ""
                    for msg in messages:
                        if isinstance(msg, dict) and "content" in msg:
                            content += msg["content"] + "\n"
                        else:
                            content += str(msg) + "\n"
                    response = self.adapter.invoke(content.strip(), **kwargs)
                else:
                    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
                    
                    formatted_messages = []
                    for msg in messages:
                        if isinstance(msg, dict):
                            role = msg.get("role", "user")
                            content = msg.get("content", "")
                            
                            if role == "system":
                                formatted_messages.append(SystemMessage(content=content))
                            elif role == "assistant":
                                formatted_messages.append(AIMessage(content=content))
                            else:  # user or default
                                formatted_messages.append(HumanMessage(content=content))
                        else:
                            formatted_messages.append(HumanMessage(content=str(msg)))
                    
                    response = self.adapter.invoke(formatted_messages, **kwargs)
            
            # 提取响应内容
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"LLM调用失败 ({self.provider}/{self.model}): {str(e)}")
            raise Exception(f"LLM调用失败: {str(e)}")
    
    def get_model_name(self) -> str:
        """获取模型名称"""
        return self.model
    
    def get_provider_name(self) -> str:
        """获取提供商名称"""
        return self.provider
    
    def get_adapter_info(self) -> Dict[str, Any]:
        """获取适配器信息"""
        return {
            "provider": self.provider,
            "model": self.model,
            "api_key_configured": self.api_key is not None and len(self.api_key) > 0,
            "adapter_type": type(self.adapter).__name__,
            "kwargs": self.kwargs
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """测试连接"""
        try:
            test_message = "Hello, this is a test message."
            response = self.invoke(test_message)
            
            return {
                "success": True,
                "response_length": len(response),
                "response_preview": response[:100] + "..." if len(response) > 100 else response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @classmethod
    def create_from_config(cls, config: Dict[str, Any]) -> 'UnifiedLLMAdapter':
        """
        从配置创建适配器
        
        Args:
            config: 配置字典，包含provider、model、api_key等信息
            
        Returns:
            UnifiedLLMAdapter实例
        """
        provider = config.get("provider")
        model = config.get("model")
        api_key = config.get("api_key")
        
        if not provider or not model:
            raise ValueError("配置中必须包含provider和model")
        
        # 提取其他参数
        kwargs = {k: v for k, v in config.items() if k not in ["provider", "model", "api_key"]}
        
        return cls(provider=provider, model=model, api_key=api_key, **kwargs)
    
    @staticmethod
    def get_supported_providers() -> List[str]:
        """获取支持的提供商列表"""
        return ["openai", "dashscope", "google", "anthropic"]
    
    @staticmethod
    def validate_provider_config(provider: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证提供商配置
        
        Args:
            provider: 提供商名称
            config: 配置字典
            
        Returns:
            验证结果
        """
        result = {"valid": True, "errors": [], "warnings": []}
        
        if provider not in UnifiedLLMAdapter.get_supported_providers():
            result["valid"] = False
            result["errors"].append(f"不支持的提供商: {provider}")
            return result
        
        # 检查必需字段
        required_fields = ["model"]
        for field in required_fields:
            if field not in config:
                result["valid"] = False
                result["errors"].append(f"缺少必需字段: {field}")
        
        # 检查API密钥
        api_key = config.get("api_key")
        if not api_key:
            # 尝试从环境变量获取
            env_map = {
                "openai": "OPENAI_API_KEY",
                "dashscope": "DASHSCOPE_API_KEY", 
                "google": "GOOGLE_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY"
            }
            env_var = env_map.get(provider)
            if not env_var or not os.getenv(env_var):
                result["warnings"].append(f"未配置API密钥，请设置环境变量{env_var}")
        
        return result


class LLMAdapterFactory:
    """LLM适配器工厂类"""
    
    @staticmethod
    def create_adapter(provider: str, model: str, api_key: Optional[str] = None, **kwargs) -> UnifiedLLMAdapter:
        """
        创建LLM适配器
        
        Args:
            provider: 提供商名称
            model: 模型名称
            api_key: API密钥
            **kwargs: 其他参数
            
        Returns:
            UnifiedLLMAdapter实例
        """
        return UnifiedLLMAdapter(provider=provider, model=model, api_key=api_key, **kwargs)
    
    @staticmethod
    def create_from_config(config: Dict[str, Any]) -> UnifiedLLMAdapter:
        """从配置创建适配器"""
        return UnifiedLLMAdapter.create_from_config(config)
    
    @staticmethod
    def create_multiple_adapters(configs: List[Dict[str, Any]]) -> List[UnifiedLLMAdapter]:
        """
        创建多个LLM适配器
        
        Args:
            configs: 配置列表
            
        Returns:
            适配器列表
        """
        adapters = []
        for config in configs:
            try:
                adapter = UnifiedLLMAdapter.create_from_config(config)
                adapters.append(adapter)
            except Exception as e:
                logger.error(f"创建适配器失败: {str(e)}")
                continue
        
        return adapters
    
    @staticmethod
    def test_all_adapters(configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        测试所有适配器
        
        Args:
            configs: 配置列表
            
        Returns:
            测试结果
        """
        results = {}
        
        for config in configs:
            try:
                adapter = UnifiedLLMAdapter.create_from_config(config)
                test_result = adapter.test_connection()
                results[f"{adapter.get_provider_name()}/{adapter.get_model_name()}"] = test_result
            except Exception as e:
                provider = config.get("provider", "unknown")
                model = config.get("model", "unknown")
                results[f"{provider}/{model}"] = {
                    "success": False,
                    "error": f"创建适配器失败: {str(e)}"
                }
        
        return results 