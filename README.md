# 🗺️ Learning Roadmap Generator

A simple web app that creates a personalized learning roadmap. Enter a field, your skill level, and the time you have, and an LLM builds a phase-by-phase plan with topics, projects, and resources.

**Tech stack:** Python · Streamlit (UI) · Groq API (LLM)

## Features

- Choose any field or topic
- Pick your level: Beginner, Intermediate, or Advanced
- Set total time (weeks or months) and weekly study hours
- Live-streamed roadmap with phases, practice tasks, resources, and a capstone project
- Download the roadmap as a Markdown file

## Project Structure

```
.
├── app.py             # Streamlit app
├── requirements.txt   # Dependencies
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/learning-roadmap-generator.git
cd learning-roadmap-generator
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Get a free key at [console.groq.com](https://console.groq.com), then either:

- create a `.env` file in the project root:
  ```
  GROQ_API_KEY=your_key_here
  ```
- or paste the key into the app's sidebar when it runs.

> ⚠️ Never commit your `.env` file. Add `.env` to your `.gitignore`.

### 5. Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Deploying on Streamlit Community Cloud

1. Push the project to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app from your repo, with `app.py` as the main file.
3. In **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
4. Deploy.

## Pushing to GitHub

```bash
git init
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .
git commit -m "Initial commit: learning roadmap generator"
git branch -M main
git remote add origin https://github.com/<your-username>/learning-roadmap-generator.git
git push -u origin main
```

## Configuration

The model is set by the `MODEL` constant in `app.py` (default: `llama-3.3-70b-versatile`). If Groq retires a model, check [console.groq.com/docs/models](https://console.groq.com/docs/models) and update it.

## Ideas for Improvement

- Export to PDF
- Save and revisit past roadmaps
- Weekly progress tracker
- Structured JSON output rendered as a timeline

## License

MIT
