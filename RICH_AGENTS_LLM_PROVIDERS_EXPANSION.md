# Rich-Agents LLM提供商扩展支持

## 📋 概述

Rich-Agents现已支持多达13个LLM提供商，涵盖国内外主流大模型服务，为用户提供更多选择和更好的使用体验。

## 🌟 新增LLM提供商

### 🇨🇳 国产LLM提供商

#### 1. DeepSeek 深度求索
- **环境变量**: `DEEPSEEK_API_KEY`
- **API地址**: https://api.deepseek.com
- **支持模型**:
  - `deepseek-chat` - 通用对话模型
  - `deepseek-coder` - 代码专用模型
  - **`deepseek-reasoner` - 推理专用模型** ⭐
- **获取地址**: https://platform.deepseek.com/api_keys
- **特色**: 专业的推理能力，在数学和逻辑推理方面表现出色

#### 2. 通义千问 (Qianwen)
- **环境变量**: `QIANWEN_API_KEY`
- **API地址**: https://dashscope.aliyuncs.com/compatible-mode/v1
- **支持模型**:
  - `qwen2.5-72b-instruct` - 72B参数模型
  - `qwen2.5-32b-instruct` - 32B参数模型
  - `qwen2.5-14b-instruct` - 14B参数模型
  - `qwen2.5-7b-instruct` - 7B参数模型
- **获取地址**: https://help.aliyun.com/zh/dashscope/
- **特色**: 阿里云开源模型，多规格选择

#### 3. 火山引擎豆包 (Doubao)
- **环境变量**: `DOUBAO_API_KEY`
- **API地址**: https://ark.cn-beijing.volces.com/api/v3
- **支持模型**:
  - `doubao-pro-32k` - 专业版32K上下文
  - `doubao-pro-4k` - 专业版4K上下文
  - `doubao-lite-32k` - 轻量版32K上下文
  - `doubao-lite-4k` - 轻量版4K上下文
- **获取地址**: https://console.volcengine.com/ark
- **特色**: 字节跳动出品，在中文理解和生成方面表现优秀

#### 4. 智谱AI GLM
- **环境变量**: `ZHIPUAI_API_KEY`
- **API地址**: https://open.bigmodel.cn/api/paas/v4
- **支持模型**:
  - `glm-4` - GLM-4基础模型
  - `glm-4-plus` - GLM-4增强版
  - `glm-4-0520` - GLM-4特定版本
  - `glm-4-air` - GLM-4轻量版
  - `glm-4-airx` - GLM-4轻量增强版
  - `glm-4-flash` - GLM-4快速版
- **获取地址**: https://open.bigmodel.cn/usercenter/apikeys
- **特色**: 清华大学技术背景，在学术和专业领域表现出色

#### 5. 百川智能 (Baichuan)
- **环境变量**: `BAICHUAN_API_KEY`
- **API地址**: https://api.baichuan-ai.com/v1
- **支持模型**:
  - `baichuan2-turbo` - 百川2代Turbo版
  - `baichuan2-turbo-192k` - 百川2代192K上下文
  - `baichuan3-turbo` - 百川3代Turbo版
  - `baichuan3-turbo-128k` - 百川3代128K上下文
- **获取地址**: https://platform.baichuan-ai.com/console/apikey
- **特色**: 专注中文优化，在中文NLP任务上表现优异

#### 6. Moonshot AI Kimi
- **环境变量**: `MOONSHOT_API_KEY`
- **API地址**: https://api.moonshot.cn/v1
- **支持模型**:
  - `moonshot-v1-8k` - 8K上下文版本
  - `moonshot-v1-32k` - 32K上下文版本
  - **`moonshot-v1-128k` - 128K长上下文版本** ⭐
- **获取地址**: https://platform.moonshot.cn/console/api-keys
- **特色**: 超长上下文支持，适合处理长文档和复杂对话

#### 7. MiniMax 海螺
- **环境变量**: `MINIMAX_API_KEY`
- **API地址**: https://api.minimax.chat/v1
- **支持模型**:
  - `abab6.5s-chat` - ABAB 6.5S对话模型
  - `abab6.5-chat` - ABAB 6.5对话模型
  - `abab5.5s-chat` - ABAB 5.5S对话模型
  - `abab5.5-chat` - ABAB 5.5对话模型
- **获取地址**: https://api.minimax.chat/user-center/basic-information/interface-key
- **特色**: 在创意写作和角色扮演方面表现突出

#### 8. 零一万物 Yi
- **环境变量**: `YI_API_KEY`
- **API地址**: https://api.lingyiwanwu.com/v1
- **支持模型**:
  - `yi-34b-chat-0205` - Yi 34B对话模型
  - `yi-34b-chat-200k` - Yi 34B 200K上下文
  - `yi-6b-chat` - Yi 6B对话模型
  - **`yi-large` - Yi大型模型** ⭐
- **获取地址**: https://platform.lingyiwanwu.com/apikeys
- **特色**: 李开复团队打造，在多语言理解方面表现优秀

#### 9. 阶跃星辰 Step
- **环境变量**: `STEPFUN_API_KEY`
- **API地址**: https://api.stepfun.com/v1
- **支持模型**:
  - `step-1v-8k` - Step 1V 8K版本
  - `step-1v-32k` - Step 1V 32K版本
  - `step-2-16k` - Step 2代16K版本
- **获取地址**: https://platform.stepfun.com/interface-key
- **特色**: 在视觉理解和多模态任务方面有独特优势

## 🔧 配置方法

### 方法1: 环境变量配置 (推荐)

```bash
# 国产LLM提供商
export DEEPSEEK_API_KEY="sk-your-deepseek-key"
export QIANWEN_API_KEY="your-qianwen-key"
export DOUBAO_API_KEY="your-doubao-key"
export ZHIPUAI_API_KEY="your-zhipuai-key"
export BAICHUAN_API_KEY="sk-your-baichuan-key"
export MOONSHOT_API_KEY="sk-your-moonshot-key"
export MINIMAX_API_KEY="your-minimax-key"
export YI_API_KEY="your-yi-key"
export STEPFUN_API_KEY="your-stepfun-key"

# 国际LLM提供商
export OPENAI_API_KEY="sk-your-openai-key"
export GOOGLE_API_KEY="AIza-your-google-key"
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
export DASHSCOPE_API_KEY="sk-your-dashscope-key"
```

### 方法2: .env文件配置

在项目根目录创建`.env`文件：

```env
# 国产LLM提供商
DEEPSEEK_API_KEY=sk-your-deepseek-key
QIANWEN_API_KEY=your-qianwen-key
DOUBAO_API_KEY=your-doubao-key
ZHIPUAI_API_KEY=your-zhipuai-key
BAICHUAN_API_KEY=sk-your-baichuan-key
MOONSHOT_API_KEY=sk-your-moonshot-key
MINIMAX_API_KEY=your-minimax-key
YI_API_KEY=your-yi-key
STEPFUN_API_KEY=your-stepfun-key

# 国际LLM提供商
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=AIza-your-google-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
DASHSCOPE_API_KEY=sk-your-dashscope-key
```

### 方法3: Rich-Agents CLI配置

使用Rich-Agents的交互式配置界面：

```bash
# 启动Rich-Agents主界面
python cli/rich_agents_main.py

# 选择 "2. 🔧 系统配置"
# 选择 "1. 🔑 API密钥配置"
# 选择对应的LLM提供商进行配置
```

## 🎯 使用示例

### 在TradingAgent中使用

```python
from tradingagents.graph.trading_graph import create_trading_graph

# 使用DeepSeek模型
trading_graph = create_trading_graph(
    llm_provider="deepseek",
    llm_model="deepseek-chat",
    use_cache=True
)

# 使用智谱AI模型
trading_graph = create_trading_graph(
    llm_provider="zhipuai", 
    llm_model="glm-4",
    use_cache=True
)
```

### 在PatentAgent中使用

```python
from patentagents.graph.patent_graph import create_patent_graph

# 使用Moonshot长上下文模型处理专利文档
patent_graph = create_patent_graph(
    llm_provider="moonshot",
    llm_model="moonshot-v1-128k",
    use_cache=True
)

# 使用豆包模型
patent_graph = create_patent_graph(
    llm_provider="doubao",
    llm_model="doubao-pro-32k", 
    use_cache=True
)
```

## 📊 模型选择建议

### 按用途分类推荐

#### 🔬 科研学术类任务
- **推荐**: 智谱AI GLM-4、DeepSeek-Reasoner
- **理由**: 在学术推理和逻辑分析方面表现出色

#### 💼 商业分析类任务  
- **推荐**: 通义千问、百川智能
- **理由**: 在中文商业场景理解方面有优势

#### 📝 创意写作类任务
- **推荐**: MiniMax海螺、Moonshot Kimi
- **理由**: 在创意生成和长文本处理方面表现优异

#### 💻 编程开发类任务
- **推荐**: DeepSeek-Coder、智谱AI GLM-4
- **理由**: 专门针对代码生成和理解进行优化

#### 🌐 多语言任务
- **推荐**: 零一万物Yi、阶跃星辰Step
- **理由**: 在多语言理解和跨文化交流方面有优势

### 按成本效益推荐

#### 💰 高性价比选择
- **免费试用**: DeepSeek、智谱AI
- **低成本**: 通义千问、豆包轻量版

#### 🏆 高性能选择  
- **最佳性能**: Moonshot 128K、DeepSeek-Reasoner
- **平衡选择**: 百川3代、GLM-4-Plus

## 🔍 API密钥获取指南

| 提供商 | 获取链接 | 免费额度 | 特殊说明 |
|--------|----------|----------|----------|
| DeepSeek | [API Keys](https://platform.deepseek.com/api_keys) | 有免费额度 | 新用户注册即可获得 |
| 通义千问 | [DashScope](https://help.aliyun.com/zh/dashscope/) | 有免费额度 | 需要阿里云账号 |
| 豆包 | [火山引擎](https://console.volcengine.com/ark) | 有免费额度 | 需要企业认证 |
| 智谱AI | [开放平台](https://open.bigmodel.cn/usercenter/apikeys) | 有免费额度 | 实名认证后可用 |
| 百川智能 | [平台控制台](https://platform.baichuan-ai.com/console/apikey) | 有免费额度 | 需要手机验证 |
| Moonshot | [平台控制台](https://platform.moonshot.cn/console/api-keys) | 有免费额度 | 支持长上下文 |
| MiniMax | [用户中心](https://api.minimax.chat/user-center/basic-information/interface-key) | 有免费额度 | 需要实名认证 |
| 零一万物 | [平台控制台](https://platform.lingyiwanwu.com/apikeys) | 有免费额度 | 李开复团队 |
| 阶跃星辰 | [接口密钥](https://platform.stepfun.com/interface-key) | 有免费额度 | 多模态能力强 |

## 🛠️ 技术实现细节

### 统一适配器架构

Rich-Agents使用统一的LLM适配器架构，支持：

1. **自动API密钥检测**: 根据环境变量自动识别可用的LLM提供商
2. **统一接口调用**: 所有LLM提供商使用相同的调用接口
3. **智能错误处理**: 自动重试和错误恢复机制
4. **性能优化**: 连接池和缓存机制

### 配置管理

- **动态配置**: 支持运行时切换LLM提供商
- **配置验证**: 自动验证API密钥格式和可用性
- **配置导出**: 支持配置的导入导出功能

## 🚀 未来规划

### 即将支持的提供商
- **腾讯混元**: 腾讯云大模型服务
- **商汤日日新**: 商汤科技大模型
- **科大讯飞星火**: 讯飞星火认知大模型
- **华为盘古**: 华为云盘古大模型

### 功能增强
- **模型性能对比**: 自动测试和比较不同模型的性能
- **智能模型选择**: 根据任务类型自动推荐最适合的模型
- **成本优化**: 智能选择最经济的模型组合
- **多模型协作**: 支持多个模型协同工作

## 📞 技术支持

如果在使用过程中遇到问题，请：

1. 查看[配置帮助文档](RICH_AGENTS_CONFIG_ENHANCEMENT.md)
2. 检查API密钥是否正确配置
3. 确认网络连接和API服务状态
4. 提交Issue到GitHub仓库

---

**Rich-Agents团队致力于为用户提供最全面、最便捷的大模型服务支持！** 🌟 