INSERT INTO `grade_type` (`name`, `id`) VALUES 
(Large order cost figure crime help mother., 1),
(Hard carry participant laugh get pressure present., 2),
(Seek beyond together development police traditional., 3),
(People here music sport., 4),
(Stop difference baby current participant performance., 5),
(Computer kid evidence we cancer executive., 6),
(Environmental morning newspaper most environment stage hospital., 7),
(Former industry then sex night., 8),
(High begin condition best., 9),
(Garden structure put national four tree., 10)
;
INSERT INTO `ingredient` (`name`, `id`) VALUES 
(Just year sister wonder past media., 1),
(Big focus child herself by local., 2),
(Market attorney remember money indicate forget., 3),
(Local long talk force scientist., 4),
(Environmental partner ask than record., 5),
(True mind charge thousand network project., 6),
(Home effect bar ok one determine attorney., 7),
(Record public quite couple song concern., 8),
(White fine effect method knowledge., 9),
(Old woman explain somebody suddenly., 10)
;
INSERT INTO `recipe_type` (`name`, `id`) VALUES 
(Another across street sometimes eat her draw., 1),
(Environmental financial among worry., 2),
(Responsibility room involve ever., 3),
(Race west stay prove., 4),
(Congress whatever need dark early political choice top., 5),
(Able hotel particular this maintain theory ever., 6),
(Billion within between deal consumer food start., 7),
(Staff how state expect character., 8),
(Citizen finally size control off., 9),
(Important particular fill effect disease., 10)
;
INSERT INTO `material` (`name`, `id`) VALUES 
(Eight society and may activity ball outside., 1),
(Too onto arm., 2),
(Really attention machine., 3),
(Sometimes hair reach make., 4),
(Form tell may same dog six program item., 5),
(Wind machine interest perhaps fall., 6),
(Everything dark foreign., 7),
(Call market season within office., 8),
(Country poor hang write weight rise cultural., 9),
(See six start difficult wrong difference one., 10)
;
INSERT INTO `unit` (`name`, `id`, `symbol`) VALUES 
(Box run customer foot official., 1, Feel its situation trade family.),
(Ten ability play keep main gun., 2, East today beyond then clear seem.),
(Say popular well., 3, Lie art watch region.),
(Drop treat area meeting., 4, Phone American agreement knowledge seem.),
(Ahead it these clear more include board., 5, Staff be environment production country.),
(Assume style my threat., 6, Indicate show north.),
(Letter safe three dead common go., 7, Able sit time American.),
(Low consider art hit less true., 8, Institution evidence if.),
(All admit both method month., 9, Baby number father send.),
(Personal first line., 10, Outside small before speak hit determine.)
;
INSERT INTO `recipe` (`name`, `id`) VALUES 
(Seem Mrs left before represent prove add., 1),
(Pull accept sing level decide., 2),
(Clearly change ok again military prepare., 3),
(Even computer and area then feel., 4),
(Do again hang research seat enter lawyer., 5),
(Method gas main yard threat house course., 6),
(Mean owner hundred claim love use campaign., 7),
(Friend turn others place., 8),
(Hang since machine administration type our., 9),
(Air ground fine several visit., 10)
;
INSERT INTO `variant` (`main_variant`, `author`, `visible`, `comment`, `id`, `recipe_id`) VALUES 
(False, Six land leader military., False, Federal order have statement. End five next local within. Those score last when., 1, 5),
(False, Small maintain since husband whole., False, Do certainly plant beautiful. Window standard so indicate., 2, 4),
(True, So couple little list., False, Represent different treatment increase lot. Even animal choose similar soon reveal. Allow yourself heavy space late., 3, 6),
(False, Tough past thing old teach toward report product., True, Necessary relationship phone PM shake respond throughout. Military much not various imagine gas. Success rich sell market set defense. Science contain success actually sometimes., 4, 4),
(False, Star political religious administration because tonight front street., False, Determine identify son. Dead love citizen fund., 5, 2),
(False, Lie gun college put everyone today., False, Present too leg fight according Republican. Piece tonight color any five none., 6, 9),
(True, Bring trip American although., True, Bring organization decide class short dinner guy. Increase clear police author. Food together even simply., 7, 5),
(False, Station get former even., False, Way economy street after. Home evidence positive deep fact coach office., 8, 3),
(True, Major visit must employee., False, Nation bar trip use. Can right claim American. Interest exactly at last kill middle laugh., 9, 2),
(True, Society team six society real whose., True, Finish allow star form., 10, 1)
;
INSERT INTO `grade` (`value`, `unit_id`, `type_id`, `variant_id`, `id`, `comment`) VALUES 
(10, 3, 9, 10, 1, Bank edge art risk. Save fine three talk fire. Much perform life establish too research.),
(1, 1, 6, 6, 2, Anyone music building real else attention consumer. Leave least outside effect story experience young scientist.),
(3, 6, 6, 8, 3, These can reflect compare century almost activity general. How conference disease appear at.),
(9, 3, 1, 9, 4, Candidate quite far responsibility along. Yard imagine order us model ready according.),
(9, 1, 9, 2, 5, Violence firm statement result deal. Meeting value evidence theory thank.),
(4, 6, 6, 4, 6, Week art beautiful can after large current. Include safe ahead seat shake together. Understand member leave read upon.),
(8, 1, 3, 7, 7, Across agreement doctor up guess scientist true. Keep second enough.),
(5, 9, 10, 6, 8, Make rule sign process. Store drop lose that.),
(2, 7, 9, 3, 9, Amount month music describe pull already. Such her section more arm.),
(7, 10, 2, 6, 10, Piece operation oil market usually top. Five oh character some bed.)
;
INSERT INTO `variant_recipe_type` (`recipe_type_id`, `variant_id`) VALUES 
(10, 4),
(4, 3),
(3, 3),
(9, 10),
(2, 1),
(5, 5),
(9, 1),
(6, 3),
(2, 1),
(10, 10)
;
INSERT INTO `materialQuantity` (`variant_id`, `material_id`, `id`, `quantity`) VALUES 
(9, 9, 1, 10),
(8, 10, 2, 10),
(3, 5, 3, 3),
(10, 2, 4, 2),
(4, 5, 5, 1),
(2, 5, 6, 9),
(1, 9, 7, 9),
(9, 2, 8, 10),
(5, 4, 9, 1),
(1, 7, 10, 2)
;
INSERT INTO `step` (`variant_id`, `text`, `id`, `picture`) VALUES 
(6, Forget cup last., 1, Person now people animal language character class. Notice Congress fly gun Democrat art for.),
(6, Wall prepare rest themselves build any build recognize., 2, Go experience rather issue budget. Full through middle toward. Prepare today enter end.),
(9, To church difference capital daughter., 3, Adult heart go election increase upon executive. Safe perform become finally field scene.),
(10, Same pressure production every., 4, Day risk picture fast election education. Across history before report teach music professional.),
(1, Floor agreement nor service exactly foot less message., 5, Policy young wear yet administration. Including suddenly these meeting thing spend. Mean support analysis exactly legal including carry part.),
(4, Sexual standard detail spring job food as., 6, Analysis around leave marriage. Nearly foot and. Those health happy road scene piece few network. Figure I front tell American.),
(2, Quickly think alone have inside., 7, Both war hospital race idea child force all. To admit boy morning agreement stay fail according.),
(3, Compare time professional meeting drop., 8, Between capital reflect cancer finish. Cold wall night wear center herself peace. Car almost give expect cell song allow.),
(4, Enough more health why such laugh., 9, Goal set foot care fast boy its. Possible line attack some wonder individual. Control research cup vote marriage yourself sign disease. Apply or two private season.),
(2, Find teacher lot song total eye brother., 10, Campaign customer practice nature their. Computer bank trip since western must. Toward develop specific.)
;
INSERT INTO `ingredientQuantity` (`ingredient_id`, `unit_id`, `variant_id`, `id`, `quantity`) VALUES 
(4, 3, 3, 1, 8),
(7, 4, 10, 2, 3),
(6, 7, 2, 3, 8),
(8, 4, 7, 4, 8),
(1, 4, 4, 5, 7),
(5, 10, 1, 6, 8),
(4, 7, 5, 7, 2),
(10, 1, 1, 8, 10),
(7, 9, 3, 9, 10),
(3, 6, 6, 10, 9)
;
INSERT INTO `variant_material_quantity` (`material_quantity_id`, `variant_id`) VALUES 
(3, 2),
(7, 7),
(5, 7),
(10, 6),
(9, 5),
(1, 5),
(4, 4),
(8, 9),
(9, 1),
(4, 1)
;
INSERT INTO `variant_ingredient_quantity` (`variant_id`, `ingredient_quantity_id`) VALUES 
(1, 7),
(7, 6),
(10, 5),
(7, 7),
(10, 1),
(4, 2),
(3, 10),
(1, 8),
(10, 9),
(8, 4)
;
