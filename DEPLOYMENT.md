# 🚀 Deployment Guide: QuantumAI Platform

This guide shows you how to deploy the entire **QuantumAI Platform** to 100% free cloud hosting so anyone in the world (judges, teachers, students) can access it 24/7 without needing your laptop!

---

## 🏗️ Architecture Overview

| Component | Technology | Recommended Free Host | Resulting URL |
| :--- | :--- | :--- | :--- |
| **Frontend** | React 18 + Vite + Three.js | **Vercel** (or Netlify) | `https://quantum-ai.vercel.app` |
| **Backend** | Python 3.12 + FastAPI + SQLite | **Render.com** (or Railway) | `https://quantum-ai-backend.onrender.com` |

---

## 📋 Step 1: Push Code to GitHub (Prerequisite)

Before deploying to Vercel/Render, your code must be on GitHub:

1. Create a repository on [GitHub](https://github.com/new) named `quantum-ai-learning-platform` (make it **Public**).
2. In your terminal inside the `sihh` folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial release for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/quantum-ai-learning-platform.git
   git push -u origin main
   ```

---

## 🐍 Step 2: Deploy the Backend (Render.com - 100% Free)

1. Go to [Render.com](https://render.com/) and sign up / log in with your GitHub account.
2. Click **New +** ➔ Select **Web Service**.
3. Connect your GitHub repository (`quantum-ai-learning-platform`).
4. Fill in the settings:
   - **Name**: `quantum-ai-backend`
   - **Region**: Singapore or Frankfurt (or closest)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
   - **Instance Type**: **Free**
5. **Environment Variables on Render** (Under "Advanced" ➔ "Environment Variables"):
   - `MONGODB_URI`: Your MongoDB Atlas connection string:
     `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/quantum_learning?retryWrites=true&w=majority`
     *(Free 512MB MongoDB cluster created in 1 min at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas))*
   - `MONGODB_DB_NAME`: `quantum_learning`
6. Click **Create Web Service**.
7. Once deployed (approx 2 mins), copy your live backend URL:
   👉 E.g.: `https://quantum-ai-backend.onrender.com`

---

## ⚛️ Step 3: Deploy the Frontend (Vercel - 100% Free)

1. Go to [Vercel.com](https://vercel.com/) and sign up / log in with GitHub.
2. Click **Add New...** ➔ **Project**.
3. Import your `quantum-ai-learning-platform` repository.
4. Configure Project:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click *Edit* and select **`frontend`**
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. **Environment Variables** (CRUCIAL — Fixes Signup/Auth on Deployed App):
   - Click **Environment Variables**
   - Add a new variable:
     - **Key**: `VITE_API_BASE`
     - **Value**: `https://quantum-ai-backend.onrender.com/api` *(Make sure to include `/api` at the end!)*
6. Click **Deploy**!

In less than 1 minute, Vercel will give you a live production URL:
👉 **`https://quantum-ai-platform.vercel.app`**


---

## ⚡ Option B: Quick 10-Second Live Demo (ngrok)
If you just need an immediate public link for a 1-hour live presentation or hackathon evaluation while your laptop is on:

1. Start your servers: `start_all.bat`
2. Run in a terminal:
   ```cmd
   ngrok http 5173
   ```
3. Share the generated `https://xxxx.ngrok-free.app` URL!
