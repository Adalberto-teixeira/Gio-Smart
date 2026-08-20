# Gio Smart Services — Site Web

Site vitrine multiservices (ménage, aide à la personne, déménagement, petits travaux, services numériques, soin des animaux) pour la zone de Martigues, basé sur un template modifié et adapté avec du contenu réel.

## Stack
- HTML5 / CSS3 (Bootstrap)
- jQuery, GSAP, Swiper.js, WOW.js
- Contact via WhatsApp (pas de backend/serveur nécessaire)

## 💬 Formulaire de contact
Le site n'a pas de backend. Le "formulaire" de `contact.html` construit un message et ouvre WhatsApp directement (`https://wa.me/33670424876?text=...`) avec le message pré-rempli, prêt à envoyer.

- Le numéro WhatsApp est défini dans `js/function.js` → variable `WHATSAPP_NUMBER` (actuellement `33670424876`, soit 06 70 42 48 76). Pour le changer, modifie cette seule ligne.
- Aucune variable d'environnement, aucun service tiers, aucun coût : fonctionne immédiatement sur n'importe quel hébergement statique (Vercel, GitHub Pages, Netlify...).

Le domaine officiel configuré dans les balises `canonical`, `sitemap.xml` et `robots.txt` est **https://giosmart-services.fr**. Si le domaine change, mets à jour ces 3 éléments.

## Structure
```
/css        Feuilles de style
/js         Scripts (jQuery, GSAP, Swiper, script custom function.js)
/images     Images du site
/webfonts   Icônes Font Awesome
*.html      Pages du site (45 pages)
sitemap.xml / robots.txt   SEO
vercel.json   Configuration du cache pour le déploiement Vercel
```

## Historique des corrections (avant mise sur GitHub)
- Uniformisation de l'email de contact → `contact@giosmart-services.fr`
- Uniformisation du numéro de téléphone → `06 70 42 48 76`
- Correction de 4 titres de page dupliqués (mauvais `<title>` copié d'une autre page)
- Réécriture de 10 méta-descriptions dupliquées (mauvais pour le SEO / contenu dupliqué)
- Correction de tous les liens internes cassés (pages inexistantes)
- Ajout d'une balise `<link rel="canonical">` sur les 45 pages
- Ajout de `robots.txt` et `sitemap.xml`
- Remplacement du formulaire PHP (`form-process.php`, incompatible avec Vercel) par un contact direct WhatsApp (aucun backend nécessaire)
- Suppression complète du blog (blog.html, blog-page-2.html, blog-page-3.html) et de tous les liens associés (menu, footer, breadcrumbs, tags) : contenu non maintenu, mauvais pour le SEO
- Nettoyage de `css/custom.css` : suppression de 159 règles CSS mortes (team, testimonials, galerie, blog...) jamais utilisées dans le HTML, environ 16% de réduction
- Nettoyage de `js/function.js` : suppression de 9 blocs de code mort (sliders, animations, sticky header, galerie) qui ciblaient des éléments inexistants sur le site, environ 52% de réduction
- Suppression de `js/validator.min.js`, devenu inutile après le passage au contact WhatsApp
- Correction de la structure HTML : suppression de balises `</html>` dupliquées trouvées sur 5 pages (`local-technique-construction.html`, `montage-cuisine-marseille.html`, `creation-site-web.html`, `carte-visite-branding.html`, `nettoyage-jardin-vitrolles.html`)
- Ajout de données structurées Schema.org (LocalBusiness) sur la page d'accueil : nom, adresse, téléphone, zone de service — améliore la visibilité sur Google Maps et les recherches locales
- Ajout de l'adresse complète de l'entreprise (12 Avenue Charles Moulet, 13500 Martigues) dans le pied de page de toutes les pages (elle n'apparaissait auparavant que sur la page mentions légales)
- Correction d'une faute de frappe dans l'email du pied de page (`icontact@` → `contact@`) sur une page
- Optimisation SEO local : ajout de « Martigues » dans le titre et la meta description de 21 pages qui ne le mentionnaient pas
- Suppression de 17 pages qui étaient devenues des « pages orphelines » après la suppression du blog (aucun lien interne ne menait vers elles, seul le sitemap les référençait) : le contenu n'était plus accessible en navigation normale et n'apportait plus de valeur sans le blog
- Mise à jour du sitemap.xml pour retirer les pages supprimées (24 URLs au lieu de 44 initialement)
- Nettoyage supplémentaire de `css/custom.css` : suppression de 85 règles mortes supplémentaires qui étaient cachées à l'intérieur des media queries (non détectées lors du premier passage)
- Uniformisation du domaine du créateur du site dans tout le code (footer et balise meta author) : plusieurs variantes coexistaient (adalbertofurtado.com, adalberto.FR), tout pointe maintenant vers adalberto.fr
- Suppression complète du projet "Site vitrine professionnel" dans la section réalisations (page `creation-site-web.html`, carte sur la page d'accueil et sur nos-réalisations, vidéo YouTube associée, images `project-1.jpg` et `project-video-bg.jpg` devenues orphelines) : ce projet correspondait à un client parti sans payer, il n'avait plus lieu d'être présenté comme référence
- Audit complet final : vérification de tous les liens internes, images, fichiers CSS/JS, balises canonical, balises H1, cohérence du téléphone et de l'email sur tout le site — aucune anomalie supplémentaire trouvée
- Suppression de 12 images inutilisées (jamais référencées dans le HTML ni le CSS) : logos d'entreprises fictives, formes décoratives, doublons... environ 660 Ko libérés
- Compression de toutes les images JPEG et PNG (redimensionnement à 1920px max, compression optimisée, réduction des couleurs pour les PNG) : le dossier `/images` passe de 15,95 Mo à 5,16 Mo, soit une réduction de 68%, sans perte de qualité visible

## À améliorer (recommandé, non bloquant)
- Ajouter Google Analytics / Search Console une fois le domaine en ligne.
- Convertir les JPEG en WebP pour un gain supplémentaire de poids (non fait ici par manque d'outil de conversion disponible, mais recommandé pour la suite).

- Suppression finale de 13 images orphelines restantes (anciennes photos d'articles de blog post-1 à post-6, et autres visuels liés à des pages déjà supprimées) — 1,1 Mo libérés supplémentaires. Vérification finale complète : liens, balises HTML, CSS, JS, attributs alt, identifiants uniques — aucune anomalie restante, site prêt pour la mise en ligne
- Correction critique : les liens du menu mobile utilisaient un format absolu (`/page.html`) qui provoquait une erreur "ERR_FILE_NOT_FOUND" en ouvrant le site en local (double-clic sur index.html). Tous les liens ont été convertis en format relatif, fonctionnel aussi bien en local que sur le serveur en ligne
- Suppression d'une page en double sur le même sujet (nettoyage après travaux/déménagement) : la page héritée du blog `nettoyage-apres-travaux-et-demenagement.html` faisait doublon avec la vraie page de service liée dans tout le menu du site — supprimée avec son unique lien entrant et son entrée dans le sitemap

- Correction d'un bug structurel critique sur `local-technique-construction.html` : la balise `<header>`, le logo et la barre de navigation complète avaient été supprimés par erreur, alors que les balises de fermeture correspondantes étaient toujours présentes en bas — cela cassait l'affichage du menu sur cette page uniquement. Structure reconstruite et vérifiée équilibrée.
- Correction d'un ancien email résiduel (`infot@giosmart.fr`, avec faute de frappe) présent dans l'encart "Besoin d'aide ?" de 6 pages de réalisations/FAQ — remplacé par `contact@giosmart-services.fr` partout
