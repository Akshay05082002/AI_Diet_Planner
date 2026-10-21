# 🥗 AI Diet Planner & Nutrition Assistant

An intelligent, full-stack web application designed to help users calculate their daily calorie needs, generate personalized AI diet plans, track daily meals, consult an AI nutritionist chatbot, and export comprehensive dietary PDF reports.

---

## ✨ Features

- 👤 **User Authentication & Profile**: Secure registration, login, and personalized user profiles with dietary goals.
- 📊 **Health Metrics Calculator**: Real-time BMR, TDEE, and BMI calculations based on personal stats and activity level.
- 🍎 **AI Meal & Diet Planner**: Automated diet chart recommendations tailored to weight loss, maintenance, or muscle gain.
- 💬 **AI Nutritionist Chatbot**: 24/7 intelligent nutrition advisor with built-in comprehensive dietary fallback knowledge.
- 🍲 **Calorie & Macro Tracker**: Log daily meals with calories, protein, carbs, and fat breakdown.
- 📸 **Food Plate Scanner**: Upload food plate images for intelligent calorie detection and logging.
- 📄 **Downloadable PDF Reports**: Export personalized diet plans and progress reports with one click.
- 🎨 **Modern Responsive UI**: Clean, interactive dashboard with sleek aesthetic styling.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy, Werkzeug, Gunicorn
- **AI Engine**: OpenAI API + Local Rule-Based Nutrition Engine Fallback
- **PDF Generation**: ReportLab
- **Database**: SQLite
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism & Responsive Design), Jinja2 Templates
- **Additional Frontends (Optional)**: React + Vite (in `/frontend`), Node Express API (in `/api`)

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI_Diet_Planner.git
cd AI_Diet_Planner
```

### 2. Create and activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Set Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional: local fallback AI works without key
```

### 5. Run the Application
```bash
python3 app.py
```
Visit **[http://localhost:5001](http://localhost:5001)** in your web browser.

---

## 🌐 Deploy to Production (Make it Public)

You can host this application online for free on **Render.com**:

1. Push this repository to **GitHub**.
2. Sign up / Log in to [Render](https://render.com).
3. Click **New +** → **Web Service**.
4. Connect your GitHub repository.
5. Configure the settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click **Deploy Web Service**!
7. Once finished, Render will provide a free live public URL (e.g. `https://your-diet-planner.onrender.com`).

---

## 📁 Project Structure

```
AI_Diet_Planner/
├── app.py                 # Main Flask application & routes
├── diet_ai.py             # Diet planning algorithm & calorie calculations
├── chatbot_ai.py          # AI chatbot handler & nutrition knowledge base
├── requirements.txt       # Python dependencies
├── Procfile               # Production WSGI process definition
├── static/                # CSS styles, assets, and icons
├── templates/             # HTML templates (Jinja2)
├── frontend/              # (Optional) React frontend
├── api/                   # (Optional) Node image upload service
└── RUN.sh                 # Quick setup script
```

---

## 📝 License
This project is open source and available under the [MIT License](LICENSE).
