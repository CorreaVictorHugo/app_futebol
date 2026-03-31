# ⚽ App Futebol — Análise de Desempenho em Partidas Amadoras

## 📌 Sobre o projeto

Aplicação web desenvolvida em Python com Flask para registro e análise de desempenho de jogadores em partidas de futebol amador.

O sistema permite cadastrar jogadores, criar partidas, registrar participações e armazenar métricas individuais como gols, assistências e notas, possibilitando a geração de indicadores e rankings.

---

## 🎯 Objetivo

O objetivo do projeto é simular um cenário real de coleta e análise de dados, estruturando informações de eventos (partidas) para posterior análise e geração de insights.

---

## 🚀 Funcionalidades

- Cadastro de jogadores
- Criação de partidas
- Vinculação de jogadores às partidas
- Registro de desempenho individual:
  - gols
  - assistências
  - nota
- Visualização de times por partida
- Geração de ranking de jogadores com base em métricas

---

## 🧠 Valor para a área de dados

Este projeto demonstra:

- Modelagem relacional de dados
- Registro estruturado de eventos
- Consolidação de métricas
- Uso de consultas agregadas (SQLAlchemy)
- Geração de indicadores analíticos

---

## 🛠️ Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML + CSS
- Jinja2

---

## 📊 Estrutura de dados

O sistema é baseado em três entidades principais:

- Jogador
- Partida
- ParticipacaoPartida

A tabela `ParticipacaoPartida` é responsável por armazenar os dados de desempenho dos jogadores em cada partida.

---

## ▶️ Como executar o projeto

1. Clone o repositório

2. Crie e ative o ambiente virtual:
python -m venv venv
venv\Scripts\activate

3. Instale as dependências:
pip install -r requirements.txt

4. Execute o projeto:
python app.py

5. Acesse no navegador:
http://127.0.0.1:5000/