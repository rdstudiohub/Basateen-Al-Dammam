import os, subprocess, json, time, sys

TOKEN = os.environ.get('REPLICATE_API_TOKEN', '')
if not TOKEN:
    print("ERROR: REPLICATE_API_TOKEN not set. Run: source /opt/data/.env")
    sys.exit(1)

AUTH = "Bearer " + TOKEN
MODEL = "black-forest-labs/flux-schnell"
API = "https://api.replicate.com/v1/models/" + MODEL + "/predictions"

print(f"API ready. Token: {TOKEN[:10]}...")

BANNERS = [
  ("pizza_banner", "Professional food photography of assorted pizzas on wooden table, Margherita, Pepperoni, Four Cheese, melted cheese stretch, fresh basil, warm lighting, dark wooden background, premium restaurant menu, 8k quality"),
  ("feteer_banner", "Traditional Egyptian Feteer pastries, golden brown flaky layers, some savory with cheese some sweet with honey, on ornate serving platter, warm ambient lighting, premium restaurant food photography, 8k"),
  ("shawarma_banner", "Four large shawarma wraps on wooden board, chicken and meat varieties, toasted flatbread, garlic sauce, pickles, french fries on side, warm golden lighting, dark background, street food style, professional food photography"),
  ("saj_banner", "Fresh Saj bread sandwiches filled with chicken and vegetables, toasted on dome grill, crispy golden exterior, sauces, on dark textured surface, steam rising, warm lighting, premium food photography"),
  ("burgers_banner", "Gourmet burger collection on dark slate board, classic cheese burger, crispy chicken burger, double beef burger, golden toasted buns, fresh lettuce tomato, melting cheese, sizzling patties, dramatic lighting, dark background, 8k"),
  ("grills_banner", "Arabian mixed grill platter, lamb kebabs, chicken shish tawook, grilled vegetables, fragrant rice, on large ornate metal tray, charcoal grill marks, smoke, warm golden lighting, premium Arabic restaurant photography, 8k"),
  ("meals_banner", "Whole roasted grilled chicken on large platter, golden crispy skin, roasted vegetables, aromatic rice, Arabic bread, fresh herbs, lemon garnish, family style serving, warm restaurant style lighting, dark background"),
  ("salads_banner", "Fresh Arabic mezza salads assortment, green salad, fattoush with crispy bread, tabbouleh with parsley, colorful vegetables arranged beautifully on dark wooden table, natural lighting, healthy fresh concept, premium food photography, 8k"),
  ("sides_banner", "Crispy golden french fries in wooden basket, loaded cheese fries with melted cheddar, dipping sauces, garlic sauce, extra cheese, on dark slate board, steam rising, warm lighting, premium fast food photography"),
  ("juices_banner", "Assorted fresh juice glasses on rustic wooden table, orange juice, mango, strawberry, pomegranate, avocado, surrounded by fresh fruits, ice cubes, condensation droplets, vibrant natural colors, sunlight, premium menu photography, 8k"),
  ("mojitos_banner", "Colorful mojito cocktails in tall glasses, blue curacao, green mint, red strawberry, passion fruit flavors, mint leaves, lime slices, crushed ice, condensation, dark wooden table, colorful vibrant drinks, warm ambient lighting, premium beverage photography")
]

def generate(key, prompt):
    out = key + ".jpg"
    if os.path.exists(out) and os.path.getsize(out) > 2000:
        print(f"  ⏩ {key}: exists ({os.path.getsize(out)} bytes)")
        return True
    
    payload = json.dumps({"input": {"prompt": prompt, "num_outputs": 1, "aspect_ratio": "4:5", "output_format": "jpg", "quality": 85}})
    
    # Submit
    try:
        r = subprocess.run(["curl", "-s", "-X", "POST", API, 
                          "-H", "Authorization: " + AUTH, 
                          "-H", "Content-Type: application/json", "-d", payload],
                         capture_output=True, text=True, timeout=60).stdout.strip()
        data = json.loads(r)
        pid = data.get("id")
        if not pid:
            print(f"  ❌ {key}: No prediction ID - {r[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ {key}: Submit error - {e}")
        return False
    
    # Poll
    for _ in range(30):
        time.sleep(3)
        try:
            pr = subprocess.run(["curl", "-s", f"https://api.replicate.com/v1/predictions/{pid}", 
                               "-H", "Authorization: " + AUTH],
                              capture_output=True, text=True, timeout=15).stdout.strip()
            sd = json.loads(pr)
            if sd.get("status") == "succeeded":
                url = sd["output"][0] if isinstance(sd["output"], list) else sd["output"]
                subprocess.run(["curl", "-sL", url, "-o", out], timeout=30)
                size = os.path.getsize(out)
                print(f"  ✅ {key}: {size} bytes")
                return True
            elif sd.get("status") == "failed":
                print(f"  ❌ {key}: Failed - {sd.get('error','')}")
                return False
        except Exception as e:
            print(f"  ⚠ {key}: Poll error - {e}")
            continue
    
    print(f"  ⏰ {key}: Timeout after ~90s")
    return False

print(f"\nGenerating {len(BANNERS)} banner images...")
success = 0
for i, (key, prompt) in enumerate(BANNERS):
    print(f"\n[{i+1}/{len(BANNERS)}] {key}")
    if generate(key, prompt):
        success += 1
    if i < len(BANNERS) - 1:
        time.sleep(3)

print(f"\n{'='*40}")
print(f"Done: {success}/{len(BANNERS)} banners generated")
