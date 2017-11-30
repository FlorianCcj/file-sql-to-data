INSERT INTO recipe_type (test, id, name) VALUES 
(B-, 1, Donna)
(A+, 2, Marvin)
(A-, 3, Lindsey)
(O+, 4, Stacy)
(O-, 5, Levi)
(AB+, 6, Natalie)
(AB-, 7, Kevin)
(B+, 8, Jonathan)
(AB-, 9, Anne)
(A-, 10, Jessica)
;

INSERT INTO grade (comment, type_id, unit_id, value, variant_id, id) VALUES 
(Labore dolores repellat. Eos ducimus earum tenetur non soluta. Magni nisi illo sapiente officia commodi aliquid., 8, 7, 4, 5, 1)
(Voluptatibus hic dignissimos. Suscipit atque animi nostrum. Incidunt vel delectus at illo., 8, 5, 1, 8, 2)
(Voluptates vero iste maiores ipsum similique molestias. Nam debitis officiis impedit recusandae. Iure fugiat atque eveniet eum modi quia., 3, 2, 9, 2, 3)
(Architecto nostrum consequuntur animi quidem ea., 3, 8, 9, 10, 4)
(Quia incidunt veritatis consequatur nesciunt accusantium., 7, 4, 8, 4, 5)
(Magnam sunt unde aspernatur. A a temporibus sequi. Aliquid corrupti officiis necessitatibus dolores error commodi., 4, 6, 8, 7, 6)
(Voluptatum corrupti tempore provident voluptatum. Molestias maxime dolore veniam cumque modi illo., 6, 3, 3, 5, 7)
(Incidunt accusantium mollitia itaque fugiat accusantium. Aperiam commodi eos eius ducimus., 1, 1, 1, 3, 8)
(Tempora nulla eum quas illo mollitia voluptate mollitia. Ea pariatur saepe. Iure dolorem consequuntur nam doloribus., 9, 9, 6, 9, 9)
(Porro fugiat perferendis possimus totam enim. Quaerat possimus quae occaecati. Nesciunt quibusdam dolorem ullam perferendis laborum totam architecto., None, None, 1, None, 10)
;

INSERT INTO recipe (id, name) VALUES 
(1, Terrence Parks)
(2, Sharon White)
(3, David Rodriguez)
(4, Robert Page)
(5, Anne Wall)
(6, Michael Estrada)
(7, Michael Reyes)
(8, Karen Martin)
(9, Misty Bowers)
(10, Manuel Baker)
;

INSERT INTO grade_type (id, name) VALUES 
(1, Tenetur quos laborum neque incidunt commodi voluptates.)
(2, Cum culpa distinctio voluptate molestiae unde.)
(3, Suscipit deserunt quos illo nisi rem sint.)
(4, Dolorum nostrum ea et.)
(5, Consequuntur quas doloribus autem.)
(6, Expedita delectus perspiciatis ab.)
(7, Nam rem quaerat vitae ad.)
(8, Voluptate aperiam mollitia laborum quaerat tempora eaque tempore.)
(9, Architecto consequatur ad ipsa porro sapiente.)
(10, Sequi non atque harum id.)
;

INSERT INTO material (id, name) VALUES 
(1, Quibusdam vitae minima nemo commodi saepe.)
(2, Nisi cumque vel quod ea accusamus qui.)
(3, Exercitationem quia similique.)
(4, Dolor enim laudantium exercitationem modi voluptate quibusdam.)
(5, Aspernatur quod fugit facere minima veniam expedita.)
(6, Voluptas totam non non odit mollitia.)
(7, Ipsam repellat cupiditate repudiandae suscipit deserunt numquam.)
(8, Qui repudiandae voluptatibus recusandae.)
(9, Omnis magnam doloribus repudiandae eveniet ut quos.)
(10, Excepturi dolorem cumque inventore quidem delectus hic.)
;

INSERT INTO variant (comment, main_variant, author, visible, recipe_id, id) VALUES 
(Architecto quo quaerat hic. Occaecati et amet non. Ipsam ipsa totam vero corrupti., False, Animi nihil qui sapiente consectetur vero laboriosam., True, 2, 1)
(Quam delectus facilis cumque architecto laudantium magni delectus. Nulla ratione tempora exercitationem quisquam repellendus labore., False, Explicabo vel at voluptatum alias., True, 4, 2)
(Nesciunt alias eos quos tempore vitae autem. Maiores et asperiores ex officia est. Exercitationem reiciendis facere ex reprehenderit molestias minus., True, Iste voluptatem tenetur nesciunt molestiae asperiores neque., False, 8, 3)
(Perferendis dolorum eum qui provident at. Ad voluptatibus autem minima numquam praesentium. Aliquid eveniet labore sit reprehenderit. Consequatur enim assumenda minus voluptatibus sed., False, Sunt labore ex voluptatem., True, 7, 4)
(Incidunt repudiandae reprehenderit neque excepturi. Amet consequatur reprehenderit itaque fugit., True, Quaerat illo voluptas., True, 8, 5)
(Temporibus maxime nulla possimus fugiat quo. Occaecati suscipit soluta dicta in quia. Praesentium cumque ea asperiores. Eveniet tempore quod non fugit molestias., False, Ad unde atque cum iste., False, 1, 6)
(Soluta pariatur debitis rerum cumque reiciendis maiores natus. Aspernatur atque sunt neque quod sunt recusandae., False, Blanditiis quod labore impedit nisi commodi consectetur., False, 2, 7)
(Ad itaque beatae numquam. Nihil voluptatum officiis est. Maxime debitis repellat., False, Doloremque qui vero tempora earum., False, 1, 8)
(Dicta provident atque nesciunt omnis. Dolor at sunt aliquam nisi. Commodi velit quisquam., True, Voluptatum architecto ducimus voluptas consequuntur ullam., True, 10, 9)
(Facilis ea dignissimos sapiente totam laboriosam consequatur ad. Quia consectetur magni odio est totam., True, Animi eius eveniet ut natus., True, None, 10)
;

INSERT INTO ingredientQuantity (unit_id, ingredient_id, variant_id, id, quantity) VALUES 
(2, 5, 8, 1, 5)
(2, 1, 7, 2, 1)
(8, 9, 9, 3, 5)
(5, 6, 8, 4, 7)
(2, 2, 2, 5, 7)
(3, 9, 3, 6, 8)
(9, 5, 6, 7, 7)
(5, 1, 3, 8, 8)
(1, 10, 10, 9, 10)
(None, None, None, 10, 6)
;

INSERT INTO step (picture, text, id, variant_id) VALUES 
(Tempore quibusdam qui facilis deleniti. Ratione minima porro cupiditate eum., Odio nulla modi ducimus labore iusto doloribus., 1, 5)
(Quas quo sint quo voluptate sint. Sit assumenda recusandae., Aliquid tempora dolorum quas., 2, 3)
(Numquam sunt esse minus minima facere. In nulla natus autem. Asperiores dolore doloribus necessitatibus vel incidunt commodi., Libero dolores error facere ipsa ipsam sed., 3, 2)
(Id soluta sint corporis porro. Nisi vero culpa non ullam. Tempora tempore enim accusamus magni iste., Repudiandae enim dolores cum excepturi dignissimos., 4, 2)
(Dolorem cumque ipsa. Occaecati commodi soluta minus fuga similique., Natus incidunt in exercitationem., 5, 3)
(Quod nam similique. Voluptatum repudiandae necessitatibus corporis et., Eligendi incidunt suscipit molestiae., 6, 7)
(Eos velit eos praesentium dolore. Quibusdam consectetur aut ipsam suscipit. Totam temporibus itaque quibusdam quidem., Quis maxime iure quos., 7, 7)
(Minus soluta ipsa saepe nihil., Iusto fuga provident maxime quas., 8, 8)
(Quis labore doloribus provident. Asperiores voluptatum recusandae neque a laboriosam quisquam aut. Repellat officia eaque recusandae ab., Sunt delectus magni rem., 9, 2)
(Facere cumque at temporibus est est impedit sit. Suscipit dolorum amet asperiores nam. Eaque culpa qui. Dolores distinctio dolore harum facere repellat., Atque dolorum dolor fugit., 10, None)
;

INSERT INTO materialQuantity (variant_id, id, material_id, quantity) VALUES 
(10, 1, 5, 8)
(4, 2, 6, 8)
(10, 3, 10, 3)
(2, 4, 5, 3)
(9, 5, 4, 1)
(5, 6, 8, 9)
(3, 7, 3, 7)
(4, 8, 1, 9)
(8, 9, 7, 4)
(None, 10, None, 1)
;

INSERT INTO variant_material_quantity (material_quantity_id, variant_id) VALUES 
(9, 10)
(9, 8)
(10, 5)
(2, 9)
(8, 2)
(7, 6)
(7, 7)
(2, 3)
(10, 4)
(None, None)
;

INSERT INTO variant_recipe_type (recipe_type_id, variant_id) VALUES 
(8, 5)
(7, 8)
(5, 8)
(2, 4)
(3, 10)
(9, 8)
(1, 9)
(6, 1)
(10, 2)
(None, None)
;

INSERT INTO variant_ingredient_quantity (ingredient_quantity_id, variant_id) VALUES 
(4, 2)
(6, 9)
(10, 8)
(10, 7)
(2, 3)
(10, 1)
(10, 4)
(7, 6)
(6, 10)
(None, None)
;

INSERT INTO unit (symbol, id, name) VALUES 
(Consectetur ducimus adipisci tempora explicabo delectus non libero., 1, Id ipsa labore.)
(Fugit voluptatum repellendus beatae., 2, Pariatur voluptatibus inventore delectus.)
(Animi dolorum sequi corrupti asperiores fugit., 3, Exercitationem veniam saepe.)
(Commodi labore dolor recusandae quae nisi., 4, Repellendus doloremque ratione reprehenderit.)
(Est tenetur quaerat quae., 5, Maxime possimus ipsam in.)
(Sit eos molestiae error tenetur., 6, Beatae impedit commodi.)
(Cum iusto ad laboriosam illo., 7, Velit consequuntur voluptas explicabo voluptates.)
(Praesentium blanditiis consequuntur debitis magnam tempora., 8, Atque nemo rerum harum earum nemo possimus.)
(Mollitia quam vero saepe ratione repudiandae minus., 9, Quam laboriosam at asperiores quisquam.)
(Aut non commodi eveniet consequatur adipisci ullam., 10, Alias tempora saepe aliquid rem vitae.)
;

INSERT INTO ingredient (id, name) VALUES 
(1, Amet laborum consequatur debitis ab aspernatur fugiat.)
(2, Architecto ea rerum tempore voluptatum.)
(3, Excepturi architecto vitae provident pariatur ex placeat eveniet.)
(4, Porro a alias non excepturi.)
(5, Dignissimos ratione doloremque.)
(6, Cumque perferendis similique officiis unde dignissimos voluptas.)
(7, Facere tenetur expedita fuga.)
(8, Nulla dolores hic officiis dolorum id iusto.)
(9, Possimus ad molestiae harum impedit.)
(10, Veritatis totam atque sunt vitae ipsa mollitia.)
;

