import streamlit as st
import mysql.connector
from datetime import datetime

# Page Configuration for a Professional Look
st.set_page_config(page_title="City Hospital Management", page_icon="🏥", layout="wide")

# Custom CSS to make it look like a Hospital App
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 5px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    </style>
    """, unsafe_allow_html=True)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",           
        password="your_password_here", 
        database="HealthTechDB"
    )

# Sidebar with Hospital Branding
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
st.sidebar.title("City Care Hospital")
st.sidebar.markdown("---")
page = st.sidebar.radio("Main Menu", ["🏥 Dashboard", "📝 Patient Registration", "💊 Medical Records", "🔍 Advanced Search", "⚙️ Admin Settings"])

# --- PAGE 1: DASHBOARD ---
if page == "🏥 Dashboard":
    st.title("Hospital Overview Dashboard")
    
    db = connect_db()
    cursor = db.cursor()
    
    # Get counts for Metrics
    cursor.execute("SELECT COUNT(*) FROM Patients")
    p_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM MedicalRecords")
    r_count = cursor.fetchone()[0]

    # Display Metrics like a real Pro Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", p_count, "New")
    col2.metric("Total Consultations", r_count)
    col3.metric("System Status", "Online", delta_color="normal")
    
    st.markdown("---")
    st.subheader("Recent Registrations")
    cursor.execute("SELECT FullName, Age, Gender, RegistrationDate FROM Patients ORDER BY RegistrationDate DESC LIMIT 5")
    st.table(cursor.fetchall())

# --- PAGE 2: REGISTRATION ---
elif page == "📝 Patient Registration":
    st.title("New Patient Enrollment")
    with st.container():
        st.info("Please enter the patient's legal details below.")
        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name")
            age = c2.number_input("Age", min_value=0, max_value=120)
            gender = c1.selectbox("Gender", ["Male", "Female", "Other"])
            contact = c2.text_input("Contact Number")
            
            if st.form_submit_button("Complete Registration"):
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO Patients (FullName, Age, Gender, Contact) VALUES (%s, %s, %s, %s)", (name, age, gender, contact))
                db.commit()
                st.success(f"Patient {name} has been successfully added to the database!")

# --- PAGE 3: MEDICAL RECORDS ---
elif page == "💊 Medical Records":
    st.title("Clinical Documentation")
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT PatientID, FullName FROM Patients")
    patients = cursor.fetchall()
    patient_dict = {p['FullName']: p['PatientID'] for p in patients}
    
    if not patient_dict:
        st.warning("No patients found in the database.")
    else:
        with st.form("med_form"):
            selected = st.selectbox("Select Patient to Treat", list(patient_dict.keys()))
            diag = st.text_area("Diagnosis / Clinical Notes")
            presc = st.text_area("Prescription / Medicine")
            doc = st.text_input("Attending Physician")
            
            if st.form_submit_button("Save Medical File"):
                p_id = patient_dict[selected]
                cursor.execute("INSERT INTO MedicalRecords (PatientID, Diagnosis, Prescription, DoctorName, VisitDate) VALUES (%s, %s, %s, %s, %s)", (p_id, diag, presc, doc, datetime.now()))
                db.commit()
                st.balloons()
                st.success(f"File updated for {selected}")

# --- PAGE 4: ADVANCED SEARCH ---
elif page == "🔍 Advanced Search":
    st.title("Global Patient Search (DBA View)")
    search_term = st.text_input("Search by Name")
    
    if search_term:
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        # Using the INDEX we created for speed!
        query = "SELECT * FROM Patients WHERE FullName LIKE %s"
        cursor.execute(query, (f"%{search_term}%",))
        results = cursor.fetchall()
        st.write(f"Found {len(results)} matches:")
        st.dataframe(results)

        # --- PAGE 5: ADMIN SETTINGS (Delete Records) ---
elif page == "⚙️ Admin Settings":
    st.title("System Maintenance")
    st.warning("Action: Deleting a patient will also remove all their medical history!")
    
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT PatientID, FullName FROM Patients")
    patients = cursor.fetchall()
    
    if patients:
        patient_names = [p['FullName'] for p in patients]
        patient_to_del = st.selectbox("Select Patient to Remove", patient_names)
        
        if st.button("Permanently Delete Patient"):
            p_id = [p['PatientID'] for p in patients if p['FullName'] == patient_to_del][0]
            cursor.execute("DELETE FROM Patients WHERE PatientID = %s", (p_id,))
            db.commit()
            st.error(f"Patient {patient_to_del} deleted successfully.")
            st.rerun() # This refreshes the page automatically
    else:
        st.info("No patients left to delete.")