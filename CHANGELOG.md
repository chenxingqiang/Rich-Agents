# Rich-Agents Changelog

## [0.2.0] - 2025-07-18 - Major LLM Provider Expansion

### 🌟 Major Additions
- **Added 9 new Chinese LLM providers**:
  - DeepSeek (deepseek-chat, deepseek-coder, deepseek-reasoner)
  - Alibaba Qianwen (qwen2.5 series multi-spec models)
  - Bytedance Doubao (pro/lite versions, supporting 4K/32K context)
  - Zhipu AI GLM (glm-4 series 6 models)
  - Baichuan Intelligence (baichuan2/3 series, supporting 192K/128K context)
  - Moonshot AI Kimi (supporting 128K ultra-long context)
  - MiniMax Hailuo (abab series dialogue models)
  - 01.AI Yi (yi-large and 4 other models)
  - StepFun Step (step-1v/step-2 series)

### 🔧 Feature Enhancements
- **Total LLM providers expanded from 4 to 13** (+225% increase)
- **Total supported models expanded from 16 to 49** (+206% increase)
- **API configuration options expanded from 8 to 17** (+112% increase)
- **Interactive API key management**: Set, test, delete, and manage API keys
- **Enhanced configuration validation**: Support for various provider API key formats
- **Improved CLI interface**: Grouped display of LLM providers vs. specialized data sources

### 🛠️ Technical Improvements
- **Unified LLM adapter refactoring**: Automatic model detection based on environment variables
- **Enhanced configuration manager**: New methods for API key management and configuration
- **Improved error handling**: Better error messages and recovery mechanisms
- **Documentation updates**: Complete provider guides and configuration instructions

### 🎯 User Experience
- **Rich CLI interface**: Enhanced visual display with provider categorization
- **Simple CLI interface**: Streamlined text-based interface for all providers
- **Configuration help**: Detailed help information for each provider
- **Status monitoring**: Real-time API key status and provider availability

### 📚 Documentation
- **RICH_AGENTS_LLM_PROVIDERS_EXPANSION.md**: Comprehensive guide for all 9 new providers
- **RICH_AGENTS_CONFIG_ENHANCEMENT.md**: Interactive configuration feature documentation
- **Updated README.md**: Complete English translation for international users
- **Provider-specific guides**: API acquisition, free quotas, and usage examples

### 🧪 Testing
- **Configuration manager tests**: Comprehensive testing of new functionality
- **CLI interface tests**: Validation of all interface improvements
- **Integration tests**: End-to-end testing of new provider support
- **System status checks**: Automated verification of provider loading

### 🔄 Migration Notes
- **Backward compatibility**: All existing configurations remain valid
- **New environment variables**: Optional new API keys for expanded providers
- **Configuration migration**: Automatic upgrade of existing config files
- **No breaking changes**: Existing workflows continue to work

---

## [0.1.0] - 2024-12-XX - Initial Release

### 🎉 Initial Features
- **Multi-agent AI toolkit**: Unified framework for different agent systems
- **TradingAgent**: Financial trading analysis with multi-agent collaboration
- **PatentAgent**: Patent intelligence system for IP management
- **4 LLM providers**: OpenAI, Anthropic, Google, Alibaba Qianwen
- **16 supported models**: Comprehensive model selection across providers
- **Unified CLI**: Single interface for all agent systems
- **Configuration management**: Flexible API key and settings management
- **Caching system**: Three-tier caching for optimal performance
- **Testing framework**: Comprehensive test suite for reliability

### 🏦 TradingAgent Features
- **Multi-agent collaboration**: Analysts, researchers, traders, risk managers
- **Data source integration**: Financial data, news, social media
- **Real-time analysis**: Live market data processing
- **Risk management**: Portfolio monitoring and risk control

### 🔬 PatentAgent Features
- **Patent discovery**: Technology trend analysis and innovation identification
- **Patent validation**: Prior art search and feasibility assessment
- **Patent analysis**: Value assessment and competitive landscape
- **Patent writing**: Automated claim generation and document formatting

### 🛠️ Technical Foundation
- **LangGraph integration**: Multi-agent orchestration framework
- **MongoDB support**: Persistent data storage
- **Redis caching**: High-performance data caching
- **Modular architecture**: Extensible design for future enhancements
- **Python packaging**: Standard PyPI distribution 