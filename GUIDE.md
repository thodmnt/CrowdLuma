# CrowdLuma MVP2 — Mode d'emploi complet
### 🎯 Écrit pour quelqu'un qui n'a jamais touché à du code

---

## C'est quoi CrowdLuma ?

Imagine un stade de foot. Tu as 10 000 spectateurs dans une tribune. Chacun sort son téléphone. En même temps, tous les téléphones affichent une couleur différente — rouge, bleu, blanc, jaune — et ensemble ça forme une image géante dans les gradins. C'est exactement ce que fait CrowdLuma.

Tout fonctionne dans le **navigateur web** de chaque téléphone. Pas besoin de télécharger une application.

---

## 📦 Ce qu'il y a dans ce dossier

```
crowdluma-mvp2/
│
├── index.html          ← Console admin pour UNE tribune + vue supporter
├── admin.html          ← Console admin simplifiée (import photo/vidéo)
├── stadium-admin.html  ← Console admin pour un STADE ENTIER (login admin)
├── orders-ops.html     ← Tableau logistique commandes (bar / livreurs / caisse)
│
├── supabase/
│   └── schema.sql      ← Le script à coller dans Supabase (expliqué plus bas)
│
├── tools/
│   └── generate_seat_qr.py  ← Outil pour créer les QR codes (besoin de Python)
│
└── GUIDE.md            ← Ce fichier !
```

---

## 🚀 PARTIE 1 — Tester sans rien installer (5 minutes)

Tu peux tester CrowdLuma **sans Internet** et **sans créer de compte nulle part**.

### Étape 1 — Ouvrir la console admin

1. Double-clique sur le fichier **`index.html`**
2. Il s'ouvre dans ton navigateur (Chrome, Firefox, Safari… peu importe)
3. Tu vois l'interface de l'admin

### Étape 2 — Créer une tribune

1. Dans « **Rangées** », tape `10`
2. Dans « **Sièges par rangée** », tape `10`
3. Clique sur le bouton **« Créer grille »**
4. Tu vois apparaître une grille de 100 petits carrés colorés à droite

### Étape 3 — Dessiner une image

1. Dans la section « **Image / logo** », clique sur le bouton de fichier
2. Sélectionne n'importe quelle image sur ton ordinateur (logo de club, photo…)
3. Clique sur **« Convertir en pixels »**
4. L'image est transformée en couleurs dans la grille !

### Étape 4 — Simuler un siège de supporter

1. Dans la section « **Vue supporter** », laisse Rangée = 12, Siège = 34
2. Clique sur **« Afficher mon instruction »**
3. Tu vois ce qu'afficherait le téléphone du supporter en siège R12-C34

### Étape 5 — Exporter le show

1. Clique sur **« Exporter JSON »**
2. Un fichier `stadium-choreo.json` se télécharge
3. Ce fichier contient toute la chorégraphie — tu peux le partager

---

## 🌐 PARTIE 2 — Créer un compte Supabase (gratuit, pour les vraies fonctions live)

Supabase, c'est un service gratuit sur Internet qui permet à l'appli de :
- Envoyer des **notifications** aux supporters (ex: « Revenez à vos sièges »)
- Lancer des **votes en direct** affichés sur les téléphones
- Recevoir les **commandes du shop** (bière, snack, etc.)

> 💡 **Si tu veux juste tester les couleurs et la chorégraphie, tu n'as pas besoin de Supabase.** Crée-le seulement quand tu veux tester les fonctions live.

### Étape 1 — Créer ton compte Supabase

1. Ouvre ton navigateur et va sur **https://supabase.com**
2. Clique sur le grand bouton **« Start your project »** (ou « Se connecter »)
3. Clique sur **« Sign up »** pour créer un compte
4. Entre ton adresse e-mail et un mot de passe, puis valide
5. Va dans ta boîte mail et clique sur le lien de confirmation que Supabase t'envoie

### Étape 2 — Créer un projet

1. Une fois connecté, clique sur **« New project »**
2. Remplis les champs :
   - **Name** (nom) : tape `crowdluma` (ou ce que tu veux)
   - **Database Password** : invente un mot de passe fort (note-le quelque part !)
   - **Region** : choisis **West EU (Ireland)** si tu es en Europe
3. Clique sur **« Create new project »**
4. ⏳ Attends 1 à 2 minutes que le projet se crée (tu vois une barre de chargement)

### Étape 3 — Créer les tables (la base de données)

Les « tables », c'est comme des feuilles Excel où CrowdLuma va stocker les commandes et les votes.

1. Dans le menu de gauche, clique sur **« SQL Editor »** (l'icône ressemble à `< >`)
2. Clique sur **« New query »** (nouveau fichier SQL)
3. Ouvre le fichier **`supabase/schema.sql`** de ton dossier CrowdLuma avec un éditeur de texte (Bloc-notes sur Windows, TextEdit sur Mac)
4. Sélectionne **tout le texte** (Ctrl+A ou Cmd+A) et copie-le (Ctrl+C ou Cmd+C)
5. Retourne dans Supabase, clique dans la zone de texte blanche, et colle (Ctrl+V ou Cmd+V)
6. Clique sur le bouton **« Run »** (le triangle vert ▶)
7. Tu dois voir apparaître « Success. No rows returned » en bas → c'est bon !

### Étape 4 — Récupérer tes clés d'accès

1. Dans le menu de gauche, clique sur **« Settings »** (l'icône d'engrenage ⚙)
2. Clique sur **« API »**
3. Tu vois deux informations importantes :
   - **Project URL** : ressemble à `https://abcdefgh.supabase.co`
   - **anon public** (sous « Project API keys ») : une longue suite de lettres et chiffres
4. Note ces deux informations (ou laisse cette page ouverte)

> ⚠️ **Important** : la clé `anon public` peut être vue par tout le monde, c'est normal. Ne partage JAMAIS la clé `service_role` — celle-là est secrète.

### Étape 5 — Configurer CrowdLuma avec tes clés

#### Dans `stadium-admin.html` (console stade complet) :

1. Ouvre `stadium-admin.html` dans ton navigateur
2. Clique sur le bouton rouge **« 🔴 Live »** en haut à droite
3. Clique sur l'onglet **« ⚙ Config »**
4. Dans **« URL Supabase »**, colle ton Project URL (ex: `https://abcdefgh.supabase.co`)
5. Dans **« Clé publique anon »**, colle ta clé anon
6. Clique sur **« Connecter à Supabase »**
7. Le point rouge 🔴 en haut du panneau doit devenir vert 🟢 → tu es connecté !

#### Dans `index.html` (si tu utilises la console tribune seule) :

1. Ouvre `index.html` dans un éditeur de texte (Bloc-notes / TextEdit)
2. Cherche le texte `supabaseUrl: '',` (vers le bas du fichier)
3. Remplace par : `supabaseUrl: 'https://TONPROJET.supabase.co',`
4. Cherche `supabaseKey: '',`
5. Remplace par : `supabaseKey: 'TACLEANNON',`
6. Sauvegarde le fichier (Ctrl+S ou Cmd+S)

---

## 🏟 PARTIE 3 — Utiliser la console stade complet

La console stade (`stadium-admin.html`) permet de gérer un stade entier avec plusieurs zones et blocs.

### Créer la structure de ton stade

1. Ouvre **`stadium-admin.html`**
2. En haut, clique sur « Mon Stade » et tape le vrai nom de ton stade
3. À gauche, tu vois déjà 2 zones créées automatiquement (Tribune Nord, Tribune Sud)

**Pour ajouter une zone :**
- Clique sur **« + Ajouter une zone »** en bas à gauche
- Dans l'éditeur à droite, change le nom et la couleur

**Pour modifier un bloc :**
- Clique sur un bloc dans la liste de gauche (ex: « Bloc A »)
- À droite, tu peux changer le nombre de rangées et de sièges
- Tu peux importer une image ou peindre les cellules manuellement

**Pour voir l'ensemble :**
- La zone centrale montre une vue d'ensemble de tout le stade
- Chaque rectangle coloré = un bloc
- Clique dessus pour l'éditer

### Configurer le Shop

1. Clique sur **« 🔴 Live »** → onglet **« 🛒 Shop »**
2. Tu vois les articles par défaut (Boisson, Snack, Menu, Programme)
3. **Pour activer un article** : coche la case à droite → il devient visible pour les supporters
4. **Pour ajouter un article** : remplis le formulaire en bas (emoji, nom, description, prix) et clique **« + Ajouter »**
5. **Pour diffuser** : clique **« Diffuser le shop aux participants →»** → tous les téléphones ouverts voient le shop se mettre à jour instantanément

### Exporter pour GitHub Pages (publication)

1. Clique sur **« Export JSON »** en haut
2. Un fichier `mon-stade.json` se télécharge
3. Ce fichier contient la chorégraphie complète
4. Tu peux le mettre sur un serveur web pour que les supporters le chargent

---

## 📱 PARTIE 4 — L'expérience du supporter

### Comment un supporter accède à l'appli ?

Chaque siège a un **QR code unique**. Quand le supporter le scanne avec son téléphone, une page web s'ouvre — pas besoin de télécharger quoi que ce soit.

La page affiche :
- **Plein écran** : la couleur que le supporter doit montrer (rouge, bleu, blanc…)
- **Bouton 🛒 Shop** (en bas à droite, visible seulement si des articles sont activés) : pour commander une boisson ou un snack
- **Bannière notification** : apparaît automatiquement si l'admin envoie un message
- **Overlay vote** : apparaît automatiquement si l'admin lance un sondage

### Simuler l'expérience supporter (pour tester)

1. Dans `index.html`, dans « Vue supporter », note l'URL affichée
2. Ou clique sur **« Copier URL du siège affiché »**
3. Envoie cette URL à ton téléphone (par SMS, WhatsApp, ou scanne un QR)
4. Ouvre-la dans le navigateur du téléphone
5. Tu vois l'écran plein écran couleur !

---

## 🔴 PARTIE 5 — Contrôler un match en live

Une fois Supabase connecté, voici comment gérer un événement réel.

### Envoyer une notification

1. **`stadium-admin.html`** → bouton **« 🔴 Live »** → onglet **« 🔔 Notif »**
2. Choisis la **cible** dans la liste :
   - 🏟 Tout le stade
   - Une zone (ex: Tribune Nord)
   - Un bloc (ex: Tribune Nord / Bloc A)
   - Un siège précis (tape l'identifiant, ex: `R12-C34`)
3. Tape ton **message** (ex: « Merci de préparer vos drapeaux pour la mi-temps »)
4. Clique **« Envoyer la notification 🔔 »**
5. En moins d'une seconde, une bannière apparaît sur les téléphones des supporters ciblés (seulement ceux qui ont l'appli ouverte)

### Lancer un vote

1. Onglet **« 📊 Vote »**
2. Tape la **question** (ex: « Homme du match ? »)
3. Tape les **options** (ex: Option A: Mbappé, Option B: Griezmann)
4. Clique **« Lancer le vote 📊 »**
5. Sur tous les téléphones ouverts : un sondage apparaît automatiquement
6. Les supporters votent, tu vois les résultats en temps réel dans l'onglet Vote
7. Clique **« Terminer le vote »** quand c'est fini → les sondages disparaissent des téléphones

### Gérer les commandes du shop

1. Onglet **« 📦 Cmdes »**
2. Tu vois toutes les commandes passées par les supporters (article, siège, heure)
3. Quand une commande est livrée : clique sur **« Livré ✓ »**
   - Le statut passe à « delivered »
   - Le supporter reçoit une notification sur son téléphone : « ✓ Votre commande est en route ! »

---

## 🖨 PARTIE 6 — Générer les QR codes pour les sièges

Cette partie nécessite **Python** (un logiciel gratuit). Si tu ne sais pas si tu l'as, va directement à « Vérifier Python » ci-dessous.

### Vérifier si Python est installé

**Sur Windows :**
1. Appuie sur les touches Windows + R
2. Tape `cmd` et appuie sur Entrée
3. Dans la fenêtre noire, tape `python --version` et appuie sur Entrée
4. Si tu vois `Python 3.x.x` → c'est bon ! Sinon, va sur **https://python.org** et télécharge Python 3

**Sur Mac :**
1. Appuie sur Cmd + Espace, tape `Terminal`, appuie sur Entrée
2. Tape `python3 --version` et appuie sur Entrée
3. Si tu vois `Python 3.x.x` → c'est bon !

### Installer les dépendances (une seule fois)

Dans le Terminal / cmd, navigue jusqu'au dossier CrowdLuma :

**Windows :** `cd C:\chemin\vers\crowdluma-mvp1`
**Mac :** `cd /chemin/vers/crowdluma-mvp1`

Puis tape :
```
pip install qrcode[pil] Pillow
```
(ou `pip3 install qrcode[pil] Pillow` sur Mac)

Attends que l'installation se termine.

### Générer les QR codes

Tape cette commande (remplace les valeurs par les tiennes) :

```bash
python tools/generate_seat_qr.py \
  --base-url https://TONSITE.github.io/crowdluma/ \
  --stand "Tribune Nord" \
  --block A \
  --rows 30 \
  --cols 25 \
  --out dist/qr-nord-A
```

**Explication de chaque option :**
- `--base-url` : l'adresse de ton site web public (où les gens vont quand ils scannent)
- `--stand` : nom de la tribune (entre guillemets si il y a des espaces)
- `--block` : nom du bloc
- `--rows` : nombre de rangées
- `--cols` : nombre de sièges par rangée
- `--out` : dossier où seront créés les fichiers

**Pour un test rapide avec seulement quelques QR :**
```bash
python tools/generate_seat_qr.py \
  --base-url https://TONSITE.github.io/crowdluma/ \
  --stand "Tribune Nord" --block A \
  --rows 5 --cols 5 --out dist/test
```

### Résultat

Dans le dossier `dist/qr-nord-A/` tu trouveras :
- 📁 `qrs/` : un fichier PNG par siège (ex: `A-R01-C01.png`)
- 📄 `seat-registry.csv` : tableau Excel avec tous les sièges et leurs URLs
- 🖨 `print-sheet.html` : page prête à imprimer, tous les QR sur une grille

Chaque image PNG contient le QR code ET le numéro de siège imprimé dessous, pour que les agents d'installation sachent où les coller même si le QR ne scanne pas.

---

## ☁️ PARTIE 7 — Publier sur GitHub Pages (gratuit)

GitHub Pages permet de mettre ton site en ligne gratuitement pour que les supporters puissent vraiment y accéder.

### Créer un compte GitHub

1. Va sur **https://github.com**
2. Clique sur **« Sign up »**
3. Crée un compte (email + mot de passe)

### Créer un dépôt (repository)

1. Une fois connecté, clique sur le **+** en haut à droite → **« New repository »**
2. Donne-lui un nom (ex: `crowdluma`)
3. Coche **« Public »**
4. Clique sur **« Create repository »**

### Uploader les fichiers

1. Dans ton nouveau dépôt, clique sur **« uploading an existing file »**
2. Glisse-dépose tous les fichiers du dossier `crowdluma-mvp1/` (index.html, admin.html, stadium-admin.html, etc.)
3. En bas, clique sur **« Commit changes »**

### Activer GitHub Pages

1. Clique sur **« Settings »** (en haut du dépôt)
2. Dans le menu de gauche, clique sur **« Pages »**
3. Sous « Branch », sélectionne **« main »** et clique **« Save »**
4. ⏳ Attends 2-3 minutes
5. Ton site est maintenant accessible à l'adresse : `https://TONPSEUDO.github.io/crowdluma/`

> C'est cette URL que tu utilises dans `--base-url` pour générer les QR codes !

---

## ❓ PARTIE 8 — Problèmes fréquents

### « Le fichier s'ouvre mais rien ne s'affiche »
→ Vérifie que tu utilises un navigateur récent (Chrome, Firefox, Edge, Safari). Internet Explorer ne fonctionne pas.

### « Supabase ne se connecte pas — le point reste rouge »
→ Vérifie que tu as bien copié l'URL et la clé sans espace au début ou à la fin. L'URL doit commencer par `https://` et finir par `.supabase.co`.

### « Les notifications ne arrivent pas sur le téléphone »
→ Le téléphone doit avoir la page web **ouverte** au moment de l'envoi. CrowdLuma n'envoie pas de notifications quand l'appli est fermée (c'est voulu pour respecter la vie privée).

### « Le QR code scannе mais la page est blanche »
→ Vérifie que le site est bien en ligne sur GitHub Pages et que l'URL dans `--base-url` est correcte (sans faute de frappe, avec le `/` final).

### « Je vois 'pip n'est pas reconnu' »
→ Sur Windows, essaie `python -m pip install qrcode[pil] Pillow`. Sur Mac, essaie `pip3 install qrcode[pil] Pillow`.

### « Supabase me dit 'relation does not exist' »
→ Tu n'as pas encore exécuté le script SQL. Reprends la Partie 2, Étape 3.

---

## 📋 Résumé — Liste de contrôle pour un vrai événement

Avant le match / l'événement :
- [ ] Créer le compte Supabase et exécuter le script SQL
- [ ] Configurer les zones et blocs dans `stadium-admin.html`
- [ ] Importer l'image/logo de la chorégraphie
- [ ] Exporter le JSON et le mettre en ligne
- [ ] Générer les QR codes pour tous les sièges
- [ ] Imprimer les QR codes et les coller sur les sièges
- [ ] Tester avec un téléphone en scannant un QR

Pendant l'événement :
- [ ] Ouvrir `stadium-admin.html` sur ton ordinateur/tablette
- [ ] Connecter Supabase (onglet Config du panneau Live)
- [ ] Activer les articles du Shop si besoin (onglet Shop)
- [ ] Lancer les notifications et votes au bon moment
- [ ] Surveiller les commandes et cliquer « Livré ✓ »

---

## 🚀 PARTIE 9 — Nouvelles fonctions MVP2

MVP2 ajoute 4 améliorations concrètes. **Tout est dans les mêmes fichiers** — pas besoin d'en ouvrir de nouveaux.

---

### Nouveauté 1 — Connexion admin sécurisée

Quand Supabase est configuré, la console stade (`stadium-admin.html`) demande un email et un mot de passe avant d'autoriser l'accès. Si quelqu'un ouvre le fichier sans connaître le mot de passe, il ne peut rien contrôler.

**Créer le compte administrateur dans Supabase :**

1. Ouvre ton projet Supabase sur **https://supabase.com**
2. Dans le menu de gauche, clique sur **« Authentication »** (l'icône de cadenas)
3. Clique sur **« Users »**
4. Clique sur **« Add user »** → **« Create new user »**
5. Tape l'e-mail de l'admin (ex: `directeur@monclub.fr`) et un mot de passe fort
6. Clique **« Create user »**

**Utiliser le login :**

1. Ouvre **`stadium-admin.html`** dans ton navigateur
2. Si Supabase est configuré (URL + clé sauvegardées), un écran de connexion apparaît automatiquement
3. Tape l'e-mail et le mot de passe créés à l'étape précédente → clique **« Se connecter »**
4. L'interface admin s'ouvre, ton prénom apparaît en haut à droite
5. Pour te déconnecter : clique sur le bouton **⏏** à côté de ton nom

> 💡 **Pas encore de Supabase ?** Un lien « Continuer sans authentification » est affiché sous le formulaire — clique dessus pour accéder à l'admin en mode démo.

---

### Nouveauté 2 — Identité unique et persistante du supporter

Chaque téléphone reçoit automatiquement un identifiant unique (appelé UUID) dès qu'il ouvre la page. Rien à faire pour le supporter — c'est invisible.

**Ce que ça change concrètement :**
- Si un supporter ferme et rouvre son QR code, il garde le même identifiant
- Toutes ses commandes au shop sont liées à cet identifiant
- Tu peux voir qui a commandé quoi dans Supabase (Dashboard → Table Editor → `orders`, colonne `participant_id`)

**Aucune configuration requise.** C'est automatique.

---

### Nouveauté 3 — Historique de commandes dans le shop

Quand un supporter ouvre le shop (bouton **🛒**), il voit en bas une section **« Mes commandes »** qui liste ses achats passés avec leur statut :
- 🟡 **en attente** — la commande a été reçue
- 🟢 **livré ✓** — l'admin a cliqué « Livré ✓ » et le supporter a reçu une notification

**Condition :** Supabase doit être connecté. Sans Supabase, la section n'apparaît pas.

---

### Nouveauté 4 — Résultats finaux du vote diffusés automatiquement

Quand l'admin clique **« Terminer le vote »** dans le panneau Live, les téléphones ouverts affichent automatiquement les résultats finaux pendant 5 secondes avant de fermer l'overlay.

Les supporters voient les barres de résultats (ex: Mbappé 68% · Griezmann 32%) directement sur leur écran, sans rien faire.

---

## 🔐 PARTIE 10 — Sécurité : conseils pour un vrai événement

### Ce qui est protégé
- ✅ La console admin est protégée par email + mot de passe (si Supabase configuré)
- ✅ Les clés Supabase `anon` sont publiques par conception — elles peuvent être vues mais les politiques de sécurité empêchent les abus
- ✅ Un supporter ne peut voir que ses propres commandes, pas celles des autres

### Ce qu'il faut faire avant un vrai match
- Ne partage jamais la clé `service_role` de Supabase (elle donne accès total à ta base)
- Crée un compte admin séparé pour chaque personne qui gère le Live (ne partage pas le même mot de passe)
- Teste toujours avec un téléphone réel avant l'événement

---

## 📦 PARTIE 12 — La page logistique commandes (orders-ops.html)

C'est une **page séparée réservée au personnel de la restauration**. Elle affiche toutes les commandes en temps réel sur un tableau de type Kanban (comme un tableau de post-its), visible par plusieurs téléphones ou tablettes en même temps.

### Les 4 colonnes du tableau

| Colonne | Qui l'utilise | Action |
|---------|--------------|--------|
| 📥 **Reçues** | Réception/cuisine | Voir les nouvelles commandes |
| 🍺 **En préparation** | Bar/cuisine | Préparer la boisson ou le plat |
| 🏃 **En livraison** | Livreur | Porter la commande au siège |
| ✅ **Encaissées** | Caisse | Confirmer le paiement et la livraison |

Chaque membre du personnel appuie sur le bouton fléché de la carte pour faire avancer la commande à l'étape suivante.

### Étape 1 — Activer Realtime dans Supabase (obligatoire une seule fois)

Pour que la page se synchronise entre plusieurs tablettes :

1. Ouvre [supabase.com](https://supabase.com) et connecte-toi
2. Clique sur ton projet
3. Dans le menu de gauche, cherche **Database** → **Replication**
4. Tu vois une liste de tables. Clique sur la table **`orders`** pour activer le suivi en temps réel
5. Sauvegarde

> Sans ça, chaque tablette devra être rechargée manuellement pour voir les nouvelles commandes.

### Étape 2 — Connecter la tablette à Supabase

1. Ouvre `orders-ops.html` dans le navigateur de la tablette ou du téléphone du bar
2. Clique sur le bouton **🔌 Connecter Supabase** en haut à droite
3. Une fenêtre s'ouvre — entre :
   - L'**URL Supabase** de ton projet (commence par `https://xxx.supabase.co`)
   - La **clé anon** (la clé publique — pas la clé service)
   - L'**ID du stade** (exactement le même que dans la console admin, ex : `stade-lyon-2025`)
4. Clique **Connecter**
5. Le bouton passe au vert — les commandes apparaissent

> ✅ Ces identifiants sont **mémorisés** automatiquement. La tablette du bar n'aura besoin de les entrer qu'une seule fois, même si on éteint et rallume le navigateur.

### Étape 3 — Utilisation pendant le match

- **Nouvelle commande ?** → Elle apparaît automatiquement dans la colonne 📥 Reçues avec un bip sonore
- **La commande est prête ?** → Appuie sur **« Préparer → »** (passe en colonne 🍺)
- **Le livreur part ?** → Appuie sur **« En livraison → »** (passe en colonne 🏃)
- **Livré et payé ?** → Appuie sur **« Encaisser ✓ »** (passe en colonne ✅)
- **Annuler une commande ?** → Le bouton ✕ rouge la retire du tableau

### Le filtre par tribune

En haut à gauche, un menu déroulant permet d'afficher **seulement les commandes d'une tribune ou d'un bloc**. Chaque tablette peut ainsi être configurée pour ne gérer qu'un secteur du stade.

### Les indicateurs visuels

- 🔴 **Bordure rouge** = commande en attente depuis plus de 5 minutes (urgence !)
- 🟡 **Pastille jaune** = la connexion Supabase Realtime tente de se reconnecter
- 🟢 **Pastille verte** = tout est connecté et synchronisé
- 💰 **Total des ventes** = affiché dans l'en-tête de la colonne ✅ Encaissées

### Le son

Le bouton 🔇/🔊 en haut active ou désactive le bip sonore à chaque nouvelle commande. Conseillé de l'activer sur la tablette de réception, désactivé sur les autres.

### Accès depuis la console admin

Dans `stadium-admin.html`, un lien **📦 Ops ↗** en haut à droite de la barre de navigation ouvre directement cette page.

---

## 📋 Résumé des fichiers

| Fichier | Rôle |
|---------|------|
| `index.html` | Console admin tribune + vue supporter |
| `admin.html` | Console simplifiée import photo/vidéo |
| `stadium-admin.html` | Console stade complet + panneau 🔴 Live + login admin |
| `orders-ops.html` | **Tableau logistique commandes** (bar, livreurs, caisse) |
| `supabase/schema.sql` | Script SQL à coller dans Supabase (une seule fois) |
| `tools/generate_seat_qr.py` | Générateur QR codes PNG avec labels imprimés |
| `GUIDE.md` | Ce guide |

---

## ❓ PARTIE 11 — Nouveaux problèmes fréquents (MVP2)

### « L'écran de connexion admin apparaît mais je n'ai pas de compte »
→ Clique sur « Continuer sans authentification » pour accéder à la démo. Pour créer un vrai compte, suis la Partie 9, Nouveauté 1.

### « Je vois mes commandes mais le statut ne se met pas à jour »
→ Ferme et réouvre le shop (bouton 🛒). Les statuts se rechargent à chaque ouverture.

### « L'écran de résultats n'apparaît pas après le vote »
→ Le téléphone doit avoir la page ouverte au moment où l'admin clique « Terminer ». Les résultats sont envoyés en temps réel via Supabase.

### « Je vois 'participant_id' vide dans la table orders »
→ Normal pour les commandes passées avant MVP2. Les nouvelles commandes l'incluront automatiquement.

### « La page orders-ops.html ne reçoit pas les commandes en temps réel »
→ Vérifie que tu as bien activé Realtime pour la table `orders` dans Supabase (Partie 12, Étape 1). Sans ça, les commandes n'arrivent pas automatiquement.

### « Les commandes n'affichent pas de tribune ni de bloc »
→ Les commandes passées avant cette mise à jour n'ont pas ces informations. Les nouvelles commandes en auront automatiquement si le supporter a scanné un QR code avec les paramètres `stand` et `block` dans l'URL.

### « Plusieurs tablettes au bar voient des informations différentes »
→ Vérifie que toutes les tablettes utilisent le **même ID de stade** lors de la connexion. Si une tablette a un ID différent, elle voit une autre base de données.

---

---

## 🎰 PARTIE 13 — Loterie et tirage au sort

### Comment ça marche ?
L'admin peut lancer un tirage au sort en direct. Tous les téléphones participants voient une animation de suspense, puis le siège gagnant est révélé.

### Étapes
1. Dans `stadium-admin.html`, clique sur **🔴 Live**
2. Va sur l'onglet **🎰 Tirage**
3. Remplis le prix à gagner (ex: "Maillot dédicacé")
4. Optionnel : filtre par bloc
5. Clique **🎰 Lancer le tirage au sort !**
6. Tous les écrans s'animent en rouge/or pendant le suspense
7. Le siège gagnant s'affiche : la personne voit "VOUS GAGNEZ !" en or

---

## 🔦 PARTIE 14 — Lampe de poche LED (Flashlight)

### Comment ça marche ?
L'admin peut allumer/éteindre la lampe LED des téléphones des supporters. Cela crée des effets de lumière impressionnants dans une salle sombre.

### ⚠️ Important
- Fonctionne sur **Android avec Chrome** (la plupart des téléphones)
- Sur iPhone (Safari), le navigateur peut demander la permission caméra
- Le spectateur doit **accepter la permission caméra** la première fois

### Étapes
1. Clique sur **🔴 Live** dans `stadium-admin.html`
2. Va sur l'onglet **🔦 Flash**
3. Choisis le mode : Continu / Stroboscope lent / Stroboscope rapide
4. Clique **🔦 Envoyer la commande flash**
5. Pour éteindre : clique **⬛ Éteindre toutes les lampes**

### Modes disponibles
| Mode | Description |
|------|-------------|
| Continu | Flash allumé en permanence (feu de bengale) |
| Stroboscope lent | Clignote 1×/seconde |
| Stroboscope rapide | Clignote 3×/seconde |
| Éteindre | Arrêt immédiat |

*CrowdLuma MVP1 + MVP2 + MVP4 — Open Source — Fait avec ❤️*
