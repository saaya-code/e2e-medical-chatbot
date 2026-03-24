# Medical Chatbot

A conversational AI chatbot that answers medical questions based on a medical reference book. It uses Google Gemini as the AI model and retrieves relevant information from the book before answering.

---

## What You Need Before Starting

- A computer with **Python 3.10** installed ([download here](https://www.python.org/downloads/release/python-3103/))
- A **Google Gemini API key** (free — instructions below)
- A terminal / command prompt
- Basic knowledge of running commands

---

## Step 1 — Get a Gemini API Key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with a Google account
3. Click **"Create API key"**
4. Copy the key — you'll need it in Step 4

---

## Step 2 — Download the Project

```bash
git clone https://github.com/saaya-code/e2e-medical-chatbot.git
cd e2e-medical-chatbot
```

Or download the ZIP from GitHub and extract it, then open a terminal inside the folder.

---

## Step 3 — Create a Virtual Environment

This keeps the project's dependencies isolated from the rest of your computer.

The project requires **Python 3.10.3** specifically. Make sure you're using that version when creating the environment.

**Check your Python version first:**
```bash
python --version
```

If it shows `Python 3.10.x`, run:
```bash
python -m venv .venv
```

If you have multiple Python versions installed and the above shows a different version, use the full path to Python 3.10 instead. For example:

**On Windows:**
```bash
py -3.10 -m venv .venv
```

**On Mac/Linux:**
```bash
python3.10 -m venv .venv
```

Then activate it:

**On Windows:**
```bash
.venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` appear at the start of your terminal line.

---

## Step 4 — Add Your API Key

Create a file called `.env` in the project root folder (same level as `app.py`) with this content:

```
GEMINI_API_KEY=paste_your_key_here
```

Replace `paste_your_key_here` with the key you copied in Step 1.

> **Note:** Never share this file or commit it to GitHub. It's already in `.gitignore`.

---

## Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

This may take a few minutes the first time.

---

## Step 6 — Run the App

```bash
python app.py
```

The first time you run it, it will process the medical book and build a local database (this takes a minute or two). After that, subsequent starts are fast.

Once you see something like:

```
Running on http://0.0.0.0:10000
```

Open your browser and go to: **http://localhost:10000**

---

## How to Use the Chatbot

Type a medical question in the chat box and press **Send**. The chatbot will search the medical book and give you an answer based on its content.

Example questions:
- *What are the symptoms of diabetes?*
- *How is hypertension treated?*
- *What causes anemia?*

---

## Project Structure

```
├── app.py              # Main application file
├── src/
│   ├── helper.py       # Loads and indexes the medical book
│   └── prompt.py       # System prompt for the AI
├── data/
│   └── Medical_book.pdf  # The medical reference document
├── templates/
│   └── chat.html       # The chat UI
├── chroma_db/          # Auto-generated vector database (don't touch)
├── requirements.txt    # Python dependencies
└── .env                # Your API key (you create this)
```

---

## Troubleshooting

**`ModuleNotFoundError`** — Make sure your virtual environment is activated (you should see `(.venv)` in the terminal) and that you ran `pip install -r requirements.txt`.

**`GEMINI_API_KEY` error** — Double-check your `.env` file exists in the project root and the key is correct with no extra spaces.

**Port already in use** — Another process is using port 10000. Either stop that process or change the port in `app.py` on the last line.

**Slow first startup** — Normal. The app is processing the PDF and building the search database. Wait for it to finish.
