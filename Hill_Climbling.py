import copy
import random

def gerar_vizinhos_knapsack(solucao, n_vizinhos=10):
    vizinhos = []
    n_itens = len(solucao)
    sorted_pos = []
    while len(vizinhos) < n_vizinhos and len(sorted_pos) < n_itens:
        pos = random.randint(0, n_itens - 1)
        if pos in sorted_pos:
            continue
        vizinho = solucao.copy()
        vizinho[pos] = 1 - vizinho[pos]
        vizinhos.append(vizinho)
        sorted_pos.append(pos)
    return vizinhos

class HillClimbing:
    def __init__(self, funcao_fitness, gerar_vizinhos, maximizar=True):
        self.funcao_fitness = funcao_fitness
        self.gerar_vizinhos = gerar_vizinhos
        self.maximizar = maximizar
        self.historico = []

    def executar(self, solucao_inicial, max_iteracoes=1000, verbose=False):
        solucao_atual = copy.deepcopy(solucao_inicial)
        fitness_atual = self.funcao_fitness(solucao_atual)
        self.historico = [fitness_atual]
        iteracao = 0
        while iteracao < max_iteracoes:
            iteracao += 1
            vizinhos = self.gerar_vizinhos(solucao_atual)
            melhor_vizinho = None
            melhor_fitness_vizinho = fitness_atual
            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)
                eh_melhor = (
                    fitness_vizinho > melhor_fitness_vizinho
                    if self.maximizar
                    else fitness_vizinho < melhor_fitness_vizinho
                )
                if eh_melhor:
                    melhor_vizinho = vizinho
                    melhor_fitness_vizinho = fitness_vizinho
            if melhor_vizinho is not None:
                solucao_atual = copy.deepcopy(melhor_vizinho)
                fitness_atual = melhor_fitness_vizinho
            else:
                break
            self.historico.append(fitness_atual)
        return solucao_atual, fitness_atual, self.historico


if __name__ == "__main__":
    import sys
    from knapsack import knapsack
    import random

    # Configuração do problema
    DIM = 20
    MAX_ITERACOES = 200

    # 1. Crie uma lista para guardar os resultados
    resultados_finais = []

    # Instancia o algoritmo uma vez, fora do loop
    hill_climbing = HillClimbing(
        funcao_fitness=lambda sol: knapsack(sol, dim=DIM)[0],
        gerar_vizinhos=gerar_vizinhos_knapsack,
        maximizar=True,
    )

    # 2. Crie um loop para rodar 30 vezes
    for i in range(30):
        # Gera uma nova solução inicial aleatória a cada rodada
        solucao_inicial = [int(random.random() > 0.8) for _ in range(DIM)]

        # Executa o algoritmo
        _, melhor_fitness, _ = hill_climbing.executar(
            solucao_inicial, max_iteracoes=MAX_ITERACOES, verbose=False # verbose=False para não poluir a tela
        )

        # 3. Adiciona o resultado final à lista
        resultados_finais.append(melhor_fitness)
        
        # Imprime o resultado da rodada atual
        print(f"Rodada {i + 1}: Fitness encontrado = {melhor_fitness}")


    # 4. No final, imprime a lista com todos os resultados
    print("\n======================================")
    print("Resultados finais das 30 rodadas:")
    print(resultados_finais)
    print("======================================")
