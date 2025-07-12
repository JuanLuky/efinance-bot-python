import re
import requests
import os
from telegram import Update
from dotenv import load_dotenv # Carrega as variáveis de ambiente do arquivo .env
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes


load_dotenv() # Carrega as variáveis de ambiente do arquivo .env

# Obtém as variáveis de ambiente
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Substitua a linha hardcoded
API_URL = os.getenv('API_URL')                # Substitua a linha hardcoded


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

# Rodar o bot
# Inicializa e executa o bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    print("🤖 Bot iniciado...")
    app.run_polling()
