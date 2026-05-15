# AI English Essay Grader

This is a Streamlit website for grading English essays and translations across CET-4, CET-6, TOEFL, IELTS, and GRE.

## Run locally

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Create `.env` in the project root:

```env
OPENAI_API_KEY=your-api-key
BASE_URL=https://api.deepseek.com
MODEL=deepseek-chat
```

3. Start the website:

```powershell
streamlit run app.py
```

## Share with a friend

The easiest option is Streamlit Community Cloud:

1. Put this project in a private GitHub repository.
2. Deploy `app.py` on Streamlit Community Cloud.
3. Add these secrets in the Streamlit app settings:

```toml
OPENAI_API_KEY = "your-api-key"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
```

4. Send your friend the Streamlit app URL.

Your friend will only use the website. They do not need to enter an API key.

## Notes

- Text input works even if OCR dependencies are not available.
- Image OCR uses EasyOCR and may take longer on the first run because the OCR model needs to load.
- Do not commit `.env` or `.streamlit/secrets.toml` to a public repository.
