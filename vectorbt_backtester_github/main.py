# main.py

import config
import strategies
import context
import backtester
import results_analyzer

def main():
    print("=== VECTORBT BACKTESTER ===")
    print(f"Actif : {config.TICKER}")
    print(f"Période : {config.START_DATE} -> {config.END_DATE}")

    # Charger les données
    price_data = backtester.load_data(
        ticker=config.TICKER,
        start=config.START_DATE,
        end=config.END_DATE
    )

    # Détection du contexte de tendance
    trend_labels = context.detect_trend(price_data["Close"])

    # Générer les setups à backtester
    setups = strategies.generate_setups()

    # Lancer les backtests
    results = backtester.run_backtests(
        price_data=price_data,
        setups=setups,
        trend_labels=trend_labels,
        config=config
    )

    # Analyse et export des résultats
    results_analyzer.analyze_and_export(results)

    print("=== FINISHED ===")

from walkforward import walkforward_validate

def main_walkforward():
    print("=== VECTORBT WALKFORWARD BACKTESTER ===")
    print(f"Actif : {config.TICKER}")
    print(f"Période : {config.START_DATE} -> {config.END_DATE}")

    # Charger les données
    price_data = backtester.load_data(
        ticker=config.TICKER,
        start=config.START_DATE,
        end=config.END_DATE
    )

    # Préparer les fonctions de stratégie
    strategy_funcs = {
        'ma_crossover': strategies.ma_crossover,
        'rsi_pullback': strategies.rsi_pullback,
        # Ajoute ici d'autres stratégies si tu veux
    }

    # Préparer la grille de paramètres (exemple simple)
    param_grid = {
        'ma_crossover': [
            {'ma_short': 20, 'ma_long': 200, 'sl_pct': 0.01, 'tp_pct': 0.02},
            {'ma_short': 50, 'ma_long': 200, 'sl_pct': 0.015, 'tp_pct': 0.03},
            # Tu peux en générer plus si besoin !
        ],
        'rsi_pullback': [
            {'rsi': 35, 'ma_long': 200, 'sl_pct': 0.01, 'tp_pct': 0.02},
            # Idem, à compléter si tu veux
        ],
    }

    # Lancer la validation walk-forward
    results = walkforward_validate(
        price_data=price_data,
        strategy_funcs=strategy_funcs,
        param_grid=param_grid,
        window_size=500,
        test_size=100,
        min_trades=15
    )

    print("=== RÉSULTATS WALK-FORWARD ===")
    print(results.head(10))
    results.to_csv('results/walkforward_results.csv', index=False)
    print("Résultats walk-forward exportés dans results/walkforward_results.csv")
    print("=== FINISHED WALK-FORWARD ===")

if __name__ == "__main__":
    main()
    print("\n=== Lancement automatique du pipeline WALK-FORWARD ===")
    main_walkforward()

# Pour lancer le pipeline classique : python main.py
# Pour lancer la version walk-forward : ajoute à la fin du fichier :
# main_walkforward()
