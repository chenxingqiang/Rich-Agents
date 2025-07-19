# Rich-Agents Quick Reference Card

## 🚀 Quick Start

### 1. Change LLM Provider
```bash
# Interactive configuration
rich-agents config

# Select from 13+ providers:
# 1. DashScope (Alibaba Cloud) - Chinese-optimized
# 2. OpenAI - Industry standard
# 3. Google AI - Multimodal capabilities
# 4. Anthropic - Analytical depth
# 5. Baichuan Intelligence - Long context
# 6. Moonshot AI - Ultra-long context
# 7. 01.AI Yi - Multimodal
# 8. Zhipu AI GLM - Fast inference
# 9. StepFun Step - Step-by-step reasoning
# 10. MiniMax Hailuo - Conversational AI
# 11. Bytedance Doubao - Enterprise-grade
# 12. DeepSeek - Code generation
# 13. DeepSeek (International) - Code analysis
```

### 2. Launch Rich-Agents
```bash
# Rich interactive CLI
rich-agents

# Simple CLI for automation
rich-agents-simple

# With specific configuration
rich-agents --provider dashscope --model qwen-plus --depth medium
```

### 3. Configure Enterprise Features
```bash
# Enable database caching
export MONGODB_ENABLED=true
export REDIS_ENABLED=true

# Test all configurations
rich-agents config --test-all
```

## 📁 Key File Locations

| Content to Modify | File Path | Specific Location |
|------------------|-----------|-------------------|
| **Unified Config** | `shared/config/rich_agents_config_manager.py` | Main configuration management |
| **CLI Interface** | `cli/rich_agents_main.py` | Rich interactive CLI |
| **Simple CLI** | `cli/rich_agents_simple.py` | Automation-friendly CLI |
| **LLM Adapters** | `shared/llm_adapters/unified_llm_adapter.py` | Multi-provider LLM interface |
| **Cache Management** | `shared/cache/adaptive_cache.py` | Intelligent caching system |
| **Database Config** | `shared/config/database_config.py` | MongoDB and Redis setup |
| **TradingAgents Config** | `tradingagents/default_config.py` | Trading-specific settings |
| **Market Analyst** | `tradingagents/agents/analysts/market_analyst.py` | Technical analysis prompts |
| **Fundamentals Analyst** | `tradingagents/agents/analysts/fundamentals_analyst.py` | Financial analysis prompts |
| **News Analyst** | `tradingagents/agents/analysts/news_analyst.py` | News sentiment analysis |
| **Bull Researcher** | `tradingagents/agents/researchers/bull_researcher.py` | Bullish analysis prompts |
| **Bear Researcher** | `tradingagents/agents/researchers/bear_researcher.py` | Bearish analysis prompts |
| **Trader Agent** | `tradingagents/agents/trader/trader.py` | Trading decision prompts |
| **Reflection System** | `tradingagents/graph/reflection.py` | Quality control prompts |

## 🎯 Common Modification Templates

### 1. Multi-Domain Prompt Template
```python
system_message = f"""
You are a professional {domain} {role_name} with the following characteristics:

🎯 Domain Context:
- Professional Area: {domain} ({domain_description})
- Expertise Level: {expertise_level}
- Analysis Scope: {analysis_scope}

📊 Core Responsibilities:
1. {responsibility_1}
2. {responsibility_2}
3. {responsibility_3}

🔍 Analysis Framework:
- Data Sources: {data_sources}
- Methodologies: {methodologies}
- Output Format: {output_format}

⚠️ Important Guidelines:
- Provide specific data support
- Avoid generic statements
- Include risk assessments
- Generate actionable insights

Please provide professional {domain} analysis based on these requirements.
"""
```

### 2. Multi-Provider Configuration Template
```python
provider_config = {
    "primary_provider": "dashscope",
    "fallback_providers": ["openai", "google", "anthropic"],
    "provider_preferences": {
        "chinese_content": ["dashscope", "baichuan", "moonshot"],
        "code_analysis": ["deepseek", "openai"],
        "long_context": ["moonshot", "baichuan", "yi"],
        "fast_inference": ["glm", "qwen-turbo", "gemini-flash"]
    },
    "intelligent_routing": True,
    "cost_optimization": True
}
```

### 3. Enterprise Database Template
```python
enterprise_config = {
    "mongodb": {
        "enabled": True,
        "host": "localhost",
        "port": 27017,
        "database": "rich_agents",
        "collections": {
            "trading_data": {"ttl_hours": 24},
            "patent_data": {"ttl_hours": 168},  # 1 week
            "analysis_results": {"ttl_hours": 72}
        }
    },
    "redis": {
        "enabled": True,
        "host": "localhost", 
        "port": 6379,
        "cache_strategies": {
            "realtime_data": {"ttl_seconds": 300},  # 5 minutes
            "historical_data": {"ttl_seconds": 3600},  # 1 hour
            "analysis_cache": {"ttl_seconds": 1800}   # 30 minutes
        }
    },
    "intelligent_cache": {
        "enabled": True,
        "fallback_chain": ["redis", "mongodb", "file_cache"],
        "adaptive_ttl": True
    }
}
```

## ⚙️ Configuration Parameters Quick Reference

### LLM Provider Configuration
```python
# 13+ LLM Providers
llm_providers = {
    "dashscope": "qwen-turbo|qwen-plus|qwen-max|qwen-max-longcontext",
    "openai": "gpt-4o|gpt-4o-mini|o1-preview|o1-mini|o3-mini", 
    "google": "gemini-2.0-flash|gemini-2.5-flash|gemini-2.5-pro",
    "anthropic": "claude-3.5-haiku|claude-3.5-sonnet|claude-4",
    "baichuan": "baichuan2-turbo|baichuan3-turbo|baichuan3-turbo-128k",
    "moonshot": "moonshot-v1-8k|moonshot-v1-32k|moonshot-v1-128k",
    "yi": "yi-34b-chat|yi-large|yi-vl-plus",
    "glm": "glm-4|glm-4-air|glm-4-flash",
    "step": "step-1v-8k|step-1v-32k|step-2-16k-nightly",
    "minimax": "abab6.5s-chat|abab6.5g-chat|abab6.5t-chat",
    "doubao": "doubao-lite-4k|doubao-pro-32k",
    "deepseek": "deepseek-chat|deepseek-coder|deepseek-reasoner"
}
```

### Domain-Specific Configuration
```python
domain_config = {
    "trading": {
        "markets": ["us_stock", "china_a_share"],
        "data_sources": ["yahoo_finance", "tongdaxin", "finnhub"],
        "analysis_types": ["technical", "fundamental", "sentiment"],
        "default_depth": "medium"
    },
    "patent": {  # Coming Soon
        "databases": ["uspto", "epo", "cnipa"],
        "analysis_types": ["prior_art", "innovation", "landscape"],
        "default_scope": "comprehensive"
    }
}
```

### API Provider Quick Setup
```env
# Chinese Providers
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
BAICHUAN_API_KEY=sk-xxxxxxxxxxxxxxxx
MOONSHOT_API_KEY=sk-xxxxxxxxxxxxxxxx
YI_API_KEY=sk-xxxxxxxxxxxxxxxx
GLM_API_KEY=xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx
STEP_API_KEY=sk-xxxxxxxxxxxxxxxx
MINIMAX_API_KEY=xxxxxxxxxxxxxxxx
DOUBAO_API_KEY=xxxxxxxxxxxxxxxx

# International Providers  
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
GOOGLE_API_KEY=xxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# Data Sources
FINNHUB_API_KEY=xxxxxxxxxxxxxxxx
ALPHA_VANTAGE_API_KEY=xxxxxxxxxxxxxxxx

# Enterprise Features
MONGODB_ENABLED=true
REDIS_ENABLED=true
```

## 🔧 Common Commands

### Configuration Management
```bash
# Interactive configuration
rich-agents config

# Configure specific provider
rich-agents config --provider dashscope

# Test API keys
rich-agents config --test-all
rich-agents config --test-provider openai

# Export/Import configuration
rich-agents config --export backup.json
rich-agents config --import backup.json

# Reset configuration
rich-agents config --reset
```

### Analysis Commands
```bash
# Single stock analysis
rich-agents --symbol AAPL --provider openai --depth medium

# Batch analysis
rich-agents batch --symbols "AAPL,TSLA,NVDA" --provider dashscope

# Market comparison
rich-agents compare --us-symbol AAPL --china-symbol 000001

# Custom configuration
rich-agents --config custom_config.json
```

### Database Management
```bash
# Check database status
rich-agents db --status

# Clear cache
rich-agents db --clear-cache

# Database statistics
rich-agents db --stats

# Backup data
rich-agents db --backup backup_file.json
```

### Development Commands
```bash
# Debug mode
RICH_AGENTS_LOG_LEVEL=DEBUG rich-agents

# Test mode
rich-agents --test-mode

# Performance profiling
rich-agents --profile

# Validate configuration
rich-agents --validate-config
```

## 🚨 Important Notes

### ⚠️ Must Do Before Modification
1. **Backup Configuration**: Always backup before changes
   ```bash
   rich-agents config --export backup_$(date +%Y%m%d).json
   ```

2. **Test Environment**: Validate in test environment first
3. **Version Control**: Track all configuration changes

### ⚠️ Common Issues and Solutions

#### API Key Issues
```bash
# Invalid format
Error: API key format invalid
Solution: Check provider-specific format requirements

# Rate limits
Error: Rate limit exceeded  
Solution: Configure multiple providers for fallback
```

#### Provider Availability
```bash
# Provider timeout
Error: Provider unavailable
Solution: System auto-fallback enabled, check network

# Model not found
Error: Model not supported
Solution: Check available models for provider
```

#### Database Connection
```bash
# MongoDB connection failed
Solution: Check Docker container and connection settings
docker ps | grep mongodb

# Redis connection failed  
Solution: Verify Redis is running and password is correct
redis-cli ping
```

### ⚠️ Performance Considerations
1. **Provider Selection**: Choose appropriate models for task complexity
2. **Cache Configuration**: Set reasonable TTL values for data types
3. **Database Resources**: Monitor MongoDB/Redis resource usage
4. **API Costs**: Track usage across multiple providers

## 🆘 Troubleshooting

### Configuration Issues
```python
# Check current configuration
from shared.config.rich_agents_config_manager import RichAgentsConfigManager
config_manager = RichAgentsConfigManager()
print(config_manager.get_config_summary())
```

### Provider Issues  
```python
# Test provider availability
config_manager.test_api_key("dashscope")
config_manager.get_available_models("openai")
```

### Database Issues
```bash
# MongoDB connection test
mongosh "mongodb://admin:password@localhost:27017/rich_agents"

# Redis connection test  
redis-cli -h localhost -p 6379 -a password ping
```

### Performance Issues
```bash
# Clear all caches
rich-agents db --clear-cache

# Check system resources
rich-agents system --status

# Provider performance stats
rich-agents providers --stats
```

## 📞 Getting Help

### Documentation
- **Architecture Guide**: System design and multi-domain framework
- **Configuration Guide**: Detailed setup and customization
- **Quick Start Guide**: 5-minute setup tutorial
- **Prompt Templates**: Ready-to-use agent prompts

### Support Channels
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides and examples
- **Community**: User discussions and best practices
- **API Support**: Provider-specific help and troubleshooting

### Common Resources
```bash
# View help
rich-agents --help
rich-agents config --help
rich-agents batch --help

# Check version
rich-agents --version

# System information
rich-agents system --info
```

---

💡 **Tip**: Bookmark this reference for quick access to Rich-Agents configuration and troubleshooting!

🌟 **Rich-Agents**: Unified Multi-Agent AI Toolkit - Supporting 13+ LLM providers, multiple professional domains, and enterprise-grade features for comprehensive AI-powered analysis.
