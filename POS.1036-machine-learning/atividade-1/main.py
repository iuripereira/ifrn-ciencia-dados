"""Detecção de câncer de mama com centróides médios.

Conjunto: Breast Cancer Wisconsin (Original), UCI.
Origem: Dr. William H. Wolberg (University of Wisconsin Hospitals, Madison),
amostras coletadas por punção aspirativa por agulha fina entre 1989 e 1991.
Cada característica citológica recebe nota de 1 (normal) a 10 (mais anormal).
Classe: 2 = benigno, 4 = maligno. 16 instâncias têm '?' em bare_nuclei.

Fluxo: carregar -> limpar -> treino/teste -> centróides médios -> avaliar -> comparar.

Aluno: Iuri Guerra de Freitas Pereira
Matrícula: 20262011280032
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.tree import DecisionTreeClassifier

# ---------------------------------------------------------------------------
# 1. Carregar
# O arquivo não tem cabeçalho;
# ---------------------------------------------------------------------------
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data"
LOCAL = Path("breast-cancer-wisconsin.data")
COLUNAS = [
    "id", "clump_thickness", "uniformity_cell_size", "uniformity_cell_shape",
    "marginal_adhesion", "single_epithelial_cell_size", "bare_nuclei",
    "bland_chromatin", "normal_nucleoli", "mitoses", "class",
]
CLASSES = [2, 4]
NOMES = {2: "benigno (2)", 4: "maligno (4)"}

df = pd.read_csv(LOCAL if LOCAL.exists() else URL, header=None, names=COLUNAS, na_values="?")
print(f"Instâncias carregadas: {len(df)}")

# ---------------------------------------------------------------------------
# 2. Limpar
# 'id' não descreve o tumor, só adiciona ruído. Instância com valor ausente
# não pode ser comparada por distância; a tarefa pede descarte.
# ---------------------------------------------------------------------------
df = df.dropna().drop(columns="id").astype(int)
X = df.drop(columns="class").to_numpy()
y = df["class"].to_numpy()
print(f"Instâncias após limpeza: {len(df)}")
print(df["class"].value_counts().rename(NOMES).to_string(), "\n")

# ---------------------------------------------------------------------------
# 3. Treino e teste
# O modelo é ajustado no treino; o teste (30%) estima o acerto em dados novos.
# stratify mantém a proporção das classes; random_state torna reproduzível.
# ---------------------------------------------------------------------------
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
print(f"Treino: {len(X_treino)} | Teste: {len(X_teste)}\n")


# ---------------------------------------------------------------------------
# 4. Classificador de centróides médios
# Treino: centróide de cada classe = média dos seus exemplos.
# Predição: classe do centróide mais próximo (distância euclidiana).
# Atributos já estão na mesma escala (1-10), então não há padronização.
# ---------------------------------------------------------------------------
class CentroidesMedios:
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.centroides_ = np.array([X[y == c].mean(axis=0) for c in self.classes_])
        return self

    def predict(self, X):
        distancias = np.linalg.norm(X[:, None, :] - self.centroides_[None, :, :], axis=2)
        return self.classes_[distancias.argmin(axis=1)]


modelo = CentroidesMedios().fit(X_treino, y_treino)
print("Centróides:")
print(pd.DataFrame(modelo.centroides_, index=[f"centróide {NOMES[c]}" for c in CLASSES],
                   columns=COLUNAS[1:-1]).round(2).to_string(), "\n")


# ---------------------------------------------------------------------------
# 5. Avaliar
# Acurácia geral: fração de acertos no teste.
# Acurácia por classe: diagonal da matriz de confusão normalizada por linha.
# Importa porque as classes são desbalanceadas e falso negativo custa mais.
# ---------------------------------------------------------------------------
def avaliar(y_real, y_pred):
    por_classe = confusion_matrix(y_real, y_pred, labels=CLASSES, normalize="true").diagonal()
    return {"acurácia geral": accuracy_score(y_real, y_pred),
            **{f"acurácia {NOMES[c]}": a for c, a in zip(CLASSES, por_classe)}}


y_pred = modelo.predict(X_teste)
print("=== Centróides médios ===")
for nome, valor in avaliar(y_teste, y_pred).items():
    print(f"{nome:>24}: {valor:.2%}")
print("\nMatriz de confusão (linhas = real, colunas = previsto):")
print(pd.DataFrame(confusion_matrix(y_teste, y_pred, labels=CLASSES),
                   index=[f"real {NOMES[c]}" for c in CLASSES],
                   columns=[f"previsto {NOMES[c]}" for c in CLASSES]).to_string(), "\n")

# Checagem: mesma regra que o NearestCentroid do scikit-learn.
assert (NearestCentroid().fit(X_treino, y_treino).predict(X_teste) == y_pred).all()

# ---------------------------------------------------------------------------
# 6. Comparação com outros modelos (extra), mesmo split e mesma métrica
# ---------------------------------------------------------------------------
modelos = {
    "Centróides médios (própria)": CentroidesMedios(),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Regressão logística": LogisticRegression(max_iter=1000),
    "Árvore de decisão": DecisionTreeClassifier(random_state=42),
    "Naive Bayes gaussiano": GaussianNB(),
}
resultados = pd.DataFrame({
    nome: avaliar(y_teste, m.fit(X_treino, y_treino).predict(X_teste))
    for nome, m in modelos.items()
}).T
print("=== Comparação ===")
print(resultados.map(lambda v: f"{v:.2%}").to_string())
