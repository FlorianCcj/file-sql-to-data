INSERT INTO `recipe_type` (`id`, `name`) VALUES 
(1, Officiis voluptates doloremque.),
(2, Quae voluptates labore cumque ipsam.),
(3, Sequi voluptates deleniti nesciunt aliquid mollitia temporibus rem.),
(4, Nobis labore consequuntur harum.),
(5, Cum ipsum unde fugit.),
(6, Laborum voluptate ipsum.),
(7, Ipsa earum quibusdam amet molestias laborum.),
(8, Repudiandae incidunt in vel fuga perspiciatis.),
(9, Expedita enim excepturi.),
(10, Aut ea fugiat unde recusandae necessitatibus facilis beatae.)
;
INSERT INTO `recipe` (`id`, `name`) VALUES 
(1, Doloremque sed dolorum asperiores fugiat.),
(2, Rem molestias ab.),
(3, Minus a unde tempora.),
(4, Dolorem rem consequatur id laboriosam quisquam.),
(5, Ea laboriosam veniam.),
(6, Reprehenderit expedita sit.),
(7, Illo fugit atque autem pariatur quidem ratione sit.),
(8, Ad adipisci alias dicta sapiente dolores.),
(9, Assumenda reiciendis deserunt fugiat quae amet.),
(10, Quibusdam odio inventore quasi necessitatibus.)
;
INSERT INTO `grade_type` (`id`, `name`) VALUES 
(1, Deserunt laudantium minima velit non provident earum provident.),
(2, Nemo fugiat modi optio corporis.),
(3, Quisquam excepturi blanditiis animi asperiores.),
(4, Illo cumque eaque sequi.),
(5, Inventore illo iste magnam cumque tempora.),
(6, Voluptatum blanditiis iusto ducimus natus.),
(7, Ratione iure reiciendis voluptatum dignissimos.),
(8, Consectetur laudantium expedita nihil.),
(9, Inventore aperiam quam libero suscipit excepturi.),
(10, Ex eligendi enim fugit.)
;
INSERT INTO `material` (`id`, `name`) VALUES 
(1, Nisi adipisci nobis maiores.),
(2, Sit porro eaque quo.),
(3, Iusto perferendis iure ut.),
(4, Quaerat minus velit dolorum.),
(5, Culpa eum ipsum quaerat a ipsam iusto.),
(6, Sequi facere ad maxime nulla.),
(7, Minus tempora illum ipsa voluptates nemo.),
(8, Quod quidem quasi modi labore similique.),
(9, Sunt temporibus porro sequi consequatur.),
(10, Ipsam in dicta voluptatum labore nobis ratione.)
;
INSERT INTO `variant` (`comment`, `main_variant`, `author`, `visible`, `recipe_id`, `id`) VALUES 
(Facere provident a aspernatur nesciunt. Hic nihil mollitia sunt eos numquam. Nulla nostrum aliquid dolor similique. Esse porro labore tenetur., False, Voluptatibus facere mollitia nihil assumenda quae., True, None, 1),
(Modi modi illo. Nam alias ducimus illum repudiandae. Hic facere veritatis similique amet sed pariatur saepe. Esse eaque atque illum laboriosam., True, Perferendis architecto sunt a., False, None, 2),
(Doloribus nisi numquam nemo. Sit consequuntur nobis sequi expedita error praesentium., True, Suscipit quasi natus sunt., True, None, 3),
(Cum voluptatum tenetur minus ab praesentium ipsa autem. Nemo saepe necessitatibus quibusdam. Perferendis sed dolores cupiditate rem soluta facere., True, Recusandae dignissimos asperiores excepturi sequi iste., True, None, 4),
(Debitis alias adipisci cum unde occaecati. Veniam quidem error minus. Nemo veniam dolores ipsam maxime. Inventore qui ab officiis explicabo consequuntur., True, Corporis delectus eveniet magni hic quod., False, None, 5),
(Non voluptates totam rem., True, Iusto ab maxime ipsa hic totam., True, None, 6),
(Omnis explicabo maxime amet nihil pariatur tempora. Iure iusto ab saepe eos ipsam., False, Atque unde dicta doloremque praesentium blanditiis quis., True, None, 7),
(Nam veniam pariatur facilis., True, Aliquid ut fuga quasi fugiat cupiditate dolor enim., False, None, 8),
(Dolore nesciunt architecto porro quo odit quis., False, Placeat atque distinctio voluptate reiciendis commodi necessitatibus., True, None, 9),
(Aliquid optio eaque alias molestiae fugiat., False, Error labore mollitia quisquam., True, None, 10)
;
INSERT INTO `unit` (`symbol`, `id`, `name`) VALUES 
(Quia illum laboriosam consequatur quidem facilis., 1, Eaque aut incidunt maiores expedita minima.),
(Veniam id tenetur nemo odio dolorem., 2, Placeat repellendus repellendus quos ab vel.),
(Vero vitae autem assumenda eligendi eius aperiam commodi., 3, Fugiat beatae aliquid dicta.),
(Molestias ut perspiciatis veritatis corrupti aut at., 4, Dolor at ratione neque earum quasi commodi.),
(Impedit vel iure molestiae., 5, Nostrum vero neque excepturi architecto nihil.),
(Nostrum dolorem doloribus aliquid dolore tempora., 6, Sit libero consequuntur minima.),
(Nobis voluptate nesciunt maiores consequuntur nesciunt iure., 7, Nostrum occaecati cupiditate laborum nesciunt natus ab.),
(In quis ipsum mollitia molestias., 8, Minus itaque voluptate vel.),
(Nihil temporibus enim quisquam consequuntur sed., 9, Recusandae cupiditate vitae placeat ea sequi.),
(Repellat atque vel., 10, Dicta cumque nulla iste.)
;
INSERT INTO `variant_recipe_type` (`recipe_type_id`, `variant_id`) VALUES 
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None)
;
INSERT INTO `ingredient` (`id`, `name`) VALUES 
(1, Sit in laudantium magnam nemo perspiciatis officia rem.),
(2, Beatae quia mollitia adipisci fugit quam.),
(3, Soluta saepe reprehenderit doloremque debitis.),
(4, Temporibus ad asperiores quisquam sit.),
(5, Eaque nihil occaecati deleniti pariatur esse quam.),
(6, Placeat cupiditate assumenda eligendi.),
(7, Ex ratione sunt assumenda totam nostrum consequuntur.),
(8, Delectus reiciendis alias harum modi esse facilis.),
(9, In quisquam molestias consectetur eos id temporibus fuga.),
(10, Commodi esse ratione soluta aspernatur.)
;
INSERT INTO `grade` (`comment`, `type_id`, `unit_id`, `value`, `variant_id`, `id`) VALUES 
(Impedit est officiis accusamus cupiditate nostrum blanditiis atque. Explicabo odio expedita natus iusto quisquam. Quasi repellendus impedit., None, None, 1, None, 1),
(Corrupti eum dicta aspernatur corrupti soluta. Aperiam vitae quo temporibus nihil. Quae voluptatum qui quasi quod., None, None, 6, None, 2),
(Neque officiis in accusamus. Voluptatibus odio error explicabo. Voluptates repellat magni., None, None, 6, None, 3),
(Laborum asperiores qui minima vel. Tenetur exercitationem sunt molestiae voluptas sapiente. Expedita qui iure consectetur laudantium nam nihil., None, None, 7, None, 4),
(Quia aliquid fugiat consequatur. Labore beatae veritatis quibusdam quaerat ut., None, None, 8, None, 5),
(Officiis quae deleniti alias eos est dolorum veritatis. Nostrum excepturi nisi quaerat aspernatur dolorem architecto accusantium. Doloremque praesentium nihil earum., None, None, 8, None, 6),
(Est in esse. Ipsam et totam esse molestiae autem aspernatur., None, None, 3, None, 7),
(Architecto minus voluptatum ratione tempore., None, None, 3, None, 8),
(Ea autem quos quasi animi veniam molestias. Incidunt corrupti ipsa omnis non. Inventore est molestias deleniti., None, None, 3, None, 9),
(Sit nulla quod necessitatibus totam. Corporis minus error nam doloremque., None, None, 4, None, 10)
;
INSERT INTO `ingredientQuantity` (`unit_id`, `ingredient_id`, `quantity`, `id`, `variant_id`) VALUES 
(None, None, 8, 1, None),
(None, None, 10, 2, None),
(None, None, 7, 3, None),
(None, None, 9, 4, None),
(None, None, 1, 5, None),
(None, None, 1, 6, None),
(None, None, 3, 7, None),
(None, None, 10, 8, None),
(None, None, 4, 9, None),
(None, None, 8, 10, None)
;
INSERT INTO `step` (`text`, `picture`, `id`, `variant_id`) VALUES 
(Quis dolores sequi maiores., Sint deserunt earum nam repellat delectus. A veritatis odit nihil quas., 1, None),
(Velit mollitia praesentium odio eum., Ex veniam esse atque. Laudantium reiciendis aspernatur alias. Minus magnam velit ipsa impedit quo. Hic a consequuntur error eius nihil., 2, None),
(Esse incidunt necessitatibus quod similique., Quis nam molestias aspernatur occaecati sunt minima. Fugiat assumenda laborum quam veritatis sunt. Sint corrupti enim consequuntur., 3, None),
(Maxime magnam neque sit., Enim magnam delectus ratione nobis., 4, None),
(Dolorum delectus temporibus esse., Nisi ullam provident laboriosam dicta repellendus autem. Laudantium aliquid facere doloribus omnis cumque sequi. Mollitia ullam in dolorum possimus deleniti., 5, None),
(Eaque vitae voluptatum architecto facilis pariatur doloremque., Repellendus a a quae delectus. Officiis officiis impedit ullam odio molestias nemo recusandae. Occaecati maxime sequi amet quaerat nobis., 6, None),
(Vitae praesentium illo sit iure fuga., Impedit odio hic ab. Distinctio harum officia et labore fugit., 7, None),
(Provident in dicta voluptatibus in error., Perspiciatis corrupti aut error. Itaque similique esse vel. Ab quos consectetur. Vero quos quidem pariatur., 8, None),
(Ad voluptate omnis quia assumenda., Nisi laudantium possimus., 9, None),
(Itaque consequuntur placeat eius in similique corrupti., Dolorum aliquam blanditiis libero iure. Voluptate magni dolorem maxime. Illo praesentium mollitia vel ea., 10, None)
;
INSERT INTO `materialQuantity` (`quantity`, `id`, `material_id`, `variant_id`) VALUES 
(2, 1, None, None),
(5, 2, None, None),
(4, 3, None, None),
(3, 4, None, None),
(10, 5, None, None),
(6, 6, None, None),
(8, 7, None, None),
(2, 8, None, None),
(8, 9, None, None),
(10, 10, None, None)
;
INSERT INTO `variant_ingredient_quantity` (`ingredient_quantity_id`, `variant_id`) VALUES 
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None)
;
INSERT INTO `variant_material_quantity` (`material_quantity_id`, `variant_id`) VALUES 
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None)
;
