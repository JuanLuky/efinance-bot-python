import re
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = '7808015731:AAEnusaNF7LI6-oAFw86B0mdPVjDit-F5fo'
# API_URL = 'http://localhost:8080/api/lancamentos'  # Temporariamente comentado

ARQUIVO_JSON = 'lancamentos.json'

# Extrai dados da mensagem
def extrair_info(mensagem):
    tipo = 'gasto' if 'gastei' in mensagem.lower() else 'ganho'
    valor_match = re.search(r'(\d+(?:[\.,]\d+)?)', mensagem)
    valor = float(valor_match.group(1).replace(',', '.')) if valor_match else 0.0

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

# Trata mensagens do Telegram
async def tratar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    dados = extrair_info(texto)

    try:
        # Comentado envio à API (você pode descomentar depois)
        # response = requests.post(API_URL, json=dados)
        salvar_localmente(dados)

        await update.message.reply_text(
            f"✅ {dados['tipo'].capitalize()} de R$ {dados['valor']:.2f} registrado na categoria '{dados['categoria']}'!"
        )
    except Exception as e:
        await update.message.reply_text("❌ Erro ao salvar os dados.")
        print(e)

# Inicializa o bot
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))
    print("🤖 Bot iniciado...")
    await app.run_polling()

if __name__ == '__main__':
    from telegram.ext import ApplicationBuilder

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    print("🤖 Bot iniciado...")
    app.run_polling()

