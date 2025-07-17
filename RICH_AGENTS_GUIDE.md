# Rich-Agents 使用指南

## 📋 概述

Rich-Agents是基于 TradingAgents成功架构扩展的统一多智能体AI工具集，目前支持两个专业领域：

- 🏦 **TradingAgent**: 金融交易分析框架
- 🔬 **PatentAgent**: 专利智能体系统

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/chenxingqiang/Rich-Agents.git
cd Rich-Agents

# 创建虚拟环境
conda create -n rich-agents python=3.10+
conda activate rich-agents

# 安装基础依赖
pip install -r requirements.txt
```

### 2. 配置API密钥

Rich-Agents需要配置LLM提供商的API密钥。在`.env`文件或环境变量中设置：

```bash
# LLM提供商 (至少配置一个)
export DASHSCOPE_API_KEY=your_dashscope_api_key      # 百炼大模型 (推荐)
export OPENAI_API_KEY=your_openai_api_key            # OpenAI
export GOOGLE_API_KEY=your_google_api_key            # Google Gemini
export ANTHROPIC_API_KEY=your_anthropic_api_key      # Anthropic Claude

# TradingAgent专用
export FINNHUB_API_KEY=your_finnhub_api_key          # 金融数据

# PatentAgent专用
export SERPAPI_API_KEY=your_serpapi_api_key          # Google Patents
export ZHIHUIYA_CLIENT_ID=your_zhihuiya_client_id    # 智慧芽客户端ID
export ZHIHUIYA_CLIENT_SECRET=your_zhihuiya_secret   # 智慧芽客户端密钥
```

### 3. 启动Rich-Agents

```bash
# 启动统一CLI界面
python main.py

# 或者直接启动特定智能体
python main.py --agent trading    # 直接启动TradingAgent
python main.py --agent patent     # 直接启动PatentAgent
```

## 🏦 TradingAgent - 金融交易分析

### 功能特色

- **多智能体协作**: 市场分析师、情绪分析师、新闻分析师、基本面分析师
- **支持多市场**: 美股市场、中国A股市场
- **风险管理**: 专业的风险评估和投资组合管理
- **实时数据**: 集成多个金融数据源

### 使用方法

#### 1. 通过Rich-Agents统一界面

```bash
python main.py
# 选择: 1. 🏦 TradingAgent
```

#### 2. 直接启动TradingAgent

```bash
# 使用传统CLI
python -m cli.main

# 或通过Rich-Agents
python main.py --agent trading
```

#### 3. 编程方式使用

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 创建配置
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "dashscope"
config["deep_think_llm"] = "qwen-max"
config["quick_think_llm"] = "qwen-turbo"

# 初始化TradingAgent
ta = TradingAgentsGraph(debug=True, config=config)

# 执行分析
_, decision = ta.propagate("AAPL", "2024-12-01")
print(decision)
```

### 支持的市场

1. **美股市场**
   - 格式: 字母代码 (如 AAPL, MSFT, TSLA)
   - 数据源: Yahoo Finance, FinnHub

2. **中国A股市场**
   - 格式: 6位数字代码 (如 000001, 600036)
   - 数据源: 通达信API, AKShare

## 🔬 PatentAgent - 专利智能体

### 功能特色

- **技术创新发现**: 自动识别技术领域的创新机会
- **专利可行性验证**: 深度分析专利申请的成功概率
- **专利价值分析**: 评估专利的技术价值和商业价值
- **专利申请撰写**: 生成符合专利局标准的申请文档

### 使用方法

#### 1. 通过Rich-Agents统一界面

```bash
python main.py
# 选择: 2. 🔬 PatentAgent
```

#### 2. 直接启动PatentAgent

```bash
python main.py --agent patent
```

#### 3. 编程方式使用

```python
from shared.config.rich_agents_config_manager import RichAgentsConfigManager
from cli.patent_cli import PatentAgentCLI

# 创建PatentAgent CLI
config_manager = RichAgentsConfigManager()
patent_cli = PatentAgentCLI(config_manager)

# 运行专利分析
patent_cli.run()
```

### 专利分析类型

1. **技术创新发现** (`discovery`)
   - 识别技术空白
   - 发现创新机会
   - 跨领域技术融合

2. **专利可行性验证** (`validation`)
   - 先行技术检索
   - 侵权风险评估
   - 授权概率预测

3. **专利价值分析** (`analysis`)
   - 技术价值评估
   - 商业价值分析
   - 市场竞争分析

4. **专利申请撰写** (`writing`)
   - 技术交底书
   - 权利要求书
   - 说明书撰写

## ⚙️ 配置管理

### 配置文件位置

Rich-Agents会在项目根目录的`config/`文件夹中自动创建配置文件：

- `config/rich_agents_config.json` - 主配置文件
- `config/trading_config.json` - TradingAgent配置
- `config/patent_config.json` - PatentAgent配置

### 主要配置项

#### LLM提供商配置

```json
{
  "llm_providers": {
    "dashscope": {
      "api_key_env": "DASHSCOPE_API_KEY",
      "models": ["qwen-turbo", "qwen-plus", "qwen-max"],
      "default_model": "qwen-turbo"
    },
    "openai": {
      "api_key_env": "OPENAI_API_KEY", 
      "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
      "default_model": "gpt-4o-mini"
    }
  }
}
```

#### TradingAgent配置

```json
{
  "agent_type": "trading",
  "max_debate_rounds": 2,
  "analysts": ["market", "social", "news", "fundamentals"],
  "markets": {
    "us_stock": {"enabled": true},
    "china_a_share": {"enabled": true}
  }
}
```

#### PatentAgent配置

```json
{
  "agent_type": "patent",
  "analysis_types": ["discovery", "validation", "analysis", "writing"],
  "patent_databases": {
    "google_patents": {"enabled": true, "priority": 1},
    "zhihuiya": {"enabled": true, "priority": 2}
  }
}
```

## 🔧 选择性安装

根据需要安装特定功能模块：

```bash
# 仅安装TradingAgent模块
pip install -e ".[trading]"

# 仅安装PatentAgent模块
pip install -e ".[patent]"

# 安装中文市场支持
pip install -e ".[chinese]"

# 安装数据库支持 (MongoDB + Redis)
pip install -e ".[database]"

# 安装可视化支持
pip install -e ".[visualization]"

# 安装开发工具
pip install -e ".[development]"

# 安装所有功能
pip install -e ".[all]"
```

## 🗄️ 数据库支持 (可选)

Rich-Agents支持MongoDB和Redis用于数据缓存和存储：

### 启用数据库

```bash
# 启动MongoDB
docker run -d -p 27017:27017 --name mongodb mongo

# 启动Redis  
docker run -d -p 6379:6379 --name redis redis

# 在环境变量中启用
export MONGODB_ENABLED=true
export REDIS_ENABLED=true
```

### 配置数据库

```json
{
  "cache": {
    "enabled": true,
    "type": "integrated",
    "mongodb": {
      "enabled": true,
      "host": "localhost",
      "port": 27017,
      "database": "rich_agents"
    },
    "redis": {
      "enabled": true,
      "host": "localhost", 
      "port": 6379,
      "db": 0
    }
  }
}
```

## 🔍 系统状态检查

通过Rich-Agents CLI可以检查系统状态：

```bash
python main.py
# 选择: 3. ⚙️ 系统配置
```

或者编程方式：

```python
from shared.config.rich_agents_config_manager import RichAgentsConfigManager

config_manager = RichAgentsConfigManager()

# 检查系统状态
status = config_manager.get_system_status()
print(f"可用智能体: {status['available_agents']}")
print(f"LLM提供商: {status['available_llm_providers']}")

# 检查API密钥状态
api_status = config_manager.check_api_keys()
for api, configured in api_status.items():
    status_text = "✅ 已配置" if configured else "❌ 未配置"
    print(f"{api}: {status_text}")

# 验证配置
validation = config_manager.validate_config()
if validation["valid"]:
    print("✅ 配置有效")
else:
    print("❌ 配置存在问题")
    for error in validation["errors"]:
        print(f"  - {error}")
```

## 🧪 运行测试

```bash
# 运行基础功能测试
python tests/test_rich_agents_simple.py

# 如果安装了pytest，可以运行完整测试
pytest tests/
```

## 📝 开发指南

### 项目结构

```
Rich-Agents/
├── shared/                    # 共享基础设施
│   ├── config/               # 统一配置管理
│   ├── llm_adapters/         # 统一LLM适配器
│   ├── cache/                # 统一缓存系统
│   └── utils/                # 通用工具
├── tradingagents/            # TradingAgent模块
├── patentagents/             # PatentAgent模块 (开发中)
├── cli/                      # CLI界面
│   ├── rich_agents_main.py   # 统一CLI入口
│   ├── trading_cli.py        # TradingAgent CLI适配器
│   └── patent_cli.py         # PatentAgent CLI适配器
├── config/                   # 配置文件目录
├── tests/                    # 测试文件
└── main.py                   # 主入口文件
```

### 扩展新的智能体

1. 在相应目录创建智能体模块
2. 在`shared/config/`中添加配置
3. 在`cli/`中创建CLI适配器
4. 在`cli/rich_agents_main.py`中注册新智能体

### 添加新的LLM提供商

1. 在`shared/llm_adapters/unified_llm_adapter.py`中添加适配器
2. 在配置中添加提供商信息
3. 更新环境变量配置

## 🚧 故障排除

### 常见问题

1. **导入错误**
   ```bash
   # 确保在项目根目录
   cd Rich-Agents
   
   # 确保Python路径正确
   export PYTHONPATH=$PWD:$PYTHONPATH
   ```

2. **API密钥错误**
   ```bash
   # 检查环境变量
   echo $DASHSCOPE_API_KEY
   
   # 或通过系统状态检查
   python main.py  # 选择系统配置
   ```

3. **依赖缺失**
   ```bash
   # 重新安装依赖
   pip install -r requirements.txt
   
   # 或安装完整功能
   pip install -e ".[all]"
   ```

4. **配置文件问题**
   ```bash
   # 删除配置文件重新生成
   rm -rf config/
   python main.py
   ```

### 日志调试

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 然后运行Rich-Agents
```

## 🔮 未来规划

### 即将推出

- **WebAgent**: 网页自动化和数据抓取智能体
- **CodeAgent**: 代码分析和自动编程智能体
- **ResearchAgent**: 学术研究和论文分析智能体

### 长期规划

- 支持更多LLM提供商
- 可视化界面 (Web UI)
- 智能体市场和插件系统
- 多语言支持

## 📞 技术支持

- **GitHub Issues**: 报告Bug和功能请求
- **文档**: 查看最新文档和示例
- **社区**: 加入开发者社区交流

## 📄 许可证

Rich-Agents基于Apache 2.0许可证开源，欢迎贡献代码！

---

**🎉 恭喜！您已经掌握了Rich-Agents的使用方法。开始您的多智能体AI之旅吧！** 