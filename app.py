import streamlit as st
import mysql.connector

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

# =====================================================
# HEADER
# =====================================================

'<div class="title">🤖 Machine Learning Penentuan Bonus Karyawan</div>'

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

proses = st.button("🔍 Proses Penentuan Bonus")

# =====================================================
# RULE ENGINE
# =====================================================

if proses:

    total_hadir = (
        hadir1 +
        hadir2 +
        hadir3 +
        hadir4 +
        hadir5 +
        hadir6
    )

    # =============================================
    # MENENTUKAN STATUS ABSEN
    # =============================================

    if total_hadir >= 140:
        status_absen = "Rajin"
    else:
        status_absen = "Kurang Rajin"

    # =============================================
    # SIMPAN DATA PENILAIAN
    # =============================================

    query_simpan = """
    INSERT INTO penilaian_karyawan
    (
        nama_karyawan,
        hadir_bulan1,
        hadir_bulan2,
        hadir_bulan3,
        hadir_bulan4,
        hadir_bulan5,
        hadir_bulan6,
        total_hadir,
        status_absen,
        lembur,
        dinas_luar,
        masa_kerja,
        kinerja
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    data = (
        nama,
        hadir1,
        hadir2,
        hadir3,
        hadir4,
        hadir5,
        hadir6,
        total_hadir,
        status_absen,
        lembur,
        dinas_luar,
        masa_kerja,
        kinerja
    )

    cursor.execute(query_simpan, data)

    koneksi.commit()

    # =============================================
    # AMBIL RULE
    # =============================================

    cursor.execute("SELECT * FROM rules")

    rules = cursor.fetchall()

    hasil_bonus = "Tidak"

    rule_cocok = None

    reasoning = ""

    # =============================================
    # PROSES RULE ENGINE
    # =============================================

    for rule in rules:

        rule_id = rule['id']

        cursor.execute(
            "SELECT parameter, nilai FROM conditions WHERE rule_id=%s",
            (rule_id,)
        )

        kondisi = cursor.fetchall()

        cocok = True

        for k in kondisi:

            parameter = k['parameter']
            nilai = k['nilai']

            if parameter == 'absen':

                if status_absen != nilai:
                    cocok = False

            elif parameter == 'lembur':

                if lembur != nilai:
                    cocok = False

            elif parameter == 'dinas_luar':

                if dinas_luar != nilai:
                    cocok = False

            elif parameter == 'masa_kerja':

                if masa_kerja != nilai:
                    cocok = False

            elif parameter == 'kinerja':

                if kinerja != nilai:
                    cocok = False

        # =========================================
        # REASONING
        # =========================================

        if cocok:

            hasil_bonus = rule['hasil']

            rule_cocok = rule_id

            reasoning = f"""
            Rule {rule_id} cocok karena:

            ✔ Status Absen = {status_absen}
            ✔ Lembur = {lembur}
            ✔ Dinas Luar = {dinas_luar}
            ✔ Masa Kerja = {masa_kerja}
            ✔ Kinerja = {kinerja}

            Semua kondisi sesuai dengan rule pada database.
            """

            break

    # =============================================
    # SIMPAN HASIL BONUS
    # =============================================

    query_bonus = """
    INSERT INTO hasil_bonus
    (
        nama_karyawan,
        hasil_bonus,
        rule_digunakan
    )

    VALUES
    (
        %s,%s,%s
    )
    """

    data_bonus = (
        nama,
        hasil_bonus,
        rule_cocok
    )

    cursor.execute(query_bonus, data_bonus)

    koneksi.commit()

    # =============================================
    # OUTPUT HASIL
    # =============================================


    st.subheader("📊 Hasil Diagnosa")

    st.write(f"### 👤 Nama Karyawan : {nama}")

    st.write(f"### 📅 Total Kehadiran : {total_hadir}")

    st.write(f"### ✅ Status Absen : {status_absen}")

    st.write(f"### 📌 Rule Yang Digunakan : Rule {rule_cocok}")

    if hasil_bonus == "Ya":
        st.success("🎉 Karyawan Mendapat Bonus")
    else:
        st.error("❌ Karyawan Tidak Mendapat Bonus")

    st.info(reasoning)