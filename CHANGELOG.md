# Rich-Agents 更新日志

## [0.2.0] - 2025-01-XX - LLM提供商大扩展

### 🌟 重大新增
- **新增9个国产LLM提供商支持**:
  - DeepSeek 深度求索 (deepseek-chat, deepseek-coder, deepseek-reasoner)
  - 通义千问 Qianwen (qwen2.5系列多规格模型)
  - 火山引擎豆包 Doubao (pro/lite版本，支持4K/32K上下文)
  - 智谱AI GLM (glm-4系列6个模型)
  - 百川智能 Baichuan (baichuan2/3系列，支持192K/128K上下文)
  - Moonshot AI Kimi (支持128K超长上下文)
  - MiniMax 海螺 (abab系列对话模型)
  - 零一万物 Yi (yi-large等4个模型)
  - 阶跃星辰 Step (step-1v/step-2系列)

### 🔧 功能增强
- **CLI配置界面全面升级**:
  - 从8个API密钥配置选项扩展到17个
  - 分组显示：LLM提供商 vs 专用数据源
  - 新增API密钥格式验证规则
  - 增强的帮助链接和获取指南

- **配置管理器优化**:
  - 更新`_get_default_main_config()`支持13个LLM提供商
  - 增强API密钥验证逻辑
  - 新增模型描述和base_url配置
  - 完善错误处理和日志记录

- **统一LLM适配器重构**:
  - 支持所有新增LLM提供商的适配器创建
  - 统一的OpenAI兼容接口调用
  - 自动API密钥检测和模型列表生成
  - 智能错误处理和重试机制

### 📚 文档更新
- 新增 `RICH_AGENTS_LLM_PROVIDERS_EXPANSION.md` 详细文档
- 更新配置帮助内容，包含所有新增提供商
- 提供详细的API密钥获取指南
- 添加模型选择建议和使用示例

### 🎯 用户体验改进
- **分类显示**: LLM提供商按国内外分组展示
- **状态刷新**: 实时显示API密钥配置状态
- **智能提示**: 提供每个提供商的特色说明
- **一键配置**: 支持通过CLI快速配置所有API密钥

### 🛠️ 技术改进
- 统一的API调用接口，支持13个提供商
- 自动识别可用的LLM提供商
- 配置验证和格式检查
- 性能优化和缓存机制

### 📊 支持的模型统计
- **总计**: 13个LLM提供商，49个不同模型
- **国产提供商**: 9个 (DeepSeek, 通义千问, 豆包, 智谱AI, 百川, Moonshot, MiniMax, 零一万物, 阶跃星辰)
- **国际提供商**: 4个 (OpenAI, Google, Anthropic, 阿里云百炼)
- **特色模型**: 支持推理专用、代码专用、长上下文等特殊模型

### 🔗 API密钥获取链接
| 提供商 | 获取链接 | 免费额度 |
|--------|----------|----------|
| DeepSeek | https://platform.deepseek.com/api_keys | ✅ |
| 通义千问 | https://help.aliyun.com/zh/dashscope/ | ✅ |
| 豆包 | https://console.volcengine.com/ark | ✅ |
| 智谱AI | https://open.bigmodel.cn/usercenter/apikeys | ✅ |
| 百川智能 | https://platform.baichuan-ai.com/console/apikey | ✅ |
| Moonshot | https://platform.moonshot.cn/console/api-keys | ✅ |
| MiniMax | https://api.minimax.chat/user-center/basic-information/interface-key | ✅ |
| 零一万物 | https://platform.lingyiwanwu.com/apikeys | ✅ |
| 阶跃星辰 | https://platform.stepfun.com/interface-key | ✅ |

---

## [0.1.0] - 2025-01-XX - 初始版本

### ✨ 首次发布
- TradingAgent多智能体金融分析系统
- PatentAgent专利发现与分析系统
- 支持4个主流LLM提供商 (百炼、OpenAI、Google、Anthropic)
- Rich CLI交互界面
- 配置管理系统
- 缓存和数据持久化 