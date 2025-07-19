# Rich-Agents System Architecture Guide

## 📖 Overview

This document provides a comprehensive overview of the Rich-Agents unified multi-agent AI toolkit architecture. Rich-Agents is designed as an extensible platform supporting multiple professional domains, starting with **TradingAgents** (financial analysis) and expanding to **PatentAgents** (patent intelligence) and beyond.

The architecture emphasizes scalability, reliability, multi-domain support, and extensive LLM provider integration (13+ providers), making it suitable for global deployment across diverse professional use cases.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Rich-Agents System                        │
├─────────────────────────────────────────────────────────────────┤
│  CLI Interface (Domain Selection + Multi-Configuration)        │
├─────────────────────────────────────────────────────────────────┤
│  Multi-Domain Agent Framework                                  │
│  ├── TradingAgents     ├── PatentAgents (Planned)             │
│  │   ├── Analysts      │   ├── Tech Analysts                  │
│  │   ├── Researchers   │   ├── Prior Art Researchers         │
│  │   └── Traders       │   └── Patent Writers                │
│  └── Shared Components: Memory, Reflection, Risk Management    │
├─────────────────────────────────────────────────────────────────┤
│  Unified LLM Provider Layer (13+ Providers)                    │
│  ├── Chinese: DashScope, Baichuan, Moonshot, Yi, GLM, etc.    │
│  ├── International: OpenAI, Google, Anthropic, DeepSeek       │
│  └── Intelligent Routing & Fallback Management                │
├─────────────────────────────────────────────────────────────────┤
│  Multi-Domain Data Layer                                       │
│  ├── Financial: US Markets (Yahoo), China A-Share (TongDaXin) │
│  ├── Patents: USPTO, EPO, CNIPA (Planned)                     │
│  └── News & Intelligence: Multi-source aggregation            │
├─────────────────────────────────────────────────────────────────┤
│  Enterprise Storage & Caching Layer                            │
│  ├── MongoDB (Persistent Multi-Domain Storage)                │
│  ├── Redis (High-Performance Multi-Domain Cache)              │
│  └── Intelligent Cache (Adaptive Multi-Tier Fallback)        │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Core Components

### 1. Unified CLI Interface Layer

#### Multi-Domain Selection System
- **Interactive Domain Selection**: TradingAgents vs PatentAgents (planned)
- **Context-Aware Configuration**: Domain-specific settings and validation
- **Unified User Experience**: Consistent interface across all domains
- **Global Localization**: English and Chinese language support

**Key Files**:
```
cli/rich_agents_main.py       - Rich CLI with interactive features
cli/rich_agents_simple.py     - Simple CLI for automation
shared/config/               - Unified configuration management
```

**Flow**:
```
Domain Selection → Provider Configuration → Use Case Setup → Agent Deployment
```

### 2. Multi-Domain Agent Framework

#### Extensible Agent Architecture
```
Rich-Agents Framework
├── Domain-Specific Agents
│   ├── TradingAgents
│   │   ├── Market Analyst (Technical Analysis)
│   │   ├── Fundamentals Analyst (Financial Analysis)
│   │   ├── News Analyst (Sentiment Analysis)
│   │   ├── Bull/Bear Researchers (Debate & Analysis)
│   │   └── Trader (Decision Making)
│   └── PatentAgents (Planned)
│       ├── Technology Analyst (Tech Trend Analysis)
│       ├── Innovation Discovery (Opportunity Mining)
│       ├── Prior Art Researcher (Patent Landscape)
│       └── Patent Writer (Document Generation)
├── Shared Components
│   ├── Memory System (Cross-Domain Learning)
│   ├── Reflection Agent (Quality Control)
│   ├── Risk Management (Multi-Domain Risk Assessment)
│   └── Configuration Manager (Unified Settings)
└── Extension Framework
    └── Plugin System (Custom Domain Support)
```

**Key Files**:
```
tradingagents/graph/trading_graph.py     - TradingAgents orchestration
patentagents/graph/patent_graph.py       - PatentAgents orchestration (planned)
shared/llm_adapters/unified_llm_adapter.py - Unified LLM interface
shared/config/rich_agents_config_manager.py - Multi-domain configuration
```

### 3. Unified LLM Provider Layer (13+ Providers)

#### Provider Architecture
```
LLM Request → Intelligent Router → Provider Selection → API Call → Response Processing
```

#### Comprehensive Provider Support

**Chinese LLM Providers (9)**:
1. **DashScope (Alibaba Cloud)**
   - Models: qwen-turbo, qwen-plus, qwen-max, qwen-max-longcontext
   - Strengths: Chinese language optimization, cost-effective
   - Use Cases: Chinese market analysis, multilingual processing

2. **Baichuan Intelligence**
   - Models: baichuan2-turbo, baichuan2-53b, baichuan3-turbo, baichuan3-turbo-128k
   - Strengths: Long context support (192K), Chinese cultural understanding
   - Use Cases: Document analysis, cultural context processing

3. **Moonshot AI Kimi**
   - Models: moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k
   - Strengths: Ultra-long context (128K), reasoning capabilities
   - Use Cases: Long document analysis, complex reasoning tasks

4. **01.AI Yi**
   - Models: yi-34b-chat-0205, yi-34b-chat-200k, yi-vl-plus, yi-large
   - Strengths: Multimodal capabilities, large context windows
   - Use Cases: Visual analysis, comprehensive reasoning

5. **Zhipu AI GLM**
   - Models: glm-3-turbo, glm-4, glm-4-0520, glm-4-air, glm-4-airx, glm-4-flash
   - Strengths: Fast inference, balanced performance
   - Use Cases: Real-time analysis, balanced cost-performance

6. **StepFun Step**
   - Models: step-1v-8k, step-1v-32k, step-2-16k-nightly
   - Strengths: Step-by-step reasoning, mathematical capabilities
   - Use Cases: Analytical reasoning, step-by-step problem solving

7. **MiniMax Hailuo**
   - Models: abab6.5s-chat, abab6.5g-chat, abab6.5t-chat
   - Strengths: Conversational AI, dialogue optimization
   - Use Cases: Interactive analysis, conversational interfaces

8. **Bytedance Doubao**
   - Models: doubao-lite-4k, doubao-lite-32k, doubao-pro-4k, doubao-pro-32k
   - Strengths: Enterprise-grade, scalable performance
   - Use Cases: Enterprise deployment, scalable analysis

9. **DeepSeek**
   - Models: deepseek-chat, deepseek-coder, deepseek-reasoner
   - Strengths: Code generation, deep reasoning
   - Use Cases: Technical analysis, code-related tasks

**International LLM Providers (4)**:
1. **OpenAI**
   - Models: GPT-4o, GPT-4o-mini, o1-preview, o1-mini, o3-mini
   - Strengths: Industry standard, reliable performance
   - Use Cases: General analysis, established workflows

2. **Google AI**
   - Models: Gemini 2.0 Flash, Gemini 2.5 Flash, Gemini 2.5 Pro
   - Strengths: Multimodal capabilities, fast inference
   - Use Cases: Visual analysis, rapid processing

3. **Anthropic**
   - Models: Claude 3.5 Haiku, Claude 3.5 Sonnet, Claude 4
   - Strengths: Analytical depth, safety-focused
   - Use Cases: In-depth analysis, safety-critical applications

4. **DeepSeek (International)**
   - Models: deepseek-chat, deepseek-coder, deepseek-reasoner
   - Strengths: Technical reasoning, code analysis
   - Use Cases: Technical documentation, code analysis

#### Intelligent Provider Management
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Request Analysis│ -> │ Provider Ranking │ -> │ Fallback Chain  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Cost Optimization│ <- │ Performance Metrics│ <- │ Error Recovery │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Key Features**:
- **Intelligent Routing**: Automatic provider selection based on task requirements
- **Cost Optimization**: Dynamic routing based on cost-performance ratios
- **Fallback Management**: Seamless switching on provider failures
- **Performance Monitoring**: Real-time provider performance tracking
- **Regional Optimization**: Prefer local providers for regional content

### 4. Multi-Domain Data Layer Architecture

#### Extensible Data Source Framework

**TradingAgents Data Sources**:
```
Financial Markets → Data Validation → Domain Cache → Agent Consumption
```

**PatentAgents Data Sources (Planned)**:
```
Patent Databases → IP Analysis → Domain Cache → Agent Consumption
```

#### Data Flow Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Domain Request  │ -> │ Source Router    │ -> │ Data Provider   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Domain Cache    │ <- │ Data Processor   │ <- │ Raw Data        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**TradingAgents Data Sources**:
- **US Stock Market**: Yahoo Finance API integration
- **China A-Share Market**: TongDaXin API for real-time data
- **Financial News**: Multi-source news aggregation
- **Market Sentiment**: Social media and news sentiment analysis

**PatentAgents Data Sources (Planned)**:
- **Patent Databases**: USPTO, EPO, CNIPA integration
- **Prior Art**: Academic papers, technical literature
- **IP Intelligence**: Patent landscape analysis
- **Technology Trends**: R&D and innovation tracking

**Key Files**:
```
tradingagents/dataflows/               - Trading data management
patentagents/dataflows/                - Patent data management (planned)
shared/cache/                          - Unified caching system
shared/utils/                          - Cross-domain utilities
```

### 5. Enterprise Storage & Caching Layer

#### Multi-Domain Three-Tier Architecture

**Tier 1: Redis (High-Performance Multi-Domain Cache)**
```
Domain-Specific Keys → Sub-millisecond Access → Real-time Data
```

**Tier 2: MongoDB (Persistent Multi-Domain Storage)**
```
Domain Collections → Structured Storage → Historical Analytics
```

**Tier 3: File Cache (Universal Fallback)**
```
Domain Directories → Reliable Fallback → Always Available
```

#### Multi-Domain Cache Management
```
Domain Request
    ↓
Redis Check (Domain-Specific Keys)
    ↓ (if miss)
MongoDB Check (Domain Collections)
    ↓ (if miss)
File Cache Check (Domain Directories)
    ↓ (if miss)
External API Call
    ↓
Store in All Tiers (Domain-Aware)
```

**Key Files**:
```
shared/cache/adaptive_cache.py         - Intelligent cache management
shared/cache/db_cache_manager.py       - Database cache coordination
shared/config/database_config.py       - Multi-domain database setup
shared/config/database_manager.py      - Connection management
```

#### Multi-Domain Database Schema

**MongoDB Collections**:
```
# TradingAgents Collections
trading_stock_data          - Historical stock prices and volumes
trading_analysis_results    - Agent analysis outputs
trading_token_usage         - LLM API usage tracking

# PatentAgents Collections (Planned)
patent_prior_art           - Patent and literature database
patent_analysis_results    - Patent analysis outputs
patent_applications        - Generated patent documents

# Shared Collections
shared_cache_metadata      - Cross-domain cache management
shared_user_sessions       - Multi-domain user interactions
shared_llm_usage          - Unified LLM provider usage
```

**Redis Key Patterns**:
```
# Domain-specific patterns
trading:{symbol}:{date}           - Trading data
patent:{id}:{type}               - Patent data
analysis:{domain}:{id}           - Analysis results
cache:meta:{domain}:{key}        - Domain cache metadata
```

## 🔄 Multi-Domain Data Flow Patterns

### 1. Unified Analysis Workflow
```
Domain Selection (CLI)
    ↓
Domain-Specific Validation
    ↓
Multi-Source Data Retrieval
    ↓
Domain Agent Analysis (Multi-LLM)
    ↓
Cross-Domain Learning
    ↓
Result Aggregation
    ↓
Domain-Aware Output Generation
    ↓
Multi-Tier Cache Storage
```

### 2. Intelligent Provider Selection
```
Analysis Request
    ↓
Domain Context Analysis
    ↓
Provider Capability Matching
    ↓
Cost-Performance Optimization
    ↓
Regional Preference Application
    ↓
Provider Selection & Fallback Setup
    ↓
Request Execution
    ↓
Performance Feedback Loop
```

### 3. Multi-Domain Error Handling
```
Component Failure
    ↓
Domain-Aware Error Detection
    ↓
Provider/Data Source Fallback
    ↓
Cross-Domain Recovery Strategies
    ↓
Graceful Degradation
    ↓
User Notification (Context-Aware)
    ↓
Learning & Improvement
```

## 🛡️ Enterprise-Grade Reliability & Scalability

### High Availability Design
- **Multi-LLM Redundancy**: 13+ providers with intelligent fallback
- **Multi-Domain Caching**: Domain-aware redundant storage
- **Cross-Domain Learning**: Shared knowledge improves all domains
- **Graceful Degradation**: Maintains functionality during failures

### Scalability Features
- **Horizontal Domain Scaling**: Add new domains without architectural changes
- **Provider Scaling**: Easy addition of new LLM providers
- **Database Clustering**: MongoDB replica sets and Redis clusters
- **Load Distribution**: Intelligent request distribution across providers

### Performance Optimization
- **Domain-Aware Caching**: Optimized cache strategies per domain
- **Provider Performance Monitoring**: Real-time performance tracking
- **Async Multi-Domain Processing**: Concurrent domain operations
- **Intelligent Resource Management**: Dynamic resource allocation

## 🔧 Configuration Management

### Multi-Domain Configuration Architecture
```
Domain Selection → Domain Config → Provider Config → Runtime Execution
```

### Configuration Hierarchy
```
1. Environment Variables (.env)
2. Domain-Specific Defaults (domain_config.py)
3. Shared Configuration (rich_agents_config_manager.py)
4. Runtime Overrides (CLI parameters)
5. Dynamic Updates (real-time configuration)
```

### Configuration Categories
- **LLM Providers**: 13+ provider configurations with API keys
- **Domain Settings**: TradingAgents, PatentAgents-specific settings
- **Database Configuration**: MongoDB, Redis multi-domain setup
- **Cache Strategies**: Domain-aware cache policies
- **Security Settings**: API key management and access control

## 📊 Monitoring & Analytics

### System Metrics
- **Multi-Provider Performance**: Response times, success rates, costs
- **Domain Usage Patterns**: Usage distribution across domains
- **Cache Effectiveness**: Hit rates by domain and data type
- **Error Rates**: Failure analysis by provider and domain

### Business Metrics
- **Cross-Domain Insights**: Patterns across different professional domains
- **Provider ROI**: Cost-effectiveness analysis per provider
- **User Engagement**: Domain preferences and usage patterns
- **Quality Metrics**: Agent performance across domains

## 🚀 Deployment Architecture

### Development Environment
```
Local Machine → File Cache → Single Domain → Basic Provider Set
```

### Production Environment
```
Load Balancer → Application Clusters → Redis Clusters → MongoDB Replica Sets → Multi-LLM Providers
```

### Cloud Deployment Options
- **Container Orchestration**: Docker + Kubernetes
- **Database Services**: MongoDB Atlas, Redis Cloud
- **LLM Provider Integration**: Multi-region API management
- **Monitoring**: Comprehensive observability stack

## 🔮 Future Architecture Enhancements

### Planned Domain Expansions
- **PatentAgents**: Patent discovery and analysis (Q2 2025)
- **LegalAgents**: Legal document analysis (Q3 2025)
- **ResearchAgents**: Academic research assistance (Q4 2025)
- **BusinessAgents**: Business intelligence and strategy (2026)

### Technical Roadmap
- **Microservices Architecture**: Domain-specific service decomposition
- **Event-Driven Architecture**: Real-time cross-domain communication
- **AI Pipeline Integration**: Automated model training and deployment
- **Global CDN**: Distributed cache and content delivery
- **Plugin Ecosystem**: Third-party domain and provider integrations

### Extensibility Framework
- **Domain Plugin System**: Easy addition of new professional domains
- **Provider Plugin System**: Streamlined LLM provider integration
- **Custom Agent Framework**: User-defined agent creation
- **API Gateway**: External service integration and management
- **Marketplace**: Community-contributed domains and agents

---

This architecture provides a robust, scalable, and extensible foundation for multi-domain professional AI assistance while maintaining the flexibility to adapt to emerging technologies and use cases. The unified approach ensures consistency across domains while allowing for domain-specific optimizations and capabilities.

🌟 **Rich-Agents**: Unified Multi-Agent AI Toolkit - Empowering professionals across multiple domains with intelligent agent collaboration and enterprise-grade reliability.
