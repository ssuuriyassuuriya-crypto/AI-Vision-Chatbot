# AI Vision Chatbot 👁️

A portfolio-ready AI Vision Chatbot inspired by the project shown in the screenshot.

## What it does

- Upload JPG/JPEG/PNG/WEBP images
- Uses Gemini multimodal AI to understand the image
- Answers questions about the uploaded image
- Keeps a short conversation history so you can ask follow-up questions
- Runs as a real Streamlit web application
- Can be deployed on Streamlit Community Cloud

## 1. Get a Gemini API key

Create a Gemini API key in Google AI Studio. Keep the key private.

## 2. Run locally

Use Python 3.11 or 3.12.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` from the example:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Start the app:

```bash
streamlit run app.py
```

## 3. Deploy it

1. Create a GitHub repository and upload the project files.
2. Open Streamlit Community Cloud and choose **Create app**.
3. Select your GitHub repository, branch, and `app.py`.
4. Open **Advanced settings → Secrets**.
5. Paste:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

6. Deploy.

Never commit `.streamlit/secrets.toml` or your API key to GitHub.

## Suggested portfolio description

**AI Vision Chatbot** — Built a multimodal AI application that accepts user-uploaded images and answers natural-language questions about their visual content. Implemented with Python, Streamlit, and Google Gemini, with secure API-key handling and cloud deployment.

## Ideas for version 2

- Object detection / counting prompts
- OCR and document Q&A
- Image comparison mode
- Downloadable chat transcript
- User authentication
- Persistent conversation database
- Voice questions
- Camera capture on mobile
