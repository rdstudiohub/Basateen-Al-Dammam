import os, json, subprocess, time, sys
tok = os.environ.get('REPLICATE_API_TOKEN', '')
if not tok:
    print("ERROR: token not set")
    sys.exit(1)
auth = "Bearer " + tok
api = "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions"
outdir = os.path.dirname(os.path.abspath(__file__))

items = [
("pizza_margherita","Classic Margherita pizza, tomato sauce, fresh mozzarella, basil, crispy thin crust, Italian style, professional food photography, warm lighting, dark background, 8k"),
("pizza_mexicano","Mexican pizza, spicy beef, jalapenos, bell peppers, onions, black beans, melted cheese, corn, on dark plate, professional food photography, 8k"),
("pizza_chicken","Chicken pizza, grilled chicken pieces, bell peppers, mushrooms, onions, melted mozzarella, golden crust, on rustic wooden surface, food photography, 8k"),
("pizza_meat","Meat lover pizza, ground beef, pepperoni, sausage, bacon, melted cheese, thick crust, cheese pull, dark background, 8k"),
("pizza_mix","Mixed pizza, pepperoni, mushrooms, olives, bell peppers, onions, melted cheese, golden brown crust, on serving plate, restaurant lighting, 8k"),
("pizza_bbq","BBQ chicken pizza, barbecue sauce, grilled chicken, red onions, cilantro, smoked gouda, wood-fired crust, on dark slate, 8k"),
("pizza_pepperoni","Classic pepperoni pizza, crispy pepperoni cups, mozzarella cheese, tomato sauce, golden crust, angle shot, professional food photo, 8k"),
("pizza_vegetables","Garden vegetable pizza, bell peppers, mushrooms, olives, onions, tomatoes, spinach, melted cheese, crispy thin crust, on wooden table, 8k"),
("pizza_tuna","Tuna pizza, flaked tuna, red onions, olives, capers, mozzarella, fresh herbs, lemon zest, on dark plate, Mediterranean style, 8k"),
("pizza_four_cheese","Four cheese pizza, mozzarella, gorgonzola, parmesan, fontina, creamy white sauce, golden bubbly crust, honey drizzle, arugula, 8k"),
("feteer_cheese","Egyptian feteer pastry, melted white cheese and cheddar, golden brown flaky layers, cut into triangles, on serving plate, 8k"),
("feteer_honey_cheese","Feteer honey and cheese, golden flaky pastry, melted cheese center, honey drizzled, nuts garnish, on brass tray, warm light, 8k"),
("feteer_chicken","Savory chicken feteer pastry, spiced chicken pieces, golden crispy layers, cut open, on wooden board, fresh herbs, 8k"),
("feteer_chicken_cheese","Chicken cheese feteer, golden flaky pastry, seasoned chicken, melted mozzarella, stretchy cheese, warm lighting, 8k"),
("feteer_mixed_cheese","Mixed cheese feteer, three cheeses, golden crispy exterior, melted interior, earthenware plate, herbs garnish, 8k"),
("feteer_hotdog","Hot dog feteer, Egyptian pastry wrapped around beef hot dog, melted cheese, ketchup, golden baked, street food, 8k"),
("feteer_meat","Meat feteer, seasoned minced beef, onions, peppers, golden flaky pastry, spiced meat filling, on wooden board, 8k"),
("feteer_pastrami","Pastrami feteer, crispy golden pastry, pastrami slices, melted cheese, rolled baked golden, sliced, pickles garnish, 8k"),
("feteer_sausage","Sausage feteer, spicy beef sausage, melted cheese, golden pastry roll, cut diagonally, ketchup mustard, street food, 8k"),
("feteer_tuna","Tuna feteer, flaked tuna, onions, herbs, cheese, golden crispy pastry, triangular pieces, lemon wedge, Mediterranean, 8k"),
("feteer_honey","Sweet honey feteer, golden flaky pastry drizzled with pure honey, ceramic plate, nuts, Egyptian dessert, warm amber, 8k"),
("feteer_cream","Cream feteer dessert, golden layered pastry, thick fresh cream, powdered sugar, ornate plate, warm lighting, premium, 8k"),
("feteer_honey_cream","Feteer honey cream, golden crispy layers, creamy center, honey drizzled, pistachios garnish, dessert, golden lighting, 8k"),
("feteer_chocolate","Chocolate feteer, golden pastry, melted chocolate sauce, chocolate drizzle, powdered sugar, berries garnish, dessert, 8k"),
("feteer_nutella","Nutella feteer, golden flaky pastry, Nutella hazelnut spread, molten center, strawberries garnish, dessert photo, 8k"),
("feteer_banana_chocolate","Banana chocolate feteer, sliced bananas, melted chocolate, golden pastry, chocolate sauce, ice cream, dessert, 8k"),
("feteer_honey_banana","Honey banana feteer, golden pastry, sliced bananas, honey, cinnamon, ceramic plate, caramelized bananas, dessert, 8k"),
("feteer_lotus","Lotus biscoff feteer, golden pastry, creamy lotus spread, crushed biscoff, caramel drizzle, dessert plating, 8k"),
("feteer_mixed_sweet","Mixed sweet feteer platter, assorted sweet pastries, honey, cream, chocolate, nuts, dates, ornate tray, desserts, 8k"),
("shawarma_arabic_chicken","Arabic chicken shawarma wrap, grilled chicken, Arabic flatbread, garlic sauce, pickles, tomatoes, cut in half, on wood, 8k"),
("shawarma_arabic_chicken_extra","Large extra Arabic chicken shawarma, double meat, thick wrap, toasted bread, garlic sauce, pickles fries side, 8k"),
("shawarma_arabic_meat","Arabic meat shawarma, thinly sliced beef, tahini sauce, pickled vegetables, Arabic bread, toasted golden, 8k"),
("shawarma_arabic_meat_extra","Large extra Arabic meat shawarma, double spiced beef, tahini, grilled vegetables, thick wrap, golden toasted, 8k"),
("shawarma_chicken","Chicken shawarma sandwich, saj bread, grilled chicken strips, garlic cream sauce, pickles, paper wrap, street food, 8k"),
("shawarma_meat","Meat shawarma sandwich, spiced beef, tahini sauce, grilled onions, tomatoes, saj bread, toasted, wooden board, 8k"),
("shawarma_mix","Mixed shawarma sandwich, chicken beef, garlic and tahini sauces, pickles, fries, cut in half, street food, 8k"),
("shawarma_chicken_meal","Chicken shawarma meal, sandwich with fries drink, basket, garlic sauce, pickles, lunch box, fast food, 8k"),
("shawarma_meat_meal","Meat shawarma meal box, shawarma wrap, crispy fries, tahini sauce, salad, drink, takeaway box, 8k"),
("shawarma_mix_meal","Mix shawarma meal platter, chicken meat shawarma, fries, garlic sauce, pickles, salad, drink, family style, 8k"),
("saj_chicken","Saj chicken sandwich, grilled chicken, thin saj bread, vegetables, garlic sauce, rolled tight, on wooden board, 8k"),
("saj_meat","Saj meat sandwich, spiced beef, saj bread, tahini sauce, grilled vegetables, rolled toasted, halved, 8k"),
("saj_mix","Saj mix sandwich, chicken beef, thin saj bread, mixed sauces, fresh vegetables, toasted golden, 8k"),
("saj_crispy","Saj crispy chicken, crunchy fried chicken strips, saj bread, lettuce, mayonnaise, tomatoes, paper wrap, 8k"),
("saj_zinger","Saj zinger spicy chicken, crispy spicy fillet, lettuce, spicy sauce, saj bread, dramatic lighting, 8k"),
("saj_mexican","Saj Mexican, seasoned chicken, jalapenos, bell peppers, corn, spicy sauce, saj bread, Mexican style, 8k"),
("saj_hotdog","Saj hot dog, beef hot dog, saj bread, ketchup, mustard, grilled onions, melted cheese, street food, 8k"),
("saj_falafel","Saj falafel wrap, crispy falafel, saj bread, tahini sauce, tomatoes, cucumbers, pickles, vegetarian, 8k"),
("burger_classic","Classic beef burger, grilled patty, lettuce, tomato, onion rings, toasted bun, sesame, premium, dark bg, 8k"),
("burger_cheese","Cheese burger, melted cheddar dripping, beef patty, lettuce, tomato, pickles, brioche bun, fries side, 8k"),
("burger_double","Double beef cheese burger, two stacked patties, double cheese, bacon, lettuce, tomato, special sauce, 8k"),
("burger_chicken","Crispy chicken burger, fried chicken fillet, lettuce, mayonnaise, soft bun, coleslaw, crunchy, 8k"),
("burger_crispy","Crispy chicken burger, extra crunchy coating, lettuce, tomato, creamy sauce, sesame bun, golden crispy, 8k"),
("burger_zinger","Zinger spicy chicken burger, extra crispy spicy chicken, jalapenos, pepper jack, spicy sauce, lettuce, 8k"),
("grill_mixed_small","Small mixed grill platter, assorted kebabs, grilled meats, small portion, round metal tray, herbs lemon, 8k"),
("grill_mixed_medium","Medium mixed grill, chicken tikka, seekh kebab, shish tawook, grilled vegetables, rice, serving tray, 8k"),
("grill_mixed_large","Large mixed grill banquet, lamb chops, kebabs, chicken, shish tawook, grilled veggies, rice, herbs, 8k"),
("kebab_meat","Beef kebab skewers, minced seasoned beef, charcoal grilled, charred exterior, herbs, lemon, smoky, 8k"),
("kebab_chicken","Chicken kebab skewers, spiced minced chicken grilled, golden brown, mint chutney, onions, wooden board, 8k"),
("shish_tawook","Shish tawook skewers, marinated chicken cubes grilled golden, bell peppers, garlic sauce, tomatoes, 8k"),
("grilled_chicken","Whole grilled chicken, golden crispy skin, roasted, platter with roasted vegetables rice, lemon herbs, 8k"),
("lamb_chops","Grilled lamb chops, charred outside pink inside, rosemary garlic, wooden board, roasted vegetables, 8k"),
("bbq_mix","Mixed BBQ platter, assorted grilled meats, lamb chops, kebabs, chicken wings, sausages, cast iron tray, 8k"),
("half_grilled_chicken","Half grilled chicken, golden brown crispy skin, rice pilaf, grilled vegetables, lemon wedge, plated meal, 8k"),
("full_grilled_chicken","Whole grilled chicken, roasted golden crispy skin, aromatic rice, grilled vegetables, herbs lemon, family, 8k"),
("broast_meal","Chicken broast meal, crispy deep fried chicken golden brown, french fries, coleslaw, garlic sauce, basket, 8k"),
("family_meal","Family meal platter, grilled chicken, rice, salads, bread, sauces, large serving, traditional Arabic, 8k"),
("family_meal_mix","Mixed family meal, assorted grilled meats, mixed rice nuts, fattoush, hummus, bread, sauces, banquet, 8k"),
("salad_green","Fresh garden salad bowl, mixed lettuce, tomatoes, cucumbers, carrots, bell peppers, vinaigrette, healthy, 8k"),
("salad_fattoush","Lebanese fattoush salad, crispy pita chips, romaine lettuce, tomatoes, cucumbers, radishes, sumac, pomegranate, 8k"),
("salad_tabbouleh","Fresh tabbouleh, finely chopped parsley, bulgur wheat, tomatoes, mint, lemon juice, olive oil, lettuce cups, 8k"),
("salad_coleslaw","Creamy coleslaw, shredded cabbage carrots, creamy dressing, wooden table, fresh crunchy, side dish, 8k"),
("salad_tahina","Tahini sauce salad bowl, creamy sesame paste, lemon, garlic, parsley, olive oil, ceramic bowl, meze, 8k"),
("fries","Golden crispy french fries, wooden serving basket, perfectly salted, ketchup mayonnaise, steam, fast food, 8k"),
("cheese_fries","Loaded cheese fries, crispy fries, melted cheddar sauce, bacon bits, green onions, sour cream, appetizer, 8k"),
("garlic_sauce","Creamy garlic sauce dip bowl, white smooth, parsley, olive oil drizzle, pita bread, Lebanese style, 8k"),
("extra_cheese","Melted cheese casserole, golden bubbly mozzarella cheddar, stretchy cheese pull, ceramic dish, steam, 8k"),
("extra_chicken","Grilled chicken pieces skewer, perfectly charred, seasoned, herbs lemon, additional protein, warm lighting, 8k"),
("extra_meat","Grilled meat pieces skewer, beef lamb, perfectly cooked, side portion, grilled vegetables, warm lighting, 8k"),
("juice_orange","Fresh orange juice, tall glass, vibrant orange, fresh oranges, pulp, condensation, natural sunlight, refreshing, 8k"),
("juice_lemon","Fresh lemon juice, glass, pale yellow, fresh lemons, mint, ice cubes, condensation, refreshing summer, 8k"),
("juice_lemon_mint","Lemon mint juice, greenish yellow, fresh mint, lime slices, ice cubes, condensation, refreshing beverage, 8k"),
("juice_cocktail","Mixed fruit cocktail juice, vibrant red orange yellow layered, fresh fruits, ice, colorful, natural light, 8k"),
("juice_mango","Thick mango juice, glass, golden yellow, fresh mango pieces, cream top, ice, tropical, rich creamy, 8k"),
("juice_strawberry","Fresh strawberry juice, vibrant pinkish red, fresh strawberries, ice, condensation, creamy, pink tones, 8k"),
("juice_avocado","Creamy avocado juice, glass, pale green, fresh avocado half, honey drizzle, milk base, thick rich, 8k"),
("juice_pomegranate","Fresh pomegranate juice, deep ruby red, fresh seeds, ice, condensation, pour splash, vibrant red, 8k"),
("juice_kiwi","Fresh kiwi juice, vibrant green, fresh kiwi slices, mint, ice, condensation, green tones, refreshing, 8k"),
("juice_watermelon","Fresh watermelon juice, bright pinkish red, watermelon slices, ice, mint, condensation, refreshing summer, 8k"),
("mojito_blue","Blue mojito cocktail, highball glass, blue curacao, mint, lime, ice, bubbles, condensation, dark background, 8k"),
("mojito_green","Green mojito, mint lime, vibrant green, mint sprigs, lime wheels, crushed ice, condensation, dark bar, 8k"),
("mojito_red","Red mojito cocktail, red berry, fresh berries, mint, lime, ice, strawberry garnish, dark background, 8k"),
("mojito_passion","Passion fruit mojito, tropical yellow-orange, fresh passion fruit seeds, mint, lime, ice, exotic, 8k"),
("mojito_strawberry","Strawberry mojito, pinkish red, fresh strawberries, mint, lime, crushed ice, strawberry garnish, 8k"),
("mojito_mango","Mango mojito, golden yellow, fresh mango puree, mint, lime, crushed ice, sliced mango garnish, tropical, 8k"),
]

def gen(key, prompt):
    out = os.path.join(outdir, key + ".jpg")
    if os.path.exists(out) and os.path.getsize(out) > 2000:
        print(f"  SKIP {key}")
        return True
    payload = json.dumps({"input": {"prompt": prompt, "num_outputs": 1, "aspect_ratio": "1:1", "output_format": "jpg", "quality": 80}})
    try:
        r = subprocess.run(["curl", "-s", "-X", "POST", api, "-H", "Authorization: " + auth, "-H", "Content-Type: application/json", "-d", payload], capture_output=True, text=True, timeout=60).stdout.strip()
        d = json.loads(r)
        pid = d.get("id")
        if not pid:
            print(f"  FAIL {key}: {r[:100]}")
            return False
        for _ in range(30):
            time.sleep(3)
            pr = subprocess.run(["curl", "-s", f"https://api.replicate.com/v1/predictions/{pid}", "-H", "Authorization: " + auth], capture_output=True, text=True, timeout=15).stdout.strip()
            sd = json.loads(pr)
            if sd.get("status") == "succeeded":
                url = sd["output"][0] if isinstance(sd["output"], list) else sd["output"]
                subprocess.run(["curl", "-sL", url, "-o", out], timeout=30)
                print(f"  OK {key} ({os.path.getsize(out)}b)")
                return True
            elif sd.get("status") == "failed":
                print(f"  FAIL {key}")
                return False
        print(f"  TIMEOUT {key}")
        return False
    except Exception as e:
        print(f"  ERROR {key}: {e}")
        return False

print(f"Items: {len(items)}")
ok = 0
for i, (k, p) in enumerate(items):
    sys.stdout.write(f"[{i+1}/{len(items)}] {k}... ")
    sys.stdout.flush()
    if gen(k, p):
        ok += 1
print(f"\nDone: {ok}/{len(items)}")
