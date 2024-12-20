## Commande pour build

```
docker build -t chat .
```

## Up docker-compose.yml

```
docker compose up 
```

## Pour modifier le port d'écoute

```
docker run -e CHAT_PORT=6767 -d chat
```