# 快速运行

在项目根目录运行：

```powershell
.\essay_env\Scripts\python.exe -m streamlit run app.py
```

打开浏览器里的地址：

```text
http://localhost:8501
```

如果你想构建这本文档，需要先安装 Jupyter Book：

```powershell
.\essay_env\Scripts\python.exe -m pip install jupyter-book
```

然后构建：

```powershell
.\essay_env\Scripts\python.exe -m jupyter_book build docs
```

构建完成后，HTML 会在：

```text
docs/_build/html/index.html
```

## 运行前检查

`.env` 文件需要包含这些配置：

```text
OPENAI_API_KEY=你的 API Key
BASE_URL=你的接口地址
MODEL=你的模型名
```

`requirements.txt` 里已经列出项目依赖：

```text
openai
python-dotenv
streamlit
easyocr
pillow
```
