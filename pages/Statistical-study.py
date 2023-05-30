import streamlit as st
import qrcode
from PIL import Image
import io

st.sidebar.markdown("#  Statistical analisys ")

st.markdown("<h1 style='text-align: center; color : lightblue;'> Statistical analisys of the TAL </h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color : lightblue;'> Summary </h1>", unsafe_allow_html=True)

st.write("The TAL is a financial tool designed to be on par with a currency. Its objective is to provide a strong alternative to the US dollar and other assets used to hedge against liquidity risk and currency devaluation. The conducted studies analyze the statistical behavior of TAL in comparison to each currency with respect to the US dollar, which is considered the primary global exchange value. ")
st.write("Two approaches are taken : the first involves creating a model to compare projections by studying historical variations of TAL and other currencies, while the second examines historical variations between different currencies to simulate TAL fluctuations. ")
st.write("It is observed that the average variation of TAL is practically zero, which can be attributed to the significance of gold in its basket. Gold serves as a hedge against fluctuations in other currencies, thereby stabilizing the basket's value. Thus, TAL proves to be a better alternative for preserving value compared to an individual currency. Additionally, TAL presents lower risk and higher stability than its six individual basket components. During times of crisis, TAL reacts more stably.")
st.write(" In conclusion, TAL positions itself as a strong alternative to the US dollar, providing stability and protection against liquidity risk and currency devaluation while allowing unrestricted access to one's funds.")
st.write(' ')
col1,col2,col3 = st.columns([3,2,3])
col2.write('Here is the QRcode for the detailed study : ')


# Chemin vers le fichier
chemin_fichier_pdf = "https://drive.google.com/file/d/1brewYky0YjhiEZksYWaaucL8ax_gkmI3/view?usp=share_link"

# Génération du code QR
qr = qrcode.QRCode(version=1, box_size=5, border=4)
qr.add_data(chemin_fichier_pdf)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")

# Conversion de l'image en bytes
bytes_io = io.BytesIO()
qr_img.save(bytes_io, format="PNG")
qr_bytes = bytes_io.getvalue()

# Affichage du code QR dans l'application Streamlit

col2.image(qr_bytes, caption="Scan the QR code to open the PDF file", use_column_width=True)
