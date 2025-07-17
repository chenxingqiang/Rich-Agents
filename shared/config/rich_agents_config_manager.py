"""
Rich-Agents 统一配置管理器
支持TradingAgent和PatentAgent两种模式的配置管理
"""

import os
import json
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class RichAgentsConfigManager:
    """Rich-Agents统一配置管理器"""
    
    def __init__(self, config_dir: Optional[Union[str, Path]] = None):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置文件目录，默认为项目根目录下的config文件夹
        """
        if config_dir is None:
            # 找到项目根目录
            current_dir = Path(__file__).resolve()
            while current_dir.parent != current_dir:
                if (current_dir / "pyproject.toml").exists() or (current_dir / "setup.py").exists():
                    break
                current_dir = current_dir.parent
            self.config_dir = current_dir / "config"
        else:
            self.config_dir = Path(config_dir)
        
        self.config_dir.mkdir(exist_ok=True)
        
        # 配置文件路径
        self.main_config_file = self.config_dir / "rich_agents_config.json"
        self.trading_config_file = self.config_dir / "trading_config.json" 
        self.patent_config_file = self.config_dir / "patent_config.json"
        
        # 加载配置
        self.main_config = self._load_config(self.main_config_file, self._get_default_main_config())
        self.trading_config = self._load_config(self.trading_config_file, self._get_default_trading_config())
        self.patent_config = self._load_config(self.patent_config_file, self._get_default_patent_config())
        
        logger.info("Rich-Agents配置管理器初始化完成")
    
    def _load_config(self, config_file: Path, default_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_file: 配置文件路径
            default_config: 默认配置
            
        Returns:
            配置字典
        """
        try:
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置确保完整性
                    merged_config = self._merge_configs(default_config, config)
                    logger.info(f"已加载配置文件: {config_file}")
                    return merged_config
            else:
                # 创建默认配置文件
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                logger.info(f"已创建默认配置文件: {config_file}")
                return default_config
        except Exception as e:
            logger.error(f"加载配置文件失败 {config_file}: {str(e)}")
            return default_config
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并用户配置和默认配置
        
        Args:
            default: 默认配置
            user: 用户配置
            
        Returns:
            合并后的配置
        """
        merged = default.copy()
        
        def _deep_merge(target: Dict[str, Any], source: Dict[str, Any]):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    _deep_merge(target[key], value)
                else:
                    target[key] = value
        
        _deep_merge(merged, user)
        return merged
    
    def _get_default_main_config(self) -> Dict[str, Any]:
        """获取主配置默认值"""
        return {
            "version": "0.1.0",
            "name": "Rich-Agents",
            "description": "多智能体AI工具集",
            "default_agent": "trading",  # trading 或 patent
            "llm_providers": {
                "dashscope": {
                    "api_key_env": "DASHSCOPE_API_KEY",
                    "models": ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"],
                    "default_model": "qwen-turbo",
                    "description": "阿里云百炼大模型"
                },
                "openai": {
                    "api_key_env": "OPENAI_API_KEY",
                    "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"],
                    "default_model": "gpt-4o-mini",
                    "description": "OpenAI GPT模型"
                },
                "google": {
                    "api_key_env": "GOOGLE_API_KEY",
                    "models": ["gemini-pro", "gemini-pro-vision", "gemini-2.0-flash", "gemini-1.5-pro"],
                    "default_model": "gemini-2.0-flash",
                    "description": "Google Gemini模型"
                },
                "anthropic": {
                    "api_key_env": "ANTHROPIC_API_KEY",
                    "models": ["claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet", "claude-3-opus"],
                    "default_model": "claude-3-5-sonnet",
                    "description": "Anthropic Claude模型"
                },
                "deepseek": {
                    "api_key_env": "DEEPSEEK_API_KEY",
                    "models": ["deepseek-chat", "deepseek-coder", "deepseek-reasoner"],
                    "default_model": "deepseek-chat",
                    "description": "DeepSeek深度求索模型",
                    "base_url": "https://api.deepseek.com"
                },
                "qianwen": {
                    "api_key_env": "QIANWEN_API_KEY",
                    "models": ["qwen2.5-72b-instruct", "qwen2.5-32b-instruct", "qwen2.5-14b-instruct", "qwen2.5-7b-instruct"],
                    "default_model": "qwen2.5-72b-instruct",
                    "description": "通义千问开源模型",
                    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
                },
                "doubao": {
                    "api_key_env": "DOUBAO_API_KEY",
                    "models": ["doubao-pro-32k", "doubao-pro-4k", "doubao-lite-32k", "doubao-lite-4k"],
                    "default_model": "doubao-pro-32k",
                    "description": "火山引擎豆包模型",
                    "base_url": "https://ark.cn-beijing.volces.com/api/v3"
                },
                "zhipuai": {
                    "api_key_env": "ZHIPUAI_API_KEY",
                    "models": ["glm-4", "glm-4-plus", "glm-4-0520", "glm-4-air", "glm-4-airx", "glm-4-flash"],
                    "default_model": "glm-4",
                    "description": "智谱AI GLM模型",
                    "base_url": "https://open.bigmodel.cn/api/paas/v4"
                },
                "baichuan": {
                    "api_key_env": "BAICHUAN_API_KEY",
                    "models": ["baichuan2-turbo", "baichuan2-turbo-192k", "baichuan3-turbo", "baichuan3-turbo-128k"],
                    "default_model": "baichuan3-turbo",
                    "description": "百川智能模型",
                    "base_url": "https://api.baichuan-ai.com/v1"
                },
                "moonshot": {
                    "api_key_env": "MOONSHOT_API_KEY",
                    "models": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
                    "default_model": "moonshot-v1-8k",
                    "description": "Moonshot AI Kimi模型",
                    "base_url": "https://api.moonshot.cn/v1"
                },
                "minimax": {
                    "api_key_env": "MINIMAX_API_KEY",
                    "models": ["abab6.5s-chat", "abab6.5-chat", "abab5.5s-chat", "abab5.5-chat"],
                    "default_model": "abab6.5s-chat",
                    "description": "MiniMax海螺模型",
                    "base_url": "https://api.minimax.chat/v1"
                },
                "yi": {
                    "api_key_env": "YI_API_KEY",
                    "models": ["yi-34b-chat-0205", "yi-34b-chat-200k", "yi-6b-chat", "yi-large"],
                    "default_model": "yi-large",
                    "description": "零一万物Yi模型",
                    "base_url": "https://api.lingyiwanwu.com/v1"
                },
                "stepfun": {
                    "api_key_env": "STEPFUN_API_KEY",
                    "models": ["step-1v-8k", "step-1v-32k", "step-2-16k"],
                    "default_model": "step-1v-8k",
                    "description": "阶跃星辰Step模型",
                    "base_url": "https://api.stepfun.com/v1"
                }
            },
            "cache": {
                "enabled": True,
                "type": "integrated",  # file, mongodb, redis, integrated
                "file_cache_dir": "cache",
                "mongodb": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 27017,
                    "database": "rich_agents",
                    "username": None,
                    "password": None
                },
                "redis": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 6379,
                    "db": 0,
                    "password": None
                }
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "rich_agents.log"
            }
        }
    
    def _get_default_trading_config(self) -> Dict[str, Any]:
        """获取TradingAgent默认配置"""
        return {
            "agent_type": "trading",
            "max_debate_rounds": 2,
            "max_risk_discuss_rounds": 2,
            "online_tools": True,
            "analysts": ["market", "social", "news", "fundamentals"],
            "research_depth": 2,
            "markets": {
                "us_stock": {
                    "enabled": True,
                    "data_source": "yahoo_finance",
                    "api_keys": {
                        "finnhub": "FINNHUB_API_KEY"
                    }
                },
                "china_a_share": {
                    "enabled": True,
                    "data_source": "tongdaxin",
                    "fallback": ["akshare", "tushare"]
                }
            },
            "risk_management": {
                "enabled": True,
                "max_position_size": 0.1,
                "stop_loss": 0.05,
                "take_profit": 0.15
            }
        }
    
    def _get_default_patent_config(self) -> Dict[str, Any]:
        """获取PatentAgent默认配置"""
        return {
            "agent_type": "patent",
            "analysis_types": ["discovery", "validation", "analysis", "writing"],
            "default_analysis_type": "discovery",
            "api_keys": {
                "google_patents": "SERPAPI_API_KEY",
                "zhihuiya": {
                    "client_id": "ZHIHUIYA_CLIENT_ID",
                    "client_secret": "ZHIHUIYA_CLIENT_SECRET"
                }
            },
            "agents": {
                "technology_analyst": {"enabled": True},
                "innovation_discovery": {"enabled": True},
                "prior_art_researcher": {"enabled": True},
                "market_intelligence": {"enabled": True},
                "patent_writer": {"enabled": True},
                "quality_assessor": {"enabled": True}
            },
            "patent_databases": {
                "google_patents": {
                    "enabled": True,
                    "max_results": 100,
                    "priority": 1
                },
                "zhihuiya": {
                    "enabled": True,
                    "max_results": 50,
                    "priority": 2
                },
                "uspto": {
                    "enabled": False,
                    "max_results": 50,
                    "priority": 3
                },
                "epo": {
                    "enabled": False,
                    "max_results": 50,
                    "priority": 4
                }
            }
        }
    
    def get_config(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """
        获取指定智能体类型的完整配置
        
        Args:
            agent_type: 智能体类型 ('trading' 或 'patent')，默认使用配置中的默认类型
            
        Returns:
            完整配置字典
        """
        if agent_type is None:
            agent_type = self.main_config.get("default_agent", "trading")
        
        if agent_type == "trading":
            return self.get_trading_config()
        elif agent_type == "patent":
            return self.get_patent_config()
        else:
            raise ValueError(f"不支持的智能体类型: {agent_type}")
    
    def get_trading_config(self) -> Dict[str, Any]:
        """获取TradingAgent完整配置"""
        config = self.main_config.copy()
        config.update(self.trading_config)
        return config
    
    def get_patent_config(self) -> Dict[str, Any]:
        """获取PatentAgent完整配置"""
        config = self.main_config.copy()
        config.update(self.patent_config)
        return config
    
    def get_llm_config(self, provider: str) -> Dict[str, Any]:
        """
        获取指定LLM提供商的配置
        
        Args:
            provider: LLM提供商名称
            
        Returns:
            LLM配置字典
        """
        llm_providers = self.main_config.get("llm_providers", {})
        if provider not in llm_providers:
            raise ValueError(f"不支持的LLM提供商: {provider}")
        
        return llm_providers[provider]
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        获取指定提供商的API密钥
        
        Args:
            provider: 提供商名称
            
        Returns:
            API密钥或None
        """
        try:
            if provider in self.main_config.get("llm_providers", {}):
                env_var = self.main_config["llm_providers"][provider]["api_key_env"]
                return os.getenv(env_var)
            elif provider == "finnhub":
                return os.getenv("FINNHUB_API_KEY")
            elif provider == "serpapi":
                return os.getenv("SERPAPI_API_KEY")
            elif provider == "zhihuiya_client_id":
                return os.getenv("ZHIHUIYA_CLIENT_ID")
            elif provider == "zhihuiya_client_secret":
                return os.getenv("ZHIHUIYA_CLIENT_SECRET")
            else:
                return None
        except Exception as e:
            logger.error(f"获取API密钥失败 {provider}: {str(e)}")
            return None
    
    def check_api_keys(self, agent_type: Optional[str] = None) -> Dict[str, bool]:
        """
        检查API密钥配置状态
        
        Args:
            agent_type: 智能体类型
            
        Returns:
            API密钥状态字典
        """
        status = {}
        
        # 检查LLM提供商API密钥
        for provider in self.main_config.get("llm_providers", {}):
            api_key = self.get_api_key(provider)
            status[f"{provider}_api"] = api_key is not None and len(api_key.strip()) > 0
        
        # 根据智能体类型检查特定API密钥
        if agent_type is None:
            agent_type = self.main_config.get("default_agent", "trading")
        
        if agent_type == "trading":
            status["finnhub_api"] = self.get_api_key("finnhub") is not None
        elif agent_type == "patent":
            status["serpapi_api"] = self.get_api_key("serpapi") is not None
            status["zhihuiya_client_id"] = self.get_api_key("zhihuiya_client_id") is not None
            status["zhihuiya_client_secret"] = self.get_api_key("zhihuiya_client_secret") is not None
        
        return status
    
    def update_config(self, agent_type: str, config_updates: Dict[str, Any]) -> bool:
        """
        更新配置
        
        Args:
            agent_type: 智能体类型
            config_updates: 配置更新
            
        Returns:
            更新是否成功
        """
        try:
            if agent_type == "main":
                self.main_config.update(config_updates)
                self._save_config(self.main_config_file, self.main_config)
            elif agent_type == "trading":
                self.trading_config.update(config_updates)
                self._save_config(self.trading_config_file, self.trading_config)
            elif agent_type == "patent":
                self.patent_config.update(config_updates)
                self._save_config(self.patent_config_file, self.patent_config)
            else:
                raise ValueError(f"不支持的配置类型: {agent_type}")
            
            logger.info(f"配置更新成功: {agent_type}")
            return True
        except Exception as e:
            logger.error(f"配置更新失败 {agent_type}: {str(e)}")
            return False
    
    def _save_config(self, config_file: Path, config: Dict[str, Any]) -> None:
        """保存配置到文件"""
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_available_llm_providers(self) -> List[str]:
        """获取可用的LLM提供商列表"""
        return list(self.main_config.get("llm_providers", {}).keys())
    
    def get_available_models(self, provider: str) -> List[str]:
        """
        获取指定提供商的可用模型列表
        
        Args:
            provider: LLM提供商名称
            
        Returns:
            模型列表
        """
        llm_config = self.get_llm_config(provider)
        return llm_config.get("models", [])
    
    def get_default_model(self, provider: str) -> str:
        """
        获取指定提供商的默认模型
        
        Args:
            provider: LLM提供商名称
            
        Returns:
            默认模型名称
        """
        llm_config = self.get_llm_config(provider)
        return llm_config.get("default_model", llm_config.get("models", [""])[0])
    
    def validate_config(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """
        验证配置完整性
        
        Args:
            agent_type: 智能体类型
            
        Returns:
            验证结果
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "api_keys": self.check_api_keys(agent_type)
        }
        
        # 检查必需的API密钥
        api_status = result["api_keys"]
        missing_keys = [key for key, status in api_status.items() if not status]
        
        if missing_keys:
            result["warnings"].extend([f"缺少API密钥: {key}" for key in missing_keys])
        
        # 检查LLM提供商配置
        available_providers = self.get_available_llm_providers()
        if not available_providers:
            result["valid"] = False
            result["errors"].append("没有配置任何LLM提供商")
        
        # 检查至少有一个LLM提供商的API密钥可用
        llm_keys_available = any(api_status.get(f"{provider}_api", False) for provider in available_providers)
        if not llm_keys_available:
            result["valid"] = False
            result["errors"].append("没有可用的LLM API密钥")
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        获取系统状态
        
        Returns:
            系统状态信息
        """
        return {
            "config_loaded": True,
            "config_files": {
                "main_config": str(self.main_config_file),
                "trading_config": str(self.trading_config_file),
                "patent_config": str(self.patent_config_file)
            },
            "available_agents": ["trading", "patent"],
            "available_llm_providers": self.get_available_llm_providers(),
            "api_keys_status": self.check_api_keys(),
            "cache_config": self.main_config.get("cache", {}),
            "version": self.main_config.get("version", "unknown")
        }
    
    def set_api_key(self, env_var: str, api_key: str) -> bool:
        """
        设置API密钥
        
        Args:
            env_var: 环境变量名
            api_key: API密钥值
            
        Returns:
            设置是否成功
        """
        try:
            # 设置环境变量
            os.environ[env_var] = api_key
            
            # 可以选择保存到配置文件或.env文件
            # 这里我们只设置环境变量，不持久化到文件（安全考虑）
            logger.info(f"API密钥已设置: {env_var}")
            return True
            
        except Exception as e:
            logger.error(f"设置API密钥失败 {env_var}: {str(e)}")
            return False
    
    def delete_api_key(self, env_var: str) -> bool:
        """
        删除API密钥
        
        Args:
            env_var: 环境变量名
            
        Returns:
            删除是否成功
        """
        try:
            # 从环境变量中删除
            if env_var in os.environ:
                del os.environ[env_var]
            
            logger.info(f"API密钥已删除: {env_var}")
            return True
            
        except Exception as e:
            logger.error(f"删除API密钥失败 {env_var}: {str(e)}")
            return False
    
    def test_api_key(self, env_var: str) -> Dict[str, Any]:
        """
        测试API密钥
        
        Args:
            env_var: 环境变量名
            
        Returns:
            测试结果
        """
        try:
            api_key = os.getenv(env_var)
            if not api_key:
                return {
                    "success": False,
                    "error": "API密钥未设置"
                }
            
            # 基本格式验证
            if len(api_key.strip()) < 5:
                return {
                    "success": False,
                    "error": "API密钥格式不正确"
                }
            
            # 这里可以添加实际的API测试调用
            # 由于不同API的测试方式不同，这里只做基本验证
            
            return {
                "success": True,
                "details": f"API密钥格式正确，长度: {len(api_key)}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_cache_config(self) -> Dict[str, Any]:
        """
        获取缓存配置
        
        Returns:
            缓存配置字典
        """
        return self.main_config.get("cache", {})
    
    def export_config(self, export_path: Optional[Union[str, Path]] = None) -> str:
        """
        导出配置到文件
        
        Args:
            export_path: 导出文件路径，默认为config目录下的exported_config.json
            
        Returns:
            导出文件路径
        """
        try:
            if export_path is None:
                export_path = self.config_dir / "exported_config.json"
            else:
                export_path = Path(export_path)
            
            # 准备导出的配置（不包含敏感信息）
            export_config = {
                "main_config": self._sanitize_config(self.main_config),
                "trading_config": self._sanitize_config(self.trading_config),
                "patent_config": self._sanitize_config(self.patent_config),
                "export_timestamp": self._get_timestamp(),
                "version": self.main_config.get("version", "unknown")
            }
            
            # 保存到文件
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"配置已导出到: {export_path}")
            return str(export_path)
            
        except Exception as e:
            logger.error(f"配置导出失败: {str(e)}")
            raise
    
    def _sanitize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        清理配置中的敏感信息
        
        Args:
            config: 原始配置
            
        Returns:
            清理后的配置
        """
        sanitized = config.copy()
        
        # 移除敏感字段
        sensitive_keys = ["password", "secret", "key", "token"]
        
        def _remove_sensitive(obj):
            if isinstance(obj, dict):
                return {
                    k: _remove_sensitive(v) if not any(sensitive in k.lower() for sensitive in sensitive_keys) 
                    else "***HIDDEN***"
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [_remove_sensitive(item) for item in obj]
            else:
                return obj
        
        return _remove_sensitive(sanitized)
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def reload_config(self) -> bool:
        """
        重新加载所有配置文件
        
        Returns:
            重新加载是否成功
        """
        try:
            self.main_config = self._load_config(self.main_config_file, self._get_default_main_config())
            self.trading_config = self._load_config(self.trading_config_file, self._get_default_trading_config())
            self.patent_config = self._load_config(self.patent_config_file, self._get_default_patent_config())
            
            logger.info("配置重新加载成功")
            return True
            
        except Exception as e:
            logger.error(f"配置重新加载失败: {str(e)}")
            return False
    
    def reset_config(self, config_type: str) -> bool:
        """
        重置配置为默认值
        
        Args:
            config_type: 配置类型 ('main', 'trading', 'patent')
            
        Returns:
            重置是否成功
        """
        try:
            if config_type == "main":
                self.main_config = self._get_default_main_config()
                self._save_config(self.main_config_file, self.main_config)
            elif config_type == "trading":
                self.trading_config = self._get_default_trading_config()
                self._save_config(self.trading_config_file, self.trading_config)
            elif config_type == "patent":
                self.patent_config = self._get_default_patent_config()
                self._save_config(self.patent_config_file, self.patent_config)
            else:
                raise ValueError(f"不支持的配置类型: {config_type}")
            
            logger.info(f"配置已重置为默认值: {config_type}")
            return True
            
        except Exception as e:
            logger.error(f"配置重置失败 {config_type}: {str(e)}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """
        获取配置摘要
        
        Returns:
            配置摘要信息
        """
        return {
            "total_configs": 3,
            "config_files": {
                "main": self.main_config_file.exists(),
                "trading": self.trading_config_file.exists(),
                "patent": self.patent_config_file.exists()
            },
            "llm_providers_count": len(self.get_available_llm_providers()),
            "api_keys_configured": sum(1 for status in self.check_api_keys().values() if status),
            "cache_enabled": self.main_config.get("cache", {}).get("enabled", False),
            "version": self.main_config.get("version", "unknown")
        } 

    def _validate_api_key_format(self, env_var: str, key: str) -> bool:
        """验证API密钥格式"""
        validation_rules = {
            "DASHSCOPE_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
            "OPENAI_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
            "GOOGLE_API_KEY": lambda k: k.startswith("AIza") and len(k) > 30,
            "ANTHROPIC_API_KEY": lambda k: k.startswith("sk-ant-") and len(k) > 30,
            "DEEPSEEK_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
            "QIANWEN_API_KEY": lambda k: len(k) > 10,  # 通义千问API密钥格式可能不同
            "DOUBAO_API_KEY": lambda k: len(k) > 20,  # 火山引擎豆包API密钥
            "ZHIPUAI_API_KEY": lambda k: len(k) > 30,  # 智谱AI API密钥通常较长
            "BAICHUAN_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
            "MOONSHOT_API_KEY": lambda k: k.startswith("sk-") and len(k) > 30,
            "MINIMAX_API_KEY": lambda k: len(k) > 20,  # MiniMax API密钥
            "YI_API_KEY": lambda k: len(k) > 20,  # 零一万物API密钥
            "STEPFUN_API_KEY": lambda k: len(k) > 20,  # 阶跃星辰API密钥
            "FINNHUB_API_KEY": lambda k: len(k) > 10,
            "SERPAPI_API_KEY": lambda k: len(k) > 10,
            "ZHIHUIYA_CLIENT_ID": lambda k: len(k) > 5,
            "ZHIHUIYA_CLIENT_SECRET": lambda k: len(k) > 10
        }
        
        validator = validation_rules.get(env_var)
        if validator:
            return validator(key)
        return len(key) > 5  # 默认最小长度验证 