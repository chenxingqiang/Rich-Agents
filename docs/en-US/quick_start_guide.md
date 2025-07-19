# Rich-Agents Quick Start Guide

## 🚀 Overview

This guide will help you get started with Rich-Agents quickly - the unified multi-agent AI toolkit supporting multiple professional domains. Rich-Agents includes expanded LLM provider support (13+ providers), interactive configuration, and enterprise-grade features.

## ⚡ Quick Setup (5 Minutes)

### 1. Installation
```bash
# Install from PyPI
pip install rich-agents

# Or install from source
git clone https://github.com/your-repo/Rich-Agents.git
cd Rich-Agents
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template (if installing from source)
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

**Minimum Required Configuration**:

**For US Stock Analysis**:
```env
# Choose one LLM provider
OPENAI_API_KEY=your_openai_api_key_here
# OR
GOOGLE_API_KEY=your_google_api_key_here
# OR  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Financial data (required)
FINNHUB_API_KEY=your_finnhub_api_key_here
```

**For China A-Share Analysis**:
```env
# DashScope (required for Chinese stocks)
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Financial data (required)
FINNHUB_API_KEY=your_finnhub_api_key_here
```

**For Multi-Provider Enterprise Setup**:
```env
# Primary providers
DASHSCOPE_API_KEY=your_dashscope_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
ANTHROPIC_API_KEY=your_anthropic_key

# Chinese providers (optional)
BAICHUAN_API_KEY=your_baichuan_key
MOONSHOT_API_KEY=your_moonshot_key
YI_API_KEY=your_yi_key
GLM_API_KEY=your_glm_key

# Data sources
FINNHUB_API_KEY=your_finnhub_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

### 3. First Run
```bash
# Launch Rich-Agents
rich-agents

# Or use simple CLI
rich-agents-simple

# Interactive workflow:
# 1. Select Domain: TradingAgents (PatentAgents coming soon)
# 2. Configure API providers (17 options available)
# 3. Select market: US Stock or China A-Share  
# 4. Enter ticker symbol (e.g., AAPL or 000001)
# 5. Choose analysis depth and LLM provider
# 6. Run comprehensive analysis
```

## 🌟 Feature Overview

### 🎯 Multi-Domain Support
- **TradingAgents**: Financial market analysis, stock evaluation, trading decisions
- **PatentAgents**: Patent discovery and analysis (Coming Soon)
- **Unified Architecture**: Shared infrastructure across domains
- **Domain Selection**: Interactive CLI domain selection

### 🤖 Expanded LLM Provider Support (13+ Providers)

#### Chinese LLM Providers (9)
- **DashScope (Alibaba Cloud)**: Qwen models - Chinese-optimized
- **Baichuan Intelligence**: Long context support (192K)
- **Moonshot AI Kimi**: Ultra-long context (128K)
- **01.AI Yi**: Multimodal capabilities
- **Zhipu AI GLM**: Fast inference, balanced performance
- **StepFun Step**: Step-by-step reasoning
- **MiniMax Hailuo**: Conversational AI optimization
- **Bytedance Doubao**: Enterprise-grade performance
- **DeepSeek**: Code generation and deep reasoning

#### International LLM Providers (4)
- **OpenAI**: Industry standard (GPT-4o, o1, o3 series)
- **Google AI**: Multimodal capabilities (Gemini 2.0/2.5)
- **Anthropic**: Analytical depth (Claude 3.5/4)
- **DeepSeek**: Technical reasoning and code analysis

### 🗄️ Enterprise Features
- **Interactive Configuration**: Rich CLI with 17 API provider options
- **MongoDB Integration**: Persistent multi-domain data storage
- **Redis Integration**: High-performance caching
- **Intelligent Cache Management**: Adaptive multi-tier caching
- **Multi-Market Support**: US stocks and China A-shares

## 📋 Step-by-Step Walkthrough

### Step 1: Domain Selection
```
? Select Professional Domain:
❯ TradingAgents - Financial market analysis and trading decisions
  PatentAgents - Patent discovery and analysis (Coming Soon)
  
? Select Use Case:
❯ Stock Analysis - Comprehensive market analysis
  Portfolio Review - Multi-stock evaluation
  Market Research - Industry and sector analysis
```

### Step 2: API Provider Configuration
```
? Configure API Providers (17 options available):

LLM Providers (13):
❯ 1. DashScope (Alibaba Cloud) - Chinese-optimized Qwen models
  2. OpenAI - Industry standard GPT models  
  3. Google AI - Multimodal Gemini models
  4. Anthropic - Analytical Claude models
  5. Baichuan Intelligence - Long context Chinese models
  6. Moonshot AI - Kimi ultra-long context models
  7. 01.AI - Yi multimodal models
  8. Zhipu AI - GLM fast inference models
  9. StepFun - Step reasoning models
  10. MiniMax - Hailuo conversational models
  11. Bytedance - Doubao enterprise models
  12. DeepSeek - Reasoning and code models
  13. DeepSeek (International) - Code analysis models

Data Sources (4):
  14. FinnHub - Financial market data
  15. Alpha Vantage - Stock market data
  16. TongDaXin - China A-share real-time data
  17. Yahoo Finance - US market data
```

### Step 3: Market and Ticker Selection
```
? Select Stock Market:
  US Stock - Examples: AAPL, SPY, TSLA, NVDA
❯ China A-Share - Examples: 000001, 600036, 300001

Format requirement: 6-digit code (e.g., 600036, 000001)
Examples: 
  • 000001 (Ping An Bank - Shenzhen)
  • 600036 (China Merchants Bank - Shanghai)  
  • 300001 (ChiNext Technology)
  • 688001 (STAR Market Innovation)

? Enter China A-Share ticker symbol: 000001
✅ Valid A-share code: 000001 (will use TongDaXin data source)
```

### Step 4: Analysis Configuration
```
? Select analysis depth:
❯ Light (1 round) - Quick analysis, 5-10 minutes
  Medium (2 rounds) - Balanced analysis, 10-15 minutes
  Deep (3 rounds) - Comprehensive analysis, 15-25 minutes

? Select your LLM Provider:
❯ DashScope (Alibaba Cloud) - Recommended for Chinese markets
  OpenAI - Industry standard, reliable performance
  Google AI - Fast multimodal capabilities
  Anthropic - Deep analytical capabilities

? Select Your Quick-Thinking Model:
❯ qwen-turbo - Fast response, cost-effective
  qwen-plus - Balanced performance
  qwen-max - Best performance for complex tasks

? Select Your Deep-Thinking Model:
❯ qwen-plus - Balanced performance (Recommended)
  qwen-max - Best performance for complex analysis
  qwen-max-longcontext - Ultra-long context support
```

## 🗄️ Enterprise Database Setup (Optional)

### Enable High-Performance Caching

**1. Start Database Services**:
```bash
# MongoDB for persistent storage
docker run -d \
  --name rich-agents-mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=your_password \
  mongo:latest

# Redis for high-performance caching  
docker run -d \
  --name rich-agents-redis \
  -p 6379:6379 \
  redis:latest redis-server --requirepass your_password
```

**2. Enable in .env**:
```env
# Enable database caching
MONGODB_ENABLED=true
REDIS_ENABLED=true

# MongoDB configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=rich_agents
MONGODB_USERNAME=admin
MONGODB_PASSWORD=your_password

# Redis configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_DB=0
```

**3. Restart Application**:
```bash
rich-agents
# System will now use enterprise database caching for improved performance
```

## 🔧 Configuration Examples

### Example 1: US Stock Analysis with OpenAI
```env
# Minimum setup for US stocks
OPENAI_API_KEY=your_openai_key
FINNHUB_API_KEY=your_finnhub_key
```

**CLI Selections**:
- Domain: TradingAgents
- Market: US Stock  
- Ticker: AAPL
- LLM Provider: OpenAI
- Models: gpt-4o-mini (quick), o1-preview (deep)

### Example 2: US Stock Analysis with Google AI
```env
# Google AI setup for US stocks
GOOGLE_API_KEY=your_google_key
FINNHUB_API_KEY=your_finnhub_key
```

**CLI Selections**:
- Domain: TradingAgents
- Market: US Stock
- Ticker: TSLA  
- LLM Provider: Google AI
- Models: Gemini 2.0 Flash (quick), Gemini 2.5 Flash (deep)

### Example 3: China A-Share Analysis
```env
# Required for Chinese stock analysis
DASHSCOPE_API_KEY=your_dashscope_key
FINNHUB_API_KEY=your_finnhub_key
```

**CLI Selections**:
- Domain: TradingAgents
- Market: China A-Share
- Ticker: 000001
- LLM Provider: DashScope
- Models: qwen-turbo (quick), qwen-plus (deep)

### Example 4: Multi-Provider Enterprise Setup
```env
# Full enterprise configuration
DASHSCOPE_API_KEY=your_dashscope_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
ANTHROPIC_API_KEY=your_anthropic_key
BAICHUAN_API_KEY=your_baichuan_key
MOONSHOT_API_KEY=your_moonshot_key

FINNHUB_API_KEY=your_finnhub_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

MONGODB_ENABLED=true
REDIS_ENABLED=true
```

**Benefits**:
- Intelligent provider fallback
- Enhanced performance with database caching
- Access to all 13+ LLM providers
- Multi-market analysis capabilities

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Errors**:
```
Error: Invalid API key format
Solution: Check .env file and ensure correct API key format
Example: OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx (48 chars)
```

**2. Provider Unavailable**:
```
Error: Provider timeout or unavailable
Solution: System automatically falls back to alternative providers
Check: Verify internet connection and API key validity
```

**3. Database Connection Issues**:
```
Error: MongoDB/Redis connection failed
Solution: System falls back to file cache automatically
Optional: Check Docker containers are running
```

**4. Invalid Ticker Format**:
```
Error: Invalid ticker symbol
Solution: 
- US stocks: Use 1-5 letter symbols (AAPL, TSLA)
- A-shares: Use 6-digit codes (000001, 600036)
```

**5. Missing Dependencies**:
```
Error: Module not found
Solution: Install additional dependencies
pip install rich-agents[enterprise]  # For database features
pip install rich-agents[chinese]     # For Chinese market support
```

### Debug Mode
```bash
# Enable debug logging
export RICH_AGENTS_LOG_LEVEL=DEBUG
rich-agents

# Or with environment variable
RICH_AGENTS_LOG_LEVEL=DEBUG rich-agents
```

### Configuration Testing
```bash
# Test all API configurations
rich-agents config --test-all

# Test specific provider
rich-agents config --test-provider dashscope

# View current configuration
rich-agents config --show
```

## 📊 Sample Analysis Output

### US Stock Analysis (AAPL)
```
📈 Rich-Agents Analysis Results for AAPL (Apple Inc.)
Domain: TradingAgents | Market: US Stock Exchange
Data Source: Yahoo Finance | LLM Provider: OpenAI

🔍 Technical Analysis:
- Current Price: $150.25 (+2.3%)
- RSI: 65.2 (Neutral to Bullish)  
- MACD: Bullish crossover signal
- Moving Averages: Above 20-day and 50-day MA
- Support: $145.00 | Resistance: $155.00

💰 Fundamental Analysis:
- P/E Ratio: 28.5 (Premium valuation)
- Revenue Growth: 8.2% YoY
- Market Cap: $2.4T
- Debt-to-Equity: 0.31 (Conservative)

📰 News Sentiment: Positive (0.72/1.0)
- Recent iPhone sales strong
- AI integration progress
- Supply chain improvements

🎯 Final Recommendation: BUY
- Target Price: $165 (+9.8% upside)
- Stop Loss: $142 (-5.5% downside)
- Risk Level: Medium
- Confidence: 85%
```

### China A-Share Analysis (000001)
```
📈 Rich-Agents Analysis Results for 000001 (平安银行)
Domain: TradingAgents | Market: Shenzhen Stock Exchange  
Data Source: TongDaXin API | LLM Provider: DashScope

🔍 Technical Analysis:
- Current Price: ¥12.85 (+1.8%)
- RSI: 58.3 (Neutral territory)
- Volume: Above 20-day average
- MA Status: Testing 50-day resistance

💰 Fundamental Analysis:
- P/E Ratio: 5.2 (Attractive valuation)
- ROE: 12.8% (Strong profitability)
- Book Value: ¥15.20 (Trading below book)
- NPL Ratio: 1.1% (Well-controlled risk)

📰 News Sentiment: Neutral (0.55/1.0)
- Banking sector policy support
- Credit growth normalization
- Digital transformation progress

🎯 Final Recommendation: HOLD
- Target Price: ¥14.50 (+12.8% upside)
- Stop Loss: ¥11.80 (-8.2% downside)  
- Risk Level: Medium-Low
- Confidence: 78%
```

## 🎯 Next Steps

### Explore Advanced Features
1. **Multi-Provider Setup**: Configure multiple LLM providers for redundancy
2. **Enterprise Database**: Enable MongoDB and Redis for enhanced performance
3. **Custom Analysis**: Modify agent prompts for specific strategies
4. **Domain Expansion**: Prepare for PatentAgents when available

### Learn More
- [Configuration Guide](configuration_guide.md) - Detailed configuration options
- [Architecture Guide](architecture_guide.md) - System architecture overview  
- [Quick Reference](quick_reference.md) - Quick lookup for common tasks
- [Prompt Templates](prompt_templates.md) - Customizable agent prompts

### Get Support
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Comprehensive guides and examples
- **Community**: Join discussions and share strategies
- **API Support**: Provider-specific help and troubleshooting

## 🚀 Advanced Usage

### Batch Analysis
```bash
# Analyze multiple stocks
rich-agents batch --symbols "AAPL,TSLA,NVDA" --provider openai

# Compare markets
rich-agents compare --us-symbol AAPL --china-symbol 000001
```

### Custom Configuration
```bash
# Use custom configuration file
rich-agents --config custom_config.json

# Override specific settings
rich-agents --provider dashscope --model qwen-max --depth deep
```

### API Integration
```python
from rich_agents import TradingAgents

# Initialize with configuration
agents = TradingAgents(
    provider="dashscope",
    model="qwen-plus",
    enable_cache=True
)

# Run analysis
result = agents.analyze_stock("AAPL", depth="medium")
print(result.recommendation)
```

---

🎉 **Congratulations!** You're now ready to use Rich-Agents for comprehensive financial analysis across multiple markets and domains. The system provides intelligent fallbacks, multi-LLM support, and enterprise-grade features for professional use.

🌟 **Rich-Agents**: Unified Multi-Agent AI Toolkit - Empowering professionals across multiple domains with intelligent agent collaboration, extensive LLM provider support, and enterprise-grade reliability.
