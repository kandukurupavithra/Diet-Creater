import streamlit as st
import sqlite3

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="Medicine Reminder",
    page_icon="💊",
    layout="centered"
)

# -----------------------------
# Database functions
# -----------------------------

def create_database():
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            time TEXT NOT NULL,
            frequency TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_medicine(name, dosage, time, frequency):
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medicines (name, dosage, time, frequency)
        VALUES (?, ?, ?, ?)
    """, (name, dosage, time, frequency))

    conn.commit()
    conn.close()


def get_medicines():
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, dosage, time, frequency
        FROM medicines
        ORDER BY time
    """)

    medicines = cursor.fetchall()
    conn.close()

    return medicines


def delete_medicine(medicine_id):
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM medicines WHERE id = ?",
        (medicine_id,)
    )

    conn.commit()
    conn.close()


# Create database when application starts
create_database()


# -----------------------------
# Frontend
# -----------------------------

st.title("💊 Medicine Reminder")

st.write("Welcome to your personal medicine reminder!")

st.divider()

# -----------------------------
# Add Medicine
# -----------------------------

st.header("➕ Add Medicine")

medicine_name = st.text_input("Medicine Name")

dosage = st.text_input("Dosage")

medicine_time = st.time_input("Medicine Time")

frequency = st.selectbox(
    "How often?",
    [
        "Once Daily",
        "Twice Daily",
        "Three Times Daily"
    ]
)

if st.button("➕ Add Medicine"):

    if medicine_name and dosage:

        time_string = medicine_time.strftime("%H:%M")

        add_medicine(
            medicine_name,
            dosage,
            time_string,
            frequency
        )

        st.success(
            f"✅ {medicine_name} has been added!"
        )

        st.rerun()

    else:
        st.warning(
            "Please enter the medicine name and dosage."
        )


# -----------------------------
# Display Medicines
# -----------------------------

st.divider()

st.header("📋 My Medicines")

medicines = get_medicines()

if not medicines:

    st.info("No medicines added yet.")

else:

    for medicine in medicines:

        medicine_id = medicine[0]
        name = medicine[1]
        dosage = medicine[2]
        time = medicine[3]
        frequency = medicine[4]

        with st.container():

            st.subheader(f"💊 {name}")

            st.write(f"💉 **Dosage:** {dosage}")
            st.write(f"⏰ **Time:** {time}")
            st.write(f"🔄 **Frequency:** {frequency}")

            if st.button(
                "🗑️ Delete",
                key=f"delete_{medicine_id}"
            ):

                delete_medicine(medicine_id)

                st.success(
                    f"{name} deleted successfully!"
                )

                st.rerun()

            st.divider()