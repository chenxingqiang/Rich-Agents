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
                    "default_model": "qwen-turbo"
                },
                "openai": {
                    "api_key_env": "OPENAI_API_KEY",
                    "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o-mini"],
                    "default_model": "gpt-4o-mini"
                },
                "google": {
                    "api_key_env": "GOOGLE_API_KEY",
                    "models": ["gemini-pro", "gemini-pro-vision", "gemini-2.0-flash"],
                    "default_model": "gemini-2.0-flash"
                },
                "anthropic": {
                    "api_key_env": "ANTHROPIC_API_KEY",
                    "models": ["claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet"],
                    "default_model": "claude-3-5-sonnet"
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