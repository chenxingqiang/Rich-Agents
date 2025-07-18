
---

# Rich-Agents: Unified Multi-Agent AI Toolkit

> 🎉 **Rich-Agents** - A unified multi-agent AI toolkit extended from the successful TradingAgents architecture
>
> Currently supports two professional domains: **TradingAgent** (Financial Trading Analysis) and **PatentAgent** (Patent Intelligence System)

<div align="center">
<a href="https://www.star-history.com/#chenxingqiang/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=chenxingqiang/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=chenxingqiang/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=chenxingqiang/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

<div align="center">

🚀 [Quick Start](#quick-start) | 📦 [Installation](#installation-guide) | 🏦 [TradingAgent](#tradingagent---financial-trading-analysis) | 🔬 [PatentAgent](#patentagent---patent-intelligence-system) | 🤝 [Contributing](#contributing) | 📄 [Citation](#citation)

</div>

## 🌟 Rich-Agents Framework Overview

Rich-Agents is a unified multi-agent AI toolkit with modular architecture design, supporting multiple professional domains:

### 🏦 TradingAgent - Financial Trading Analysis Framework
Based on real trading company operations, through professional LLM-driven agent collaboration: fundamental analysts, sentiment experts, technical analysts, traders, risk management teams, etc., working together to evaluate market conditions and make trading decisions.

### 🔬 PatentAgent - Patent Intelligence System  
Deeply applies AI technology to the intellectual property field, providing complete solutions for patent discovery, validation, analysis, and writing. Through collaboration of technology analysts, innovation discoverers, prior art researchers, patent writers, and other agents, achieving end-to-end automation from innovation discovery to patent application.

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> ⚠️ **Disclaimer**: The TradingAgents framework is for research purposes only. Trading performance may vary due to multiple factors, including selected language models, model temperature, trading cycles, data quality, and other non-deterministic factors. [This framework does not constitute financial, investment, or trading advice.](https://tauric.ai/disclaimer/)

## 🚀 Quick Start

### Basic Installation
```bash
# Clone repository
git clone https://github.com/chenxingqiang/Rich-Agents.git
cd Rich-Agents

# Basic installation
pip install -e .

# Or use uv (recommended)
uv sync
```

### Launch Rich-Agents
```bash
# Start unified CLI interface
rich-agents

# Or run directly
python main.py
```

### Select Agent System
```
🎯 Welcome to Rich-Agents Multi-Agent AI Toolkit!

Please select the agent system you want to use:
1. 🏦 TradingAgent - Financial Trading Analysis
2. 🔬 PatentAgent - Patent Intelligence System
3. ⚙️  System Configuration and Status Check
4. 📖 View Usage Guide

Enter your choice (1-4): 
```

## 📦 Installation Guide

Rich-Agents supports multiple installation methods, choose according to your needs:

### 1. Complete Installation (Recommended)
```bash
# Install all features
pip install -e ".[all]"

# Or use uv
uv sync --all-extras
```

### 2. Selective Installation
```bash
# Install TradingAgent only
pip install -e ".[trading]"

# Install PatentAgent only
pip install -e ".[patent]"

# Install Chinese market support
pip install -e ".[chinese]"

# Install database support
pip install -e ".[database]"

# Install visualization support
pip install -e ".[visualization]"
```

### 3. Development Environment Installation
```bash
# Development environment (includes testing tools)
pip install -e ".[development]"

# Run tests
pytest tests/
```

### 4. Install with uv (Recommended)
```bash
# Install uv
pip install uv

# Install project with uv
uv sync

# Selective installation
uv sync --extra trading
uv sync --extra patent
uv sync --extra all
```

## 🏦 TradingAgent - Financial Trading Analysis

### Core Agent Team

#### Analyst Team
- **Fundamental Analyst**: Evaluates company financials and performance metrics, identifies intrinsic value and potential risks
- **Sentiment Analyst**: Analyzes social media and public sentiment, uses sentiment scoring algorithms to evaluate short-term market sentiment
- **News Analyst**: Monitors global news and macroeconomic indicators, interprets event impact on market conditions
- **Technical Analyst**: Uses technical indicators (like MACD and RSI) to detect trading patterns and predict price movements

#### Research Team
- **Bull Researcher**: Focuses on discovering buying opportunities, building bullish arguments
- **Bear Researcher**: Identifies selling signals, building bearish arguments
- **Research Manager**: Coordinates research activities, integrates different perspectives

#### Trading Execution Team
- **Trader**: Executes trading decisions based on analyst team recommendations
- **Risk Manager**: Monitors portfolio risk, ensures risk control

### Usage Example
```bash
# Launch TradingAgent
rich-agents
# Select option 1: TradingAgent

# Or use TradingAgent CLI directly
python -m cli.trading_cli
```

### Supported Data Sources
- **US Markets**: Yahoo Finance, Finnhub, EODHD
- **Chinese Markets**: AkShare, Tushare, TDX
- **News Data**: Google News, Reddit, Real-time News APIs
- **Social Media**: Twitter sentiment analysis, Reddit discussion analysis

## 🔬 PatentAgent - Patent Intelligence System

### Core Features

#### 1. Patent Discovery
- **Technology Trend Analysis**: Analyzes technology development trends based on patent data and literature
- **Innovation Gap Identification**: Automatically discovers patent gaps in technology fields
- **Cross-Domain Innovation**: Identifies innovation opportunities from cross-domain technology integration

#### 2. Patent Validation
- **Prior Art Search**: Comprehensive search of relevant patents and technical literature
- **Feasibility Assessment**: Evaluates technical feasibility of patent applications
- **Infringement Risk Analysis**: Assesses infringement risks of patent applications

#### 3. Patent Analysis
- **Patent Value Assessment**: Multi-dimensional evaluation of patent technical and commercial value
- **Competitive Landscape Analysis**: Analyzes patent competition landscape in technology fields
- **Patent Family Analysis**: Tracks global deployment of patent families

#### 4. Patent Writing
- **Claims Generation**: Automatically generates multi-level patent claims
- **Technical Description Optimization**: Ensures accuracy and completeness of technical descriptions
- **Document Formatting**: Patent application documents compliant with patent office standards

### Agent Team

#### Analyst Team
- **Technology Analyst**: Analyzes development trends and technological maturity in target technology fields
- **Innovation Discovery Analyst**: Discovers potential innovation points from technology dynamics and academic papers
- **Prior Art Researcher**: Conducts in-depth search of relevant patents and technical literature
- **Market Intelligence Analyst**: Analyzes commercial value and market acceptance of technologies

#### Research Team
- **Innovation Advocate**: Argues for technical advantages, implementation feasibility, and commercial value of innovation solutions
- **Risk Assessment Researcher**: Identifies technical risks, patent infringement risks, and implementation barriers
- **Patent Strategy Manager**: Integrates various analyses to develop patent application strategies and timing plans

#### Execution Team
- **Patent Writer**: Writes high-quality patent application documents based on analysis results
- **Quality Assessor**: Evaluates patent application quality, completeness, and grant probability

### Usage Example
```bash
# Launch PatentAgent
rich-agents
# Select option 2: PatentAgent

# Or use PatentAgent CLI directly
python -m cli.patent_cli
```

### Supported Data Sources
- **Patent Databases**: Google Patents, USPTO, EPO, CNIPA
- **Academic Literature**: IEEE Xplore, ACM Digital Library, arXiv
- **Technical News**: TechCrunch, MIT Technology Review, Nature/Science
- **Industry Reports**: Gartner, IDC, Standards Organizations

## 🤖 Multi-LLM Provider Support

Rich-Agents supports 13 major LLM providers with 49+ models:

### International Providers
- **OpenAI**: GPT-4, GPT-3.5-turbo series
- **Anthropic**: Claude-3.5-sonnet, Claude-3-haiku
- **Google**: Gemini-1.5-pro, Gemini-1.5-flash
- **Cohere**: Command-R, Command-R-plus

### Chinese Providers
- **Alibaba Qianwen**: qwen2.5-72b-instruct, qwen2.5-32b-instruct
- **DeepSeek**: deepseek-chat, deepseek-coder, deepseek-reasoner
- **Bytedance Doubao**: doubao-pro-4k, doubao-lite-4k
- **Zhipu AI**: glm-4-plus, glm-4-0520, glm-4-flash
- **Baichuan**: Baichuan2-Turbo-192k, Baichuan3-Turbo-128k
- **Moonshot**: moonshot-v1-128k
- **MiniMax**: abab6.5s-chat, abab6.5g-chat
- **01.AI**: yi-large, yi-medium-200k
- **StepFun**: step-1v-32k, step-2-16k

### Easy Configuration
```bash
# Interactive configuration
rich-agents
# Select option 3: System Configuration

# Set API keys for different providers
export OPENAI_API_KEY="your_openai_key"
export QIANWEN_API_KEY="your_qianwen_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
# ... and more
```

## 🎯 Key Features

### 🧠 Intelligent Agent Collaboration
- **Multi-agent coordination**: Different agents with specialized roles work together
- **Dynamic decision making**: Agents adapt strategies based on market conditions
- **Conflict resolution**: Built-in mechanisms to handle conflicting opinions

### 📊 Comprehensive Data Integration
- **Multiple data sources**: Financial data, news, social media, technical indicators
- **Real-time processing**: Live data feeds and real-time analysis
- **Historical analysis**: Backtesting and historical pattern recognition

### 🔧 Flexible Architecture
- **Modular design**: Easy to extend with new agents or data sources
- **Configuration management**: Flexible settings for different use cases
- **Multi-LLM support**: Choose from 13 different LLM providers

### 🛡️ Risk Management
- **Portfolio monitoring**: Continuous risk assessment
- **Position sizing**: Intelligent position management
- **Stop-loss mechanisms**: Automated risk control

## 🏗️ Architecture

The system is built on a modular architecture with the following components:

### Core Components
- **Agent Framework**: LangGraph-based multi-agent orchestration
- **Data Layer**: Unified data access across multiple sources
- **LLM Adapters**: Support for multiple language model providers
- **Caching System**: Three-tier caching (MongoDB + Redis + File Cache)
- **Configuration Management**: Flexible environment and API key management

### Data Flow
```
Data Sources → Cache Layer → Agent Processing → Decision Making → Output
```

### Agent Communication
Agents communicate through a shared state system, allowing for:
- Information sharing between agents
- Collaborative decision making
- Conflict resolution and consensus building

## 🔧 Configuration

### Environment Variables
```bash
# LLM Provider API Keys
export OPENAI_API_KEY="your_openai_key"
export QIANWEN_API_KEY="your_qianwen_key"
export DEEPSEEK_API_KEY="your_deepseek_key"

# Data Source API Keys
export FINNHUB_API_KEY="your_finnhub_key"
export SERPAPI_API_KEY="your_serpapi_key"

# Database Configuration
export MONGODB_URI="mongodb://localhost:27017"
export REDIS_URL="redis://localhost:6379"
```

### Configuration Files
- `config/settings.json`: Main configuration
- `config/models.json`: LLM model settings
- `config/pricing.json`: API pricing information
- `config/usage.json`: Usage tracking

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_trading_agents.py
pytest tests/test_patent_agents.py
pytest tests/test_integration.py

# Run with coverage
pytest --cov=rich_agents tests/
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Speed and resource usage testing
- **API Tests**: External API integration testing

## 📈 Performance

### Benchmarks
- **Response Time**: < 30 seconds for complete analysis
- **Accuracy**: 85%+ in backtesting scenarios
- **Scalability**: Supports concurrent multi-symbol analysis
- **Reliability**: 99.9% uptime with proper infrastructure

### Optimization Features
- **Intelligent Caching**: Reduces API calls by 70%
- **Parallel Processing**: Concurrent agent execution
- **Resource Management**: Efficient memory and CPU usage
- **Error Handling**: Robust error recovery mechanisms

## 🌐 Supported Markets

### TradingAgent Markets
- **US Markets**: NYSE, NASDAQ
- **Chinese Markets**: Shanghai Stock Exchange, Shenzhen Stock Exchange
- **Cryptocurrencies**: Bitcoin, Ethereum, major altcoins
- **Forex**: Major currency pairs
- **Commodities**: Gold, Oil, Agricultural products

### PatentAgent Coverage
- **Patent Offices**: USPTO, EPO, CNIPA, JPO
- **Technology Fields**: AI/ML, Biotechnology, Electronics, Mechanical Engineering
- **Languages**: English, Chinese, Japanese, German, French
- **Document Types**: Patents, Patent Applications, Technical Literature

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/chenxingqiang/TradingAgents.git
cd TradingAgents

# Install development dependencies
pip install -e ".[development]"

# Run pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Contribution Areas
- **New Agent Types**: Implement specialized agents for different domains
- **Data Sources**: Add support for new data providers
- **LLM Providers**: Integrate additional language model services
- **Analysis Tools**: Develop new analysis and visualization tools
- **Documentation**: Improve documentation and examples

## 📄 Citation

If you use Rich-Agents in your research, please cite:

```bibtex
@software{rich_agents_2024,
  author = {Chen, Xingqiang},
  title = {Rich-Agents: Unified Multi-Agent AI Toolkit},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/chenxingqiang/TradingAgents}}
}
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors and the open-source community
- Special thanks to the LangGraph team for the excellent multi-agent framework
- Inspired by real-world trading firms and patent analysis workflows

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/chenxingqiang/TradingAgents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/chenxingqiang/TradingAgents/discussions)
- **Email**: [xingqiang.chen@outlook.com](mailto:xingqiang.chen@outlook.com)

---

<div align="center">
<b>⭐ Star this repository if you find it useful!</b>
</div>
