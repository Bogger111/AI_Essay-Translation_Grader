# app.py：网页界面

`app.py` 是项目入口。运行 Streamlit 时，启动的就是这个文件。

## 页面做了什么

页面分成几块：

1. 侧边栏显示 OCR 是否可用。
2. 上传作文题目图片。
3. 输入或自动填入作文题目。
4. 上传作文内容图片。
5. 输入或自动填入作文内容。
6. 点击按钮后开始批改。
7. 展示大模型返回的批改结果。

## 关键函数

`recognize_uploaded_image` 是图片上传识别的通用函数。

它接收四个参数：

| 参数 | 含义 |
| --- | --- |
| `uploaded_file` | Streamlit 上传的图片文件 |
| `target_key` | 识别结果要填入哪个输入框 |
| `processed_key` | 用来记录这张图片是否已经识别过 |
| `label` | 页面提示文字，例如“作文题目”或“作文内容” |

```{literalinclude} ../app.py
:language: python
:start-after: st.set_page_config
:end-before: with st.sidebar:
```

## 为什么要用 `st.session_state`

Streamlit 每次用户操作都会重新运行整个 `app.py`。

如果不用 `st.session_state`，上传图片后识别出的文字很容易在页面刷新时丢失。

项目里用两个状态保存识别结果：

| key | 保存内容 |
| --- | --- |
| `topic_input` | 作文题目 |
| `essay_input` | 作文正文 |

还用两个状态避免同一张图片反复识别：

| key | 保存内容 |
| --- | --- |
| `topic_ocr_processed` | 已识别过的题目图片标识 |
| `essay_ocr_processed` | 已识别过的作文图片标识 |
