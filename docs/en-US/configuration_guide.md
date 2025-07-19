# Rich-Agents Configuration and Customization Guide

## 📖 Overview

This document provides a comprehensive guide for configuring and customizing the Rich-Agents unified multi-agent AI toolkit. Rich-Agents supports multiple professional domains with extensive LLM provider integration (13+ providers) and enterprise-grade features.

Through this guide, you will learn:
- How to configure the unified multi-domain system
- How to set up 13+ LLM providers with interactive configuration
- How to customize agents for different professional domains
- How to configure enterprise features (MongoDB, Redis, multi-tier caching)
- How to customize prompts and add new capabilities

## 🌟 Rich-Agents Features Overview

### 🎯 Multi-Domain Support
- **TradingAgents**: Financial market analysis, stock evaluation, trading decisions
- **PatentAgents**: Patent discovery, prior art research, patent drafting (Planned)
- **Unified Architecture**: Shared infrastructure across all domains
- **Domain Selection**: Interactive CLI domain and use case selection

### 🤖 Expanded LLM Provider Support (13+ Providers)

#### Chinese LLM Providers (9)
- **DashScope (Alibaba Cloud)**: Qwen model series - Chinese-optimized
- **Baichuan Intelligence**: Long context support (192K), cultural understanding
- **Moonshot AI Kimi**: Ultra-long context (128K), reasoning capabilities
- **01.AI Yi**: Multimodal capabilities, large context windows
- **Zhipu AI GLM**: Fast inference, balanced performance
- **StepFun Step**: Step-by-step reasoning, mathematical capabilities
- **MiniMax Hailuo**: Conversational AI, dialogue optimization
- **Bytedance Doubao**: Enterprise-grade, scalable performance
- **DeepSeek**: Code generation, deep reasoning

#### International LLM Providers (4)
- **OpenAI**: Industry standard (GPT-4o, o1, o3 series)
- **Google AI**: Multimodal capabilities (Gemini 2.0/2.5 series)
- **Anthropic**: Analytical depth (Claude 3.5/4 series)
- **DeepSeek**: Technical reasoning and code analysis

### 🗄️ Enterprise Features
- **Interactive Configuration**: Rich CLI with 17 API provider options
- **MongoDB Integration**: Persistent multi-domain data storage
- **Redis Integration**: High-performance caching
- **Intelligent Cache Management**: Adaptive multi-tier caching with fallback
- **Multi-Market Support**: US stocks and China A-shares

## 🔧 Configuration File Locations

### 1. Core Configuration Files

#### 📁 `shared/config/rich_agents_config_manager.py`
**Purpose**: Unified configuration management for all domains and providers

```python
# Main configuration structure
MAIN_CONFIG = {
    # LLM Provider Settings (13+ providers)
    "llm_providers": {
        "dashscope": {
            "api_key_env": "DASHSCOPE_API_KEY",
            "models": ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"],
            "default_model": "qwen-plus",
            "base_url": "https://dashscope.aliyuncs.com/api/v1"
        },
        "openai": {
            "api_key_env": "OPENAI_API_KEY", 
            "models": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini", "o3-mini"],
            "default_model": "gpt-4o"
        },
        # ... 11 more providers
    },
    
    # Domain-specific settings
    "domains": {
        "trading": {
            "markets": ["us_stock", "china_a_share"],
            "data_sources": ["yahoo_finance", "tongdaxin"],
            "default_market": "us_stock"
        },
        "patent": {
            "databases": ["uspto", "epo", "cnipa"],
            "default_database": "uspto"
        }
    },
    
    # Enterprise features
    "database": {
        "mongodb_enabled": False,
        "redis_enabled": False,
        "intelligent_cache": True
    }
}
```

### 2. Interactive Configuration System

#### 📁 CLI Configuration Interface
Rich-Agents provides an interactive configuration system with 17 API provider options:

**LLM Providers (13)**:
1. DashScope (Alibaba Cloud) - Qwen models
2. OpenAI - GPT series
3. Google AI - Gemini series
4. Anthropic - Claude series
5. Baichuan Intelligence - Long context models
6. Moonshot AI - Kimi models
7. 01.AI - Yi series
8. Zhipu AI - GLM series
9. StepFun - Step models
10. MiniMax - Hailuo series
11. Bytedance - Doubao series
12. DeepSeek - Reasoning models
13. DeepSeek (International) - Code analysis models

**Data Sources (4)**:
14. FinnHub - Financial data
15. Alpha Vantage - Market data
16. TongDaXin - China A-share real-time data
17. Yahoo Finance - US market data

## 🌟 Interactive Configuration Setup

### 1. Launch Configuration Interface
```bash
# Start Rich-Agents configuration
rich-agents

# Or use simple CLI
rich-agents-simple
```

### 2. API Provider Configuration Workflow
```
? Select API to configure:
❯ 1. DashScope (Alibaba Cloud) - Chinese-optimized Qwen models
  2. OpenAI - Industry standard GPT models
  3. Google AI - Multimodal Gemini models
  4. Anthropic - Analytical Claude models
  5. Baichuan Intelligence - Long context Chinese models
  ...
  13. DeepSeek (International) - Code analysis models
  ─────────────────────────────────────────────────
  14. FinnHub - Financial market data
  15. Alpha Vantage - Stock market data
  16. TongDaXin - China A-share real-time data
  17. Yahoo Finance - US market data
```

### 3. Provider-Specific Configuration

#### DashScope Configuration Example
```
🔧 DashScope (Alibaba Cloud) Configuration

Description: Chinese-optimized Qwen model series with excellent Chinese language understanding
Available Models:
  • qwen-turbo - Fast response, cost-effective
  • qwen-plus - Balanced performance (Recommended)
  • qwen-max - Best performance for complex tasks
  • qwen-max-longcontext - Ultra-long context support

? Enter your DashScope API Key: sk-xxxxxxxxxxxxxxxx
✅ API key format validated
✅ API key tested successfully
✅ Configuration saved

Available actions:
1. Test API key
2. Delete API key
3. View configuration
4. Return to main menu
```

#### OpenAI Configuration Example
```
🔧 OpenAI Configuration

Description: Industry standard with reliable performance across all use cases
Available Models:
  • gpt-4o - Latest GPT-4 optimized
  • gpt-4o-mini - Cost-effective GPT-4
  • o1-preview - Advanced reasoning
  • o1-mini - Compact reasoning model
  • o3-mini - Latest compact model

? Enter your OpenAI API Key: sk-xxxxxxxxxxxxxxxx
✅ API key format validated
✅ API key tested successfully
✅ Configuration saved
```

## 🗄️ Enterprise Database Configuration

### 1. MongoDB Setup (Persistent Storage)
```bash
# Start MongoDB with Docker
docker run -d \
  --name rich-agents-mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=your_password \
  mongo:latest
```

**Environment Configuration**:
```env
# MongoDB Settings
MONGODB_ENABLED=true
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=admin
MONGODB_PASSWORD=your_password
MONGODB_DATABASE=rich_agents
```

### 2. Redis Setup (High-Performance Cache)
```bash
# Start Redis with Docker
docker run -d \
  --name rich-agents-redis \
  -p 6379:6379 \
  redis:latest redis-server --requirepass your_password
```

**Environment Configuration**:
```env
# Redis Settings
REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_DB=0
```

### 3. Intelligent Cache Configuration
```python
# Adaptive cache settings
cache_config = {
    "intelligent_cache": True,
    "cache_strategies": {
        "trading_data": {
            "ttl_hours": 2,
            "strategy": "adaptive"
        },
        "patent_data": {
            "ttl_hours": 24,
            "strategy": "persistent"
        }
    },
    "fallback_chain": ["redis", "mongodb", "file_cache"]
}
```

## 🎯 Domain-Specific Configuration

### 1. TradingAgents Configuration

#### Market Selection
```python
trading_config = {
    "supported_markets": {
        "us_stock": {
            "data_source": "yahoo_finance",
            "validation_pattern": r'^[A-Z]{1,5}$',
            "examples": ["AAPL", "SPY", "TSLA"]
        },
        "china_a_share": {
            "data_source": "tongdaxin",
            "validation_pattern": r'^\d{6}$',
            "examples": ["000001", "600036", "300001"]
        }
    },
    "default_market": "us_stock"
}
```

#### Agent Configuration
```python
trading_agents_config = {
    "analysts": {
        "market_analyst": {"enabled": True, "priority": "high"},
        "fundamentals_analyst": {"enabled": True, "priority": "high"},
        "news_analyst": {"enabled": True, "priority": "medium"},
        "social_media_analyst": {"enabled": True, "priority": "low"}
    },
    "researchers": {
        "bull_researcher": {"enabled": True, "debate_rounds": 2},
        "bear_researcher": {"enabled": True, "debate_rounds": 2}
    },
    "traders": {
        "conservative_trader": {"enabled": True, "risk_tolerance": "low"},
        "aggressive_trader": {"enabled": False, "risk_tolerance": "high"}
    }
}
```

### 2. PatentAgents Configuration (Planned)

#### Patent Database Setup
```python
patent_config = {
    "supported_databases": {
        "uspto": {
            "api_endpoint": "https://developer.uspto.gov/api",
            "data_types": ["patents", "applications", "citations"]
        },
        "epo": {
            "api_endpoint": "https://ops.epo.org/3.2",
            "data_types": ["patents", "families", "legal_status"]
        },
        "cnipa": {
            "api_endpoint": "https://api.cnipa.gov.cn",
            "data_types": ["patents", "utility_models", "designs"]
        }
    },
    "default_database": "uspto"
}
```

## 🤖 Agent Prompt Customization

### 1. TradingAgents Prompt Templates

#### Market Analyst Customization
**File**: `tradingagents/agents/analysts/market_analyst.py`

```python
system_message = f"""
You are a professional market analyst specializing in {market_type} market analysis.

🎯 Analysis Framework:
- Market: {market_type} ({market_description})
- Focus: Technical indicators and market trends
- Depth: {analysis_depth}
- Time Horizon: {time_horizon}

📊 Technical Indicators Priority:
1. Moving Averages: SMA/EMA analysis
2. Momentum: RSI, MACD signals
3. Volatility: Bollinger Bands, ATR
4. Volume: Volume-price relationships

🔍 Analysis Requirements:
- Select up to 8 complementary indicators
- Provide detailed trend analysis
- Avoid generic "mixed signals" statements
- Include specific data support
- Generate actionable insights

Output Format:
- Technical analysis report
- Key indicator summary table
- Trend direction assessment
- Support/resistance levels

Please provide professional {market_type} market analysis.
"""
```

#### Bull/Bear Researcher Templates
**File**: `tradingagents/agents/researchers/bull_researcher.py`

```python
bull_prompt = f"""
You are a professional bull analyst building a strong investment case.

🎯 Advocacy Framework:
- Growth Potential: Market opportunities, revenue projections, scalability
- Competitive Advantages: Unique products, market positioning, moats
- Positive Catalysts: Financial health, industry trends, positive news
- Risk Mitigation: Address bear concerns with data-driven rebuttals

💪 Debate Strategy:
- Present compelling evidence
- Counter pessimistic arguments
- Highlight upside opportunities
- Maintain professional optimism

Available Intelligence:
- Market Analysis: {market_research_report}
- Fundamentals: {fundamentals_report}
- News Sentiment: {news_report}
- Social Media: {sentiment_report}
- Historical Context: {past_memory_str}

Provide convincing bull analysis and engage in dynamic debate.
"""
```

### 2. PatentAgents Prompt Templates (Planned)

#### Technology Analyst Template
```python
tech_analyst_prompt = f"""
You are a professional technology analyst specializing in innovation discovery.

🔬 Analysis Framework:
- Technology Domain: {tech_domain}
- Innovation Focus: {innovation_areas}
- Market Context: {market_context}
- Time Horizon: {analysis_timeframe}

🎯 Key Responsibilities:
1. Technology Trend Analysis: Current state and future directions
2. Innovation Opportunity Identification: White spaces and gaps
3. Competitive Landscape: Key players and their strategies
4. Market Readiness: Commercial viability assessment

📊 Data Sources:
- Patent Databases: USPTO, EPO, CNIPA
- Academic Literature: IEEE, ACM, arXiv
- Industry Reports: Market research and analysis
- Technology News: Latest developments and breakthroughs

Output Requirements:
- Technology landscape overview
- Innovation opportunity matrix
- Competitive analysis summary
- Market readiness assessment

Provide comprehensive technology analysis for {tech_domain}.
"""
```

## 🎨 Advanced Customization

### 1. Custom LLM Provider Integration

#### Adding New Provider
```python
# In rich_agents_config_manager.py
def add_custom_provider(provider_name, config):
    """Add a custom LLM provider configuration."""
    custom_provider_config = {
        "api_key_env": f"{provider_name.upper()}_API_KEY",
        "models": config.get("models", []),
        "default_model": config.get("default_model"),
        "base_url": config.get("base_url"),
        "description": config.get("description", "Custom LLM provider")
    }
    
    # Add to main configuration
    MAIN_CONFIG["llm_providers"][provider_name] = custom_provider_config
    
    return custom_provider_config
```

### 2. Custom Domain Integration

#### Domain Plugin Framework
```python
# Domain plugin structure
class CustomDomain:
    def __init__(self, domain_name):
        self.domain_name = domain_name
        self.agents = {}
        self.data_sources = {}
        self.config = {}
    
    def register_agent(self, agent_class):
        """Register a custom agent for this domain."""
        pass
    
    def register_data_source(self, source_class):
        """Register a custom data source."""
        pass
    
    def configure(self, config_dict):
        """Configure domain-specific settings."""
        pass
```

### 3. Multi-Language Prompt Support

#### Internationalization Framework
```python
PROMPT_TEMPLATES = {
    "en-US": {
        "market_analyst": {
            "system_message": "You are a professional market analyst...",
            "analysis_framework": "Analysis Framework:",
            "output_format": "Output Format:"
        }
    },
    "zh-CN": {
        "market_analyst": {
            "system_message": "您是一位专业的市场分析师...",
            "analysis_framework": "分析框架：",
            "output_format": "输出格式："
        }
    },
    "ja-JP": {
        "market_analyst": {
            "system_message": "あなたはプロの市場アナリストです...",
            "analysis_framework": "分析フレームワーク：",
            "output_format": "出力形式："
        }
    }
}
```

## 🚀 Quick Configuration Examples

### 1. Financial Analysis Setup (US Markets)
```env
# Minimum required for US stock analysis
OPENAI_API_KEY=your_openai_key_here
FINNHUB_API_KEY=your_finnhub_key_here

# Optional: Enhanced performance
REDIS_ENABLED=true
MONGODB_ENABLED=true
```

### 2. Chinese Market Analysis Setup
```env
# Required for China A-share analysis
DASHSCOPE_API_KEY=your_dashscope_key_here
FINNHUB_API_KEY=your_finnhub_key_here

# Optional: Additional providers
OPENAI_API_KEY=your_openai_key_here
BAICHUAN_API_KEY=your_baichuan_key_here
```

### 3. Multi-Provider Enterprise Setup
```env
# Primary providers
DASHSCOPE_API_KEY=your_dashscope_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
ANTHROPIC_API_KEY=your_anthropic_key

# Chinese providers
BAICHUAN_API_KEY=your_baichuan_key
MOONSHOT_API_KEY=your_moonshot_key
YI_API_KEY=your_yi_key
GLM_API_KEY=your_glm_key

# Data sources
FINNHUB_API_KEY=your_finnhub_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

# Enterprise features
MONGODB_ENABLED=true
REDIS_ENABLED=true
INTELLIGENT_CACHE=true
```

## 📋 Configuration Management Commands

### 1. Interactive Configuration
```bash
# Launch configuration interface
rich-agents config

# Configure specific provider
rich-agents config --provider dashscope

# Test all configurations
rich-agents config --test-all

# Export configuration
rich-agents config --export config_backup.json
```

### 2. Programmatic Configuration
```python
from shared.config.rich_agents_config_manager import RichAgentsConfigManager

# Initialize configuration manager
config_manager = RichAgentsConfigManager()

# Set API key
config_manager.set_api_key("dashscope", "your_api_key")

# Test API key
result = config_manager.test_api_key("dashscope")

# Get available models
models = config_manager.get_available_models("dashscope")

# Export configuration
config_manager.export_config("backup.json")
```

## 🔧 Troubleshooting

### Common Configuration Issues

1. **API Key Format Errors**
```python
# Validate API key format
def validate_api_key(provider, key):
    patterns = {
        "openai": r"^sk-[A-Za-z0-9]{48}$",
        "dashscope": r"^sk-[A-Za-z0-9]{32}$",
        "google": r"^[A-Za-z0-9_-]{39}$"
    }
    return bool(re.match(patterns.get(provider, r".*"), key))
```

2. **Provider Availability Issues**
```python
# Check provider status
def check_provider_status(provider_name):
    try:
        response = test_api_call(provider_name)
        return {"status": "available", "latency": response.elapsed.total_seconds()}
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}
```

3. **Database Connection Problems**
```bash
# Test MongoDB connection
mongosh "mongodb://admin:password@localhost:27017/rich_agents"

# Test Redis connection
redis-cli -h localhost -p 6379 -a your_password ping
```

## 📝 Best Practices

### 1. Security
- Store API keys in environment variables, never in code
- Use different keys for development and production
- Regularly rotate API keys
- Monitor API usage and costs

### 2. Performance
- Enable Redis for high-frequency usage
- Use MongoDB for historical analysis
- Configure appropriate cache TTL values
- Monitor provider response times

### 3. Reliability
- Configure multiple providers for fallback
- Test configurations regularly
- Monitor error rates and success metrics
- Implement proper logging and alerting

---

💡 **Rich-Agents Configuration**: This unified configuration system supports multiple professional domains with extensive customization options, enterprise-grade features, and intelligent provider management.

🌟 **Rich-Agents**: Unified Multi-Agent AI Toolkit - Empowering professionals across multiple domains with intelligent agent collaboration and comprehensive configuration management.
