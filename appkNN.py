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

st.title("Machine Learning Penentuan Bonus Karyawan")

nama = st.text_input("Nama Karyawan")

hadir1 = st.number_input("Kehadiran Bulan 1", 0, 31)
hadir2 = st.number_input("Kehadiran Bulan 2", 0, 31)
hadir3 = st.number_input("Kehadiran Bulan 3", 0, 31)
hadir4 = st.number_input("Kehadiran Bulan 4", 0, 31)
hadir5 = st.number_input("Kehadiran Bulan 5", 0, 31)
hadir6 = st.number_input("Kehadiran Bulan 6", 0, 31)

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

    st.subheader("Hasil Prediksi")

    st.write("Nama Karyawan :", nama)

    st.write("Total Kehadiran :", total_hadir)

    st.write("Accuracy :", round(accuracy, 2))

    st.write("Precision :", round(precision, 2))

    st.write("Recall :", round(recall, 2))

    if hasil[0] == 1:
        st.success("Karyawan Mendapat Bonus")
    else:
        st.error("Karyawan Tidak Mendapat Bonus")

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
