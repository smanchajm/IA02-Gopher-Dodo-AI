""" Module permettant de gérer les statistiques des parties jouées """
import os
import pandas as pd


def append_to_csv(dataframe: pd.DataFrame, filename: str):
    """
    Fonction permettant d'ajouter une ligne à un fichier CSV
    """
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    path_file = os.path.join(parent_dir, "../Benchmarks", filename)

    # Vérifier si le fichier existe
    file_exists = os.path.isfile(path_file)

    # Créer le dossier Benchmarks s'il n'existe pas déjà
    os.makedirs(os.path.dirname(path_file), exist_ok=True)

    # Écrire dans le fichier
    with open("benchmark.csv", "a", newline="", encoding="utf-8") as f:
        if not file_exists:
            dataframe.to_csv(f, header=True, index=False)
        else:
            dataframe.to_csv(f, header=False, index=False)


def add_to_benchmark(
    list_results,
    filename: str,
    game: str,
    game_number: int,
    strategy_1: str,
    strategy_2: str,
    grid: int,
):
    """
    Fonction permettant d'ajouter les statistiques d'une partie à un fichier CSV
    """

    # Calcul des statistiques
    win_number = sum(res["winner"] == 1 for res in list_results)
    loss_number = game_number - win_number
    new_benchmark = {
        "game": game,
        "strategy_1": strategy_1,
        "strategy_2": strategy_2,
        "Grid": grid,
        "game_number": game_number,
        "win_rate": sum(res["winner"] == 1 for res in list_results) / game_number,
        "average_turns": sum(res["total_turns"] for res in list_results) / game_number,
        "min_turns": min(res["total_turns"] for res in list_results),
        "max_turns": max(res["total_turns"] for res in list_results),
        "average_iteration_time": sum(
            res["average_iteration_time"] for res in list_results
        )
        / game_number,
        "average_iteration_time_max": sum(
            res["average_iteration_time_max"] for res in list_results
        )
        / game_number,
        "average_iteration_time_min": sum(
            res["average_iteration_time_min"] for res in list_results
        )
        / game_number,
        "average_total_time": sum(res["total_time"] for res in list_results)
        / game_number,
        "average_turns_win": (
            (
                sum(res["total_turns"] for res in list_results if res["winner"] == 1)
                / win_number
            )
            if win_number > 0
            else 0
        ),
        "average_turns_loss": (
            (
                sum(res["total_turns"] for res in list_results if res["winner"] == -1)
                / loss_number
            )
            if loss_number > 0
            else 0
        ),
    }

    # Création d'un DataFrame avec une seule ligne
    df_results = pd.DataFrame([new_benchmark])
    print(f"Temps de la partie : {df_results["average_total_time"]}")
    # Ajout des statistiques à un fichier CSV
    append_to_csv(df_results, f"{filename}.csv")
