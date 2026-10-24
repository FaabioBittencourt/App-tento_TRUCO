# 🃏 Marcador de Tento para Truco

Um aplicativo moderno e intuitivo de **Marcador de Tento para jogos de Truco**; 
Desenvolvido em Python utilizando o framework **KivyMD** para uma interface limpa seguindo o Material Design;
Banco de dados **SQLite3** para persistência e histórico de partidas.

---

## ✨ Funcionalidades

- **Marcador de Pontos:** Incremento e decremento simples de tentos (pontos).
- **Modo Truco:** Botões rápidos para aumentar a pontuação da rodada.
- **Histórico de Partidas:** Registro automático das partidas jogadas guardado localmente.
- **Personalização:** Definição dos nomes dos times/jogadores antes de iniciar, gravação de voz com interação ao decorrer da partida.
- **Interface Responsiva:** Design que se adapta tanto a telas de smartphones quanto desktop.

## 🚀 Tecnologias Utilizadas

- [Python 3](https://python.org) - Linguagem base do projeto.
- [Kivy](https://kivy.org) & [KivyMD](https://readthedocs.io) - Framework para interface gráfica Material Design.
- [SQLite3](https://python.org) - Banco de dados local e nativo para o histórico.

### Pré-requisitos
Certifique-se de ter o Python instalado. É altamente recomendável utilizar um ambiente virtual (venv).

## 🗄️ Estrutura do Banco de Dados

O banco de dados SQLite é gerado automaticamente no primeiro início do app (`truco.db`). Ele armazena:
- **Tabela `partidas`:** ID, Nome do Time A, Nome do Time B, Pontuação Final A, Pontuação Final B e Data/Hora.
- **Partidas com porcentagem de vitórias dos jogadores ou duplas.
- **Sistema pensado em sorteio sem repetição de duplas.

- OBS: Frontend não foi meu foco no projeto!
