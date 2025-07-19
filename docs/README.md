# Rich-Agents Documentation

## 📚 Documentation Structure

This documentation serves the Rich-Agents unified multi-agent AI toolkit, supporting multiple professional domains:

### 🎯 Supported Domains
- **TradingAgents**: Financial trading analysis and market intelligence
- **PatentAgents**: Patent discovery, validation, analysis, and drafting (Coming Soon)

### 🌍 Language-Specific Documentation

#### 🇺🇸 English Documentation (`en-US/`)
**Status**: ✅ Included in version control

Contains comprehensive guides for English-speaking users:
- **Architecture Guide** (`architecture_guide.md`) - System architecture and technical implementation
- **Configuration Guide** (`configuration_guide.md`) - Detailed instructions for modifying system configurations and agent prompts
- **Quick Start Guide** (`quick_start_guide.md`) - 5-minute setup and usage tutorial
- **Quick Reference** (`quick_reference.md`) - Quick lookup card for common modifications and file locations
- **Prompt Templates** (`prompt_templates.md`) - Ready-to-use prompt templates for various agent roles

#### 🇨🇳 Chinese Documentation (`zh-CN/`)
**Status**: ✅ Included in version control

Contains comprehensive guides in Chinese for Chinese-speaking users:
- **主文档** (`README.md`) - 中文版系统概览和快速开始
- **架构指南** (`architecture_guide.md`) - 系统架构和技术实现详解
- **配置指南** (`configuration_guide.md`) - 详细的配置修改和新功能设置指南
- **快速开始指南** (`quick_start_guide.md`) - 5分钟快速设置和使用教程
- **快速参考** (`quick_reference.md`) - 新手友好的快速查找卡片
- **提示词模板库** (`prompt_templates.md`) - 可直接使用的提示词模板

## 🎯 Quick Start

### For English Users
Navigate to [`en-US/`](en-US/) directory for:
- System architecture overview
- Multi-domain configuration instructions
- LLM provider setup (13+ providers supported)
- Prompt customization guides
- Template libraries and troubleshooting tips

### For Chinese Users
Navigate to [`zh-CN/`](zh-CN/) directory for:
- 系统架构说明
- 多领域配置指南
- 中国A股市场功能
- 百炼(DashScope)等国产LLM集成指南
- 数据库配置说明
- 提示词定制指南
- 故障排除技巧

## 📖 Available Guides

| Guide | English | Chinese | Description |
|-------|---------|---------|-------------|
| **Main Documentation** | [📖 View](en-US/) | [📖 查看](zh-CN/README.md) | System overview and domain selection |
| **Architecture Guide** | [🏗️ View](en-US/architecture_guide.md) | [🏗️ 查看](zh-CN/architecture_guide.md) | Multi-domain system architecture and technical implementation |
| **Configuration Guide** | [📖 View](en-US/configuration_guide.md) | [📖 查看](zh-CN/configuration_guide.md) | Complete guide for modifying configurations and new features |
| **Quick Start Guide** | [🚀 View](en-US/quick_start_guide.md) | [🚀 查看](zh-CN/quick_start_guide.md) | 5-minute setup and usage tutorial |
| **Quick Reference** | [📋 View](en-US/quick_reference.md) | [📋 查看](zh-CN/quick_reference.md) | Quick lookup for common modifications |
| **Prompt Templates** | [🎯 View](en-US/prompt_templates.md) | [🎯 查看](zh-CN/prompt_templates.md) | Ready-to-use prompt templates |

## 🔧 Key Topics Covered

### Multi-Domain Support
- **TradingAgents**: Financial market analysis, stock evaluation, trading decisions
- **PatentAgents**: Patent discovery, prior art research, patent drafting (Planned)
- **Domain Selection**: CLI-based domain and use case selection
- **Shared Infrastructure**: Unified LLM providers, caching, and configuration management

### LLM Provider Configuration (13+ Providers)
- **Chinese Providers**: DashScope (Qwen), Baichuan, Moonshot, Yi, GLM, Step, MiniMax, Doubao ⭐ **Expanded Support**
- **International Providers**: OpenAI (GPT), Google (Gemini), Anthropic (Claude), DeepSeek
- **Intelligent Fallback**: Automatic provider switching and error recovery
- **API Key Management**: Secure credential storage and validation

### Market and Data Support
- **US Stock Market**: Yahoo Finance integration with real-time data
- **China A-Share Market**: TongDaXin API integration ⭐ **New Feature**
  - Shanghai Stock Exchange (60xxxx)
  - Shenzhen Stock Exchange (00xxxx) 
  - ChiNext Board (30xxxx)
  - STAR Market (68xxxx)
- **Patent Databases**: USPTO, EPO, CNIPA integration (Planned)

### Database and Caching Systems
- **MongoDB**: Persistent data storage for enterprise deployment
- **Redis**: High-performance caching for real-time applications
- **Intelligent Cache**: Adaptive cache management with automatic fallback
- **Multi-tier Storage**: Redundant data storage for high availability

### Agent Customization
- **TradingAgents**: Market analysts, fundamentals analysts, news analysts, bull/bear researchers, trader decision agents
- **PatentAgents**: Technology analysts, innovation discovery agents, prior art researchers, patent writers (Planned)
- **Risk Management**: Conservative, aggressive, and neutral debate agents
- **Reflection System**: Quality control and learning from experience

### Advanced Features
- **Multi-market Support**: US stocks and China A-shares
- **Multi-domain Architecture**: Extensible framework for different professional domains
- **Database Integration**: MongoDB and Redis for enterprise deployment
- **Intelligent Caching**: Adaptive cache strategies with fallback mechanisms
- **Multi-LLM Support**: 13+ LLM providers with intelligent routing
- **Real-time Data**: Live market data access and processing
- **Cross-domain Analytics**: Shared insights across different domains

## 🚀 Getting Started

1. **Choose Your Domain**: Select TradingAgents for financial analysis (PatentAgents coming soon)
2. **Choose Your Language**: Select the appropriate documentation directory
3. **Start with Quick Reference**: Get familiar with key file locations and configurations
4. **Read Configuration Guide**: Understand the multi-domain system architecture
5. **Use Prompt Templates**: Copy and customize templates for your specific needs
6. **Test Changes**: Always validate modifications in a safe environment

## 🛠️ Development Workflow

### For Contributors
1. **English Documentation**: 
   - Modify files in `en-US/` directory
   - Focus on international features and general architecture
   - Commit changes to version control

2. **Chinese Documentation**: 
   - Modify files in `zh-CN/` directory
   - Include Chinese market-specific features
   - Commit changes to version control

3. **Domain-Specific Documentation**:
   - TradingAgents: Focus on financial market features
   - PatentAgents: Patent and IP-related functionality (Planned)

### Version Control Policy
- ✅ **Include**: Both `en-US/` and `zh-CN/` directories
- ✅ **Include**: All language versions for global community benefit
- ✅ **Include**: This README file for navigation
- 🎯 **Rationale**: Multi-language support enhances accessibility for global users

## 📝 Contributing

When contributing to documentation:

1. **Update English docs** for features that benefit the international community
2. **Update Chinese docs** for features specific to Chinese markets or users
3. **Maintain consistency** between language versions when covering shared features
4. **Test all examples** before documenting them
5. **Consider localization** - some features may be more relevant to specific regions or domains
6. **Domain-specific content** - Clearly indicate which domain (Trading/Patent) the documentation applies to

## 🔗 Related Resources

### Core System Files
- **Configuration**: `shared/config/rich_agents_config_manager.py`
- **CLI Interface**: `cli/rich_agents_main.py`, `cli/rich_agents_simple.py`
- **LLM Adapters**: `shared/llm_adapters/unified_llm_adapter.py`
- **TradingAgents**: `tradingagents/` directory
- **PatentAgents**: `patentagents/` directory (Planned)

### External Resources
- **PyPI Package**: [rich-agents](https://pypi.org/project/rich-agents/)
- **GitHub Repository**: Main Rich-Agents codebase
- **API Documentation**: Provider-specific API references
- **Community**: Discussion forums and user groups

## 📞 Support

For questions about:
- **Architecture and Setup**: See Architecture Guide and Quick Start Guide
- **Configuration**: See Configuration Guide
- **Prompts and Customization**: See Prompt Templates
- **Quick Help**: See Quick Reference
- **Domain-Specific Issues**: Check domain-specific documentation
- **Bug Reports**: Submit to project repository

## 🆕 Recent Updates

### v0.2.x Series
- **Expanded LLM Support**: Added 9 new Chinese LLM providers (DeepSeek, Qianwen, Doubao, GLM, Baichuan, Moonshot, MiniMax, Yi, Step)
- **Enhanced Configuration**: Interactive CLI configuration with 17 API provider options
- **International Documentation**: Complete English documentation for global distribution
- **Package Distribution**: Available on PyPI as `rich-agents`

### Upcoming Features
- **PatentAgents Domain**: Patent discovery and analysis capabilities
- **Enhanced Multi-domain CLI**: Improved domain selection and configuration
- **Advanced Analytics**: Cross-domain insights and reporting
- **API Gateway**: External service integration capabilities

---

💡 **Note**: This documentation structure supports both community sharing and professional use cases while maintaining clean version control and multi-domain extensibility.

🌟 **Rich-Agents**: Unified Multi-Agent AI Toolkit - Empowering professionals across multiple domains with intelligent agent collaboration.
