# Rich-Agents 交互式配置功能增强

## 📋 功能概述

Rich-Agents现已支持完整的交互式系统配置功能，用户可以在使用过程中方便地配置API密钥和系统设置，无需手动编辑配置文件或环境变量。

## ✨ 新增功能

### 🔑 交互式API密钥配置

#### 支持的API密钥
1. **LLM提供商** (至少配置一个)
   - 百炼大模型 (DashScope) - `DASHSCOPE_API_KEY`
   - OpenAI GPT - `OPENAI_API_KEY`
   - Google Gemini - `GOOGLE_API_KEY`
   - Anthropic Claude - `ANTHROPIC_API_KEY`

2. **TradingAgent专用**
   - Finnhub金融数据 - `FINNHUB_API_KEY`

3. **PatentAgent专用**
   - SerpApi Google Patents - `SERPAPI_API_KEY`
   - 智慧芽客户端ID - `ZHIHUIYA_CLIENT_ID`
   - 智慧芽客户端密钥 - `ZHIHUIYA_CLIENT_SECRET`

#### 配置功能
- ✅ **设置API密钥** - 添加或更新API密钥
- ✅ **测试API密钥** - 验证API密钥格式和可用性
- ✅ **删除API密钥** - 安全删除已配置的API密钥
- ✅ **复制配置命令** - 生成环境变量设置命令
- ✅ **格式验证** - 自动验证API密钥格式
- ✅ **帮助链接** - 提供获取API密钥的直接链接

### 🏦 TradingAgent配置管理

- 📊 **数据源配置** - 配置金融数据API
- 🏛️ **市场设置** - 设置默认分析市场
- 🧠 **智能体设置** - 配置分析师和研究员
- 🔄 **重置为默认** - 恢复默认配置

### 🔬 PatentAgent配置管理

- 🔍 **专利数据源** - 配置专利检索API
- 🧠 **AI分析服务** - 配置智慧芽等AI服务
- 🎯 **分析类型** - 设置默认分析类型
- 🔄 **重置为默认** - 恢复默认配置

### 💾 缓存配置管理

- 🔄 **启用/禁用缓存** - 控制缓存开关
- 🗄️ **配置MongoDB** - MongoDB连接设置
- ⚡ **配置Redis** - Redis连接设置
- 🧹 **清理缓存** - 清理所有缓存数据

### 🛠️ 系统管理功能

- 🔄 **重新加载配置** - 刷新所有配置文件
- 📋 **导出配置** - 保存当前配置到文件
- 📖 **配置帮助** - 查看详细配置指南
- 🔍 **配置验证** - 检查配置完整性和有效性

## 🎯 使用方法

### 1. 启动配置中心

```bash
# 方法1: 通过主界面
python main.py
# 选择 "3. ⚙️ 系统配置"

# 方法2: 直接运行配置CLI
python -c "from cli.rich_agents_main import RichAgentsCLI; cli = RichAgentsCLI(); cli.show_system_config()"
```

### 2. 配置界面导航

```
⚙️ Rich-Agents 系统配置中心
======================================================================

🏠 系统信息:
  版本: v0.1.0
  可用智能体: TradingAgent, PatentAgent
  LLM提供商: dashscope, openai, google, anthropic
  配置目录: /path/to/config

🔑 API密钥状态:
  dashscope_api: ❌ 未配置 - 百炼大模型 (阿里云) - [获取链接]
  openai_api: ✅ 已配置 - OpenAI GPT模型 - [获取链接]
  ...

💾 缓存配置:
  缓存启用: ✅ 启用
  缓存类型: file
  MongoDB: ❌ 未连接
  Redis: ❌ 未连接

🔍 配置验证:
  ✅ 所有配置都有效

🛠️ 配置选项:
1. 🔑 配置API密钥 - 添加或更新API密钥
2. 🏦 TradingAgent配置 - 金融数据源和LLM设置
3. 🔬 PatentAgent配置 - 专利数据源和AI设置
4. 💾 缓存配置 - MongoDB和Redis设置
5. 🔄 重新加载配置 - 刷新所有配置文件
6. 📋 导出配置 - 保存当前配置到文件
7. 📖 配置帮助 - 查看详细配置指南
8. 🚪 返回主菜单 - 退出配置中心
```

### 3. API密钥配置示例

```
🔧 配置 百炼大模型 (DashScope)
----------------------------------------

API信息:
• 名称: 百炼大模型 (DashScope)
• 环境变量: DASHSCOPE_API_KEY
• 描述: 阿里云百炼大模型服务，支持通义千问等模型
• 帮助文档: https://help.aliyun.com/zh/dashscope/
• 格式示例: sk-xxx...xxx

当前值: sk-1234567...abcd

配置选项:
1. 🔑 设置新的API密钥
2. 🔍 测试当前API密钥
3. 🗑️ 删除API密钥
4. 📋 复制配置命令
5. 🚪 返回
```

## 🔧 技术实现

### 配置管理器增强

在 `shared/config/rich_agents_config_manager.py` 中新增了以下方法：

```python
def set_api_key(self, env_var: str, api_key: str) -> bool
def delete_api_key(self, env_var: str) -> bool
def test_api_key(self, env_var: str) -> Dict[str, Any]
def get_cache_config(self) -> Dict[str, Any]
def export_config(self, export_path: Optional[Union[str, Path]] = None) -> str
def reload_config(self) -> bool
def reset_config(self, config_type: str) -> bool
```

### CLI界面增强

#### Rich版本 (`cli/rich_agents_main.py`)
- 美观的表格和面板布局
- 颜色主题和图标
- 实时状态更新
- 链接支持

#### 简化版本 (`cli/rich_agents_simple.py`)
- 纯文本界面
- 基本功能完整
- 兼容性好
- 轻量级

### API密钥验证

```python
def _validate_api_key_format(self, env_var: str, key: str) -> bool:
    validation_rules = {
        "DASHSCOPE_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
        "OPENAI_API_KEY": lambda k: k.startswith("sk-") and len(k) > 20,
        "GOOGLE_API_KEY": lambda k: k.startswith("AIza") and len(k) > 30,
        "ANTHROPIC_API_KEY": lambda k: k.startswith("sk-ant-") and len(k) > 30,
        # ...
    }
```

## 📖 配置帮助

### 环境变量设置方法

#### 方法1: 临时设置 (当前会话)
```bash
export DASHSCOPE_API_KEY="your_api_key_here"
export OPENAI_API_KEY="your_api_key_here"
```

#### 方法2: 永久设置 (添加到shell配置)
```bash
echo 'export DASHSCOPE_API_KEY="your_api_key_here"' >> ~/.bashrc
echo 'export OPENAI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### 方法3: .env文件
```bash
# 在项目根目录创建.env文件
cat > .env << EOF
DASHSCOPE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
FINNHUB_API_KEY=your_api_key_here
SERPAPI_API_KEY=your_api_key_here
ZHIHUIYA_CLIENT_ID=your_client_id
ZHIHUIYA_CLIENT_SECRET=your_client_secret
EOF
```

### API密钥获取链接

| API | 获取地址 | 免费额度 |
|-----|----------|----------|
| 百炼 (DashScope) | https://help.aliyun.com/zh/dashscope/ | 有限免费额度 |
| OpenAI GPT | https://platform.openai.com/api-keys | $5 免费额度 |
| Google Gemini | https://ai.google.dev/gemini-api/docs/api-key | 免费额度 |
| Anthropic Claude | https://console.anthropic.com/ | 有限免费额度 |
| Finnhub | https://finnhub.io/dashboard | 60次/分钟免费 |
| SerpApi | https://serpapi.com/manage-api-key | 100次/月免费 |
| 智慧芽 | https://open-zhihuiya-com.libproxy1.nus.edu.sg/ | 企业服务 |

## 💡 最佳实践

### 安全建议
1. **保护API密钥安全** - 不要在代码中硬编码API密钥
2. **定期轮换密钥** - 定期更换API密钥增强安全性
3. **最小权限原则** - 只授予必要的API权限
4. **监控使用情况** - 定期检查API配额和使用情况

### 配置建议
1. **至少配置一个LLM提供商** - 确保基本功能可用
2. **根据需求配置专用API** - TradingAgent需要Finnhub，PatentAgent需要SerpApi
3. **启用缓存** - 提高性能和减少API调用
4. **定期备份配置** - 使用导出功能备份配置

### 故障排除
1. **API密钥格式错误** → 检查格式是否正确
2. **网络连接失败** → 检查网络和防火墙设置
3. **配额不足** → 检查API使用限额
4. **权限错误** → 确认API密钥权限设置

## 🚀 未来规划

### 即将推出的功能
- [ ] **可视化配置界面** - Web界面配置
- [ ] **配置模板** - 预设配置模板
- [ ] **批量配置** - 批量导入/导出配置
- [ ] **配置同步** - 多设备配置同步
- [ ] **高级缓存配置** - 更细粒度的缓存控制
- [ ] **API使用统计** - 实时API使用情况监控

### 长期目标
- [ ] **云端配置管理** - 云端配置存储和同步
- [ ] **团队配置共享** - 团队配置管理和权限控制
- [ ] **自动配置优化** - AI驱动的配置优化建议
- [ ] **配置版本控制** - 配置变更历史和回滚

## 📞 技术支持

如需帮助，请访问：
- **GitHub Issues**: https://github.com/TauricResearch/TradingAgents/issues
- **文档**: https://github.com/TauricResearch/TradingAgents/wiki
- **讨论区**: https://github.com/TauricResearch/TradingAgents/discussions

---

**Rich-Agents v0.1.0** - 让AI配置变得简单而强大！ 🎉✨ 