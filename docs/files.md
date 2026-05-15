# 文件地图

## 项目根目录

| 路径 | 说明 |
| --- | --- |
| `app.py` | 网页入口 |
| `ocr.py` | 图片 OCR |
| `main.py` | 批改主流程 |
| `prompt.py` | 构造大模型提示词 |
| `rag.py` | 读取知识库 |
| `requirements.txt` | Python 依赖 |
| `.env` | 本地密钥和模型配置 |
| `knowledge_base/` | 写作评分标准、句型、词汇等资料 |
| `essay_env/` | 虚拟环境 |
| `docs/` | 这本 Jupyter Book |

## knowledge_base

| 文件 | 可能用途 |
| --- | --- |
| `scoring.md` | 评分标准 |
| `structure.md` | 作文结构建议 |
| `vocab.md` | 高级词汇 |
| `sentence_patterns.md` | 句型模板 |
| `common_topics.md` | 常见话题资料 |

## 不需要关心的文件

| 文件或目录 | 说明 |
| --- | --- |
| `__pycache__/` | Python 自动生成的缓存 |
| `streamlit.out.log` | 之前启动 Streamlit 时产生的日志 |
| `streamlit.err.log` | 之前启动 Streamlit 时产生的错误日志 |

这些不是项目核心逻辑。
