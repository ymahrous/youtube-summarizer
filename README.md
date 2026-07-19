# YouTube AI Summarizer

An AI-powered **YouTube video summarization application** built with **Streamlit**.  
The app allows users to paste any public YouTube video URL and generate a concise, high-quality summary using an AI backend API.

Designed for quickly extracting insights from:

- Lectures
- Podcasts
- Tutorials
- Interviews
- Educational videos

---

## Features

### YouTube Video Input
- Paste any public YouTube URL
- Embedded video preview
- Supports videos with available captions/transcripts

### AI-Powered Summaries
- Generates intelligent summaries through an external AI API
- Adjustable summary length
- Preserves important details from long videos

### Summary Analytics
After generation, the app displays:

- Word count
- Estimated reading time
- Requested summary length
- AI processing indicator

### Download & Copy
Users can:

- Download summaries as `.txt`
- Copy generated summaries easily

### Summary History
Keeps the latest generated summaries:

- Stores recent URLs
- Saves timestamps
- Allows reopening previous summaries

### Modern UI
Includes:

- Custom Streamlit styling
- Hero landing section
- Responsive layout
- Cards and metrics
- Clean dashboard experience

---

# Architecture

```
User
 |
 | YouTube URL
 ↓
Streamlit Frontend
 |
 | POST Request
 ↓
AI Summarization API
 |
 | Generated Summary
 ↓
Streamlit Dashboard
```

---

# Project Structure

Recommended structure:

```
youtube-ai-summarizer/
│
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API configuration
│
└── README.md
```

---

# Requirements

- Python 3
- Streamlit
- Requests

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```txt
streamlit
requests
```

---

# Configuration

The application requires two secrets:

- AI API endpoint
- API authentication key

Create:

```
.streamlit/secrets.toml
```

Add:

```toml
TEMP_API_URL="https://your-api-url.com"
API_KEY="your-api-key"
```

The application uses:

```python
TEMP_API_URL/api/v1/generate
```

as the summarization endpoint.

---

# Running Locally

Clone the repository:

```bash
git clone <repository-url>

cd youtube-ai-summarizer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure secrets:

```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

Start Streamlit:

```bash
streamlit run app.py
```

The application will open at:

```
http://localhost:8501
```

---

# API Request Format

The app sends a POST request:

### Endpoint

```
POST /api/v1/generate
```

### Headers

```json
{
  "Authorization": "Bearer YOUR_API_KEY"
}
```

### Body

```json
{
  "youtube_url": "https://youtube.com/watch?v=example",
  "max_length": 3000
}
```

### Expected Response

```json
{
  "response": {
    "summary": "Generated AI summary..."
  }
}
```

---

# Application Workflow

1. User enters a YouTube URL
2. App validates the input
3. Video preview is displayed
4. User selects summary length
5. Request is sent to AI backend
6. AI generates summary
7. Summary statistics are calculated
8. Result is displayed and stored in history

---

# Configuration Options

The sidebar allows users to control:

## Maximum Summary Length

Range:

```
500 - 5000 words
```

Default:

```
3000 words
```

Longer summaries provide more detailed explanations.

---

# Error Handling

The application handles:

### Timeout Errors

When AI processing takes too long.

### Connection Errors

When the backend API cannot be reached.

### HTTP Errors

When the API returns an invalid response.

### Invalid Input

When no YouTube URL is provided.

---

# Deployment

## Streamlit Cloud

1. Push the project to GitHub
2. Create a new Streamlit deployment
3. Add secrets:

```
TEMP_API_URL
API_KEY
```

4. Deploy

---

# Security Notes

- Never commit `.streamlit/secrets.toml`
- Keep API keys private
- Use environment variables or Streamlit secrets in production

Add:

```
.streamlit/secrets.toml
```

to `.gitignore`.

Example:

```gitignore
.streamlit/secrets.toml
__pycache__/
.env
```

---

# License

This project is available under the MIT License.

---

# Author

Built with:

- Python
- Streamlit
- AI APIs
- YouTube content processing
