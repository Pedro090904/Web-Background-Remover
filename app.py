import io
import os
from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image

app = Flask(__name__)
CORS(app)

# Aumenta o limite de tamanho de upload para 16MB (opcional, mas bom ter)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    # Procura o arquivo index.html na mesma pasta
    if os.path.exists('index.html'):
        return send_file('index.html')
    return "Erro: Arquivo index.html não encontrado."

@app.route('/remover-fundo', methods=['POST'])
def remover_fundo():
    print("--- Recebendo requisição ---")
    
    if 'image' not in request.files:
        print("Erro: Nenhuma imagem enviada no corpo da requisição.")
        return 'Nenhuma imagem enviada', 400
    
    file = request.files['image']
    if file.filename == '':
        print("Erro: Nome do arquivo vazio.")
        return 'Nenhum arquivo selecionado', 400

    try:
        print(f"Processando imagem: {file.filename}")
        
        # 1. Converte o arquivo enviado para uma Imagem PIL
        input_image = Image.open(file.stream)

        # 2. Remove o fundo
        # alpha_matting=True melhora bordas, mas pode ser lento. 
        # Se ficar muito lento, remova os parametros extras e deixe só remove(input_image)
        output_image = remove(input_image)

        # 3. Salva em memória (BytesIO) para devolver
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        print("Sucesso: Fundo removido e imagem pronta para envio.")
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        print(f"ERRO CRÍTICO NO SERVIDOR: {e}")
        return f"Erro ao processar imagem: {str(e)}", 500

if __name__ == '__main__':
    print("Servidor rodando em http://localhost:5000")
    app.run(debug=True, port=5000)