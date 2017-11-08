class demi_journee_1 {
	Automatic_progressiv_Webs_App() {
		Maxim Salnikov
		NGSW (ne sert que pour la prod)
		slack : http://bit.ly/go-pwa-slack
		ng new pouet --service-worker
		ng build --prod



		npm i @angular/service-worker
	}
	Breaking_the_eyes() {
		ARIA : accessible rich internet accessibility
		Tools ;
			Chrome Vox,
			ChromeLens : permet de simuler different probleme de vue
			aXe

		d autre outil permette de mesurer le contraste

		ajouter 'filter: blur(9px)' pour simuler les malvoyant

		penser a mettre les tabindex=1 permettant
		<span (click)="upvote()" class="vote-icon up"></span> 
		<span (click)="upvote()" class="vote-icon" tabindex=0 role="button" aria-label="Up vote" (keydown)="voteKeyDonw($event,1)"></span> 
		<span aria-live="polite">{{votes}}</span>

		<h2 ></h2>

		[attr.aria-label]="some expression"

		voteKeyDown(ev: KeyboardEvent, vote: number) {

		}
	}
	Web_application_security() {
		Dominique Kundel
		twillio : authentification par voix/sms/autre

		autre

		- HttpOnly coocky
		- safe jwt implementation
		- use noopener
		- csrf tokens
		bit.ly/oniesie-life
		bit.ly/sec-angularconnect
	}
	Workshop() {
		
	}
	angular_animation_movie() {
		yearofmoo.com
	}

	Service worker
	server side rendering
	aot compilation
	
}