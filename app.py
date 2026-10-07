from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
import qrcode
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

DATABASE = "database.db"


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# CREATE DATABASE TABLE
# -----------------------------

def init_db():

    conn = get_db_connection()

    # -------------------------
    # PETS TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            breed TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT,
            owner TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    # -------------------------
    # VACCINATIONS TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id TEXT NOT NULL,
            vaccine_name TEXT NOT NULL,
            date_given TEXT NOT NULL,
            next_due_date TEXT,
            veterinarian TEXT,
            notes TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets (pet_id)
        )
    """)

    # -------------------------
    # MEDICATIONS TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id TEXT NOT NULL,
            medicine_name TEXT NOT NULL,
            dosage TEXT,
            start_date TEXT,
            end_date TEXT,
            veterinarian TEXT,
            notes TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets (pet_id)
        )
    """)

    # -------------------------
    # HEALTH RECORDS TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id TEXT NOT NULL,
            record_type TEXT NOT NULL,
            record_date TEXT NOT NULL,
            description TEXT,
            veterinarian TEXT,
            notes TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets (pet_id)
        )
    """)

    # -------------------------
    # TREATMENT HISTORY TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id TEXT NOT NULL,
            treatment_name TEXT NOT NULL,
            treatment_date TEXT NOT NULL,
            veterinarian TEXT,
            notes TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets (pet_id)
        )
    """)

    # -------------------------
    # REMINDERS TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id TEXT NOT NULL,
            reminder_type TEXT NOT NULL,
            reminder_date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets (pet_id)
        )
    """)

        # -------------------------
    # ACTIVITY MONITORING TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS activity_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id TEXT NOT NULL,
            activity_value REAL NOT NULL,
            activity_level TEXT,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (pet_id) REFERENCES pets (pet_id)
        )
    """)

    conn.commit()
    conn.close()
    
# -----------------------------
# DASHBOARD
# -----------------------------

@app.route("/")
def home():

    conn = get_db_connection()

    # Get all registered pets
    pets = conn.execute(
        "SELECT * FROM pets ORDER BY id DESC"
    ).fetchall()

    # Count registered pets
    pet_count = conn.execute(
        "SELECT COUNT(*) FROM pets"
    ).fetchone()[0]

    # Count vaccination records
    vaccine_count = conn.execute(
        "SELECT COUNT(*) FROM vaccinations"
    ).fetchone()[0]

    # Count reminders
    reminder_count = conn.execute(
        "SELECT COUNT(*) FROM reminders"
    ).fetchone()[0]

    reminders = conn.execute("""
        SELECT reminders.*, pets.name AS pet_name
        FROM reminders
        JOIN pets
        ON reminders.pet_id = pets.pet_id
        ORDER BY reminder_date ASC
    """).fetchall()

    # Get latest activity record
    latest_activity = conn.execute("""
        SELECT
            activity_records.pet_id,
            pets.name,
            activity_records.activity_value,
            activity_records.activity_level,
            activity_records.recorded_at
        FROM activity_records
        JOIN pets
        ON activity_records.pet_id = pets.pet_id
        ORDER BY activity_records.recorded_at DESC
        LIMIT 1
    """).fetchone()

    conn.close()

    return render_template(
        "index.html",
        pets=pets,
        pet_count=pet_count,
        vaccine_count=vaccine_count,
        reminder_count=reminder_count,
        reminders=reminders,
        latest_activity=latest_activity
    )

# -----------------------------
# REGISTER PET
# -----------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        breed = request.form["breed"]
        age = request.form["age"]
        gender = request.form.get("gender", "")
        owner = request.form["owner"]
        phone = request.form["phone"]

        conn = get_db_connection()

        # Generate next Pet ID
        last_pet = conn.execute(
            "SELECT id FROM pets ORDER BY id DESC LIMIT 1"
        ).fetchone()

        if last_pet:
            next_number = last_pet["id"] + 1
        else:
            next_number = 1

        pet_id = f"SPH-{next_number:03d}"

        # Save pet
        conn.execute("""
            INSERT INTO pets
            (pet_id, name, breed, age, gender, owner, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pet_id,
            name,
            breed,
            age,
            gender,
            owner,
            phone
        ))

        conn.commit()
        conn.close()

        # Create QR folder
        qr_folder = os.path.join(
            "static",
            "qrcodes"
        )

        os.makedirs(qr_folder, exist_ok=True)

        # QR points to this pet's profile
        profile_url = url_for(
            "pet_profile",
            pet_id=pet_id,
            _external=True
        )

        qr = qrcode.make(profile_url)

        qr_path = os.path.join(
            qr_folder,
            f"{pet_id}.png"
        )

        qr.save(qr_path)

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet_id
            )
        )

    return render_template("register_pet.html")


# -----------------------------
# PET PROFILE
# -----------------------------

@app.route("/pet/<pet_id>")
def pet_profile(pet_id):

    conn = get_db_connection()

    pet = conn.execute(
        "SELECT * FROM pets WHERE pet_id = ?",
        (pet_id,)
    ).fetchone()

    conn.close()

    if pet is None:
        return "Pet not found", 404

    return render_template(
        "pet_profile.html",
        pet=pet
    )

# -----------------------------
# PET REMINDERS
# -----------------------------

@app.route("/pet/<pet_id>/reminders", methods=["GET", "POST"])
def pet_reminders(pet_id):

    conn = get_db_connection()

    # Find the pet
    pet = conn.execute(
        "SELECT * FROM pets WHERE pet_id = ?",
        (pet_id,)
    ).fetchone()

    if pet is None:
        conn.close()
        return "Pet not found", 404

    # Add reminder
    if request.method == "POST":

        reminder_type = request.form["reminder_type"]
        reminder_date = request.form["reminder_date"]
        description = request.form.get("description", "")

        conn.execute("""
            INSERT INTO reminders
            (
                pet_id,
                reminder_type,
                reminder_date,
                description
            )
            VALUES (?, ?, ?, ?)
        """, (
            pet_id,
            reminder_type,
            reminder_date,
            description
        ))

        conn.commit()
        conn.close()

        # Redirect after POST so refresh doesn't duplicate the reminder
        return redirect(
            url_for(
                "pet_reminders",
                pet_id=pet_id
            )
        )

    # Get reminders for this pet
    reminders = conn.execute("""
        SELECT *
        FROM reminders
        WHERE pet_id = ?
        ORDER BY reminder_date ASC
    """, (pet_id,)).fetchall()

        # Get latest activity record
    latest_activity = conn.execute("""
        SELECT
            activity_records.pet_id,
            pets.name,
            activity_records.activity_value,
            activity_records.activity_level,
            activity_records.recorded_at
        FROM activity_records
        JOIN pets
        ON activity_records.pet_id = pets.pet_id
        ORDER BY activity_records.recorded_at DESC
        LIMIT 1
    """).fetchone()


    conn.close()

    return render_template(
        "reminders.html",
        pet=pet,
        reminders=reminders,
        latest_activity=latest_activity
    )

# -----------------------------
# OLD PROFILE LINK
# -----------------------------

@app.route("/profile")
def profile():

    conn = get_db_connection()

    pet = conn.execute(
        "SELECT * FROM pets ORDER BY id DESC LIMIT 1"
    ).fetchone()

    conn.close()

    if pet is None:
        return redirect(url_for("register"))

    return redirect(
        url_for(
            "pet_profile",
            pet_id=pet["pet_id"]
        )
    )



# -----------------------------
# VACCINATIONS
# -----------------------------

@app.route("/vaccinations")
def vaccinations():

    conn = get_db_connection()

    records = conn.execute("""
        SELECT vaccinations.*, pets.name
        FROM vaccinations
        JOIN pets ON vaccinations.pet_id = pets.pet_id
        ORDER BY vaccinations.id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "vaccinations.html",
        records=records
    )


    
# -----------------------------
# PET VACCINATION RECORDS
# -----------------------------

@app.route("/pet/<pet_id>/vaccinations", methods=["GET", "POST"])
def pet_vaccinations(pet_id):

    conn = get_db_connection()

    # Find the pet
    pet = conn.execute(
        "SELECT * FROM pets WHERE pet_id = ?",
        (pet_id,)
    ).fetchone()

    if pet is None:
        conn.close()
        return "Pet not found", 404

    # Add vaccination
    if request.method == "POST":

        vaccine_name = request.form["vaccine_name"]
        date_given = request.form["date_given"]
        next_due_date = request.form.get("next_due_date", "")
        veterinarian = request.form.get("veterinarian", "")
        notes = request.form.get("notes", "")

        conn.execute("""
            INSERT INTO vaccinations
            (
                pet_id,
                vaccine_name,
                date_given,
                next_due_date,
                veterinarian,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            pet_id,
            vaccine_name,
            date_given,
            next_due_date,
            veterinarian,
            notes
        ))

        conn.commit()

    # Get vaccination records for this pet
    records = conn.execute("""
        SELECT *
        FROM vaccinations
        WHERE pet_id = ?
        ORDER BY id DESC
    """, (pet_id,)).fetchall()

    conn.close()

    return render_template(
        "pet_vaccinations.html",
        pet=pet,
        records=records
    )
# -----------------------------
# PET MEDICATIONS
# -----------------------------

@app.route("/pet/<pet_id>/medications", methods=["GET", "POST"])
def pet_medications(pet_id):

    conn = get_db_connection()

    # Find the pet
    pet = conn.execute(
        "SELECT * FROM pets WHERE pet_id = ?",
        (pet_id,)
    ).fetchone()

    if pet is None:
        conn.close()
        return "Pet not found", 404

    # Add medication
    if request.method == "POST":

        medicine_name = request.form["medicine_name"]
        dosage = request.form.get("dosage", "")
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")
        veterinarian = request.form.get("veterinarian", "")
        notes = request.form.get("notes", "")

        conn.execute("""
            INSERT INTO medications
            (
                pet_id,
                medicine_name,
                dosage,
                start_date,
                end_date,
                veterinarian,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pet_id,
            medicine_name,
            dosage,
            start_date,
            end_date,
            veterinarian,
            notes
        ))

        conn.commit()

    # Get medication records for this pet
    records = conn.execute("""
        SELECT *
        FROM medications
        WHERE pet_id = ?
        ORDER BY id DESC
    """, (pet_id,)).fetchall()

    conn.close()

    return render_template(
        "pet_medications.html",
        pet=pet,
        records=records
    )

# -----------------------------
# PET HEALTH RECORDS
# -----------------------------

@app.route("/pet/<pet_id>/health-records", methods=["GET", "POST"])
def pet_health_records(pet_id):

    conn = get_db_connection()

    # Find the pet
    pet = conn.execute(
        "SELECT * FROM pets WHERE pet_id = ?",
        (pet_id,)
    ).fetchone()

    if pet is None:
        conn.close()
        return "Pet not found", 404

    # Add health record
    if request.method == "POST":

        record_type = request.form["record_type"]
        record_date = request.form["record_date"]
        description = request.form.get("description", "")
        veterinarian = request.form.get("veterinarian", "")
        notes = request.form.get("notes", "")

        conn.execute("""
            INSERT INTO health_records
            (
                pet_id,
                record_type,
                record_date,
                description,
                veterinarian,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            pet_id,
            record_type,
            record_date,
            description,
            veterinarian,
            notes
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("pet_health_records", pet_id=pet_id))

    # Get health records for this pet
    records = conn.execute("""
        SELECT *
        FROM health_records
        WHERE pet_id = ?
        ORDER BY id DESC
    """, (pet_id,)).fetchall()

    conn.close()

    return render_template(
        "pet_health_records.html",
        pet=pet,
        records=records
    )
# -----------------------------
# PET TREATMENT HISTORY
# -----------------------------

@app.route("/pet/<pet_id>/treatments", methods=["GET", "POST"])
def pet_treatments(pet_id):

    conn = get_db_connection()

    # Find the pet
    pet = conn.execute(
        "SELECT * FROM pets WHERE pet_id = ?",
        (pet_id,)
    ).fetchone()

    if pet is None:
        conn.close()
        return "Pet not found", 404

    # Add treatment
    if request.method == "POST":

        treatment_name = request.form["treatment_name"]
        treatment_date = request.form["treatment_date"]
        veterinarian = request.form.get("veterinarian", "")
        notes = request.form.get("notes", "")

        conn.execute("""
            INSERT INTO treatments
            (
                pet_id,
                treatment_name,
                treatment_date,
                veterinarian,
                notes
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            pet_id,
            treatment_name,
            treatment_date,
            veterinarian,
            notes
        ))

        conn.commit()
        conn.close()

        return redirect(
            url_for(
                "pet_treatments",
                pet_id=pet_id
            )
        )

    # Get treatment records for this pet
    records = conn.execute("""
        SELECT *
        FROM treatments
        WHERE pet_id = ?
        ORDER BY id DESC
    """, (pet_id,)).fetchall()

    conn.close()

    return render_template(
        "treatments.html",
        pet=pet,
        records=records
    )

# -----------------------------
# ESP32 ACTIVITY API
# -----------------------------

@app.route("/api/activity", methods=["POST"])
def receive_activity():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    pet_id = data.get("pet_id")
    activity_value = data.get("activity_value")
    activity_level = data.get("activity_level")

    if not pet_id or activity_value is None:
        return jsonify({
            "success": False,
            "message": "Missing pet_id or activity_value"
        }), 400

    from datetime import datetime

    recorded_at = datetime.now(
    ZoneInfo("Asia/Kolkata")
).strftime(
    "%Y-%m-%d %H:%M:%S"
)
    conn = get_db_connection()

    # Check whether the pet exists
    pet = conn.execute(
        "SELECT * FROM pets WHERE pet_id = ?",
        (pet_id,)
    ).fetchone()

    if pet is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "Pet not found"
        }), 404

    # Store activity record
    conn.execute("""
        INSERT INTO activity_records
        (
            pet_id,
            activity_value,
            activity_level,
            recorded_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        pet_id,
        activity_value,
        activity_level,
        recorded_at
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Activity recorded successfully"
    })

# -----------------------------
# START APPLICATION
# -----------------------------

if __name__ == "__main__":

    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)