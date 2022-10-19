from enum import Enum
from urllib import response

import unidecode
import nltk
from nltk import tokenize

stemmer = nltk.stem.RSLPStemmer()
responses = []

# global total_value
total_value = 0

class State(Enum):
    START = 1
    PIZZA_FLAVOUR = 3
    PIZZA_SIZE = 4
    HAMBURGER_FLAVOUR = 6
    WANT_SOMETHING = 7
    MANAGER = 8
    END = 9


def AddWords(question, response, required, state):
    requiredToken = GetTokens(required)
    if len(requiredToken) > 0:
        responses.append((GetTokens(question), requiredToken[0], response, state))
    else:
        responses.append((GetTokens(question), "", response, state))


def GetTokens(text):
    result = []

    for word in tokenize.word_tokenize(text, language='portuguese'):
        token = stemmer.stem(word)
        result.append(unidecode.unidecode(token))

    return result


def ResponseMatch(tokens, response, required):

    # print(tokens, response, required)

    total = 0
    hasRequiredToken = (required == "")

    for token in tokens:
        if token == required:
            hasRequiredToken = True

        for resp in response:
            if token == resp:
                total += 1

    if hasRequiredToken:
        return (total / len(tokens)) * 100

    return 0


current_state = None


def change_state(state):

    # print("Mudando estado para:", state)
    current_state = state
    responses = []
    if state == State.START:
        AddWords("pizza", "Temos calabresa, 4 queijos e mineira, escolha:", "", State.PIZZA_FLAVOUR)
        AddWords("hamburguer", "Temos x-salada, x-bacon e x-vegan, escolha:", "", State.HAMBURGER_FLAVOUR)
        AddWords("gerente", "Passando para o gerente, aguarde na linha...", "", State.MANAGER)
    elif state == State.PIZZA_FLAVOUR:
        AddWords("calabresa", "Você quer broto, grande e gigante?", "", State.PIZZA_SIZE)
        AddWords("4 queijos", "Você quer broto, grande e gigante?", "", State.PIZZA_SIZE)
        AddWords("mineira", "Você quer broto, grande e gigante?", "", State.PIZZA_SIZE)
    elif state == State.PIZZA_SIZE:
        AddWords("broto", "Ok, entendi. Quer mais alguma coisa?", "", State.WANT_SOMETHING)
        AddWords("grande", "Ok, entendi. Quer mais alguma coisa?", "", State.WANT_SOMETHING)
        AddWords("gigante", "Ok, entendi. Quer mais alguma coisa?", "", State.WANT_SOMETHING)
    elif state == State.HAMBURGER_FLAVOUR:
        AddWords("x-bacon", "Ok, entendi. Quer mais alguma coisa?", "", State.WANT_SOMETHING)
        AddWords("x-salada", "Ok, entendi. Quer mais alguma coisa?", "", State.WANT_SOMETHING)
        AddWords("x-vegan", "Ok, entendi. Quer mais alguma coisa?", "", State.WANT_SOMETHING)
    elif state == State.WANT_SOMETHING:
        AddWords("sim", "Ok, o que mais você deseja? Temos pizza e hamburguer.", "", State.START)
        AddWords("não", "Sua conta deu: R$" + str(total_value), "", State.END)

    AddWords("cancelar", "Tudo bem, começando de novo.\nO que você deseja? Temos pizza e hamburguer. Caso queira, também pode falar com o gerente.", "", State.START)

    return state


current_state = change_state(State.START)


def FindBestResponse(text):
    tokens = GetTokens(text)

    currResp = "Desculpe, eu não entendi o que você escreveu! :("
    bestHit = 0.1

    state = None

    print(tokens)

    for response in responses:
        currHit = ResponseMatch(tokens, response[0], response[1])

        # print(tokens, response[0], response[1], currHit)

        if currHit > bestHit:
            bestHit = currHit
            currResp = response[2]
            state = response[3]

    if state is not None:
        # print(current_state, state, tokens, tokens[0])
        #
        # if current_state == State.WANT_SOMETHING:
        #     if tokens[0] == 'brot':
        #         total_value += 30
        #     elif tokens[0] == 'grand':
        #         total_value += 60
        #     elif tokens[0] == 'gigant':
        #         total_value += 90
        # # elif current_state == State.HAMBURGER_FLAVOUR:
        #     elif tokens[0] == 'x-sal':
        #         total_value += 25
        #     elif tokens[0] == 'x-bacon':
        #         total_value += 30
        #     elif tokens[0] == 'x-vegan':
        #         total_value += 45

        change_state(state)

    return currResp


# AddWords("Olá", "Olá, em que posso ajudar?", "")
# AddWords("Oi", "Olá, em que posso ajudar?", "")
# AddWords("Qual o seu nome?", "Meu nome é ChatBot!", "Qual")
# AddWords("Quem é você?", "Eu sou um ChatBot!", "Quem")
# AddWords("Quantos anos você tem?", "Eu tenho alguns dias de vida!", "Quantos")
# AddWords("Como assim?", "Sei lá, eu sou um robô!", "Como")
# AddWords("Quando você nasceu?", "Acho que algum dia em 2022", "Quando")
# AddWords("Quem é o seu criador?", "Um programador!", "Quem")
# AddWords("Qual o nome do seu criador?", "Alisson Linhares", "Qual")
# AddWords("Vai tomar no cu", "Vai você!", "vai")
# AddWords("Vai tomar no rabo", "Vai você!", "vai")
# AddWords("Você é um corno", "Seu pai!", "")

print('Olá! Bem-vindo(a) a Pizza Planet! O que voce deseja hoje? Pizza, Hamburguer ou falar com o gerente?')

while True:
    text = input('You: ')
    print("Bot: " + FindBestResponse(text))

