<?php
class Demi-journee1 {
	function Cocktail-temp-reel-pour-l-olympia(sale2) {
		echo "cf nodejs et socket.io";
		echo "mix de rabittNQ, nodejs, symfony";
		echo "php genere un tokken, le stock en base, et l'envoie au front";
		echo "le front quand il appelle nodejs, node tcheck la base pour verifier si il existe";
		echo "";
		echo "si le temps reel crash passage sur des requettes ajax toutes les 5 sec";
		echo "crash informer (et remise en fonctionnement) via les socket";
	}
	
	function L-AB-Testing-chez-M6-Web(sale1) {
		echo "c'est juste du test par les utilisateur, test sur une petite partie de la population,";
		echo " 5% sur la variante 1, 5% sur la variante 2 etc";
		echo "";
		echo "cache varnish ... encore";
		echo "tu fais les test puis tu les balance a une platform hadoop pour avoir un retour et savoir les repercutions sur les visiteurs";
		echo "Tester c'est douter, mais le doute c'est le debut de la sagesse";
	}
	
	function Ecrire-des-tests-pour-le-long-terme(sale2) {
		echo "evanos - @selrahcD";
		echo "test : decouvrir des bugs, permettre de refactorer, documenter, reflechir a l'interface du systeme; detecter des problemes de design";
		echo "independant de l'implementation, decrire le comportement du systeme, avoir un resultat predictible, rapides, independant les uns des autres, simple a mettre en place";
		echo "";
		echo "techno : phpunit, profecy";
		echo "";
		echo "";
		/**
		 * @test
		 */ 
		public function il annonce le plat du jour()
		public function il_annonce_le_plat_du_jour()
		echo "toujours au present, pas deconditionnel (pas de should)";
		echo "";
		echo "arange -> act -> assert";
		echo "givne -> when -> done";
		echo "";
		echo "design patern";
		echo "builder";
		echo "factory";
		echo "";
	}
	
	function L-art-subtil-du-nomage(sale1) {
		echo "Julien Janvier de akeno";
		echo "declaratif plutot qu'imperatif";
		echo "natural voc plutot que dev voc";
		echo "look for perfection, tell the (hard) truth";
	}
}

class demi-journne2 {
	function Le-streaming-d-api(salle1) {
		$trac = <<<EOD
		audrey neuveu de saagie aneveu/WebHookDemo
		
		Polling, webhook, websub, websock, server-send event
		depend de la frequence 
		et usage (donnee qui arrive ou genere workflow)
		
		Polling : je fais une requete, j ai une reponse
		Webhook: user define http callback, AMQP broker (comme rabbitNQ) (preque temps reel, 5 sec de latence)
			+ without dedicated ressource
			+ easilr consumed
			+ easilr integrated
		
			- poor user experience
			- debugging
			- does not work wiyh all client
			- manual setup
			- public ressource -> ddos
			- miss missed norification
			- deduplication
		EOD;
		$truc = <<<EOD
		matthiasnehisen.com
		WEBSUB
			open protocol
			W3C recomand
			based on publich/ subscripbe pattern and on topic
			git : pubsubhubhub

			sur facebook demande d'aller recuperer la donnée plutot que de l'envoyer en payload

			pour et contre
				- un apperl en plus
				- plus de ddos

			Webhook bien pour event mais pas pour donnee

			----- websocket and server-send event -----
			
			websocket = bidir, text et binaire
			server-send event = server to client, que text

			websocket -> reconf proxy
			SSE -> HTTP, mais session potentiellement indefini

			websocket -> pas de format, free style(
			SSE -> text avec prefix data: avant

			json-patch ?
		EOD
	}

	function climbing-the-abstract-synthax-tree() {
		$truc = <<<EOD
			james Titcumb


		EOD;
	}
	
	function Developper-plus-rapidement-avec-Symfony4
	
	function c-est-quoi-la-etre-different-en-IT(sale1) {

	}

	function ligthing-talks(sale1) {

	}
}