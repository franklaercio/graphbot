## Descrição
Este projeto consiste em um bot para a plataforma Telegram que oferece funcionalidades de criação de questionários (quizzes) e enquetes (polls). Ele permite aos usuários interagirem com o bot através de comandos específicos para acessar essas funcionalidades.

![Screenshot from 2024-02-22 01-44-37](https://github.com/franklaercio/graphbot/assets/38151364/a1b51a80-f0c0-48b9-88a0-34bda14d62e1)


## Funcionalidades
O bot possui as seguintes funcionalidades principais:
- **Quiz**: Permite criar e enviar questionários aos usuários, que podem responder às perguntas apresentadas.
- **Enquete**: Possibilita a criação de enquetes para coletar opiniões ou votos dos usuários.
- **Visualização de Prévia**: Oferece uma prévia para as enquetes que serão criadas.

## Requisitos
- Python 3.7 ou superior
- Bibliotecas Python:
  - python-dotenv
  - python-telegram-bot

## Configuração
Antes de executar o bot, é necessário configurar as seguintes variáveis de ambiente:
- `TOKEN`: Token de acesso ao bot do Telegram. Você pode obter este token ao criar um novo bot com o BotFather no Telegram.

Certifique-se de criar um arquivo `.env` no mesmo diretório do script e adicionar as variáveis necessárias.

## Instalação
1. Clone ou faça o download do repositório em seu ambiente local.
2. Instale as dependências do projeto executando o seguinte comando:

```shell
pip install -r requirements.txt
```
## Utilização
Execute o script `main.py` para iniciar o bot. Uma vez em execução, o bot estará pronto para receber e responder a comandos do Telegram.

### Comandos Disponíveis
- `/start`: Inicia o bot e fornece uma breve descrição das funcionalidades disponíveis.
- `/quiz`: Inicia um novo questionário (quiz) para os usuários responderem.
- `/help`: Exibe uma mensagem de ajuda com informações sobre como usar o bot.

## Contribuição
Contribuições são bem-vindas! Se você encontrar problemas, bugs ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request para este repositório.

## Licença
Este projeto é licenciado sob a [MIT License](LICENSE).

---

Este projeto foi desenvolvido por Frank e é mantido pela comunidade acadêmica da UFRN.
