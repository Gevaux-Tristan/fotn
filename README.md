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
  Rendu : intensité, grain, taille du grain, halation, bloom, vignettage, estompé). Export → `fotn_<preset>_<horodatage>-<id>.jpg`.

## Fichiers
- `index.html` — toute l'app. `generic.jpg` — image de référence des cartes.
- `luts/<stock>.png` — les LUTs 3D (Hald CLUT 125×125) chargées à l'exécution. `luts/lut-identity.png`
  + `luts/genhald.py` — image identité et générateur pour cuire de nouvelles LUTs dans Lightroom.
- `icon.svg` + PNG, `manifest.webmanifest` — branding / PWA.

## Lancer en local
```bash
python3 -m http.server 8791   # à la racine du repo, puis http://localhost:8791/
```
La caméra exige un contexte sécurisé (**HTTPS** ou `localhost`).

## Déployer
Hébergement statique. Déployé sur GitHub Pages : https://gevaux-tristan.github.io/fotn/

## Effets optiques (post-passe spatiale)
- **Halation** : halo rouge-orangé autour des hautes lumières (lumière réfléchie par la base du film).
- **Bloom** : diffusion douce des hautes lumières.
- Les deux sont calculés sur un tampon ~128 px flouté puis remis à l'échelle → même rendu en
  vignette, en aperçu et à l'export. Fusion en *screen*.
- **Grain** : bruit de valeur à graine fixe (stable entre deux rendus), taille relative au cadre,
  plus fort dans les tons moyens, légère composante chromatique sur les pellicules couleur.

## Importer un look depuis un outil web (ex. Dehancer Online), usage perso
1. Charger `luts/lut-identity-1000.png` (1000×1000, bloc 8×8 par nœud, résiste à la recompression).
2. Appliquer le preset en **désactivant grain, halation, bloom, vignettage, netteté** : un effet
   spatial casserait la LUT (on les refait dans fotn).
3. Exporter sans redimensionner (PNG/TIFF de préférence, sinon JPEG qualité max), en PNG dans `luts/<nom>.png`.
4. Ajouter une ligne dans `PRESETS` (`{name, film, cat, lut:'luts/<nom>.png'}`). Le loader accepte
   125×125 ou tout multiple (lecture au centre de chaque bloc).
