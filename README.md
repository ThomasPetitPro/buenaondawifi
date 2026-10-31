# Wi-Fi Buena Onda Lille 🎃

Page d'accueil Wi-Fi du bar Buena Onda (34 rue Saint-Sébastien, Lille), thème Halloween orange.
Le client suit le compte Instagram, puis le nom du réseau et le mot de passe s'affichent.

## 1. Renseigner les infos

Dans `index.html`, modifier le bloc `CONFIG` :

```js
const CONFIG = {
  instagram: "buenaondalille",
  ssid:      "NOM_DU_RESEAU",
  password:  "MOT_DE_PASSE"
};
```

## 2. Héberger sur GitHub Pages

1. Créer un dépôt public sur GitHub (ex. `buena-onda-wifi`) et y pousser ces fichiers.
2. Dépôt → **Settings** → **Pages** → Source : **Deploy from a branch** → branche `main`, dossier `/ (root)` → **Save**.
3. Après environ une minute, la page est en ligne sur `https://TON-PSEUDO.github.io/buena-onda-wifi/`.

## 3. Générer le QR code et l'affichette

```bash
pip install "qrcode[pil]"
python make_qr.py            # URL par défaut : https://thomaspetitpro.github.io/buenaondawifi/
```

Fichiers produits :
- `qr-buena-onda.png` : le QR code seul
- `affichette-buena-onda.png` : affichette Halloween A6 (300 dpi)
- `affichettes-A4.pdf` : 4 affichettes sur une feuille A4, à imprimer puis découper

Tester le QR avec un téléphone avant d'imprimer.

## Bon à savoir

- Le mot de passe est lisible dans le code de la page : utiliser un réseau Wi-Fi invités séparé du réseau interne.
- Le suivi du compte n'est pas vérifié (principe de confiance).
