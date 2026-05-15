# rag.py 和 prompt.py：知识库与提示词

## rag.py

`rag.py` 当前实现比较简单：它会读取 `knowledge_base` 文件夹里的所有文本，然后全部返回给模型。

```{literalinclude} ../rag.py
:language: python
```

现在的 `retrieve_knowledge(query)` 还没有真正按问题检索，只是把所有知识库内容拼起来。

这意味着：

| 优点 | 缺点 |
| --- | --- |
| 简单稳定 | 知识库变大后，提示词会变长 |
| 不需要向量数据库 | 不会根据作文主题筛选最相关资料 |

## prompt.py

`prompt.py` 负责告诉模型应该怎么批改。

它会把三部分内容塞进提示词：

1. 知识库资料：`knowledge`
2. 作文题目：`topic`
3. 学生作文：`essay`

```{literalinclude} ../prompt.py
:language: python
:start-at: def build_prompt
```

## 提示词决定了批改风格

如果你想改变批改结果的格式，主要改 `prompt.py`。

例如：

| 想改什么 | 应该改哪里 |
| --- | --- |
| 分数满分从 15 改成 20 | `prompt.py` 的评分规则 |
| 让语气更温和 | `prompt.py` 的老师身份描述 |
| 增加语法表格 | `prompt.py` 的输出格式 |
| 减少输出长度 | `prompt.py` 的批改要求 |
