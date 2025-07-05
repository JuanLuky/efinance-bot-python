import re
import json
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 👉 Coloque aqui o token do seu Bot
TELEGRAM_TOKEN = '7808015731:AAEnusaNF7LI6-oAFw86B0mdPVjDit-F5fo'

# 👉 URL da sua API que vai receber os dados (Spring Boot, por exemplo)
API_URL = 'http://localhost:8080/api/lancamentos'  # Ajuste para sua URL real

ARQUIVO_JSON = 'lancamentos.json'

# Função para extrair dados da mensagem
def extrair_info(mensagem):
    tipo = 'gasto' if 'gastei' in mensagem.lower() else 'ganho'
    valor_match = re.search(r'(\d+(?:[\.,]\d+)?)', mensagem)
    valor = float(valor_match.group(1).replace(',', '.')) if valor_match else 0.0

    # Extrai a categoria da frase
    partes = mensagem.lower().split('com')
    categoria = partes[1].strip() if len(partes) > 1 else 'geral'

    return {
        'tipo': tipo,
        'valor': valor,
        'categoria': categoria
    }
# Salva localmente em JSON
def salvar_localmente(dado):
    # Se o arquivo não existir, cria com lista vazia
    if not os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'w') as f:
            json.dump([], f)

    # Lê o conteúdo existente e adiciona o novo
    with open(ARQUIVO_JSON, 'r+') as f:
        dados = json.load(f)
        dados.append(dado)
        f.seek(0)
        json.dump(dados, f, indent=2)    
      
# # Função que trata as mensagens recebidas do telegram e enviar ao --- BACK END
async def tratar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    dados = extrair_info(texto)

    # Envia para API
    try:
        response = requests.post(API_URL, json=dados)
        if response.status_code == 201 or response.status_code == 200:
            await update.message.reply_text(f"✅ {dados['tipo'].capitalize()} de R$ {dados['valor']:.2f} registrado na categoria '{dados['categoria']}'!")
        else:
            await update.message.reply_text("❌ Erro ao enviar dados para o servidor.")
    except Exception as e:
        await update.message.reply_text("❌ Erro ao conectar com a API.")
        print(e)

# Inicializa o bot
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Escuta todas as mensagens de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    print("🤖 Bot iniciado...")
    await app.run_polling()

# Rodar o bot
if __name__ == '__main__':
    from telegram.ext import ApplicationBuilder

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    print("🤖 Bot iniciado...")
    app.run_polling()
