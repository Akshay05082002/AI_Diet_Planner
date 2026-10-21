#!/bin/bash
# AI Diet Planner - Complete Setup & Run Guide

echo "================================"
echo "🚀 AI DIET PLANNER - QUICK START"
echo "================================"

PROJECT_DIR="/Users/akshaykumar/Desktop/Projects /AI-POWER-DIET-PLANNER/AI_Diet_Planner"
cd "$PROJECT_DIR"

echo ""
echo "✓ Step 1: Verify Python & Node installation"
python3 --version
node --version
npm --version

echo ""
echo "✓ Step 2: Install/Update Python dependencies"
./venv/bin/pip install -q -r requirements.txt

echo ""
echo "✓ Step 3: Install Node API dependencies (optional - for image uploads)"
cd api
npm install --silent
cd ..

echo ""
echo "✓ Step 4: Install React dependencies"
cd frontend
npm install --silent
cd ..

echo ""
echo "================================"
echo "✅ SETUP COMPLETE!"
echo "================================"
echo ""
echo "📌 TO RUN THE PROJECT:"
echo ""
echo "Terminal 1 - START FLASK BACKEND:"
echo "  cd \"$PROJECT_DIR\""
echo "  ./venv/bin/python3 app.py"
echo ""
echo "Terminal 2 - START REACT FRONTEND (optional):"
echo "  cd \"$PROJECT_DIR/frontend\""
echo "  npm run dev"
echo ""
echo "Terminal 3 - START NODE API (optional):"
echo "  cd \"$PROJECT_DIR/api\""
echo "  npm run dev"
echo ""
echo "🌐 THEN OPEN IN BROWSER:"
echo "  Flask (with all features): http://localhost:5001"
echo "  React (modern UI):         http://localhost:5173"
echo ""
echo "📝 FIRST TIME:"
echo "  1. Register new account"
echo "  2. Fill your profile (age, weight, height, etc.)"
echo "  3. Go to Dashboard → Calories Tracker"
echo "  4. Add meals or use AI to generate meal plan"
echo "  5. Chat with AI nutritionist"
echo "  6. Download PDF report"
echo ""
