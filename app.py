import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO

# 1. Configuração da Página
st.set_page_config(page_title="Removedor de Fundo", page_icon="✂️")

st.title("✂️ Removedor de Fundo Mágico")
st.write("Faça upload de uma imagem e veja a mágica acontecer.")

# 2. O componente de Upload (Drag & Drop)
uploaded_file = st.file_uploader("Escolha uma imagem (JPG ou PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mostra a imagem original
    st.subheader("Imagem Original")
    image = Image.open(uploaded_file)
    st.image(image, caption="Original", use_column_width=True)

    # Botão para processar
    if st.button("Remover Fundo"):
        with st.spinner("A IA está trabalhando..."):
            
            # 3. A Mágica do Rembg
            # Precisamos converter para bytes para a IA processar
            output_image = remove(image)
            
            # Mostra o resultado
            st.subheader("Resultado")
            st.image(output_image, caption="Sem Fundo", use_column_width=True)

            # 4. Botão de Download
            # Convertendo a imagem processada de volta para bytes para download
            buf = BytesIO()
            output_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="Baixar Imagem PNG",
                data=byte_im,
                file_name="sem_fundo.png",
                mime="image/png"
            )