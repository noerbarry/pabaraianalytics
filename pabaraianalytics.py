import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from PIL import Image
import io
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import re
import base64
import pyecharts.options as opts
from pyecharts.faker import Faker
import numpy as np


# Menampilkan copy right di sidebar
st.sidebar.markdown("---")
st.sidebar.write("© Pabarai Analytics")
st.page_title="pabarai analytics"
st.page_icon="favicon.ico"
   
# Inisialisasi aplikasi Firebase
cred = credentials.Certificate('pabaranalytics-firebase-adminsdk-th0qb-1efdb39cf3.json')  # Ganti dengan path ke serviceAccountKey.json Anda

try:
    app = firebase_admin.get_app("pabar")
except ValueError:  # Jika aplikasi "pabar" belum diinisialisasi sebelumnya
    app = firebase_admin.initialize_app(cred, name="pabar")
db = firestore.client(app)

# Fungsi untuk mendaftar akun baru
def sign_up(email, password):
    try:
        if not email or not password:
            st.error('Email dan password harus diisi.')
            return False

        # Validasi format email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error('Format email tidak valid.')
            return False

        # Periksa apakah email sudah digunakan
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).limit(1).get()
        if query:
            st.error('Email sudah terdaftar. Gunakan email lain.')
            return False

        # Simpan data pengguna ke Firebase
        user_data = {
            'email': email,
            'password': password
        }
        db.collection('users').add(user_data)
        return True
    except auth.FirebaseAuthError as error:
        st.error(f"Error: {str(error)}")
        return False

# Fungsi untuk memeriksa kecocokan email dan password
def sign_in(email, password):
    try:
        # Periksa kecocokan email dan password di Firebase
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).where('password', '==', password).limit(1).get()
        if query:
            return True
        return False
    except auth.FirebaseAuthError as error:
        st.error(f"Error: {str(error)}")
        return False

# Fungsi untuk logout
def logout():
    st.session_state['user'] = None
    st.warning('Anda telah keluar dari akun.')
    st.experimental_rerun()

# Fungsi untuk mengunduh grafik
def download_chart(chart, filename):
    img_data = io.BytesIO()
    chart.write_image(img_data, format='png')
    img_data.seek(0)

    encoded_img_data = base64.b64encode(img_data.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{encoded_img_data}" download="{filename}">Unduh Grafik</a>'
    st.write(href, unsafe_allow_html=True)
    
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
        chart_type = st.selectbox('Jenis Grafik', ['Line Chart', 'Bar Chart', 'Histogram', 'Elements', 'Plost', 'Plotly Chart'])
        if chart_type == 'Line Chart':
            st.subheader('Grafik Line')
            uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file, delimiter=';')

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
                data = pd.read_csv(uploaded_file, delimiter=';')
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
                data = pd.read_csv(uploaded_file, delimiter=';')
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

        elif chart_type == 'Elements': 
             st.subheader('Grafik Elements')
             uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
             if uploaded_file is not None:
                 data = pd.read_csv(uploaded_file, delimiter=';')
                 st.dataframe(data)

                 label_column = st.selectbox('Pilih Kolom Label', data.columns)
                 value_column = st.selectbox('Pilih Kolom Nilai', data.columns)

                 # Jika tombol "Tampilkan Grafik" ditekan
                 if st.button('Tampilkan Grafik'):
                     # Membuat objek pie chart
                     fig = go.Figure(data=[go.Pie(labels=data[label_column], values=data[value_column])])

                     # Menampilkan grafik pie chart di layar menggunakan st.plotly_chart()
                     st.plotly_chart(fig)

                     # Mengunduh grafik
                     st.markdown("### Download Grafik")
                     download_chart(fig, 'elements_chart.png')
        elif chart_type == 'Scatter Plot':
             st.subheader('Scatter Plot')
             uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
             if uploaded_file is not None:
                 data = pd.read_csv(uploaded_file, delimiter=';')
                 st.dataframe(data)

                 x_column = st.selectbox('Pilih Kolom X', data.columns)
                 y_column = st.selectbox('Pilih Kolom Y', data.columns)

                 # Jika tombol "Tampilkan Grafik" ditekan
                 if st.button('Tampilkan Grafik'):
                     # Membuat grafik scatter plot menggunakan matplotlib
                     fig, ax = plt.subplots(figsize=(8, 6))
                     ax.scatter(data[x_column], data[y_column])
                     ax.set_xlabel(x_column)
                     ax.set_ylabel(y_column)
                     ax.set_title('Scatter Plot')

                     # Menampilkan grafik scatter plot di layar menggunakan st.pyplot()
                     st.pyplot(fig)

                     # Mengunduh grafik
                     st.markdown("### Download Grafik")
                     download_chart(fig, 'scatter_plot.png') 

        elif chart_type == 'Plotly Chart':
            st.subheader('Plotly Chart')
            uploaded_file = st.file_uploader('Unggah file CSV', type=['csv'])
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file, delimiter=';')
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
  

# Fungsi untuk tampilan awal
def show_login_page():
    st.subheader('Halaman Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if sign_in(email, password):
            st.success('Login berhasil.')
            user_data = {
                'email': email,
                'password': password
            }
            st.session_state['user'] = user_data
            show_main_menu(user_data)
        else:
            st.error('Login gagal. Email atau password salah.')

# Fungsi untuk tampilan pendaftaran
def show_signup_page():
    st.subheader('Halaman Pendaftaran')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Konfirmasi Password', type='password')
    if st.button('Daftar'):
        if password == confirm_password:
            if sign_up(email, password):
                st.success('Pendaftaran berhasil. Silakan login.')
            else:
                st.error('Email sudah digunakan. Silakan gunakan email lain.')
        else:
            st.error('Konfirmasi password tidak cocok.')

# Fungsi utama
def main():
    st.title('Visualize Your Data with Ease')
    st.write('Effortless Data Visualization: Seamlessly Generate Line, Bar, Histogram, and Plotly Charts from CSV Uploads')
    st.write('© Pabarai Analytics')
    st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
    )

    st.sidebar.title('Menu')
    user = st.session_state.get('user')

    if user is None:
        menu = st.sidebar.radio('Navigasi', ['Login', 'Daftar'])

        if menu == 'Login':
            show_login_page()
        elif menu == 'Daftar':
            show_signup_page()
    else:
        show_main_menu(user)

# Menjalankan aplikasi
if __name__ == '__main__':
    main()
