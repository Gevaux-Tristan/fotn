# Fudge

**Fudge** — webapp photo mobile-first (compatible desktop), **caméra d'abord** : on arrive sur le
viseur, on photographie avec un **preset appliqué en temps réel**, puis on affine et on exporte.
Interface noir & jaune (Kodak), typographie Google Sans. App mono-fichier (`index.html`, sans dépendance).

## Logique
- **Caméra-first** : à l'ouverture, le viseur live s'affiche. Un bandeau de presets se parcourt
  horizontalement et le rendu s'applique **en direct** sur le flux (résolution réduite pour la fluidité,
  grain ajouté à la capture). Déclencheur → la photo est capturée avec le look, puis ouverte dans
  l'éditeur pour réglages + export. Bascule avant/arrière, import depuis la galerie, repli si la
  caméra est refusée/indisponible.
- **Bibliothèque de presets** (~22) inspirés de pellicules réelles : négatifs (Portra, Gold, Superia),
  diapos (Velvia, Provia, Kodachrome), ciné (CineStill 800T, Vision3), lomo/cross-process, vintage,
  N&B (Tri-X, HP5, Acros, Delta, Sépia, Sélénium). Chaque preset est un **look paramétrique** calibré.
- **Moteur de rendu pixel** (`renderRecipe` / `buildOps`) : balance des blancs, matrice
  colorimétrique, split-tone, contraste, courbes hautes/basses lumières, grain, vignettage. Le même
  moteur alimente le viseur live, les cartes de la galerie, l'aperçu éditeur et l'export.
- **Galerie** : chaque carte applique le preset sur une même image de référence (`generic.jpg`).
  Filtres Favoris / Couleur / Noir & blanc ; affichage compact / grand / liste + « Charger plus ».
- **Éditeur** : aperçu plein cadre de votre photo + **réglages universels** en onglets (Lumière :
  exposition, contraste, hautes lumières, ombres ; Couleur : saturation, température, teinte ;
  Rendu : grain, vignettage, estompé). Export → `fudge_<preset>_<horodatage>.jpg`.

## Fichiers
- `index.html` — toute l'app (presets embarqués). `generic.jpg` — image de référence des cartes.
- `logo.svg`, `icon.svg` + PNG, `manifest.webmanifest` — branding / PWA.

## Lancer en local
```bash
cd fuji-recipes && python3 -m http.server 8765   # puis http://localhost:8765/
```
La caméra exige un contexte sécurisé (**HTTPS** ou `localhost`).

## Déployer
Hébergement statique. Déployé sur GitHub Pages : https://gevaux-tristan.github.io/Fudge/
