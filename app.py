from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app) # Permite que o navegador acesse a API sem bloquear

@app.route('/')
def index():
    # Serve o arquivo HTML quando acessa a raiz
    return send_file('index.html')

@app.route('/remover-fundo', methods=['POST'])
def remover_fundo():
    if 'image' not in request.files:
        return 'Nenhuma imagem enviada', 400
    
    file = request.files['image']
    
    # 1. Processar a imagem na memória (RAM)
    # Isso é ótimo porque não lota seu HD com arquivos temporários
    input_image = Image.open(file.stream)
    
    # 2. Remover o fundo
    output_image = remove(input_image)
    
    # 3. Preparar para devolver (converter para bytes)
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # 4. Devolver a imagem pronta para o navegador
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5000)