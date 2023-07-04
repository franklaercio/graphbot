import logging
import quiz_question
import random
import os

from dotenv import load_dotenv

load_dotenv()

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    await update.message.reply_text(
        "Please select /poll to get a Poll, /quiz to get a Quiz or /preview"
        " to generate a preview for your poll"
    )


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = random.choice(get_questions())

    message = await update.effective_message.reply_poll(
        question.title, question.options, type=Poll.QUIZ, correct_option_id=question.answer, open_period=30, is_anonymous=False
    )
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {
        message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
    }
    context.bot_data.update(payload)


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Thank you for your vote!")

def get_questions():
    return [
            quiz_question.QuizQuestion(title="Grafo", options=["Um conjunto de elementos conectados por linhas", "Uma representação visual de dados numéricos", "Uma técnica de ordenação de dados alfanuméricos", "Um tipo de linguagem de programação"], answer=0),
            quiz_question.QuizQuestion(title="Grafo direcionado", options=["Um grafo onde todas as arestas têm o mesmo peso", "Um grafo em que todas as arestas possuem um sentido definido", "Um grafo com um número mínimo de arestas", "Um grafo que não possui ciclos"], answer=1),
            quiz_question.QuizQuestion(title="Multigrafo", options=["Um grafo que possui um número mínimo de arestas", "Um grafo onde todas as arestas têm o mesmo peso", "Um grafo com múltiplas arestas entre os mesmos pares de vértices", "Um grafo que não possui ciclos"], answer=2),
            quiz_question.QuizQuestion(title="Hipergrafo", options=["Um grafo com múltiplas arestas entre os mesmos pares de vértices", "Um grafo que não possui ciclos", "Um grafo que possui um número mínimo de arestas", "Um grafo onde todas as arestas têm o mesmo peso"], answer=2),
            quiz_question.QuizQuestion(title="Pseudografo", options=["Um grafo que não possui ciclos", "Um grafo onde todas as arestas têm o mesmo peso", "Um grafo com múltiplas arestas entre os mesmos pares de vértices", "Um grafo que permite loops (arestas que conectam um vértice a si mesmo)"], answer=3),
            quiz_question.QuizQuestion(title="Ordem e tamanho de um grafo", options=["O número de vértices e o número de arestas de um grafo", "O número mínimo de arestas que um grafo deve ter", "Um tipo especial de vértice", "Um tipo especial de aresta"], answer=0),
            quiz_question.QuizQuestion(title="Adjacência de vértices e arestas", options=["A relação de conexão entre vértices vizinhos e a relação de conexão entre arestas vizinhas de um grafo", "A matriz que representa as relações de conexão entre os vértices de um grafo", "Uma técnica de ordenação de dados numéricos", "Um tipo de linguagem de programação"], answer=0),
            quiz_question.QuizQuestion(title="Grau", options=["O número de vértices e o número de arestas de um grafo", "A medida de centralidade de um vértice em um grafo", "O número de arestas que incidem em um vértice", "A ordem do grafo"], answer=3),
            quiz_question.QuizQuestion(title="Sucessores e antecessores", options=["O número de vértices e o número de arestas de um grafo", "Os vértices adjacentes a um vértice específico", "Os vértices que possuem uma aresta que sai de um vértice específico", "Os vértices que possuem uma aresta que entra em um vértice específico"], answer=2),
            quiz_question.QuizQuestion(title="Sequência de graus", options=["A relação de conexão entre vértices vizinhos e a relação de conexão entre arestas vizinhas de um grafo", "A matriz que representa as relações de conexão entre os vértices de um grafo", "O conjunto de graus dos vértices de um grafo", "A técnica para calcular a distância entre vértices de um grafo"], answer=2),
            quiz_question.QuizQuestion(title="Matriz de adjacência", options=["Uma matriz que representa as relações de conexão entre os vértices de um grafo", "Uma matriz utilizada para ordenar os vértices de um grafo", "Uma matriz que armazena os pesos das arestas de um grafo ponderado", "Uma técnica para calcular a distância entre vértices de um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Lista de adjacência", options=["Uma estrutura de dados que representa as conexões entre os vértices de um grafo", "Uma técnica de ordenação de vértices em um grafo", "Uma matriz que representa as relações de conexão entre os vértices de um grafo", "Uma técnica para calcular a distância entre vértices de um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Fecho transitivo", options=["Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "A sequência de vértices visitados em um percurso em um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez", "Um conjunto de arestas que conectam todos os vértices de um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Passeio", options=["Uma sequência de vértices visitados em um percurso em um grafo", "Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez", "Um conjunto de arestas que conectam todos os vértices de um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Cadeia", options=["Um conjunto de arestas que conectam todos os vértices de um grafo", "Uma sequência de vértices visitados em um percurso em um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez", "Um conjunto de vértices que podem ser alcançados a partir de um vértice específico"], answer=1),
            quiz_question.QuizQuestion(title="Caminho", options=["Uma sequência de vértices visitados em um percurso em um grafo", "Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Um conjunto de arestas que conectam todos os vértices de um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez"], answer=0),
            quiz_question.QuizQuestion(title="Ciclo", options=["Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Uma sequência de vértices visitados em um percurso em um grafo", "Um conjunto de arestas que conectam todos os vértices de um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez"], answer=3),
            quiz_question.QuizQuestion(title="Cadeia Euleriana", options=["Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Uma sequência de vértices visitados em um percurso em um grafo", "Um conjunto de arestas que conectam todos os vértices de um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez"], answer=1),
            quiz_question.QuizQuestion(title="Caminho Hamiltoniano", options=["Uma sequência de vértices visitados em um percurso em um grafo", "Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Um conjunto de arestas que conectam todos os vértices de um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez"], answer=0),
            quiz_question.QuizQuestion(title="Ciclo Hamiltoniano", options=["Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Uma sequência de vértices visitados em um percurso em um grafo", "Um conjunto de arestas que conectam todos os vértices de um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez"], answer=3),
            quiz_question.QuizQuestion(title="Grafo Euleriano", options=["Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Uma sequência de vértices visitados em um percurso em um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez", "Um conjunto de arestas que conectam todos os vértices de um grafo"], answer=2),
            quiz_question.QuizQuestion(title="Grafo Hamiltoniano", options=["Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Uma sequência de vértices visitados em um percurso em um grafo", "Um conjunto de arestas que conectam todos os vértices de um grafo", "Um ciclo que visita todos os vértices de um grafo exatamente uma vez"], answer=1),
            quiz_question.QuizQuestion(title="Problema do caixeiro viajante", options=["Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Uma técnica para calcular a distância entre vértices de um grafo", "Uma técnica de ordenação de vértices em um grafo", "Um problema de encontrar o menor caminho que visita todos os vértices de um grafo exatamente uma vez"], answer=3),
            quiz_question.QuizQuestion(title="Distância", options=["Uma técnica de ordenação de vértices em um grafo", "Um conjunto de vértices que podem ser alcançados a partir de um vértice específico", "Uma técnica para calcular a distância entre vértices de um grafo", "Um problema de encontrar o menor caminho que visita todos os vértices de um grafo exatamente uma vez"], answer=2),
            quiz_question.QuizQuestion(title="Cintura", options=["O menor número de arestas em um ciclo de um grafo", "A maior distância entre dois vértices de um grafo", "O número de arestas de um grafo", "A maior sequência de vértices visitados em um percurso em um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Circunferência", options=["A maior distância entre dois vértices de um grafo", "O menor número de arestas em um ciclo de um grafo", "O número de arestas de um grafo", "A maior sequência de vértices visitados em um percurso em um grafo"], answer=1),
            quiz_question.QuizQuestion(title="Excentricidade", options=["A maior distância entre dois vértices de um grafo", "O menor número de arestas em um ciclo de um grafo", "O número de arestas de um grafo", "A maior sequência de vértices visitados em um percurso em um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Raio", options=["O menor número de arestas em um ciclo de um grafo", "A maior distância entre dois vértices de um grafo", "O número de arestas de um grafo", "A maior sequência de vértices visitados em um percurso em um grafo"], answer=1),
            quiz_question.QuizQuestion(title="Diâmetro", options=["O menor número de arestas em um ciclo de um grafo", "A maior distância entre dois vértices de um grafo", "O número de arestas de um grafo", "A maior sequência de vértices visitados em um percurso em um grafo"], answer=1),
            quiz_question.QuizQuestion(title="Centro", options=["A maior distância entre dois vértices de um grafo", "O menor número de arestas em um ciclo de um grafo", "O vértice com a menor excentricidade em um grafo", "O número de arestas de um grafo"], answer=2),
            quiz_question.QuizQuestion(title="Índice de Wiener", options=["Uma medida de conectividade de um grafo", "O menor número de arestas em um ciclo de um grafo", "A maior distância entre dois vértices de um grafo", "O número de arestas de um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Corda", options=["Uma aresta que liga dois vértices não adjacentes em um ciclo de um grafo", "A maior distância entre dois vértices de um grafo", "O menor número de arestas em um ciclo de um grafo", "O número de arestas de um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Grafo Par", options=["Um grafo com um número par de vértices", "Um grafo com um número par de arestas", "Um grafo que possui um ciclo", "Um grafo que não possui ciclo"], answer=1),
            quiz_question.QuizQuestion(title="Grafo conexo", options=["Um grafo que possui um ciclo", "Um grafo com apenas um componente conexo", "Um grafo sem arestas", "Um grafo com apenas um vértice"], answer=1),
            quiz_question.QuizQuestion(title="k-conexidade", options=["Uma medida de conectividade de um grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um grafo com k vértices"], answer=0),
            quiz_question.QuizQuestion(title="Componente conexa", options=["Uma aresta que liga dois vértices não adjacentes em um ciclo de um grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um grafo com k vértices"], answer=1),
            quiz_question.QuizQuestion(title="Articulação", options=["Um vértice cuja remoção aumenta o número de componentes conexas de um grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um vértice que possui o maior grau no grafo"], answer=0),
            quiz_question.QuizQuestion(title="Ponte", options=["Uma aresta cuja remoção aumenta o número de componentes conexas de um grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Uma aresta que possui o maior peso no grafo"], answer=0),
            quiz_question.QuizQuestion(title="Conjunto de desconexão", options=["Um conjunto de vértices que, se removidos, tornam o grafo desconexo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um conjunto de vértices que possuem o maior grau no grafo"], answer=0),
            quiz_question.QuizQuestion(title="Corte em vértices", options=["Um conjunto de vértices que, se removidos, aumentam o número de componentes conexas do grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um conjunto de vértices que possuem o maior grau no grafo"], answer=0),
            quiz_question.QuizQuestion(title="Corte em arestas", options=["Um conjunto de arestas que, se removidas, aumentam o número de componentes conexas do grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um conjunto de vértices que possuem o maior grau no grafo"], answer=0),
            quiz_question.QuizQuestion(title="Matriz de cortes", options=["Uma matriz que representa as relações de conexão entre os vértices de um grafo", "Uma matriz que contém as distâncias entre todos os pares de vértices de um grafo", "Uma matriz que representa os cortes entre os vértices de um grafo", "Uma matriz que representa os pesos das arestas de um grafo"], answer=2),
            quiz_question.QuizQuestion(title="Subgrafo", options=["Um grafo que contém um conjunto de vértices e arestas do grafo original", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um conjunto de vértices que possuem o maior grau no grafo"], answer=0),
            quiz_question.QuizQuestion(title="Tipos de subgrafos", options=["Subgrafo induzido, subgrafo gerador, subgrafo máximo", "Grafo conexo, grafo bipartido, grafo completo", "Bloco, rank, nulidade", "Árvore, grafo planar, grafo torneio"], answer=0),
            quiz_question.QuizQuestion(title="Árvore", options=["Um grafo sem ciclos e conexo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Árvore geradora", options=["Uma árvore que contém todos os vértices de um grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um grafo sem ciclos e conexo"], answer=0),
            quiz_question.QuizQuestion(title="Outros tipos de árvores", options=["Árvore binária, árvore AVL, árvore B", "Subgrafo induzido, subgrafo gerador, subgrafo máximo", "Caminho Hamiltoniano, ciclo Hamiltoniano, grafo Hamiltoniano", "Grafo conexo, grafo bipartido, grafo completo"], answer=0),
            quiz_question.QuizQuestion(title="Bloco", options=["Um grafo sem ciclos e conexo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "Um subgrafo de um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Rank", options=["O número de linhas ou colunas independentes em uma matriz de um grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "O número de vértices em um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Nulidade", options=["O número de linhas ou colunas independentes em uma matriz de um grafo", "Um grafo com apenas um componente conexo", "Um grafo com apenas um vértice", "O número de vértices em um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Número ciclomático", options=["Uma medida da complexidade topológica de um grafo planar", "O número de linhas ou colunas independentes em uma matriz de um grafo", "O número de vértices em um grafo", "O número de componentes conexas em um grafo"], answer=0),
            quiz_question.QuizQuestion(title="Grafo Bipartido", options=["Um grafo cujos vértices podem ser divididos em dois conjuntos, onde não há arestas entre vértices do mesmo conjunto", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Grafo completo", options=["Um grafo onde cada vértice está conectado a todos os outros vértices por uma aresta", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Clique", options=["Um subconjunto de vértices em um grafo onde todos os vértices são adjacentes entre si", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Grafo Torneio", options=["Um grafo direcionado onde existe uma aresta entre cada par de vértices", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Grafo Regular", options=["Um grafo onde todos os vértices têm o mesmo grau", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Grafo Planar", options=["Um grafo que pode ser desenhado em um plano sem que as arestas se cruzem", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Número de cruzamento de arestas", options=["O número de arestas em um grafo planar", "O número de vezes que as arestas de um grafo se cruzam", "O número de vértices em um grafo", "O número de componentes conexas em um grafo"], answer=1),
            quiz_question.QuizQuestion(title="Grafo complemento e grafo complementar", options=["Dois termos que se referem ao mesmo conceito, a inversão das arestas de um grafo", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Isomorfismo de grafos", options=["Uma correspondência biunívoca entre vértices de dois grafos preservando a estrutura e as relações entre os vértices", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Grafo de linha", options=["Um grafo que representa as relações entre linhas de um plano", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Número cromático", options=["O menor número de cores necessárias para colorir os vértices de um grafo de forma que vértices adjacentes tenham cores diferentes", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Número de estabilidade", options=["O tamanho do maior conjunto independente em um grafo", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Conjuntos independentes", options=["Subconjuntos de vértices em um grafo onde não há arestas entre vértices do mesmo conjunto", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Cobertura de vértices", options=["Um conjunto de vértices que contém pelo menos um vértice de cada aresta em um grafo", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Cobertura de arestas", options=["Um conjunto de arestas que contém pelo menos um vértice de cada aresta em um grafo", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0),
            quiz_question.QuizQuestion(title="Conjunto dominante", options=["Um conjunto de vértices que, se dominantes, podem alcançar todos os outros vértices do grafo por meio de arestas", "Um grafo sem ciclos e conexo", "Um grafo com apenas um vértice", "Um grafo com apenas uma aresta"], answer=0)
        ]

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a help message"""
    await update.message.reply_text("Use /quiz, /poll or /preview to test this bot.")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(PollHandler(receive_quiz_answer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()