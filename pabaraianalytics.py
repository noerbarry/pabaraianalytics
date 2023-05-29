import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.io as pio
import io
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
 
# Menampilkan copy right di sidebar
st.sidebar.markdown("---")
st.sidebar.write("© Pabarai Analytics")

# Inisialisasi aplikasi Firebase 
# Specify the full path to the service account key file
service_account_path = 'pabaranalytics-firebase-adminsdk-th0qb-1efdb39cf3.json'

# Initialize Firebase credentials
cred = credentials.Certificate(service_account_path)
 
try:
    app = firebase_admin.get_app("pabar")
except ValueError:  # Jika aplikasi "pabar" belum diinisialisasi sebelumnya
    app = firebase_admin.initialize_app(cred, name="pabar")
db = firestore.client(app)

# Fungsi untuk mendaftar akun baru
def sign_up(email, password):
    # Periksa apakah email sudah digunakan
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1).get()
    if query:
        return False

    # Simpan data pengguna ke Firebase
    user_data = {
        'email': email,
        'password': password
    }
    db.collection('users').add(user_data)
    return True

# Fungsi untuk memeriksa kecocokan email dan password
def sign_in(email, password):
    # Periksa kecocokan email dan password di Firebase
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).where('password', '==', password).limit(1).get()
    if query:
        return True
    return False

# Fungsi untuk logout
def logout():
    st.session_state['user'] = None
    st.warning('Anda telah keluar dari akun.')
    st.experimental_rerun()

def download_chart(chart, filename):
    fig = chart.to_image(format="png")
    with open(filename, "wb") as f:
        f.write(fig)
    st.markdown(f'<a href="data:image/png;base64,{fig}" download="{filename}">Unduh Grafik</a>', unsafe_allow_html=True)

# Fungsi untuk menampilkan menu utama setelah login
def show_main_menu(user):
    st.subheader('Menu Utama')
    menu = st.sidebar.selectbox('Navigasi', ['Profil', 'Grafik'])

    if menu == 'Profil':
        st.subheader('Profil Pengguna')
        st.write('Email:', user['email'])  # Mengakses email pengguna dari dictionary
        if st.button('Logout'):
            logout()
    elif menu == 'Grafik':
        st.subheader('Pilih Jenis Grafik')
        chart_type = st.selectbox('Jenis Grafik', ['Line Chart', 'Bar Chart', 'Histogram', 'Plotly Chart'])
        if chart_type == 'Line Chart':
            st.subheader('Grafik Line')
            uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                st.dataframe(data)

                x_column = st.selectbox('Pilih Kolom X', data.columns)
                y_column = st.selectbox('Pilih Kolom Y', data.columns)

                # Jika tombol "Tampilkan Grafik" ditekan
                if st.button('Tampilkan Grafik'):
                    # Membuat grafik line menggunakan Plotly Express
                    fig = px.line(data, x=x_column, y=y_column)

                    # Menampilkan grafik line di layar menggunakan st.plotly_chart()
                    st.plotly_chart(fig)

                    # Mengunduh grafik
                    st.markdown("### Download Grafik")
                    download_chart(fig, 'line_chart.png')

        elif chart_type == 'Bar Chart':
            st.subheader('Grafik Batang')
            uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                st.dataframe(data)

                x_column = st.selectbox('Pilih Kolom X', data.columns)
                y_column = st.selectbox('Pilih Kolom Y', data.columns)

                # Jika tombol "Tampilkan Grafik" ditekan
                if st.button('Tampilkan Grafik'):
                    # Membuat grafik batang menggunakan Plotly Express
                    fig = px.bar(data, x=x_column, y=y_column)

                    # Menampilkan grafik batang di layar menggunakan st.plotly_chart()
                    st.plotly_chart(fig)

                    # Mengunduh grafik
                    st.markdown("### Download Grafik")
                    download_chart(fig, 'bar_chart.png')

        elif chart_type == 'Histogram':
            st.subheader('Histogram')
            uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                st.dataframe(data)

                column = st.selectbox('Pilih Kolom', data.columns)

                # Jika tombol "Tampilkan Histogram" ditekan
                if st.button('Tampilkan Histogram'):
                    hist_data = data[column].tolist()

                    # Membuat objek Figure dan Axes
                    fig, ax = plt.subplots(figsize=(8, 6))

                    # Plot histogram pada Axes
                    ax.hist(hist_data, bins='auto', color='blue', alpha=0.7)

                    # Set label dan judul pada Axes
                    ax.set_xlabel('Data')
                    ax.set_ylabel('Frequency')
                    ax.set_title('Histogram')

                    # Menampilkan histogram di layar menggunakan st.pyplot()
                    st.pyplot(fig)

                    # Save the figure to a BytesIO object
                    img_buffer = io.BytesIO()
                    plt.savefig(img_buffer, format='png')
                    img_buffer.seek(0)

                    # Create a download button for the histogram image
                    st.download_button(
                        label="Download Histogram",
                        data=img_buffer,
                        file_name="histogram.png",
                        mime="image/png"
                    )

        elif chart_type == 'Plotly Chart':
            st.subheader('Plotly Chart')
            uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                st.dataframe(data)

                x_column = st.selectbox('Pilih Kolom X', data.columns)
                y_column = st.selectbox('Pilih Kolom Y', data.columns)

                # Jika tombol "Tampilkan Grafik" ditekan
                if st.button('Tampilkan Grafik'):
                    # Membuat grafik menggunakan Plotly Express
                    fig = px.scatter(data, x=x_column, y=y_column)

                    # Menampilkan grafik di layar menggunakan st.plotly_chart()
                    st.plotly_chart(fig)

                    # Mengunduh grafik
                    st.markdown("### Download Grafik")
                    download_chart(fig, 'plotly_chart.png')

# Halaman login
st.title('Login')
email = st.text_input('Email')
password = st.text_input('Password', type='password')

# Cek jika tombol "Masuk" ditekan
if st.button('Masuk'):
    if sign_in(email, password):
        st.success('Anda berhasil masuk!')
        st.session_state['user'] = {'email': email, 'password': password}
        show_main_menu(st.session_state['user'])
    else:
        st.error('Email atau password salah.')

# Halaman pendaftaran
st.title('Daftar')
new_email = st.text_input('Email baru')
new_password = st.text_input('Password baru', type='password')
confirm_password = st.text_input('Konfirmasi password', type='password')

# Cek jika tombol "Daftar" ditekan
if st.button('Daftar'):
    if new_password != confirm_password:
        st.error('Password tidak cocok. Harap coba lagi.')
    else:
        if sign_up(new_email, new_password):
            st.success('Akun berhasil didaftarkan!')
        else:
            st.error('Email sudah digunakan. Harap gunakan email lain.')

# Cek jika pengguna sudah login
if 'user' in st.session_state:
    show_main_menu(st.session_state['user'])
