import copy
import random
from knapsack import knapsack

def gerar_vizinhos_knapsack(solucao, n_vizinhos=10):
    """
    Gera vizinhos para o problema knapsack
    Estratégia: flip de um bit aleatório
    """
    vizinhos = []
    n_itens = len(solucao)
    posicoes_sorteadas = []
    
    while len(vizinhos) < n_vizinhos and len(posicoes_sorteadas) < n_itens:
        pos = random.randint(0, n_itens - 1)
        if pos in posicoes_sorteadas:
            continue
        
        vizinho = solucao.copy()
        vizinho[pos] = 1 - vizinho[pos]
        vizinhos.append(vizinho)
        posicoes_sorteadas.append(pos)
        
    return vizinhos

class StochasticHillClimbing:
    def __init__(self, funcao_fitness, gerar_vizinhos, maximizar=True):
        """
        Inicializa o algoritmo Stochastic Hill Climbing
        """
        self.funcao_fitness = funcao_fitness
        self.gerar_vizinhos = gerar_vizinhos
        self.maximizar = maximizar
        self.historico = []

    def executar(self, solucao_inicial, max_iteracoes=1000, verbose=False):
        """
        Executa o algoritmo Stochastic Hill Climbing
        """
        solucao_atual = copy.deepcopy(solucao_inicial)
        fitness_atual = self.funcao_fitness(solucao_atual)
        self.historico = [fitness_atual]
        iteracao = 0

        while iteracao < max_iteracoes:
            iteracao += 1
            vizinhos = self.gerar_vizinhos(solucao_atual)
            vizinhos_melhores = []
            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)
                eh_melhor = (
                    fitness_vizinho > fitness_atual
                    if self.maximizar
                    else fitness_vizinho < fitness_atual
                )
                if eh_melhor:
                    vizinhos_melhores.append(vizinho)

            if not vizinhos_melhores:
                if verbose:
                    print(f"Convergiu na iteração {iteracao}")
                break
            
            proxima_solucao = random.choice(vizinhos_melhores)
            solucao_atual = copy.deepcopy(proxima_solucao)
            fitness_atual = self.funcao_fitness(solucao_atual)
            self.historico.append(fitness_atual)
            
        return solucao_atual, fitness_atual, self.historico


if __name__ == "__main__":

    # Configuração do problema
    DIM = 20
    MAX_ITERACOES = 200
    NUM_EXECUCOES = 30 # <<< Definindo o número de rodadas

    # 1. Crie uma lista para guardar os resultados
    resultados_finais_stochastic = []

    # Instancia o algoritmo uma vez, fora do loop
    stochastic_hc = StochasticHillClimbing(
        funcao_fitness=lambda sol: knapsack(sol, dim=DIM)[0],
        gerar_vizinhos=gerar_vizinhos_knapsack,
        maximizar=True,
    )

    print(f"--- EXECUTANDO STOCHASTIC HILL CLIMBING {NUM_EXECUCOES} VEZES ---")

    # 2. Crie um loop para rodar 30 vezes
    for i in range(NUM_EXECUCOES):
        # Gera uma nova solução inicial aleatória a cada rodada
        solucao_inicial = [random.randint(0, 1) for _ in range(DIM)]

        # Executa o algoritmo (com verbose=False para uma saída mais limpa)
        _, melhor_fitness, _ = stochastic_hc.executar(
            solucao_inicial, max_iteracoes=MAX_ITERACOES, verbose=False
        )

        # 3. Adiciona o resultado final à lista
        resultados_finais_stochastic.append(melhor_fitness)
        
        # Imprime o resultado da rodada atual
        print(f"Rodada {i + 1}: Fitness encontrado = {melhor_fitness}")


    # 4. No final, imprime a lista com todos os resultados
    print("\n=======================================================")
    print("Resultados finais das 30 rodadas (Stochastic):")
    print(resultados_finais_stochastic)
    print("=======================================================")