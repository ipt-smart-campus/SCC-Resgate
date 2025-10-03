# Resgate — Espaços Ocupados (Flask + MVC)

Interface leve para visualizar, em tempo quase real, os Espaços ocupados no Smart Campus Core (SCC).

## 1) O que o projeto permite

- Listar os Espaços que estão ocupados “neste momento”, organizados por localização (Instituição → Campus → Bloco → Área → Espaço).
- Atualização automática a cada 30s, sem recarregar a página.
- Endpoint de API interno (`/api/occupied-now`) para consumo cliente.
- Filtro opcional por Bloco (query param `?building=bloco-x`).

## 2) Arquitetura e estrutura (MVC)

- Model — `models/`
	- `room_model.py`: representa um Espaço.
	- `booking_model.py`: representa uma marcação (Booking) e determina se está ativa agora.
- View — `templates/` e `static/`
	- `templates/base.html`: layout base (tema claro).
	- `templates/occupied.html`: lista de Espaços ocupados.
	- `static/refresh.js`: atualização periódica e render do lado do cliente.
- Controller — `controllers/`
	- `occupancy_controller.py`: rotas Web e API; delega a lógica para o Service.
- Service — `services/`
	- `occupancy_service.py`: regra de negócio (obter dados do SCC, transformar e filtrar “ocupados agora”).
	- `curl_client.py`: cliente HTTP (via `curl`) para o SCC.
- Utilitários — `utils/`
	- `timeutils.py`: datas (início da semana, ISO).
- Config — `config.py`: leitura centralizada de variáveis de ambiente.
- App — `app.py`: app factory e registo de blueprints.

```
.
├── app.py
├── config.py
├── controllers/
│   └── occupancy_controller.py
├── models/
│   ├── booking_model.py
│   └── room_model.py
├── services/
│   ├── curl_client.py
│   └── occupancy_service.py
├── utils/
│   └── timeutils.py
├── templates/
│   ├── base.html
│   └── occupied.html
└── static/
		└── refresh.js
```

## 3) Requisitos e dependências

- Python 3.12
- Docker (opcional, recomendado para execução isolada)
- Dependências Python: `Flask==3.0.3`

## 4) Configuração

Variáveis de ambiente:

- `API_BASE` (obrigatório em produção): Base URL do Smart Campus Core. Ex.: `http://scc.sua-infra:5000`
- `API_SPACES_ENDPOINT` (opcional): endpoint dos espaços. Default: `/api/spaces`
- `TZ` (opcional): fuso horário. Default: `Europe/Lisbon`

No `docker-compose.yml` de exemplo:

```
API_BASE: "http://host.docker.internal:5000"
API_ROOMS_ENDPOINT: "/api/spaces"
```

## 5) Como executar

Com Docker:

iniciar projeto pela primeira vez:

```powershell
docker-compose up -d --build
```

inciar projeto após a primeira vez:

```powershell
docker-compose up -d
```

verificar estado containers:

```powershell
docker ps"
```

Aceder: http://localhost:8088

Sem Docker (apenas dev):

```powershell
$env:API_BASE = "http://localhost:5000" ; python app.py
```

## 6) Segurança e boas práticas

- A app consome o SCC apenas no backend (não expõe credenciais no cliente).
- Autoescape nos templates + escape no JS para evitar XSS.
- Em produção, desative `debug=True` e coloque atrás de um proxy com TLS (Nginx/Traefik) e autenticação (OIDC/LDAP/SAML) se necessário.
- Considere rate limiting e caching.

## 7) Manutenção e evolução

Melhorias sugeridas:

- Substituir `curl` por `requests`/`httpx` com timeouts, reintentos e pooling.
- Cache de respostas por curto período (ex.: Redis) para reduzir N+1 chamadas.
- Logging estruturado e métricas (Prometheus) + dashboards.
- Testes unitários (models e services) e CI.
- Live updates (SSE/WebSockets) se o SCC suportar.

## 8) Desenvolvimento

- Padrão MVC aplicado: Controllers só tratam HTTP e delegam ao Service; Views apenas apresentam; Models representam dados.
- Adicione novas rotas criando novos controllers e serviços correspondentes.
- Use `config.py` para qualquer parâmetro de ambiente.

## 9) Troubleshooting

- Se a lista estiver vazia, verifique `API_BASE` e se o SCC responde a `/api/spaces` e `/api/bookings`.
- Use `/api/debug` para inspecionar espaços e configuração ativa.
- Ver logs do container: `docker logs -f resgate-ipt-smartcampuscore`.

