http://www.jlg-consulting.com/orsys/IHM/support/

institut 4.10 -> symfony full stack
meval.orsys.org

Context:

  l affordance : est-ce qu il y a besoind une doc

  Ergonomie :
  – Discipline scientifique
  – Etude des IHM
  – Améliorations de 3 axes :
    • Confort
    • Efficience
    • Sécurité

  lergonomie se resume a: 
  1. Test  utilisateur (TU) : Observer un utilisateur entrain d’utiliser le produit logiciel et déduire ce qui peut être amélioré.
  2. Le prototypage  (PR) : Portail, appli, processus, wireframe, storyboard, habillage, prototype.
  3. Audit ergonomique  (AE) : Respect des critères d’«utilisabilité»
  4. Modéliser l’utilisateur (MU) : Qui, objectifs, volonté, scénario...

  ergonomie normer: ISO-9241-210 (semble etre le livre de donald normal retranscrit)
  ergonomie necessite de VOIR FAIRE l utilisateur

  différente méméoire
    pas d effort pour celle ci dessous:
      memoire episodique: tout ce qui c est passe
      memoire procedural: ecrire, marcher, ...
      memoire sementique: memoire des sens, immatériel, par coeur,
      memoire sptiale: se mouvoir dans l espace
    la petite (beaucoup plus complique, regarde un mur, retourne toi et decirt le):
      de travail:
      iconique
      auditive

  eviter autant que possible que l utilisateur utilise la petit memoire (exemple numero de telephone, mettre un lien pour numeroter)
  => saturation de la MCT (memoire courte de travail) => humour, deviation, delegation, colere, abandon

  (fr) ergonomie : (en) usability

  pour faire un logiciel, on isole le procesus nominal et 100% de la page est consacré a ca

Test  utilisateur

  user testing: +/- 10
  deroulement du test:
    intro: 5 min
    pres de l utilisateur: 2 min (
      nom, 
      prenom, 
      niveau intellectuelle/d etude,
      niveau d utilisation informatique
    )
    balade dans la page d accueil (3 min)
    donner des objectifs (35 min)
    conclusion (5 min)
      montrer ce qu il n a pas reussi a faire et observer ses reactions
    sus (5 min)
    debriefing 
      lister 3 points les plus prioritaires
      les cités 1 par personne (si deja dit passé au 2 e)

  message de bienvenue: slide 64
    1. Mettre a l aise avec du sourire et des croissants
    2. Faire signer une demande de cession de droit a l image (doc jurique)
    3. L utilisateur a le droit de se tromper, donc ne pas stresser
    4. L utilisateur doit etre le plus bavard possible
    5. L utilisateur n a pas le droit d etre aider, donc le facilitateur ne peut repondre aux question
      - Il y repondra apres le test en meme temps que l utilisateur laissera ses impressions

  sus: slide 65
    1. je pense que j utiliserai ce systeme frequemment
    2. J ai trouve ce systeme inutilement complexe
    3. Je pense que ce systeme est facile a utiliser
    4. Je pense que j aurai besoin de l aide d une personne technique pour etre capable d utiliser ce systeme
    5. J ai trouve que l ensemble des fonctions de ce systeme etaient bien combinees
    6. J ai pense qu il y avait trop d incoherence dans ce systeme
    7. J imagine que la plupart des gens vont apprendre tres rapidemment a utiliser ce systeme
    8. J ai trouver ce systeme tres lourd a utiliser
    9. Je me suis senti en confiance en utilisant ce systeme
    10. J ai eu besoin d apprendre beaucoup de choses avant de pouvoir utiliser ce systeme

    note entre 1 et 5 pour chaque question
      1 pas du tout d accord
      5 parfaitement d acccord

      (score 68 needed)
      pour les question impaire score-1
      question paire 5-score
      somme des scores*2.5 pour mettre sur 100

Protorypage:
  1 appli = 1 objectif utilisateur = 1 processus nominal
  sinon un portail
  attention a bien distingué processus nominal, processus correcteur et processus secondaire

  commencer par un proto avec un processus numinal
  et ensuite l enrichir avec les pro cor et sec sans abimé le pro nom

  UX:
    1. process nominal
      "il doit n en rester qu un"
      5 etape max
      5 sous etape max 
    2. storyboard wireframe papier
      tester avec un user, test de perception
      on explique rien, on voit si il le comprend
      2 question autorisees
        - qu est ce que tu vois ?
        - t as envie de cliquer ou ?
      - essayer d etre le plus fidele a ce que ca va etre plus tard, rediger la phrase au complet
        mettre des données fausses mais realiste 
    3. mise au propre: wireframe informatique
  UI:
    4. storyboard avec graphisme:
      couleur, charte graphic, ...
    5. prototype:
      quelque chose de fonctionnel, de testable, avec DB
  pour chaque phase, un retour utilisateur

  interview du metier:
    vous etes qui
    vous faites quoi
    pour l instant vous faites comment
    est ce que la procedur c est deja mal passe
  trouver le processus nominal
  trouver un nom, une phrase d accroche
  decomposer le processus nominal

audit_ergonomique:
  soit don, soit methode
  checklist (la plus connu les criteres ergonomique de Bastien Scapin 1993)
  cocoaheads.fr/wp-content/uploads/file/Erognomic_Criteria
    1. Guidage:
              ou suis-je (signe distinctif: logo = site id, fil d ariane)
              ne me laisse pas tomber en erreur (restricteur: completion auto, caracteres filtrees, ...)
              layout type: site ID, tagline, utilitaire, navigation primaire
              en 2018 on prefere avoir des boutons, meme pour entrer un chiffre, on met 1, 2, 5 bouton plutot qu un input number
        1. Incitation
        2. Groupement
            1. Distinction par la localisation
            2. Distinction par la forme
        3. Feedback immediat
        4. Lisibilité
              espacement (eviter le justifier), contraste, taille
    2. Charge de travail
        1. brievete
            1. Concision
            2. Action minimal
        2. Densite d information
    3. Controle explicite
        1. Action explicite
        2. controle utilisateur
    4. Adaptabilite
        1. Flexibilite
              triangle: objectif, utilisateur context
              pas de moyenne, prevoir les uns les autres pas la moyenne des 2
        2. Adaptation a l experience utilisateur (pas UX mais son passe)
    5. Gestion des erreurs
        1. Protection contre les erreurs
        2. Qualité des messages d erreurs
        3. Corrections des erreurs
    6. Homogeneite Coherence
    7. Signifiance et Denominations
    8. Compatibilite

  bouton de recherche de trainline
  s assurer que lors du clique sur bouton, le disable pour eviter le spam click
  ne jamais donner d order ou blamer l utilisateur

modelisation utilisateur:
  # /!\ livrer des personnae (profil d utilisateur) a chacun
  personae:
    1. Sa personne: Qui est-il
    2. Son objectif: Que cherche t il a faire, 
    3. Ses outils: Que doit-on mettre en place pour lui permettre de faire ce qu il souhaite ?
    4. Sa volonte: faut il l inviter a faire quelque chose, Comment le convaincre
    5. KPI: Quels objectif doit on remplir a chaque etape de parcours client, Comment mesurer ces objectifs

  le scenario nominal de l utilisateur

  exemple de personae: (slide 138)
    Christina Moletti
    Freelance Graphic Designer

    "Living life is a creative proccess too"
    - Have enough money but not much

resource:
  auteur:
    en:
      Suzan Weinschenk
      donald normal
      don t make me think de Steve Krug (++ test d usabilité)      
    fr:
      amelie boucher
      nogier jean-francois
  ecole:
    nngroup.com (articles, repport)
    les goblins
  document:
    roue des emotions de Robert Plutchik (1927-2006)
    critere ergonomique de bastin - scapin
  extension:
    wappalizer: (identify les lib)
  site:
    jlg-consulting.com/private/xxx/ergonomie/
    pixabay : photo libre de droit
    a voir: dock.io
    rail https://developers.google.com/web/fundamentals/performance/rail
    opacity et transformation sont les 2 seuls animation qui appel le GPU
