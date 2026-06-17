import streamlit as st
import mysql.connector
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score
)

# ==========================================
# KONEKSI DATABASE
# ==========================================

koneksi = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistem bonus karyawan"
)

# ==========================================
# AMBIL DATASET
# ==========================================

query = "SELECT * FROM dataset_bonus"

df = pd.read_sql(query, koneksi)

# ==========================================
# FITUR DAN LABEL
# ==========================================

X = df[[
    'status_absen',
    'lembur',
    'dinas_luar',
    'masa_kerja',
    'kinerja'
]]

y = df['bonus']

# ==========================================
# SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# MODEL KNN
# ==========================================

model = KNeighborsClassifier(n_neighbors=3)

model.fit(X_train, y_train)

# ==========================================
# TESTING MODEL
# ==========================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

# ==========================================
# INPUT USER
# ==========================================

st.markdown("""
<h1 style='text-align:center; color:#22c55e; font-size:40px; font-weight:800;'>
🤖 Machine Learning Penentuan Bonus Karyawan
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; color:#cbd5e1; margin-top:-10px;'>
 Machine Learning K-Nearest Neighbor (KNN) Penentuan Bonus Karyawan
</p>
""", unsafe_allow_html=True)

nama = st.text_input("👤 Nama Karyawan")

hadir1 = st.number_input("📅 Kehadiran Bulan 1", 0, 31)
hadir2 = st.number_input("📅 Kehadiran Bulan 2", 0, 31)
hadir3 = st.number_input("📅 Kehadiran Bulan 3", 0, 31)
hadir4 = st.number_input("📅 Kehadiran Bulan 4", 0, 31)
hadir5 = st.number_input("📅 Kehadiran Bulan 5", 0, 31)
hadir6 = st.number_input("📅 Kehadiran Bulan 6", 0, 31)

lembur = st.selectbox("⏱ Lembur", ["Ya", "Tidak"])
dinas_luar = st.selectbox("✈️ Dinas Luar", ["Ya", "Tidak"])
masa_kerja = st.selectbox("🧑‍💼 Masa Kerja", ["Baru", "Lama"])
kinerja = st.selectbox("📊 Kinerja", ["Baik", "Sangat Baik"])

# ==========================================
# PROSES PREDIKSI
# ==========================================

if st.button("Proses Prediksi"):

    total_hadir = (
        hadir1 +
        hadir2 +
        hadir3 +
        hadir4 +
        hadir5 +
        hadir6
    )

    # Status Absen
    if total_hadir >= 140:
        status_absen = 1
    else:
        status_absen = 0

    # Encoding
    lembur_input = 1 if lembur == "Ya" else 0

    dinas_input = 1 if dinas_luar == "Ya" else 0

    masa_kerja_input = 1 if masa_kerja == "Lama" else 0

    if kinerja == "Sangat Baik":
        kinerja_input = 2
    else:
        kinerja_input = 1

    # Data Baru
    data_baru = [[
        status_absen,
        lembur_input,
        dinas_input,
        masa_kerja_input,
        kinerja_input
    ]]

    # Prediksi
    hasil = model.predict(data_baru)

    # ==========================================
    # OUTPUT
    # ==========================================

    st.subheader("Hasil Prediksi 📊")

    st.write("👤 Nama Karyawan :", nama)

    st.write("📅 Total Kehadiran :", total_hadir)

    st.write("🎯 Accuracy :", round(accuracy, 2))

    st.write("📌 Precision :", round(precision, 2))

    st.write("🔁 Recall :", round(recall, 2))

    if hasil[0] == 1:
        st.success("🏆 Karyawan Mendapat Bonus")
    else:
        st.error("❌ Karyawan Tidak Mendapat Bonus")

    # ==========================================
    # CONFUSION MATRIX
    # ==========================================

    cm = confusion_matrix(y_test, y_pred)

    cm_df = pd.DataFrame(
        cm,
        index=["Aktual Tidak Bonus", "Aktual Bonus"],
        columns=["Prediksi Tidak Bonus", "Prediksi Bonus"]
    )

    st.subheader("Confusion Matrix")

    st.dataframe(cm_df)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    color: white;
}

.main-box {
    background-color: #111827;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(34,197,94,0.3);
    margin-top: 10px;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #4ade80;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 25px;
}

.stTextInput label,
.stSelectbox label,
.stNumberInput label {
    color: white !important;
    font-weight: bold;
}

.stTextInput input,
.stNumberInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px;
    border: 1px solid #22c55e;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #22c55e, #16a34a);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    padding: 12px;
}

.stButton>button:hover {
    background: linear-gradient(to right, #4ade80, #22c55e);
    color: white;
}

.hasil-box {
    background-color: #111827;
    padding: 25px;
    border-radius: 20px;
    margin-top: 25px;
    border-left: 6px solid #22c55e;
    box-shadow: 0px 0px 15px rgba(34,197,94,0.3);
}

</style>
""", unsafe_allow_html=True)
