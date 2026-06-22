# API do Modelo — usando o modelo dentro do n8n

Transforma o modelo combinado (texto + tabela) num **serviço HTTP**. Assim, o n8n
(ou qualquer sistema) consegue chamar o modelo para classificar avaliações novas.

É o padrão de produção real: **o modelo vira uma API, e o pipeline a consome.**

---

## A ideia

```
n8n coleta uma avaliação nova   →   chama POST /prever   →   modelo responde 👍/👎
                                                                   ↓
                                                        n8n salva / alerta se 👎
```

Tudo da aula num pipeline só: o modelo treinado na Parte 1 vira o serviço que o
pipeline da Parte 2 (n8n) consome.

---

## Rodar localmente

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Na primeira vez, ele baixa o Olist e treina o modelo (alguns segundos).
Depois acesse **http://localhost:8000/docs** para testar pelo navegador.

---

## Testar com curl

```bash
curl -X POST http://localhost:8000/prever \
  -H "Content-Type: application/json" \
  -d '{"texto": "produto excelente, chegou antes do prazo"}'
```

Resposta:
```json
{ "satisfeito": true, "probabilidade": 0.97, "usou_texto": true }
```

E um pedido **sem texto**, mas com entrega atrasada (o modelo usa a tabela):
```bash
curl -X POST http://localhost:8000/prever \
  -H "Content-Type: application/json" \
  -d '{"texto": "", "dias_entrega": 40, "dias_estimado": 15, "atrasou": 1}'
```

---

## Configurar no n8n (HTTP Request node)

| Campo | Valor |
|-------|-------|
| Method | `POST` |
| URL | `http://localhost:8000/prever` (ou a URL pública, se hospedado) |
| Body Content Type | `JSON` |
| Body | `{ "texto": "{{ $json.comentario }}" }` |

O resultado (`satisfeito`, `probabilidade`) volta para o workflow e pode ser usado
no próximo nó — por exemplo, um nó "IF" que envia alerta quando `satisfeito = false`.

---

## Importante sobre hospedagem

Para o **n8n.cloud** chamar a API, ela precisa de uma **URL pública**:

| Cenário | Funciona? |
|---------|-----------|
| API no seu laptop (`localhost`) + n8n.cloud | ❌ a nuvem não enxerga seu localhost |
| API no laptop + n8n **self-host** (mesma máquina) | ✅ |
| API hospedada (HuggingFace Spaces / Render) + n8n.cloud | ✅ caminho completo |

Para uma demo em sala, rodar local + n8n self-host é o mais simples.
Para produção, hospede a API num serviço gratuito.
