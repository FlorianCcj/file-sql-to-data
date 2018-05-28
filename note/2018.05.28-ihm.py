http://www.jlg-consulting.com/orsys/IHM/support/

institut 4.10 -> symfony full stack
meval.orsys.org


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

Ex:
  nop - le sign in est pas correctement contraster
  pas la page mot de pass oubliee
  pas de bouton sign up
  un peu perdu,
  l identification de l utilisateur est trop gros, trop en avant
  c est une liste, et select a unit ... pas coherent
  plus visuel, une image de l unité, quelques chose de plus specifique
  recommandation du dernier navigateur, inutil, detection a faire
  selection pas intuitive, le ok non plus, scroller pour y acceder
  non de la plateform plus visible, un peu perdu
  les icones sont un peu petit
  manqie le alt (legende sur les boutons)
  profil utilisateur avoir plus d information (les unités aussi)
  preference, si peu, pas besoin d une page
  le logo en haut a droite pour revenir a la page d accueil

  selection de l unite puis ok -> bouton vert bizarre
  page de graph
  le bouton pour reduire le menu pas intuitif,
  retour ariere graph non plus
  menu de gauche, un peu surchargé
    pas avatar mais l entite ca serait cool
  changer l echelle de temps directement sur le dashboard
  pas l echelle sur le graph 
  parcours de graph, translation pas tres comprehensible
  pouvoir zoomer sur le graph
  un indicateur auto calculer 
  si probleme avoir un lien direct sur le detail
  pas la meme couleur dashboard
  pouvoir tapper la date directement
  les gros bouton pour l echelle, est pas clair
  un click pour poser un marqueur

  dashboard2  un peu trop permi de conduire
  les graph legende pas intuitive
  1 - la navbar pas clair  
  2 - les legendes sur les graph
  3 - le marqueur
  

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