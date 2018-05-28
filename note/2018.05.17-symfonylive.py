2018.05.17:
  demi-journee1:
    php7:
      live.symfony.com
      blog.jpauli.tech
      nikic.github.io
      php depuis 95
      870 k ligne en C

      sf:
        98 packet independant

      laziness => moins on en fait mieux on se porte, on recommence a 0
      spl_autoload_cell ? (15-20% de load des class)
      userland ?

      php execute
      index.php -> AST(translate php) -> compilition (give opcode) => execute (give result)
      3 firsts state => opcache

      dead-code elimination
      if (false) {} => remove

      autoload garbage collector each 10 k object

      A ?? B vs isset(A)
      https://blog.blackfire.io
      joind.in/23110

      websocket:
        pusher (si possible)
        node
        go (a privilégier)
    
    deezer-cli-php:
      scritp
        nommer les arguemnts
        output
          php://stderr
          php://output
        not auto (in log spec carac)
          use color
          use highlighr
        add help
        faire une console qui en fonction des arguments lance le script demander

      php script.py 1> std.log

      quand on envoit un fichier, balancer un sha1 pour verifier l etat du fichier 

    Bienvenue-dans-la-matrice:
      benoit jaquemont

      outil:
        strace: snif noyaux (the syscalls sniffer)
          strace <my program>
          strace -p <PID>
          man man
          man 2 execve
          strace -e write # afficher que la command write
          reset
          php blabla.php > /dev/null #hide output
          php blabla.php 2>&1 /dev/null #return
          strace -T -p 1132
          strace -e read,write, connect php script.php
        lsof: 
          list tout les fichiers ouvers
          lsof -p PID
        ltrace:
          trace les lib
          ltrace -e getenv php script.php
          strace -e sslread -e sslwrite php script.php
          vi ~/.ltrace.conf
            int SSL_write(void*, string, int);
            int SSL_read(void*, +string, int);

        gbd: the universal debugger
        perf: lightwieght performance profilling

        pour docker: capabilities attach
      joind.in/talk/b4405
    
    e-learning-sans-internet:
      societe elao - appli chalboard education
      techno sf -react; redux, service worker, graphQl
      PWA:
        rapide
        respo
        secu
        installable
        offline
        pas de store d appli necessaire
      SF : overblog/GraphQLBundle
      stokage in navigateur:
        localstorage text 2,5 Mo
        cachestorage ressource 50 Mo

      service worker:
        install as proxy, intercep all call, check cacheStorage

      to offline:
        online:
          login
          getcourse -> localstorage
          getResource -> cachestorage
        spool of download: 
          take part by part: [metatdata]
            -> loop session [course content] 
            -> then loop [resource]
        to validate:
          front -> sms provider -> webhook -> back -> sms provider -> validate
      display on index:
        web app manifest -> standard to create json
      https://blog.elao.com
  demi-journee2:
    morpheus-async:
      Joel Wurtz
    
    Jarvis-serialias:
      Kevin Dunglas

      voir OWASP (Open Web Appliaction Security Project)

    Jarvis-CQRS:
      Arnaud Lemaire
      twiter: lilobase

      

    Jarvis-Ethique-et-macaron:
      Laurent Chemla

    Lighting-talks
2018.05.18:
  demi-journee3:
    Jarvis-graphql-vs-rest:
      Kevin Dunglas

      schema gen component
      https://schema.org

      on peut copier le dossier docker dans n importe quel projet symfony 

      composer create-project symfony/squeleton
      composer req api

      json-ld/hydra

    Jarvis-dns:
      Julien Poli
      bind: DNS server
      dig: debuger

      zytrax.com -> dns: doc de bind

      mdc ???
      youtube/watch?v=oN7ripK5uGM

    Jarvis-evenement-in-linear('11h25-12h05'):
      Julien Vinder

    jarvis-traduire-efficacement-une-appli-sf('12h10-12h30'):
      Mathieu Santostefano

      .po .mo (gettext) en train de mourir
      .xlf (XLIFF) monter en puissance

  demi-journee4:
    Morpheus-decrypter-votre-contrat-de-travail:
      Helene Schapira

      contrainte de forme : tout fr ... full stack et ux designer, demerder vous
      de continue: pas de discrimination ni contrainte de celibat

      le code du travail s applique a tous sauf au secteur public

      http://www.legifrance.gouv.fr
      http://www.travail-emploi.gouv.fr
      http://www.service-public.fr

      beaucoup de texte ... interdependants ... et contradictoires

      syntec ???
      1er mai au 31 octobre
      si l employeur force a fractioner (pas de 4 semeine durant periode estivale )=> jour de fractionnement

      DUE: decision unilateral de l employeur
      PEBKAC

      direct => inspection du travail

    morpheus-merci-de-laissez-votre-code-dans-letat-dans-lequel-vous-aimeriez-le-trouver:
      Cedric spalvierie
      http://skwi

      Always code as if the guy who ends up maintaining your code will be a violent 
      psycopath who knows where you live
      John Woods

      2 com:
      - la com entre devs
        - ecrire du code humain: "any fools can write code that cumputer can understand. Good programmers"
        "write code that humans can understant" Martin Fowler
        - documenter (readme, documentation vivante)
        - faire de la reuve (pair programming, mobprogramming, revue)
      - la com avec le reste
        - feedback loop
        - sorry we re open (la porte est toujours ouverte)
          - ce n est pas a l equipe de detecter les problemes 
        - 1 on 1 (entretien individuel avec les gens de l equipe)

      Head First Design Pattern O reil
      documentation vivante
        -auto invalide (test)
        -auto generee
          - pickles (prend des scenarion gerkins et va generee une doc)
        - historique
          - message de commit 
          - penser au context 
          - expliquer pourquoi 
          - peut etremultilign

      certain dise que la revue de code > test et audit de secu

      Talents remporte des points mais c est le travail d equipe et la cohesion qui remporte des matchs
      Mickel Jordan

      une revue de code de 10 lignes on va y passer 1 heure 
      une revue de code avec 100 lignes on va y passer 2 minutes

    Jarvis-GraphQl:
        

    Jarvis-Jouons:
