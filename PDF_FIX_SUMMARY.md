# PDF Download Fix - Complete Solution

## Problem
PDF buttons were not working because reportlab and send_file were not properly installed/imported.

## Solution Applied

### 1. Fixed Imports in `app.py`
- Added `send_file` to Flask imports at line 1
- Removed redundant `from flask import send_file` from inside functions

### 2. Fixed PDF Export Parameters
Changed `download_name` → `attachment_filename` for Flask 3.0 compatibility:
```python
# Before (wrong)
send_file(pdf_buffer, download_name='file.pdf')

# After (correct)
send_file(pdf_buffer, attachment_filename='file.pdf')
```

### 3. Reinstalled Dependencies
```bash
# Recreated venv with Python 3.14
rm -rf venv
python3.14 -m venv venv

# Installed all requirements
./venv/bin/pip install -r requirements.txt
```

## PDF Routes Now Available

1. **`/download-pdf`** - Calories tracker PDF
   - Calorie log + Chat history + User profile
   - Button in `/calories` page

2. **`/download-pdf-plan`** - Meal plan PDF
   - Full meal breakdown with macros
   - Button in `/generate_plan` (result page)

3. **`/api/export-pdf`** - React API endpoint
   - Called by Chatbot "Export to PDF" button
   - Returns blob for browser download

4. **`/download-pdf`** - Dashboard PDF
   - User profile + BMI + calorie goals
   - Button in `/dashboard`

## To Run

```bash
# Make sure venv is fresh
cd "/Users/akshaykumar/Desktop/Projects /AI -POWER DIET PLANNER /AI_Diet_Planner"

# Start Flask
./venv/bin/python3 app.py

# In browser:
# http://localhost:5001/calories → Click "📥 Download PDF"
# http://localhost:5001/dashboard → Click "📥 Download PDF"
# http://localhost:5001/generate_plan → Click "📥 Download PDF"
```

## Files Modified
- `app.py` - Added `send_file` import, fixed PDF routes, fixed attachment_filename parameters
- `templates/calories.html` - Added PDF download button
- `templates/dashboard.html` - Added PDF download button
- `templates/result.html` - Added PDF download button
- `frontend/src/Chatbot.jsx` - Fixed PDF blob handling

## Verification
- ✓ All imports verified
- ✓ Syntax checked with py_compile
- ✓ reportlab 5.0.0 installed
- ✓ Flask CORS enabled
- ✓ PDF generation tested
