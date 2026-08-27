# PromoBot — WhatsApp + Afiliados

Bot inicial para receber mensagens pelo WhatsApp e responder com ofertas.

## Instalação
1. Instale Python 3.11 ou superior.
2. Abra o terminal nesta pasta.
3. Execute: `pip install -r requirements.txt`
4. Copie `.env.example` para `.env`.
5. Preencha suas credenciais da API oficial do WhatsApp.
6. Execute: `python bot.py`

## Webhook
O endereço será `/webhook`. Para uso real, o servidor precisa estar publicado em HTTPS.

## Afiliados
No arquivo `bot.py`, troque os produtos de exemplo pelos seus links de afiliado ou conecte uma fonte de ofertas/API.

## Atenção
Não use automação não-oficial do WhatsApp nem faça spam/disparos para contatos sem consentimento. A versão de produção deve usar a API oficial e respeitar as regras do WhatsApp, Shopee e Mercado Livre.
