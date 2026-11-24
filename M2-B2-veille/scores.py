"""Évaluation d'une solution de détection : fonction texte → liste de (debut, fin, categorie).

Une donnée est TROUVÉE si au moins une détection la recouvre, quelle que soit la catégorie annoncée :
pour la protection, l'essentiel est qu'elle soit masquée. Une détection qui ne recouvre aucune donnée
personnelle est un masquage À TORT. Cette convention est un choix : elle peut être discutée dans le protocole.
"""

import time

import pandas as pd


def _recouvre(a_debut, a_fin, b_debut, b_fin) -> bool:
    return a_debut < b_fin and b_debut < a_fin


def _comparer(solution, avis: pd.DataFrame, verite: pd.DataFrame):
    oublis, torts = [], []
    for _, ligne in avis.iterrows():
        detections = solution(ligne["texte"])
        reelles = verite[verite["avis_id"] == ligne["avis_id"]]
        for _, e in reelles.iterrows():
            if not any(_recouvre(d[0], d[1], e["debut"], e["fin"]) for d in detections):
                oublis.append({"avis_id": e["avis_id"], "categorie": e["categorie"], "valeur": e["valeur"]})
        for d in detections:
            if not any(_recouvre(d[0], d[1], e["debut"], e["fin"]) for _, e in reelles.iterrows()):
                torts.append({"avis_id": ligne["avis_id"], "categorie": d[2], "valeur": ligne["texte"][d[0]:d[1]]})
    return oublis, torts


def evaluer(solution, avis: pd.DataFrame, verite: pd.DataFrame) -> pd.DataFrame:
    """Par catégorie : données présentes, trouvées, ratées, et masquages à tort (catégorie annoncée par la solution)."""
    debut = time.perf_counter()
    oublis, torts = _comparer(solution, avis, verite)
    ms = (time.perf_counter() - debut) * 1000 / len(avis)
    presentes = verite["categorie"].value_counts()
    ratees = pd.Series([o["categorie"] for o in oublis], dtype=object).value_counts()
    a_tort = pd.Series([t["categorie"] for t in torts], dtype=object).value_counts()
    res = pd.DataFrame({"presentes": presentes, "ratees": ratees, "a_tort": a_tort}).fillna(0).astype(int)
    res.insert(1, "trouvees", res["presentes"] - res["ratees"])
    res.loc["TOTAL"] = res.sum()
    res["rappel"] = (res["trouvees"] / res["presentes"].where(res["presentes"] > 0)).round(2)
    res.attrs["ms_par_avis"] = round(ms, 1)
    print(f"{ms:.1f} ms par avis")
    return res


def erreurs(solution, avis: pd.DataFrame, verite: pd.DataFrame) -> pd.DataFrame:
    """La liste des oublis et des masquages à tort, avec le texte de l'avis."""
    oublis, torts = _comparer(solution, avis, verite)
    lignes = [{"type": "oubli", **o} for o in oublis] + [{"type": "à tort", **t} for t in torts]
    return pd.DataFrame(lignes, columns=["type", "avis_id", "categorie", "valeur"]).merge(avis, on="avis_id")
