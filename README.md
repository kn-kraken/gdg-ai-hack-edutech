# FrontEnd

# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.


# Backend

# Gemini Feynman Practice – Backend

This is the Flask backend for a web application that uses Google's Gemini API to help users practice the Feynman Technique. The AI acts like a curious 12-year-old child who asks follow-up questions about the user's explanations.

---

## 🚀 Features

- Flask API endpoint (`/ask`) to interact with Gemini
- Gemini 1.5 model with a fixed system prompt simulating a middle school learner
- CORS enabled for frontend communication
- `.env` support for secure API key handling

---

## 🧰 Requirements

Make sure you have **Python 3.8+** installed.

Install the required packages in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
