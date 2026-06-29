# fotn

**fotn** — webapp photo mobile-first (compatible desktop) : on prend une photo avec la **caméra
native du système** (ou on importe), puis on choisit un **look** inspiré des pellicules argentiques,
on l'affine et on exporte. Interface monochrome (noir/blanc/gris), typographie Geist. App
mono-fichier (`index.html`, sans dépendance, sans build).

## Logique
- **Caméra native** : le bouton appareil photo ouvre la caméra **du système** (`<input capture>`) —
  qualité maximale, format natif, orientation correcte, aucun viseur custom. La photo revient dans
  l'app et s'ouvre dans l'éditeur. Import depuis la galerie via le bouton image.
- **Presets = vraies LUTs 3D** issues des profils Lightroom *Analog Vision Studio V2 (Frontier)* :
  Portra 400, Pro 400H, Gold 200, ColorPlus 200, Kodacolor 100, UltraMax 400, Velvia 100, HP5+.
  Chaque profil `.xmp` est un *Look* dont toute la couleur est une LUT 3D embarquée ; elle est
  « cuite » sur une image identité (Hald CLUT) dans Lightroom puis stockée en PNG (`luts/<stock>.png`,
  125×125 = 25³ nœuds) et appliquée en **interpolation trilinéaire** → rendu identique au profil.
- **Moteur de rendu pixel** (`renderRecipe` / `buildOps`) : la **LUT** porte le look (appliquée en
  premier, dosée par l'**intensité**), puis les réglages universels (expo, balance des blancs,
  contraste, hautes/basses lumières, saturation, grain, vignettage) se superposent. Le même moteur
  alimente les cartes de la galerie, les vignettes du bandeau, l'aperçu éditeur et l'export.
- **Galerie** : chaque carte applique le preset sur une même image de référence (`generic.jpg`).
  Filtres Favoris / Couleur / Noir & blanc ; affichage compact / grand / liste + « Charger plus ».
- **Éditeur (façon VSCO)** : aperçu plein cadre de votre photo, **bandeau de presets** dont chaque
  vignette montre le look appliqué à *votre* photo (tap pour changer de look, les réglages sont
  conservés), **recadrage** (bouton « Recadrer » → boîte ajustable + chips de ratio : Libre, Original,
  1:1, 4:5, 5:4, 3:2, 2:3, 16:9, 9:16, grille des tiers), **curseur d'intensité** du look, et
  **réglages universels** en onglets (Lumière :
  exposition, contraste, hautes lumières, ombres ; Couleur : saturation, température, teinte ;
  Rendu : intensité, grain, vignettage, estompé). Export → `fotn_<preset>_<horodatage>-<id>.jpg`.

## Fichiers
- `index.html` — toute l'app. `generic.jpg` — image de référence des cartes.
- `luts/<stock>.png` — les LUTs 3D (Hald CLUT 125×125) chargées à l'exécution. `luts/lut-identity.png`
  + `luts/genhald.py` — image identité et générateur pour cuire de nouvelles LUTs dans Lightroom.
- `icon.svg` + PNG, `manifest.webmanifest` — branding / PWA.

## Lancer en local
```bash
cd fuji-recipes && python3 -m http.server 8765   # puis http://localhost:8765/
```
La caméra exige un contexte sécurisé (**HTTPS** ou `localhost`).

## Déployer
Hébergement statique. Déployé sur GitHub Pages : https://gevaux-tristan.github.io/fotn/
