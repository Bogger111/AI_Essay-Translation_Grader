# 常见问题

## 页面打不开

确认你在项目根目录运行：

```powershell
.\essay_env\Scripts\python.exe -m streamlit run app.py
```

然后访问：

```text
http://localhost:8501
```

## OCR 不可用

如果侧边栏显示 OCR 不可用，安装依赖：

```powershell
.\essay_env\Scripts\python.exe -m pip install easyocr pillow
```

第一次运行 EasyOCR 可能会下载模型文件，需要等待一会儿。

## 图片识别不准

可以尝试：

1. 上传更清晰的图片。
2. 尽量让文字水平、不要倾斜。
3. 避免阴影、反光、模糊。
4. 一张图只放题目或作文正文，减少干扰。

## 大模型调用失败

检查 `.env`：

```text
OPENAI_API_KEY=...
BASE_URL=...
MODEL=...
```

还要确认：

1. API Key 没有写错。
2. `BASE_URL` 是 OpenAI 兼容接口。
3. `MODEL` 是服务商支持的模型名。

## 想修改批改格式

改 `prompt.py`。

例如想减少输出内容，就删掉提示词里不需要的输出项。

## 想提高知识库检索效果

现在的 `rag.py` 会读取整个 `knowledge_base`。

后续可以升级成真正的检索：

1. 把知识库切成小段。
2. 给每段建立向量。
3. 根据作文题目和正文找最相关的几段。
4. 只把相关资料放进提示词。
