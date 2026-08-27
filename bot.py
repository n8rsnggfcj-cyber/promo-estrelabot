import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

TOKEN = os.getenv("WHATSAPP_TOKEN", "")
PHONE_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")
GRAPH_VERSION = os.getenv("GRAPH_API_VERSION", "v23.0")

# TROQUE pelos seus produtos/links de afiliado.
OFFERS = [
    {"name": "Celular em promoção", "price": "R$ 999,90", "discount": "20% OFF", "category": "celular", "url": "SEU_LINK_SHOPEE_OU_ML"},
    {"name": "Fone Bluetooth", "price": "R$ 69,90", "discount": "40% OFF", "category": "fone", "url": "SEU_LINK_SHOPEE_OU_ML"},
    {"name": "Oferta para PC", "price": "R$ 199,90", "discount": "30% OFF", "category": "pc", "url": "SEU_LINK_SHOPEE_OU_ML"},
]

def choose_offers(text):
    t = text.lower()
    cats = []
    if any(w in t for w in ["celular", "smartphone", "telefone"]): cats.append("celular")
    if any(w in t for w in ["fone", "headset", "bluetooth"]): cats.append("fone")
    if any(w in t for w in ["pc", "computador", "placa de vídeo", "gpu"]): cats.append("pc")
    if cats:
        return [x for x in OFFERS if x["category"] in cats]
    return OFFERS

def send_message(to, text):
    if not TOKEN or not PHONE_ID:
        print(f"[TESTE] Para {to}:\n{text}")
        return
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    response.raise_for_status()

def build_reply(text):
    t = text.strip().lower()
    if t in {"oi", "olá", "ola", "menu", "promoções", "promocoes"}:
        return (
            "🔥 *PROMOBOT*\n\n"
            "Eu encontro promoções para você!\n\n"
            "Experimente:\n"
            "📱 celular\n"
            "🎧 fone Bluetooth\n"
            "🖥️ ofertas de PC"
        )

    offers = choose_offers(t)
    if not offers:
        return "Não encontrei uma oferta dessa categoria ainda. Tente celular, fone ou PC."

    lines = ["🔥 *OFERTAS ENCONTRADAS* 🔥", ""]
    for i, item in enumerate(offers, 1):
        lines += [
            f"*{i}. {item['name']}*",
            f"💰 {item['price']}  |  🏷️ {item['discount']}",
            f"🛒 {item['url']}",
            ""
        ]
    return "\n".join(lines)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/webhook")
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Token inválido", 403

@app.post("/webhook")
def webhook():
    data = request.get_json(silent=True) or {}
    try:
        value = data["entry"][0]["changes"][0]["value"]
        messages = value.get("messages", [])
        if not messages:
            return "OK", 200

        msg = messages[0]
        sender = msg["from"]
        text = msg.get("text", {}).get("body", "")
        if text:
            send_message(sender, build_reply(text))
    except (KeyError, IndexError, TypeError, requests.RequestException) as exc:
        print("Erro:", exc)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
