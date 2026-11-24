# M2-B2, partie 2 — Veille et benchmark (individuel)



```
data/avis_verifies.csv         60 avis fictifs
data/entites_verifiees.csv     51 données personnelles relevées à la main (position, catégorie)
scores.py                      evaluer() et erreurs(), fournies
notebooks/02_benchmark.ipynb   notebook de travail
VEILLE.md                      gabarit de la fiche de veille
RECOMMANDATION.md              gabarit de la recommandation
```

| Catégorie | Contenu |
|---|---|
| `NOM` | nom ou prénom de client, de proche ou d'employé |
| `EMAIL`, `TELEPHONE`, `ADRESSE` | coordonnées |
| `CHAMBRE` | numéro de chambre |
| `RESERVATION` | numéro de dossier ou de fidélité |
| `IDENTITE` | passeport, plaque, pseudonyme en ligne |

Les avis contiennent aussi des pièges sans donnée personnelle (lieux, prix, mots courants qui ressemblent à des prénoms). Des informations de santé y figurent : elles ne sont pas annotées, mais elles comptent pour la conclusion.

```bash
python -m venv .venv
```

```bash
.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

Les solutions testées s'installent en plus. **Un environnement virtuel par solution** évite les conflits de versions. Les avis ne doivent jamais être envoyés à un service en ligne, sauf pour télécharger un modèle.
