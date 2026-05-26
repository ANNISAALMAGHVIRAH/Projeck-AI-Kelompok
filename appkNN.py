import streamlit as st
import mysql.connector

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Sistem Penentuan Bonus Karyawan",
    page_icon="💰",
    layout="centered"
)

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

# =====================================================
# KONEKSI DATABASE
# =====================================================

koneksi = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistem bonus karyawan"
)

cursor = koneksi.cursor(dictionary=True)

# Ambil data dari database
query = "SELECT * FROM dataset_bonus"
df = pd.read_sql(query, koneksi)

## Fitur dan Label
X = df[['status_absen',
        'lembur',
        'dinas_luar',
        'masa_kerja',
        'kinerja']]

y = df['bonus']

# Membagi data training dan testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Membuat model kNN
model = KNeighborsClassifier(n_neighbors=3)

# Training model
model.fit(X_train, y_train)

# Prediksi data testing
y_pred = model.predict(X_test)

# Menghitung accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy :", accuracy)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="title">🤖 Machine Learning Penentuan Bonus Karyawan</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Machine Learning k-Nearest Neighbor (kNN) Penentuan Bonus Karyawan</div>',
    unsafe_allow_html=True
)

# =====================================================
# FORM INPUT
# =====================================================


nama = st.text_input("Nama Karyawan")

st.subheader("📅 Kehadiran Selama 6 Bulan")

col1, col2 = st.columns(2)

with col1:
    hadir1 = st.number_input("Bulan 1", 0, 31)
    hadir2 = st.number_input("Bulan 2", 0, 31)
    hadir3 = st.number_input("Bulan 3", 0, 31)

with col2:
    hadir4 = st.number_input("Bulan 4", 0, 31)
    hadir5 = st.number_input("Bulan 5", 0, 31)
    hadir6 = st.number_input("Bulan 6", 0, 31)

lembur = st.selectbox(
    "Lembur",
    ["Ya", "Tidak"]
)

dinas_luar = st.selectbox(
    "Dinas Luar",
    ["Ya", "Tidak"]
)

masa_kerja = st.selectbox(
    "Masa Kerja",
    ["Baru", "Lama"]
)

kinerja = st.selectbox(
    "Kinerja",
    ["Baik", "Sangat Baik"]
)

proses = st.button(
    "🔍 Proses Penentuan Bonus",
    key="btn_proses_bonus"
)

if proses:

    total_hadir = (
        hadir1 +
        hadir2 +
        hadir3 +
        hadir4 +
        hadir5 +
        hadir6
    )

    if total_hadir >= 140:
        status_absen = 1
    else:
        status_absen = 0

    lembur_input = 1 if lembur == "Ya" else 0

    dinas_input = 1 if dinas_luar == "Ya" else 0

    masa_kerja_input = 1 if masa_kerja == "Lama" else 0

    if kinerja == "Sangat Baik":
        kinerja_input = 2
    else:
        kinerja_input = 1

    data_baru = [[
        status_absen,
        lembur_input,
        dinas_input,
        masa_kerja_input,
        kinerja_input
    ]]

    hasil = model.predict(data_baru)
    
    st.subheader("📊 Hasil Prediksi")

    st.write(f"### 👤 Nama Karyawan : {nama}")

    st.write(f"### 📅 Total Kehadiran : {total_hadir}")

    st.write(f"### 🎯 Accuracy Model : {accuracy:.2f}")
    
    from sklearn.metrics import precision_score, recall_score
    
    precision = precision_score(y_test, y_pred)
    
    recall = recall_score(y_test, y_pred)
    
    st.write(f"📌 Precision : {precision:.2f}")
    st.write(f"📌 Recall : {recall:.2f}")

    if hasil[0] == 1:
        st.success("🎉 Karyawan Mendapat Bonus")
    else:
        st.error("❌ Karyawan Tidak Mendapat Bonus")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)



cm_df = pd.DataFrame(
    cm,
    index=["Aktual Tidak Bonus", "Aktual Bonus"],
    columns=["Prediksi Tidak Bonus", "Prediksi Bonus"]
)

st.subheader("Confusion Matrix")

st.dataframe(cm_df)
