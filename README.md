
---

# Rich-Agents: 统一多智能体AI工具集

> 🎉 **Rich-Agents** - 基于TradingAgents成功架构扩展的统一多智能体AI工具集
>
> 当前支持两个专业领域：**TradingAgent**（金融交易分析）和**PatentAgent**（专利智能体系统）

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

🚀 [快速开始](#快速开始) | 📦 [安装指南](#安装指南) | 🏦 [TradingAgent](#tradingagent-金融交易分析) | 🔬 [PatentAgent](#patentagent-专利智能体) | 🤝 [贡献](#contributing) | 📄 [引用](#citation)

</div>

## 🌟 Rich-Agents 框架概览

Rich-Agents是一个统一的多智能体AI工具集，采用模块化架构设计，支持多个专业领域：

### 🏦 TradingAgent - 金融交易分析框架
基于真实交易公司的运作模式，通过专业的LLM驱动智能体协作：基本面分析师、情绪专家、技术分析师、交易员、风险管理团队等，共同评估市场条件并做出交易决策。

### 🔬 PatentAgent - 专利智能体系统  
将AI技术深度应用于知识产权领域，提供专利发现、验证、分析与撰写的完整解决方案。通过技术分析师、创新发现师、先行技术研究员、专利撰写员等智能体协作，实现从创新发现到专利申请的全流程自动化。

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> ⚠️ **免责声明**: TradingAgents框架仅用于研究目的。交易表现可能因多种因素而异，包括所选的语言模型、模型温度、交易周期、数据质量和其他非确定性因素。[本框架不构成财务、投资或交易建议。](https://tauric.ai/disclaimer/)

## 🚀 快速开始

### 基础安装
```bash
# 克隆仓库
git clone https://github.com/chenxingqiang/TradingAgents.git
cd TradingAgents

# 基础安装
pip install -e .

# 或使用uv安装（推荐）
uv sync
```

### 启动Rich-Agents
```bash
# 启动统一CLI界面
rich-agents

# 或直接运行
python main.py
```

### 选择智能体系统
```
🎯 欢迎使用 Rich-Agents 多智能体AI工具集！

请选择您要使用的智能体系统：
1. 🏦 TradingAgent - 金融交易分析
2. 🔬 PatentAgent - 专利智能体 
3. ⚙️  系统配置和状态检查
4. 📖 查看使用指南

请输入您的选择 (1-4): 
```

## 📦 安装指南

Rich-Agents支持多种安装方式，您可以根据需要选择：

### 1. 完整安装（推荐）
```bash
# 安装所有功能
pip install -e ".[all]"

# 或使用uv
uv sync --all-extras
```

### 2. 按需安装
```bash
# 仅安装TradingAgent
pip install -e ".[trading]"

# 仅安装PatentAgent
pip install -e ".[patent]"

# 安装中文市场支持
pip install -e ".[chinese]"

# 安装数据库支持
pip install -e ".[database]"

# 安装可视化支持
pip install -e ".[visualization]"
```

### 3. 开发环境安装
```bash
# 开发环境（包含测试工具）
pip install -e ".[development]"

# 运行测试
pytest tests/
```

### 4. 使用uv安装（推荐）
```bash
# 安装uv
pip install uv

# 使用uv安装项目
uv sync

# 选择性安装
uv sync --extra trading
uv sync --extra patent
uv sync --extra all
```

## 🏦 TradingAgent - 金融交易分析

### 核心智能体团队

#### 分析师团队
- **基本面分析师**: 评估公司财务和业绩指标，识别内在价值和潜在风险
- **情绪分析师**: 分析社交媒体和公众情绪，使用情绪评分算法评估短期市场情绪
- **新闻分析师**: 监控全球新闻和宏观经济指标，解读事件对市场状况的影响
- **技术分析师**: 利用技术指标（如MACD和RSI）检测交易模式并预测价格走势

#### 研究团队
- **多头研究员**: 专注于发现买入机会，构建看涨论证
- **空头研究员**: 识别卖出信号，构建看跌论证
- **研究经理**: 协调研究活动，整合不同观点

#### 交易执行团队
- **交易员**: 基于分析团队的建议执行交易决策
- **风险管理员**: 监控投资组合风险，确保风险控制

### 使用示例
```bash
# 启动TradingAgent
rich-agents
# 选择选项1: TradingAgent

# 或直接使用TradingAgent CLI
python -m cli.trading_cli
```

### 支持的数据源
- **美国市场**: Yahoo Finance, Finnhub, EODHD
- **中国市场**: AkShare, Tushare, TDX
- **新闻数据**: Google News, Reddit, 实时新闻API
- **社交媒体**: Twitter情绪分析, Reddit讨论分析

## 🔬 PatentAgent - 专利智能体

### 核心功能

#### 1. 专利发现
- **技术趋势分析**: 基于专利数据和文献分析技术发展趋势
- **创新空白识别**: 自动发现技术领域中的专利空白
- **交叉领域创新**: 识别跨领域技术融合的创新机会

#### 2. 专利验证
- **先行技术检索**: 全面检索相关专利和技术文献
- **可行性评估**: 评估专利申请的技术可行性
- **侵权风险分析**: 评估专利申请的侵权风险

#### 3. 专利分析
- **专利价值评估**: 多维度评估专利的技术和商业价值
- **竞争态势分析**: 分析技术领域的专利竞争格局
- **专利族分析**: 追踪专利家族的全球布局

#### 4. 专利撰写
- **权利要求生成**: 自动生成多层次的权利要求
- **技术描述优化**: 确保技术描述的准确性和完整性
- **文档格式化**: 符合专利局标准的申请文档

### 智能体团队

#### 分析师团队
- **技术分析师**: 分析目标技术领域的发展趋势和技术成熟度
- **创新发现师**: 从技术动态和学术论文中发现潜在创新点
- **先行技术研究员**: 深度检索相关专利和技术文献
- **市场情报分析师**: 分析技术的商业价值和市场接受度

#### 研究团队
- **创新推进研究员**: 论证创新方案的技术优势和实施可行性
- **风险评估研究员**: 识别技术风险和专利侵权风险
- **专利策略管理员**: 综合分析，制定专利申请策略

#### 执行团队
- **专利撰写员**: 基于分析结果撰写高质量专利申请文档
- **质量评估师**: 评估专利申请的质量和获权可能性

### 使用示例
```bash
# 启动PatentAgent
rich-agents
# 选择选项2: PatentAgent

# 技术领域示例
技术领域: 人工智能
技术方向: 计算机视觉
创新主题: 深度学习图像识别
```

### 支持的数据源
- **专利数据库**: Google Patents, USPTO, EPO, 智慧芽
- **学术文献**: IEEE Xplore, ACM Digital Library, arXiv
- **技术新闻**: TechCrunch, MIT Technology Review
- **行业报告**: Gartner, IDC技术趋势报告

## ⚙️ 配置管理

Rich-Agents使用统一的配置管理系统，支持多种LLM提供商：

### 支持的LLM提供商
- **百炼(通义千问)**: 阿里云百炼平台
- **OpenAI**: GPT-3.5, GPT-4系列
- **Google**: Gemini Pro, Gemini Ultra
- **Anthropic**: Claude 3系列

### 配置文件
```bash
# 查看配置状态
rich-agents
# 选择选项3: 系统配置和状态检查

# 配置文件位置
~/.rich_agents/config.json
```

### 环境变量配置
```bash
# LLM API密钥
export DASHSCOPE_API_KEY="your_dashscope_key"
export OPENAI_API_KEY="your_openai_key"
export GOOGLE_API_KEY="your_google_key"
export ANTHROPIC_API_KEY="your_anthropic_key"

# 数据源API密钥
export FINNHUB_API_KEY="your_finnhub_key"
export EODHD_API_KEY="your_eodhd_key"
export SERPAPI_API_KEY="your_serpapi_key"
export ZHIHUIYA_API_KEY="your_zhihuiya_key"
```

## 🏗️ 架构设计

### 统一架构
```
Rich-Agents/
├── shared/                 # 共享基础设施
│   ├── config/            # 统一配置管理
│   └── llm_adapters/      # 统一LLM适配器
├── cli/                   # 统一CLI系统
│   ├── rich_agents_main.py    # 主CLI入口
│   ├── rich_agents_simple.py  # 简化CLI
│   ├── trading_cli.py          # TradingAgent CLI
│   └── patent_cli.py           # PatentAgent CLI
├── tradingagents/         # TradingAgent模块
├── patentagents/          # PatentAgent模块
└── tests/                 # 测试套件
```

### 模块化设计
- **共享基础设施**: 配置管理、LLM适配器、缓存系统
- **独立智能体模块**: 每个智能体系统独立开发和维护
- **统一CLI界面**: 提供一致的用户体验
- **可扩展架构**: 支持未来添加新的智能体系统

## 🧪 测试

Rich-Agents包含完整的测试套件：

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_rich_agents_integration.py
pytest tests/test_trading_agents.py
pytest tests/test_patent_agents.py

# 查看测试覆盖率
pytest --cov=. tests/
```

## 📚 文档

- [快速开始指南](docs/zh-CN/quick_start_guide.md)
- [架构指南](docs/zh-CN/architecture_guide.md)
- [配置指南](docs/zh-CN/configuration_guide.md)
- [API参考](docs/zh-CN/api_reference.md)

## 🤝 Contributing

我们欢迎社区贡献！请查看[贡献指南](CONTRIBUTING.md)了解如何参与：

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 Citation

如果您在研究中使用了Rich-Agents，请引用：

```bibtex
@software{rich_agents_2025,
  title={Rich-Agents: A Unified Multi-Agent AI Toolkit},
  author={Turingai Team},
  year={2025},
  url={https://github.com/chenxingqiang/TradingAgents}
}
```

## 📝 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 🙏 致谢

感谢所有为Rich-Agents项目做出贡献的开发者和研究人员。

---

<div align="center">
Made with ❤️ by Turingai Team
</div>
