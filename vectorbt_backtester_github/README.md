# VectorBT Backtester Pro (Starter)

## 🚀 Description

Framework modulaire en Python pour tester automatiquement **des milliers de stratégies** sur n'importe quel actif, avec classement automatique (CAGR, Sharpe, Profit Factor…).

---

## 📁 Structure du projet

```
vectorbt_backtester/
│
├── main.py
├── config.py
├── strategies.py
├── context.py
├── backtester.py
├── results_analyzer.py
├── utils.py
├── requirements.txt
├── README.md
└── results/
```

---

## ⚙️ Installation

1. **Clone le dossier ou copie-le où tu veux**
2. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏁 Lancer un backtest

Dans un terminal, place-toi dans le dossier et lance :
```bash
python main.py
```

Le script :
- Télécharge les données de l’actif défini dans `config.py`
- Détecte la tendance (haussier, baissier…)
- Génère et backteste des centaines/ milliers de setups
- Classe et exporte les meilleurs/pires dans `results/`

---

## ⚙️ Modifier les paramètres

Tout se passe dans **`config.py`** :
- Change l’actif : `TICKER = "RXL.PA"`
- Change la période : `START_DATE`, `END_DATE`
- Modifie les plages de paramètres (MA, RSI, SL/TP…)

---

## 📈 Ajouter tes propres stratégies

Dans **`strategies.py`**, ajoute une fonction :
```python
def ma_crossover(price, ma_short, ma_long):
    # Logique d’entrée/sortie ici
    return entries, exits
```
et adapte la boucle du backtest dans `backtester.py`.

---

## 📊 Résultats

- CSVs exportés dans `results/`
- Top stratégies visibles dans le terminal à la fin

---

## 📬 Besoin d’aide ou upgrade ?
Pose ta question à ChatGPT ou améliore ce README pour garder une trace de tes modifs 😉

---

*(Prochaine étape : ajout du multi-actif, scoring graphique, saisonnalité auto, etc.)*

## Quickstart

```bash
# 1) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run
python main.py
```

## Project layout

- `*.py` — source modules (backtester, strategies, walkforward, validator, etc.)
- `results/` — CSV outputs (gitignored by default)
- `requirements.txt` — dependencies
- `.gitignore` — standard Python ignores
- `README.md` — this file

---
## Attribution

Ce dépôt a été nettoyé et structuré avec l’aide de ChatGPT (GPT-5 Thinking) :
- Normalisation du style Python (espaces/retours ligne, tabs → 4 espaces)
- Suppression des artefacts (`__pycache__`, `.__*`, `__MACOSX`)
- Ajout : `.gitignore`,
- `pyproject.toml`, mise à jour du `README`
- Détection des dépendances réelles → `requirements.txt` (numpy, pandas, pandas_ta, tqdm, vectorbt, yfinance)
