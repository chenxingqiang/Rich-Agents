"""
PatentAgent Writers Package
专利智能体撰写员包
"""

# 导入撰写员函数
try:
    from .patent_writer import create_patent_writer, validate_patent_draft, analyze_patent_claims
    
    __all__ = ["create_patent_writer", "validate_patent_draft", "analyze_patent_claims"]
except ImportError:
    # 如果导入失败，提供空的__all__
    __all__ = [] 