# Rich-Agents 包发布指南

本指南详细说明如何将Rich-Agents包发布到PyPI，并支持pip和uv两种安装方式。

## 📦 发布前准备

### 1. 环境准备

```bash
# 安装发布工具
pip install build twine

# 或使用uv
uv add --dev build twine
```

### 2. 版本管理

更新版本号在 `pyproject.toml` 中：

```toml
[project]
name = "rich-agents"
version = "0.1.0"  # 更新版本号
```

### 3. 文档检查

确保以下文件最新：
- [x] `README.md` - 项目描述和使用指南
- [x] `LICENSE` - MIT许可证
- [x] `pyproject.toml` - 包配置
- [x] `CHANGELOG.md` - 变更日志（可选）

## 🏗️ 构建包

### 1. 清理旧构建

```bash
# 清理旧的构建文件
rm -rf build/ dist/ *.egg-info/
```

### 2. 构建包

```bash
# 使用build工具构建
python -m build

# 或使用uv构建
uv build
```

构建完成后，会在 `dist/` 目录生成：
- `rich-agents-0.1.0.tar.gz` (源码包)
- `rich_agents-0.1.0-py3-none-any.whl` (wheel包)

### 3. 验证包

```bash
# 检查包的完整性
twine check dist/*

# 本地测试安装
pip install dist/rich-agents-0.1.0.tar.gz
```

## 🚀 发布到PyPI

### 1. 配置PyPI凭证

```bash
# 配置PyPI凭证
# 方法1: 使用.pypirc文件
cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
EOF

# 方法2: 使用环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here
```

### 2. 先发布到测试PyPI

```bash
# 发布到测试PyPI
twine upload --repository testpypi dist/*

# 从测试PyPI安装验证
pip install --index-url https://test.pypi.org/simple/ rich-agents
```

### 3. 发布到正式PyPI

```bash
# 发布到正式PyPI
twine upload dist/*
```

## 📋 发布检查清单

### 发布前检查
- [ ] 代码测试通过 (`pytest tests/`)
- [ ] 文档更新完整
- [ ] 版本号已更新
- [ ] 变更日志已更新
- [ ] 依赖关系正确
- [ ] 许可证文件存在

### 发布后验证
- [ ] PyPI页面显示正常
- [ ] 包可以正常安装
- [ ] 基本功能测试通过
- [ ] 文档链接正确

## 🔧 支持uv安装

Rich-Agents已配置为完全支持uv安装方式：

### 1. 基础安装

```bash
# 使用uv安装
uv add rich-agents

# 或全局安装
uv tool install rich-agents
```

### 2. 可选依赖安装

```bash
# 安装所有功能
uv add "rich-agents[all]"

# 按需安装
uv add "rich-agents[trading]"
uv add "rich-agents[patent]"
uv add "rich-agents[chinese]"
uv add "rich-agents[database]"
uv add "rich-agents[visualization]"
```

### 3. 开发环境

```bash
# 开发环境安装
uv add "rich-agents[development]"

# 从源码安装
uv add --editable .
```

## 📊 包配置详解

### pyproject.toml 关键配置

```toml
[project]
name = "rich-agents"
version = "0.1.0"
description = "Rich-Agents: 统一多智能体AI工具集"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}

# 作者信息
authors = [
    {name = "TauricResearch Team", email = "research@tauric.ai"},
]

# 关键词和分类
keywords = [
    "artificial-intelligence",
    "multi-agent",
    "trading",
    "patent",
    "llm"
]

# PyPI分类器
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

# 可选依赖
[project.optional-dependencies]
trading = ["yfinance>=0.2.63", "finnhub-python>=2.4.23"]
patent = ["google-search-results>=2.4.2"]
all = ["yfinance>=0.2.63", "google-search-results>=2.4.2"]

# 命令行工具
[project.scripts]
rich-agents = "cli.rich_agents_main:app"
trading-agent = "cli.trading_cli:main"
patent-agent = "cli.patent_cli:main"

# 项目链接
[project.urls]
Homepage = "https://github.com/TauricResearch/TradingAgents"
Repository = "https://github.com/TauricResearch/TradingAgents"
Issues = "https://github.com/TauricResearch/TradingAgents/issues"
```

## 🔄 自动化发布

### GitHub Actions工作流

创建 `.github/workflows/release.yml`:

```yaml
name: Release to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

### 版本标签

```bash
# 创建版本标签
git tag v0.1.0
git push origin v0.1.0

# 在GitHub创建Release
# 这将触发自动发布流程
```

## 🎯 发布后推广

### 1. 社区分享

- [ ] 在GitHub发布Release Notes
- [ ] 在相关技术社区分享
- [ ] 更新项目文档
- [ ] 通知用户升级

### 2. 监控反馈

- [ ] 监控PyPI下载统计
- [ ] 收集用户反馈
- [ ] 跟踪GitHub Issues
- [ ] 持续改进文档

## 📈 版本管理策略

### 语义化版本控制

- `MAJOR.MINOR.PATCH` (如 1.0.0)
- `MAJOR`: 不兼容的API更改
- `MINOR`: 向后兼容的功能添加
- `PATCH`: 向后兼容的错误修复

### 发布周期

- **Alpha**: 内部测试版本 (0.1.0a1)
- **Beta**: 公开测试版本 (0.1.0b1)
- **Release Candidate**: 发布候选 (0.1.0rc1)
- **Stable**: 稳定版本 (0.1.0)

## 🛠️ 故障排除

### 常见问题

1. **构建失败**
   ```bash
   # 检查pyproject.toml语法
   python -m build --check
   ```

2. **上传失败**
   ```bash
   # 检查包完整性
   twine check dist/*
   ```

3. **依赖冲突**
   ```bash
   # 检查依赖兼容性
   pip-compile pyproject.toml
   ```

### 调试技巧

```bash
# 详细构建日志
python -m build --verbose

# 详细上传日志
twine upload --verbose dist/*

# 检查包内容
tar -tzf dist/rich-agents-0.1.0.tar.gz
```

---

**发布Rich-Agents，让AI多智能体技术惠及更多开发者！** 🚀✨ 