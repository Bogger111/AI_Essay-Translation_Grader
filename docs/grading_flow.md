# main.py：作文批改流程

`main.py` 是批改逻辑的核心。

最重要的函数是：

```python
grade_essay(topic, essay)
```

它的流程是：

1. 把作文题目和作文正文合在一起，交给 `retrieve_knowledge`。
2. 从知识库读取参考资料。
3. 调用 `build_prompt` 生成完整提示词。
4. 调用大模型接口。
5. 返回模型生成的批改结果。

```{literalinclude} ../main.py
:language: python
:start-at: def grade_essay
:end-before: if __name__
```

## `.env` 的作用

`main.py` 通过下面的代码读取环境变量：

```python
load_dotenv()
```

然后使用：

| 环境变量 | 用途 |
| --- | --- |
| `OPENAI_API_KEY` | API Key |
| `BASE_URL` | 模型服务地址 |
| `MODEL` | 模型名称，默认是 `deepseek-chat` |

## 模型调用

项目使用 OpenAI 兼容格式：

```python
client.chat.completions.create(...)
```

只要服务支持 OpenAI 兼容接口，就可以通过 `.env` 换不同模型或不同服务商。
