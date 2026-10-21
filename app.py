import io
import os
from datetime import datetime

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from diet_ai import (
    bmi_category,
    calculate_bmi,
    calculate_bmr,
    calculate_tdee,
    estimate_calories,
    generate_diet_plan,
    goal_calories,
    recognize_image_stub,
)
from chatbot_ai import get_ai_response

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey123")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ai_diet_planner.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4MB upload limit

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(16))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    activity = db.Column(db.String(16))
    goal = db.Column(db.String(16))
    preference = db.Column(db.String(16))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_profile(self):
        return all(
            [self.age, self.gender, self.height, self.weight, self.activity, self.goal, self.preference]
        )

    def target_calories(self):
        if not self.has_profile():
            return None
        bmr = calculate_bmr(self.gender, self.weight, self.height, self.age)
        tdee = calculate_tdee(bmr, self.activity)
        return goal_calories(tdee, self.goal)


class MealEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("meals", lazy=True))


with app.app_context():
    db.create_all()


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}


@app.route("/")
def home():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not fullname or not email or not password:
            flash("Please complete all registration fields.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please log in.", "danger")
            return redirect(url_for("login"))

        user = User(
            fullname=fullname,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        flash("Registration successful. You are now logged in.", "success")
        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session["user_id"] = user.id
        flash("Login successful.", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    bmi = calculate_bmi(user.weight, user.height) if user.has_profile() else None
    bmi_cat = bmi_category(bmi) if bmi is not None else "N/A"
    cal_target = user.target_calories()

    if not user.has_profile():
        flash("Please complete your profile to see your dashboard.", "warning")

    return render_template(
        "dashboard.html",
        fullname=user.fullname,
        bmi=bmi or "--",
        bmi_cat=bmi_cat,
        cal_target=cal_target or "--",
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            user.age = int(request.form.get("age", user.age or 0))
        except ValueError:
            user.age = None

        user.gender = request.form.get("gender", user.gender)
        try:
            user.height = float(request.form.get("height", user.height or 0))
        except ValueError:
            user.height = None
        try:
            user.weight = float(request.form.get("weight", user.weight or 0))
        except ValueError:
            user.weight = None

        user.activity = request.form.get("activity", user.activity)
        user.goal = request.form.get("goal", user.goal)
        user.preference = request.form.get("preference", user.preference)

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("profile.html", existing=user)


@app.route("/generate_plan")
def generate_plan():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if not user.has_profile():
        flash("Please complete your profile before generating a diet plan.", "warning")
        return redirect(url_for("profile"))

    cal_target = user.target_calories()
    plan = generate_diet_plan(cal_target, user.preference)
    session["diet_plan"] = plan
    session["diet_plan_created_at"] = datetime.utcnow().isoformat()

    bmi = calculate_bmi(user.weight, user.height)
    bmi_cat = bmi_category(bmi)

    return render_template(
        "result.html",
        fullname=user.fullname,
        bmi=bmi,
        bmi_cat=bmi_cat,
        cal_target=cal_target,
        plan=plan,
    )


def create_plan_pdf(plan, user, cal_target):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Diet Plan", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"Name: {user.fullname}", styles["Normal"]))
    story.append(Paragraph(f"Target Calories: {cal_target} kcal", styles["Normal"]))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    table_data = [["Meal", "Food", "Calories", "Protein", "Carbs", "Fat"]]
    for meal, data in plan["meals"].items():
        table_data.append(
            [meal.capitalize(), data["name"], str(data["cal"]), str(data["protein"]), str(data["carbs"]), str(data["fat"])]
        )

    table = Table(table_data, hAlign="LEFT", colWidths=[80, 200, 60, 60, 60, 60])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (2, 1), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(f"Total Calories: {plan['total_calories']} kcal", styles["Normal"]))
    story.append(Paragraph(f"Total Protein: {plan['total_protein']} g", styles["Normal"]))
    story.append(Paragraph(f"Total Carbs: {plan['total_carbs']} g", styles["Normal"]))
    story.append(Paragraph(f"Total Fat: {plan['total_fat']} g", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route("/download-pdf-plan")
def download_pdf_plan():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    plan = session.get("diet_plan")
    if not plan:
        flash("Generate a diet plan before downloading the PDF.", "warning")
        return redirect(url_for("dashboard"))

    cal_target = user.target_calories()
    pdf_buffer = create_plan_pdf(plan, user, cal_target)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="ai_diet_plan.pdf",
    )


def create_entry_pdf(entries, user, cal_goal=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Diet Planner - Food Log", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Name: {user.fullname}", styles["Normal"]))
    if cal_goal:
        story.append(Paragraph(f"Daily Goal: {cal_goal} kcal", styles["Normal"]))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    table_data = [["#", "Item", "Calories"]]
    total = 0
    for idx, entry in enumerate(entries, start=1):
        table_data.append([str(idx), entry.name, str(entry.calories)])
        total += entry.calories

    if len(table_data) == 1:
        table_data.append(["-", "No meals logged", "0"])

    table = Table(table_data, hAlign="LEFT", colWidths=[40, 320, 90])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00b894")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(f"Total Calories: {total} kcal", styles["Normal"]))
    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route("/download-pdf")
def download_pdf():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    entries = MealEntry.query.filter_by(user_id=user.id).order_by(MealEntry.created_at.asc()).all()
    if not entries:
        flash("Add some meals before downloading the PDF.", "warning")
        return redirect(url_for("calories"))

    cal_goal = session.get("custom_goal") or user.target_calories()
    pdf_buffer = create_entry_pdf(entries, user, cal_goal)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="meal_log.pdf",
    )


def get_chat_history():
    return session.get("chat_history", [])


def append_chat_message(user_message, ai_response):
    history = get_chat_history()
    record = {
        "user": user_message,
        "ai": ai_response,
        "timestamp": datetime.utcnow().isoformat(),
    }
    history.append(record)
    session["chat_history"] = history
    return record


def create_chat_history_pdf(history, user):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Nutrition Chat History", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Name: {user.fullname}", styles["Normal"]))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    table_data = [["Time", "User", "AI Response"]]
    for entry in history:
        table_data.append([
            entry["timestamp"],
            entry["user"],
            entry["ai"],
        ])

    table = Table(table_data, hAlign="LEFT", colWidths=[110, 180, 180])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#764ba2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ]
        )
    )
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route("/api/chat-history")
def api_chat_history():
    user = get_current_user()
    if not user:
        return jsonify({"messages": []}), 401
    return jsonify({"messages": get_chat_history()})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required."}), 401

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Message is required."}), 400

    profile = {
        "age": user.age,
        "gender": user.gender,
        "height": user.height,
        "weight": user.weight,
        "activity": user.activity,
        "goal": user.goal,
        "preference": user.preference,
    }
    ai_text = get_ai_response(user_message, profile)
    record = append_chat_message(user_message, ai_text)
    return jsonify(record)


@app.route("/api/clear-chat", methods=["POST"])
def api_clear_chat():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required."}), 401
    session.pop("chat_history", None)
    return jsonify({"status": "ok"})


@app.route("/api/export-pdf", methods=["POST"])
def api_export_pdf():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required."}), 401

    history = get_chat_history()
    if not history:
        return jsonify({"error": "No chat history available."}), 400

    pdf_buffer = create_chat_history_pdf(history, user)
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="chat_history.pdf",
    )


@app.route("/calories")
def calories():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    entries = MealEntry.query.filter_by(user_id=user.id).order_by(MealEntry.created_at.asc()).all()
    total = sum(entry.calories for entry in entries)
    custom_goal = session.get("custom_goal")
    cal_goal = custom_goal or user.target_calories()

    return render_template(
        "calories.html",
        entries=entries,
        total=total,
        cal_goal=cal_goal,
        custom_goal=custom_goal,
    )


@app.route("/calories/add", methods=["POST"])
def calories_add():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    name = request.form.get("name", "").strip()
    calories_value = request.form.get("calories", "").strip()
    calories = None
    if calories_value:
        try:
            calories = int(float(calories_value))
        except ValueError:
            calories = None

    if not name:
        flash("Enter a meal name before saving.", "danger")
        return redirect(url_for("calories"))

    if calories is None:
        calories = estimate_calories(name)

    entry = MealEntry(user_id=user.id, name=name, calories=calories)
    db.session.add(entry)
    db.session.commit()

    flash("Meal added successfully.", "success")
    return redirect(url_for("calories"))


@app.route("/calories/autogen", methods=["POST"])
def calories_autogen():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if not user.has_profile():
        flash("Complete your profile before generating an AI plan.", "warning")
        return redirect(url_for("profile"))

    cal_target = user.target_calories()
    plan = generate_diet_plan(cal_target, user.preference)
    session["diet_plan"] = plan
    session["diet_plan_created_at"] = datetime.utcnow().isoformat()

    MealEntry.query.filter_by(user_id=user.id).delete()
    for meal, data in plan["meals"].items():
        entry = MealEntry(user_id=user.id, name=f"{meal.capitalize()}: {data['name']}", calories=int(data["cal"]))
        db.session.add(entry)
    db.session.commit()

    flash("AI meal plan generated and added to your tracker.", "success")
    return redirect(url_for("calories"))


@app.route("/calories/reset", methods=["POST"])
def calories_reset():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    MealEntry.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    flash("All meal entries have been cleared.", "success")
    return redirect(url_for("calories"))


@app.route("/calories/set_goal", methods=["POST"])
def calories_set_goal():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    custom_goal = request.form.get("custom_goal", "").strip()
    if not custom_goal:
        flash("Enter a custom calorie goal first.", "danger")
        return redirect(url_for("calories"))

    try:
        custom_goal_value = int(float(custom_goal))
        if custom_goal_value <= 0:
            raise ValueError
    except ValueError:
        flash("Enter a valid calorie goal above 0.", "danger")
        return redirect(url_for("calories"))

    session["custom_goal"] = custom_goal_value
    flash("Custom goal saved.", "success")
    return redirect(url_for("calories"))


@app.route("/calories/clear_goal", methods=["POST"])
def calories_clear_goal():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    session.pop("custom_goal", None)
    flash("Custom calorie goal cleared.", "info")
    return redirect(url_for("calories"))


@app.route("/calories/upload", methods=["POST"])
def calories_upload():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    upload = request.files.get("plate_image")
    if not upload or not upload.filename:
        flash("Please upload an image file.", "danger")
        return redirect(url_for("calories"))

    filename = secure_filename(upload.filename)
    predictions = recognize_image_stub(filename)

    if not predictions:
        flash("No food items detected in the uploaded image.", "warning")
        return redirect(url_for("calories"))

    for item in predictions:
        calories = int(item.get("calories", 0))
        if calories <= 0:
            continue
        entry = MealEntry(user_id=user.id, name=item["name"], calories=calories)
        db.session.add(entry)
    db.session.commit()

    flash("Food items detected and added to your tracker.", "success")
    return redirect(url_for("calories"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
