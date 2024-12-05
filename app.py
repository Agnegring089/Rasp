from flask import Flask, render_template, request, redirect, url_for, jsonify
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# Lista de cafés
cafes = [
    {"id": 1, "nome": "Expresso", "preco": 5.0, "imagem": "static/imagens/expresso.jpg"},
    {"id": 2, "nome": "Cappuccino", "preco": 7.0, "imagem": "static/imagens/capuccino.jpeg"},
    {"id": 3, "nome": "Latte", "preco": 6.5, "imagem": "static/imagens/latte.jpg"},
]

@app.route('/')
def index():
    return render_template('index.html', cafes=cafes)

@app.route('/confirmar/<int:cafe_id>', methods=['GET', 'POST'])
def confirmar(cafe_id):
    cafe = next((c for c in cafes if c["id"] == cafe_id), None)
    if not cafe:
        return "Café não encontrado", 404

    if request.method == 'POST':
        nome = request.form.get('nome')
        # Lógica de processamento do nome ou envio para o backend pode ser adicionada aqui.
        return f"Obrigado, {nome}! Pedido confirmado para o café {cafe['nome']}."

    # Gerar QR Code Pix
    chave_pix = "sua_chave_pix"
    valor = cafe["preco"]
    qr_data = f"PIX|{chave_pix}|{valor:.2f}"
    qr_img = qrcode.make(qr_data)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render_template('confirmar.html', cafe=cafe, qr_code=qr_code_base64)

@app.route('/api/pedidos', methods=['GET'])
def listar_pedidos():
    return jsonify(pedidos)

@app.route('/api/pedidos/<int:pedido_id>', methods=['GET'])
def obter_pedido(pedido_id):
    pedido = next((p for p in pedidos if p['id'] == pedido_id), None)
    if pedido:
        return jsonify(pedido)
    return jsonify({"error": "Pedido não encontrado"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
