# 🛡️ RightsMate: The Labor Rights Defender

## The Idea

Let's be real: nobody reads the Terms & Conditions. Now imagine you are a factory worker or a delivery driver, and your employment contract is a 50-page PDF full of confusing legal jargon. You wouldn't know if you were signing away your rights to overtime pay or sick leave.

That's why I built **RightsMate**.

It's a simple tool where you upload a complicated labor law document (like the *Factories Act*), and it lets you chat with it. You ask, "Can my boss fire me without notice?" and it gives you a straight answer based on the actual rules, not a Google guess.


## 🌍 The SDG Connection

This project focuses on **SDG 8: Decent Work and Economic Growth**.
Specifically, it targets **Target 8.8**, which is about protecting labor rights. My logic was simple: You can't fight for your rights if you don't even know what they are.

---

## 💡 How I approached this (Design Thinking)

### 1. Empathize (The "Why")

I started by looking at who actually suffers from bad labor laws. It's usually people who can't afford lawyers—interns, daily wage workers, and factory staff. They face a huge barrier: **Language**. Legal English is basically a foreign language to most people.

### 2. Define (The Problem)

* **The Problem:** Workers are vulnerable to exploitation (like unpaid dues or unsafe conditions) because they don't understand their contracts.
* **The Goal:** Build a "translator" that turns legal docs into simple, actionable advice.

### 3. Ideate (The Solution)

I didn't want just a "summary tool" because summaries can miss details. I needed a bot that could answer *specific* questions.

* *Idea:* Use **RAG (Retrieval Augmented Generation)**. This allows the AI to "read" the specific PDF I give it and answer from that text only.

---

## ⚙️ Under the Hood (Workflow)

I used a local AI setup for this prototype to keep it free and private. Here is how the data flows through the app:

<img width="848" height="1880" alt="document_qa" src="https://github.com/user-attachments/assets/7e891aa1-8667-4717-b170-58c7c417399d" />


### The "Prompt Logic"

One challenge was making sure the AI didn't hallucinate (make things up). I had to tune the system prompt to be strict.

> **My Prompt:** "You are RightsMate. Answer the user's question using ONLY the context provided below. If the answer isn't in the document, say 'I don't know.' Keep your language simple and helpful."

---

## 📸 Project Screenshots

### 1. The Home Screen
<img width="1278" height="715" alt="image" src="https://github.com/user-attachments/assets/457e7dfa-0b30-405a-82fa-a4ff3e6ed0bf" />

*The interface is kept super clean so it's not intimidating.*

### 2. The AI "Thinking"
![opera_JzcfX8DpKn](https://github.com/user-attachments/assets/6c5e5bc8-468e-4190-9081-a838ba0bc7f1)

*Here you can see the model processing the query against the Factories Act.*

---

## 🐛 Challenges I Faced (Real Talk)

Building this wasn't exactly smooth sailing.

1. **The "Ollama" Issue:** At first, I tried to connect to a cloud model, but I kept hitting API rate limits and "Model Gated" errors. I ended up switching to a local version using **Ollama** and **IBM Granite (Micro)**. It's a bit slower on my older laptop (takes about 30 seconds to answer), but it's 100% reliable.
2. **PDF Parsing:** Some legal PDFs are scanned images. I had to make sure I found a clean, digital PDF for the text loader to work properly.

---

## 🚀 Future Scope (What's Next?)

If I had more time and resources, here is what I'd add:

* **Voice Support:** Many target users might not be comfortable typing. Adding a "Speak" button would be a game-changer.
* **Multilingual Support:** Right now it works in English. I want to plug in a translation layer so a worker can ask in Hindi and get an answer in Hindi, even if the law is in English.
* **Cloud Deployment:** Moving this from my laptop to a proper cloud server so the responses are instant.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **Framework:** Flask (for the web app)
* **AI Engine:** LangChain + Ollama
* **Database:** ChromaDB (Vector Store)

---

### How to Run This

1. Install Python and Git.
2. Install Ollama and run `ollama pull ibm/granite4:micro`.
3. Clone this repo and run `pip install -r requirements.txt`.
4. Run `python app.py` and go to `localhost:5000`.
