# PatentAgent 目标文件

## 📋 项目概述

**目标**: 将现有的TradingAgent多智能体金融分析系统改造为PatentAgent专利发现、验证、分析与撰写系统。保持原有的多智能体协作架构，但将核心功能从金融交易分析转向专利创新发现与知识产权管理。

**核心理念**: 借鉴TradingAgent的成功架构模式，构建一个能够自动发现技术创新点、验证专利可行性、分析专利价值并协助撰写专利申请的智能系统。

---

## 🎯 系统架构设计

### 🏗️ 高层架构映射

```
┌─────────────────────────────────────────────────────────────────┐
│                        PatentAgent 系统                         │
├─────────────────────────────────────────────────────────────────┤
│  CLI界面 (技术领域选择 + 专利类型配置)                           │
├─────────────────────────────────────────────────────────────────┤
│  多智能体专利框架                                               │
│  ├── 技术分析师      ├── 创新发现师                             │
│  ├── 先行技术研究员  ├── 可行性验证员                           │
│  └── 专利撰写员      └── 价值评估师                             │
├─────────────────────────────────────────────────────────────────┤
│  多LLM提供商层                                                  │
│  ├── 百炼(通义千问)  ├── OpenAI(GPT)                           │
│  ├── Google(Gemini) └── Anthropic(Claude)                     │
├─────────────────────────────────────────────────────────────────┤
│  专利数据层                                                     │
│  ├── 专利数据库 (USPTO, EPO, CNIPA)                           │
│  ├── 技术文献库 (IEEE, ACM, arXiv)                            │
│  └── 行业动态 & 技术新闻                                        │
├─────────────────────────────────────────────────────────────────┤
│  缓存与存储层                                                   │
│  ├── MongoDB (专利数据持久化)                                   │
│  ├── Redis (高性能检索缓存)                                     │
│  └── 文件缓存 (专利文档存储)                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 智能体角色重新设计

### 1. 分析师团队 (Analyst Team)

#### 🔬 技术分析师 (Technology Analyst)
- **原型**: Market Analyst
- **职责**: 分析目标技术领域的发展趋势、技术成熟度、市场需求
- **工具**: 技术文献检索、专利趋势分析、技术路线图生成
- **输出**: 技术领域分析报告、创新机会识别

#### 🧬 创新发现师 (Innovation Discovery Analyst)
- **原型**: News Analyst
- **职责**: 从最新技术动态、学术论文、行业报告中发现潜在创新点
- **工具**: 文献挖掘、技术新闻分析、创新模式识别
- **输出**: 创新机会清单、技术空白分析

#### 📊 先行技术研究员 (Prior Art Researcher)
- **原型**: Fundamentals Analyst
- **职责**: 深度检索相关专利、技术文献，评估现有技术状态
- **工具**: 专利数据库检索、引用分析、技术分类
- **输出**: 先行技术报告、专利风景分析

#### 🌐 市场情报分析师 (Market Intelligence Analyst)
- **原型**: Social Media Analyst
- **职责**: 分析技术的商业价值、市场接受度、竞争态势
- **工具**: 市场报告分析、竞争对手专利分析、商业模式评估
- **输出**: 市场价值评估、商业化可行性分析

### 2. 研究团队 (Research Team)

#### 🚀 创新推进研究员 (Innovation Advocate)
- **原型**: Bull Researcher
- **职责**: 论证创新方案的技术优势、实施可行性、商业价值
- **策略**: 积极挖掘技术优势，构建强有力的创新论证
- **输出**: 创新优势分析、实施路径建议

#### 🛡️ 风险评估研究员 (Risk Assessment Researcher)
- **原型**: Bear Researcher
- **职责**: 识别技术风险、专利侵权风险、实施障碍
- **策略**: 审慎评估潜在问题，提出风险缓解方案
- **输出**: 风险评估报告、规避策略建议

#### ⚖️ 专利策略管理员 (Patent Strategy Manager)
- **原型**: Research Manager
- **职责**: 综合各方分析，制定专利申请策略和时间规划
- **能力**: 平衡创新推进和风险控制，制定最优专利策略
- **输出**: 专利申请策略、优先级排序

### 3. 执行团队 (Execution Team)

#### ✍️ 专利撰写员 (Patent Writer)
- **原型**: Trader
- **职责**: 基于分析结果，撰写高质量的专利申请文档
- **能力**: 技术描述、权利要求撰写、附图设计
- **输出**: 专利申请草稿、技术交底书

#### 🔍 质量评估师 (Quality Assessor)
- **原型**: Risk Manager
- **职责**: 评估专利申请的质量、完整性、获权可能性
- **能力**: 专利审查标准、权利要求分析、文档完整性检查
- **输出**: 质量评估报告、改进建议

---

## 📊 数据源适配规划

### 1. 专利数据库集成

#### 🌍 Google Patents API (SerpApi)
- **API集成**: [Google Patents API](https://serpapi.com/search?engine=google_patents)
- **数据类型**: 全球专利搜索、专利详情、引用分析、发明人/受让人信息
- **特色功能**: 
  - 支持高级搜索语法和多维度筛选
  - 提供专利PDF下载和图像获取
  - 包含专利状态和国家/地区信息
  - 支持学者论文结果集成
- **更新频率**: 实时
- **API可用性**: 99.960% uptime

#### 🇨🇳 智慧芽专利数据平台
- **API集成**: [智慧芽开放平台](https://open-zhihuiya-com.libproxy1.nus.edu.sg/tutorials/getStart)
- **数据类型**: 中国专利数据、全球专利检索、专利分析
- **AI能力集成**:
  - **[AI01] 药物DDT抽取**: 从专利文本中提取药物、适应症、靶点信息
  - **[AI30] 相似专利检索与比对**: 智能专利相似度分析
  - **[AI31] 专利核心发明点**: 自动识别专利的核心创新点
  - **[AI40] 可行性分析助手**: 专利可行性评估报告
  - **[AI61] AI翻译**: 多语言专利文档翻译
- **更新频率**: 实时
- **认证方式**: OAuth 2.0 (Client ID/Secret)

#### 🇺🇸 美国专利商标局 (USPTO)
- **API集成**: USPTO Patent Examination Research Dataset
- **数据类型**: 专利申请、授权专利、审查历史
- **更新频率**: 实时

#### 🇪🇺 欧洲专利局 (EPO)
- **API集成**: Open Patent Services (OPS)
- **数据类型**: 欧洲专利、PCT申请、专利族信息
- **更新频率**: 日更新

### 2. 技术文献数据库

#### 📚 学术数据库
- **IEEE Xplore**: 工程技术文献
- **ACM Digital Library**: 计算机科学文献
- **arXiv**: 预印本论文
- **Google Scholar**: 综合学术搜索

#### 🏭 行业报告
- **Gartner**: 技术趋势报告
- **IDC**: 市场研究报告
- **技术标准组织**: IEEE, ISO, IETF标准文档

### 3. 技术新闻与动态

#### 📰 技术媒体
- **TechCrunch**: 创业技术动态
- **MIT Technology Review**: 前沿技术分析
- **Nature/Science**: 科学突破报道
- **中文科技媒体**: 36氪、钛媒体、雷锋网

---

## 🔄 工作流程设计

### 1. 专利发现流程 (Patent Discovery)

```
技术领域输入 → 技术分析师分析 → 创新发现师挖掘机会 → 
市场情报分析师评估价值 → 先行技术研究员检索现状 → 
创新机会报告生成
```

### 2. 专利验证流程 (Patent Validation)

```
创新方案输入 → 先行技术深度检索 → 创新推进研究员论证优势 → 
风险评估研究员识别风险 → 专利策略管理员制定策略 → 
可行性评估报告
```

### 3. 专利分析流程 (Patent Analysis)

```
专利技术输入 → 技术分析师技术解读 → 市场情报分析师商业分析 → 
先行技术研究员竞争分析 → 价值评估报告生成
```

### 4. 专利撰写流程 (Patent Writing)

```
技术方案确认 → 专利撰写员起草申请 → 质量评估师审核评估 → 
反馈修改循环 → 最终专利申请文档
```

---

## 🛠️ 技术实现规划

### 1. 核心模块改造

#### 📁 目录结构映射
```
patentagents/
├── agents/
│   ├── analysts/
│   │   ├── technology_analyst.py        # 技术分析师
│   │   ├── innovation_discovery.py      # 创新发现师
│   │   ├── prior_art_researcher.py      # 先行技术研究员
│   │   └── market_intelligence.py       # 市场情报分析师
│   ├── researchers/
│   │   ├── innovation_advocate.py       # 创新推进研究员
│   │   ├── risk_assessor.py            # 风险评估研究员
│   │   └── patent_strategy_manager.py   # 专利策略管理员
│   ├── writers/
│   │   ├── patent_writer.py            # 专利撰写员
│   │   └── quality_assessor.py         # 质量评估师
│   └── utils/
│       ├── patent_states.py           # 专利状态管理
│       ├── patent_memory.py           # 专利记忆系统
│       └── patent_utils.py            # 专利工具集
├── dataflows/
│   ├── google_patents_utils.py        # Google Patents API接口
│   ├── zhihuiya_utils.py              # 智慧芽专利数据接口
│   ├── uspto_utils.py                 # USPTO数据接口
│   ├── epo_utils.py                   # EPO数据接口
│   ├── literature_utils.py           # 文献检索工具
│   ├── tech_news_utils.py             # 技术新闻聚合
│   └── patent_cache_manager.py        # 专利缓存管理
├── graph/
│   ├── patent_graph.py               # 专利智能体图
│   ├── discovery_logic.py            # 发现逻辑
│   ├── validation_logic.py           # 验证逻辑
│   ├── analysis_logic.py             # 分析逻辑
│   └── writing_logic.py              # 撰写逻辑
└── config/
    ├── patent_config.py              # 专利配置管理
    └── database_config.py            # 数据库配置
```

### 2. 状态管理重新设计

#### 📊 PatentState (专利状态)
```python
class PatentState(MessagesState):
    # 基础信息
    technology_domain: str              # 技术领域
    innovation_topic: str               # 创新主题
    analysis_date: str                  # 分析日期
    
    # 分析阶段输出
    technology_report: str              # 技术分析报告
    innovation_opportunities: str       # 创新机会报告
    prior_art_report: str              # 先行技术报告
    market_intelligence: str           # 市场情报报告
    
    # 研究阶段输出
    innovation_advocacy: str            # 创新推进分析
    risk_assessment: str               # 风险评估报告
    patent_strategy: str               # 专利策略建议
    
    # 执行阶段输出
    patent_draft: str                  # 专利申请草稿
    quality_assessment: str            # 质量评估报告
    final_patent_application: str      # 最终专利申请
```

### 3. 工具集适配

#### 🔧 PatentToolkit (专利工具包)
```python
class PatentToolkit:
    # Google Patents API 专利检索工具
    def search_google_patents(self, query: str, **kwargs) -> Dict:
        """
        使用Google Patents API进行专利检索
        
        Args:
            query: 搜索查询词，支持高级语法如 "(Coffee) OR (Tea)"
            **kwargs: 其他搜索参数
                - page: 页码 (默认1)
                - num: 每页结果数 (10-100)
                - sort: 排序方式 ('new', 'old', 默认按相关性)
                - country: 国家代码过滤 ('US,CN,EP')
                - status: 专利状态 ('GRANT', 'APPLICATION')
                - inventor: 发明人姓名
                - assignee: 受让人名称
                - before/after: 日期范围 ('priority:20221231')
        
        Returns:
            Dict: 包含专利结果、摘要统计等信息
        """
        
    def get_patent_details(self, patent_id: str) -> Dict:
        """获取专利详细信息，包括PDF链接、图像、引用等"""
        
    def search_similar_patents(self, patent_id: str, threshold: float = 0.8) -> List:
        """基于专利ID搜索相似专利"""
    
    # 智慧芽专利数据工具
    def search_zhihuiya_patents(self, keywords: str, **filters) -> Dict:
        """使用智慧芽API进行专利检索"""
        
    def extract_patent_core_invention(self, patent_text: str) -> Dict:
        """使用智慧芽AI31提取专利核心发明点"""
        
    def analyze_patent_feasibility(self, patent_content: str) -> Dict:
        """使用智慧芽AI40进行专利可行性分析"""
        
    def compare_patent_similarity(self, patent_a: str, patent_b: str) -> Dict:
        """使用智慧芽AI30进行专利相似度比对"""
        
    def translate_patent_text(self, text: str, target_lang: str) -> str:
        """使用智慧芽AI61进行专利文档翻译"""
    
    # 传统专利数据库接口
    def search_uspto_patents(self, keywords: str, classification: str) -> List:
        """USPTO专利检索"""
        
    def search_epo_patents(self, keywords: str, ipc_class: str) -> List:
        """EPO专利检索"""
    
    # 文献检索工具
    def search_ieee_papers(self, keywords: str, year_range: Tuple[int, int]) -> List:
        """IEEE学术文献检索"""
        
    def search_arxiv_papers(self, keywords: str, categories: List[str]) -> List:
        """arXiv预印本论文检索"""
        
    def search_google_scholar(self, query: str, citation_threshold: int = 10) -> List:
        """Google Scholar学术搜索"""
    
    # 技术分析工具
    def analyze_patent_trends(self, technology_field: str, time_range: Tuple[str, str]) -> Dict:
        """分析专利技术趋势"""
        
    def generate_patent_landscape(self, technology_area: str) -> Dict:
        """生成专利技术地图"""
        
    def assess_patent_strength(self, patent_id: str) -> Dict:
        """评估专利强度和价值"""
        
    def build_patent_citation_network(self, patent_ids: List[str]) -> Dict:
        """构建专利引用网络图"""
    
    # 创新发现工具
    def identify_technology_gaps(self, field: str, existing_patents: List[str]) -> List:
        """识别技术空白领域"""
        
    def discover_emerging_technologies(self, news_sources: List[str], time_window: int = 30) -> List:
        """发现新兴技术趋势"""
        
    def analyze_research_frontiers(self, literature_corpus: List[Dict]) -> Dict:
        """分析研究前沿"""
        
    def cross_domain_innovation_discovery(self, domains: List[str]) -> List:
        """跨领域创新机会发现"""
    
    # 专利撰写工具
    def generate_patent_claims(self, technical_description: str) -> List[str]:
        """生成专利权利要求"""
        
    def create_patent_drawings(self, technical_specs: Dict) -> List[str]:
        """创建专利附图"""
        
    def format_patent_application(self, content_sections: Dict) -> str:
        """格式化专利申请文档"""
        
    def validate_patent_format(self, patent_draft: str) -> Dict:
        """验证专利文档格式和完整性"""
        
    # 专利价值评估工具
    def evaluate_patent_commercial_value(self, patent_id: str) -> Dict:
        """评估专利商业价值"""
        
    def assess_infringement_risk(self, patent_content: str, existing_patents: List[str]) -> Dict:
        """评估专利侵权风险"""
        
    def predict_patent_grant_probability(self, patent_application: str) -> float:
        """预测专利授权概率"""
```

---

## 🎯 具体实现目标

### 阶段一: 基础架构改造 (2-3周)
1. **目录结构重组**: 将trading相关模块重命名为patent相关
2. **状态管理适配**: 设计PatentState和相关数据结构
3. **基础工具开发**: 实现专利检索和文献检索的基础API
4. **CLI界面改造**: 技术领域选择和专利类型配置

### 阶段二: 智能体角色开发 (3-4周)
1. **分析师团队**: 开发4个分析师智能体的提示词和逻辑
2. **研究团队**: 实现3个研究员的协作和决策逻辑
3. **执行团队**: 构建专利撰写和质量评估能力
4. **记忆系统**: 适配专利知识的存储和检索

### 阶段三: 数据源集成 (2-3周)
1. **专利数据库**: 
   - 集成Google Patents API (SerpApi)进行全球专利检索
   - 集成智慧芽API实现中国专利数据和AI分析功能
   - 集成USPTO、EPO官方API接口
2. **文献数据库**: 连接IEEE、ACM、arXiv等学术资源
3. **技术新闻**: 聚合技术媒体和行业报告
4. **缓存优化**: 优化专利数据的存储和检索性能

#### 🔧 API集成示例代码

```python
# Google Patents API 使用示例
from serpapi import GoogleSearch

def search_patents_google(query, **params):
    """使用Google Patents API搜索专利"""
    search = GoogleSearch({
        "engine": "google_patents",
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        **params
    })
    
    results = search.get_dict()
    return {
        "patents": results.get("organic_results", []),
        "summary": results.get("summary", {}),
        "total_results": len(results.get("organic_results", []))
    }

# 智慧芽API使用示例
import requests

def search_patents_zhihuiya(keywords, **filters):
    """使用智慧芽API搜索专利"""
    headers = {
        "Authorization": f"Bearer {os.getenv('ZHIHUIYA_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": keywords,
        "filters": filters,
        "page_size": 50
    }
    
    response = requests.post(
        "https://open-zhihuiya-com.libproxy1.nus.edu.sg/api/v1/patents/search",
        json=payload,
        headers=headers
    )
    
    return response.json()

def extract_core_invention_zhihuiya(patent_text):
    """使用智慧芽AI31提取专利核心发明点"""
    headers = {
        "Authorization": f"Bearer {os.getenv('ZHIHUIYA_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": patent_text,
        "ai_model": "AI31"  # 专利核心发明点提取
    }
    
    response = requests.post(
        "https://open-zhihuiya-com.libproxy1.nus.edu.sg/api/v1/ai/analyze",
        json=payload,
        headers=headers
    )
    
    return response.json()
```

### 阶段四: 工作流程优化 (2-3周)
1. **发现流程**: 完善技术机会发现的智能体协作
2. **验证流程**: 优化专利可行性验证的逻辑链
3. **分析流程**: 强化专利价值分析的深度和准确性
4. **撰写流程**: 提升专利申请文档的质量和规范性

### 阶段五: 测试与优化 (2-3周)
1. **功能测试**: 全面测试各个智能体的功能
2. **集成测试**: 验证端到端的工作流程
3. **性能优化**: 优化响应速度和资源使用
4. **用户体验**: 完善CLI界面和输出格式

---

## 🌟 创新特色功能

### 1. 智能专利发现
- **全球专利检索**: 基于Google Patents API实现99.96%可用性的全球专利搜索
- **技术趋势预测**: 基于文献和专利数据预测技术发展方向
- **创新空白识别**: 自动发现技术领域中的专利空白
- **交叉领域创新**: 识别跨领域技术融合的创新机会
- **AI增强分析**: 利用智慧芽AI能力进行智能专利分析

### 2. 深度先行技术分析
- **专利族分析**: 追踪专利家族的全球布局
- **引用网络分析**: 构建专利引用关系图谱
- **技术演进路径**: 绘制技术发展的历史脉络

### 3. 智能专利撰写
- **权利要求生成**: 自动生成多层次的权利要求
- **技术描述优化**: 确保技术描述的准确性和完整性
- **附图自动生成**: 根据技术描述生成专利附图
- **核心发明点提取**: 使用智慧芽AI31自动识别专利核心创新点
- **多语言支持**: 智慧芽AI61提供专利文档多语言翻译

### 4. 专利价值评估
- **技术价值评分**: 基于多维度指标评估专利技术价值
- **商业价值预测**: 预测专利的商业化潜力
- **侵权风险评估**: 评估专利申请的侵权风险
- **相似专利检索**: 智慧芽AI30进行智能专利相似度分析
- **可行性分析**: 智慧芽AI40提供专利可行性评估报告
- **实时专利监控**: 基于Google Patents API的实时专利状态追踪

---

## 🎪 用户交互设计

### 1. CLI交互流程
```
欢迎使用PatentAgent! 请选择您的需求:
1. 🔍 技术创新发现
2. ✅ 专利可行性验证  
3. 📊 专利价值分析
4. ✍️ 专利申请撰写

请输入技术领域 (如: 人工智能, 生物技术, 新能源):
> 人工智能

请输入具体技术方向 (如: 深度学习, 计算机视觉, 自然语言处理):
> 计算机视觉

正在启动PatentAgent智能体团队...
🔬 技术分析师正在分析计算机视觉领域...
🧬 创新发现师正在挖掘创新机会...
📊 先行技术研究员正在检索相关专利...
🌐 市场情报分析师正在评估商业价值...
```

### 2. 输出报告格式
```markdown
# PatentAgent 分析报告

## 📋 基本信息
- **技术领域**: 人工智能 - 计算机视觉
- **分析日期**: 2025-01-XX
- **分析类型**: 技术创新发现

## 🔬 技术分析摘要
[技术分析师的详细分析]

## 💡 创新机会识别
[创新发现师的机会清单]

## 📚 先行技术状态
[先行技术研究员的检索结果]

## 💰 商业价值评估
[市场情报分析师的价值分析]

## 🎯 推荐行动方案
[专利策略管理员的建议]
```

---

## 🔧 技术栈保持

### 保留的优秀架构
1. **多LLM支持**: 继续支持百炼、OpenAI、Google、Anthropic
2. **缓存系统**: 保持MongoDB + Redis + 文件缓存的三层架构
3. **智能体框架**: 继续使用LangGraph进行智能体编排
4. **配置管理**: 保持灵活的配置系统和环境变量管理

### 新增技术依赖
1. **专利API客户端**: 
   - **Google Patents API (SerpApi)**: `pip install google-search-results`
   - **智慧芽开放平台**: 官方SDK或REST API调用
   - **USPTO, EPO**: 官方API客户端
2. **文献检索库**: 学术数据库的Python客户端
3. **文档处理**: PDF解析、专利文档格式化工具
4. **可视化工具**: 专利地图、技术路线图生成

### API密钥配置
```env
# Google Patents API (SerpApi)
SERPAPI_API_KEY=your_serpapi_key_here

# 智慧芽专利数据平台
ZHIHUIYA_CLIENT_ID=your_zhihuiya_client_id
ZHIHUIYA_CLIENT_SECRET=your_zhihuiya_client_secret
ZHIHUIYA_ACCESS_TOKEN=your_access_token

# 其他专利数据库
USPTO_API_KEY=your_uspto_key
EPO_API_KEY=your_epo_key

# 学术数据库
IEEE_API_KEY=your_ieee_key
ARXIV_API_KEY=your_arxiv_key_if_needed
```

---

## 🎉 预期成果

### 1. 功能成果
- **自动化专利发现**: 减少90%的人工技术调研时间
- **智能专利验证**: 提供95%准确率的先行技术分析
- **高质量专利撰写**: 生成符合专利局标准的申请文档
- **全面价值评估**: 多维度评估专利的技术和商业价值

### 2. 用户体验
- **一站式服务**: 从创新发现到专利申请的全流程支持
- **智能化决策**: AI辅助的专利策略制定
- **高效协作**: 多智能体协同工作，提供全面分析
- **专业输出**: 符合专利代理人标准的专业文档

### 3. 技术创新
- **AI+专利**: 将人工智能技术深度应用于知识产权领域
- **多源数据融合**: 整合全球专利数据库和技术文献
- **智能协作**: 多智能体在专利领域的创新应用
- **开源贡献**: 为开源社区提供专利分析工具

---

## 📈 项目里程碑

### 近期目标 (1-2个月)
- [ ] 完成基础架构改造
- [ ] 实现核心智能体角色
- [ ] 集成主要专利数据源
- [ ] 发布PatentAgent v0.1.0

### 中期目标 (3-6个月)  
- [ ] 优化专利撰写质量
- [ ] 增强价值评估准确性
- [ ] 扩展国际专利数据库支持
- [ ] 构建专利知识图谱

### 长期目标 (6-12个月)
- [ ] 支持多语言专利分析
- [ ] 集成专利诉讼数据
- [ ] 开发专利组合管理功能
- [ ] 建立专利价值预测模型

---

**让我们将TradingAgent的成功架构延续到专利领域，为知识产权行业带来AI革命！** 🚀✨
