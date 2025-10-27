import numpy as np

experimentos = 100000
p_ganhar = 0.01
n = 50

amostras = np.random.rand(experimentos, n) < p_ganhar
ganhos = np.sum(amostras, axis=1)
probabilidade = np.mean(ganhos == 1)

print("Resultado teórico: 30.5% de chance")
print(f"Resultado obtido após 100,000 experimentos: {probabilidade:.5f}")
