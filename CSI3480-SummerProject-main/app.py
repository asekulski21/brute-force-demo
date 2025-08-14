#!/usr/bin/env python3

"""
Project Name: Brute Force Demo Project
Description: Simulates a brute force attack to guess a password
Author: Andrae Taylor, Christina Carvalho, Alexander Sekulski
Date: 7/24/2025
"""



import time
import random
import streamlit as st
import re
import string
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Constants
COMMON_PASSWORD_LIST = "small-password-list/smallpasswordlist.txt"
TARGET_PASSWORD = "secret_user_info/secret_password.txt"

def analyze_password_strength(password: str) -> dict:
    """Analyze password strength and provide detailed feedback"""
    score = 0
    feedback = []
    
    # Length analysis
    if len(password) < 8:
        feedback.append("❌ Too short (less than 8 characters)")
    elif len(password) < 12:
        feedback.append("⚠️ Moderate length (8-11 characters)")
        score += 1
    else:
        feedback.append("✅ Good length (12+ characters)")
        score += 2
    
    # Character variety analysis
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    char_types = sum([has_lower, has_upper, has_digit, has_special])
    if char_types == 1:
        feedback.append("❌ Only one character type used")
    elif char_types == 2:
        feedback.append("⚠️ Two character types used")
        score += 1
    elif char_types == 3:
        feedback.append("✅ Three character types used")
        score += 2
    else:
        feedback.append("✅ All four character types used")
        score += 3
    
    # Common patterns
    if password.lower() in ['password', '123456', 'qwerty', 'admin']:
        feedback.append("❌ Very common password")
        score -= 2
    elif password.lower() in ['password123', '123456789', 'qwerty123']:
        feedback.append("❌ Common pattern with numbers")
        score -= 1
    
    # Sequential characters
    if any(password[i:i+3] in string.ascii_lowercase for i in range(len(password)-2)):
        feedback.append("⚠️ Contains sequential letters")
        score -= 1
    
    # Repeated characters
    if len(set(password)) < len(password) * 0.7:
        feedback.append("⚠️ Many repeated characters")
        score -= 1
    
    # Dictionary word check
    common_words = ['password', 'admin', 'user', 'login', 'welcome', 'hello', 'test']
    if password.lower() in common_words:
        feedback.append("❌ Common dictionary word")
        score -= 2
    
    # Entropy calculation (simplified)
    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32
    
    entropy = len(password) * (charset_size ** 0.5)
    
    # Overall strength rating
    if score <= 0:
        strength = "Very Weak"
        color = "red"
    elif score <= 2:
        strength = "Weak"
        color = "orange"
    elif score <= 4:
        strength = "Moderate"
        color = "yellow"
    elif score <= 6:
        strength = "Strong"
        color = "lightgreen"
    else:
        strength = "Very Strong"
        color = "green"
    
    return {
        "score": score,
        "strength": strength,
        "color": color,
        "feedback": feedback,
        "entropy": round(entropy, 1),
        "length": len(password),
        "char_types": char_types,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_special": has_special
    }

def generate_incremental_passwords(max_length: int = 4) -> list[str]:
    """Generate passwords using incremental attack method"""
    passwords = []
    chars = string.ascii_lowercase + string.digits  # 36 characters
    
    # Generate all combinations up to max_length
    from itertools import product
    for length in range(1, max_length + 1):
        # Generate combinations of current length
        for combo in product(chars, repeat=length):
            passwords.append(''.join(combo))
    
    return passwords

def calculate_attack_speed(attempts: int, elapsed_time: float) -> dict:
    """Calculate and format attack speed metrics"""
    if elapsed_time <= 0:
        return {
            "passwords_per_second": 0,
            "passwords_per_minute": 0,
            "estimated_total_time": 0,
            "progress_percentage": 0
        }
    
    passwords_per_second = attempts / elapsed_time
    passwords_per_minute = passwords_per_second * 60
    
    return {
        "passwords_per_second": round(passwords_per_second, 2),
        "passwords_per_minute": round(passwords_per_minute, 2),
        "elapsed_time": round(elapsed_time, 2),
        "attempts": attempts
    }

def get_password_list() -> list[str]:
    """Get the common password list - embedded for web deployment"""
    return [
        "123", "password", "dogs", "cats", "tomato", "oakland_university", "password123", "loveyou",
        "ilovedogs", "ilovecats", "apple", "sunshine", "456", "flower", "happy", "ilovebirds",
        "sky", "cloud", "rain", "snow", "wind", "sun", "lake", "mountain", "forest", "beach",
        "ocean", "desert", "valley", "hill", "grass", "leaf", "branch", "root", "seed", "bush",
        "vine", "cactus", "rose", "tulip", "daisy", "lily", "maple", "pine", "cedar", "birch",
        "dog", "cat", "bird", "fish", "tiger", "lion", "bear", "wolf", "fox", "deer", "rabbit",
        "squirrel", "horse", "cow", "pig", "sheep", "goat", "duck", "goose", "eagle", "hawk",
        "owl", "snake", "lizard", "frog", "turtle", "whale", "dolphin", "shark", "jellyfish",
        "starfish", "crab", "lobster", "octopus", "apple", "banana", "orange", "grape", "lemon",
        "lime", "peach", "pear", "cherry", "berry", "mango", "kiwi", "pineapple", "watermelon",
        "carrot", "potato", "onion", "garlic", "broccoli", "spinach", "lettuce", "tomato",
        "cucumber", "pepper", "bean", "pea", "corn", "wheat", "rice", "bread", "cheese", "milk",
        "butter", "egg", "meat", "fish", "chicken", "turkey", "ham", "bacon", "sausage", "pizza",
        "pasta", "soup", "salad", "cake", "cookie", "pie", "icecream", "candy", "chocolate", "sugar",
        "salt", "pepper", "spice", "coffee", "tea", "juice", "water", "soda", "book", "pen",
        "pencil", "paper", "desk", "chair", "table", "lamp", "clock", "window", "door", "wall",
        "floor", "ceiling", "roof", "house", "apartment", "car", "bike", "bus", "train", "plane",
        "boat", "road", "bridge", "tunnel", "city", "town", "village", "park", "garden",
        "playground", "school", "library", "museum", "store", "market", "mall", "office",
        "hospital", "church", "temple", "mosque", "castle", "tower", "star", "moon", "planet",
        "comet", "galaxy", "nebula", "rocket", "astronaut", "space", "earth", "fire", "air",
        "water", "stone", "sand", "dust", "mud", "clay", "metal", "wood", "glass", "plastic",
        "cloth", "leather", "silk", "wool", "cotton", "gold", "silver", "diamond", "pearl",
        "bridge", "candle", "mirror", "phone", "laptop", "keyboard", "screen", "mouse", "clock123",
        "watch", "ring", "necklace", "bracelet", "shoe", "sock", "hat", "scarf", "glove", "coat",
        "shirt", "pants", "skirt", "dress", "belt", "bag", "wallet", "key", "lock", "chain",
        "rope", "ladder", "hammer", "nail", "screw", "wrench", "drill", "saw", "paint", "brush",
        "canvas", "picture", "frame", "album", "camera", "video", "music", "song", "dance",
        "piano", "guitar", "drum", "flute", "violin", "note", "rhythm", "beat789", "stage",
        "curtain", "light", "shadow", "color", "blue456", "red", "green", "yellow", "purple",
        "orange", "black", "white", "gray", "pink", "brown", "gold321", "silver", "bronze",
        "copper", "iron", "steel", "magnet", "wheel", "engine", "fuel", "road987", "path",
        "trail", "fence", "gate", "yard", "porch", "step", "stair", "elevator", "escalator",
        "hall", "room", "kitchen", "bedroom", "bathroom", "closet", "shelf", "bookcase", "couch",
        "pillow", "blanket", "sheet", "towel", "soap", "shampoo", "brush654", "comb", "razor",
        "mirror222", "sink", "faucet", "pipe", "bucket", "sponge", "broom", "dustpan", "vacuum",
        "mop", "trash", "recycle", "bottle", "can", "jar", "plate", "bowl", "cup", "spoon",
        "fork", "knife", "napkin", "tablecloth", "oven", "stove", "fridge", "freezer", "microwave",
        "toaster", "blender", "mixer", "pot", "pan", "kettle", "grill", "firepit", "smoke",
        "ash", "spark", "flame", "heat", "cold", "frost", "ice", "steam", "fog", "mist", "dew",
        "puddle", "stream", "pond", "waterfall", "spring", "cave", "cliff", "canyon", "ridge",
        "peak", "summit", "slope", "meadow", "field", "farm", "barn", "tractor", "plow",
        "harvest", "crop", "seed123", "soil", "dirt", "pebble", "boulder", "gem", "crystal",
        "quartz", "ruby", "sapphire", "emerald", "amber", "fossil", "bone", "shell", "feather",
        "wing", "claw", "beak", "tail", "smile", "laugh", "cry", "shout", "whisper", "talk",
        "sing", "hum", "whistle", "clap", "wave", "point", "touch", "grab", "hold", "drop",
        "throw", "catch", "kick", "jump", "run", "walk", "crawl", "climb", "swim", "dive",
        "float", "sink789", "fly", "soar", "glide", "fall", "trip", "slip", "slide", "swing",
        "spin", "twist", "turn", "bend", "stretch", "lift", "push", "pull", "shake", "stir",
        "mix", "pour", "fill", "empty", "open", "close", "lock456", "unlock", "tie", "untie",
        "cut", "chop", "slice", "peel", "grate", "boil", "bake", "fry", "grill123", "roast",
        "steam", "chill", "freeze", "thaw", "taste", "smell", "hear", "see", "feel", "dream",
        "think", "learn", "teach", "read", "write", "draw", "paint321", "sketch", "erase",
        "color", "shade", "outline", "circle", "square", "triangle", "star222", "heart",
        "arrow", "line", "dot", "curve", "angle", "shape", "size", "weight", "height", "width",
        "length", "speed", "time", "hour", "minute", "second", "day", "night", "morning",
        "evening", "noon", "midnight", "dawn", "dusk", "summer", "winter", "spring", "fall654",
        "season", "weather", "storm", "thunder", "lightning", "raindrop", "snowflake", "hail",
        "breeze", "gust", "tornado", "hurricane", "flood", "drought", "heatwave", "frostbite",
        "sunburn", "shade987", "shelter", "tent", "cabin", "lodge", "hut", "igloo", "teepee",
        "yurt", "campfire", "lantern", "torch", "flashlight", "bulb", "glow", "spark123",
        "ember", "blaze", "smoke", "fog456", "haze", "dust", "pollen", "spore", "moss", "fern",
        "ivy", "bamboo", "reed", "weed", "thorn", "petal", "stem", "bud", "bloom", "fruit",
        "nut", "shell", "pit", "rind", "juice789", "pulp", "zest", "syrup", "honey", "jam",
        "jelly", "cream", "foam", "bubble", "ripple", "wave123", "tide", "current", "shore",
        "reef", "island", "peninsula", "bay", "gulf", "cove", "lagoon", "hope", "joy", "peace",
        "love", "trust", "fear", "anger", "calm", "excitement", "sadness", "pride", "shame",
        "courage", "doubt", "faith", "wish", "dream123", "goal", "plan", "idea", "thought",
        "memory", "vision", "imagination", "creativity", "skill", "talent", "effort", "work",
        "task", "job", "duty", "role", "game", "sport", "race", "match", "score", "goal456",
        "point", "team", "player", "coach", "referee", "ball", "net", "goalpost", "field789",
        "court", "track", "rink", "pool", "gym", "stadium", "arena", "bench", "bleacher",
        "ticket", "fan", "cheer", "chant", "whistle321", "trophy", "medal", "ribbon", "prize",
        "reward", "challenge", "puzzle", "riddle", "quiz", "test", "exam", "grade", "score123",
        "report", "study", "lesson", "homework", "project", "research", "discovery", "invention",
        "machine", "tool", "gear", "lever", "pulley", "spring222", "bolt", "nut", "washer",
        "cable", "wire", "battery", "switch", "plug", "socket", "circuit", "power", "energy",
        "force", "motion", "speed654", "distance", "direction", "map", "compass", "globe",
        "atlas", "path987", "route", "journey", "trip", "adventure", "quest", "mission",
        "voyage", "travel", "destination", "landmark", "monument", "statue", "fountain",
        "plaza", "square456", "street", "avenue", "boulevard", "alley", "sidewalk", "crosswalk",
        "signal", "traffic", "vehicle", "truck", "van", "motorcycle", "scooter", "skateboard",
        "rollerblade", "helmet", "pad", "glove123", "vest", "badge", "flag", "banner", "sign",
        "poster", "billboard", "ad", "message", "letter", "note789", "email", "text", "call",
        "chat", "voice", "sound", "echo", "noise", "silence", "music321", "harmony", "melody",
        "tune", "beat", "rhythm222", "lyric", "chorus", "verse", "poem", "story", "book456",
        "chapter", "page", "word", "sentence", "paragraph", "quote", "phrase", "proverb", "joke",
        "riddle123", "myth", "legend", "tale", "fable", "moral", "lesson654", "truth", "fact",
        "lie", "secret", "mystery", "clue", "hint", "answer789", "code", "program", "software",
        "app", "website", "server", "cloud123", "data", "file", "folder", "drive", "disk",
        "chip", "circuit456", "screen", "monitor", "tablet", "smartphone", "charger",
        "cable789", "port", "pixel", "icon", "button", "menu", "link", "page321", "browser",
        "search", "query", "result", "network", "signal", "wifi", "router", "modem",
        "password654", "username", "profile", "account", "login", "logout", "update",
        "download", "upload", "stream222", "video", "audio", "image", "photo", "album",
        "frame987", "lens", "focus", "zoom", "flash", "tripod", "filter", "edit", "crop",
        "resize", "share", "post", "comment", "like", "tag", "hashtag", "trend", "viral", "meme",
        "gif", "emoji", "sticker", "chat123", "message", "inbox", "notification", "alert",
        "reminder", "calendar", "event", "schedule", "plan456", "task", "goal", "priority",
        "deadline", "meeting", "call789", "conference", "webinar", "presentation", "slide",
        "chart", "graph", "table", "data321", "statistic", "trend", "pattern", "cycle",
        "rhythm", "flow", "wave654", "tide", "current", "drift", "ripple", "splash", "droplet",
        "puddle222", "pond", "lake", "river987", "creek", "brook", "waterfall", "fountain",
        "geyser", "spray", "mist", "fog", "dew", "frost", "ice123", "snow", "sleet", "hail",
        "rain", "storm", "breeze456", "gust", "wind", "gale", "hurricane", "tornado", "thunder",
        "lightning", "cloud789", "sky", "horizon", "dawn", "dusk", "twilight", "sunrise",
        "sunset", "star321", "comet", "meteor", "moon", "planet", "orbit", "galaxy", "nebula",
        "cosmos", "space654", "rocket", "satellite", "probe", "shuttle", "astronaut", "suit",
        "helmet", "gravity", "weightless", "vacuum", "void", "dust222", "particle", "atom",
        "molecule", "cell", "tissue", "organ", "heart987", "lung", "brain", "bone", "muscle",
        "nerve", "blood", "vein", "artery", "pulse", "breath", "sigh", "yawn", "cough",
        "sneeze", "hiccup", "blink", "wink", "stare", "glance", "gaze123", "squint", "vision",
        "sight", "blind", "focus456", "window", "curtain123", "blinds", "shade", "sill",
        "glass", "pane", "frame456", "lock", "latch", "knob", "handle", "hinge", "bolt789",
        "screw", "nail", "hammer", "pliers", "screwdriver", "tape", "glue", "string", "thread",
        "needle", "stitch", "fabric", "cotton321", "linen", "velvet", "denim", "lace", "ribbon",
        "zipper", "button654", "pocket", "seam", "hem", "collar", "sleeve", "cuff", "vest222",
        "jacket", "sweater", "hoodie", "scarf987", "mittens", "socks", "boots", "sandals",
        "sneakers", "laces", "sole", "heel", "bag123", "purse", "backpack", "suitcase",
        "luggage", "wallet", "coin", "bill", "cash", "card456", "receipt", "ticket", "stamp",
        "envelope", "parcel", "box", "crate", "barrel", "bucket789", "jug", "bottle", "jar",
        "lid", "cap", "cork", "straw321", "spoon", "fork", "knife", "ladle", "tongs", "spatula",
        "whisk", "bowl654", "plate", "saucer", "mug", "glass", "pitcher", "tray", "napkin222",
        "tablecloth", "placemat", "coaster", "stove", "oven", "grill987", "toaster", "blender",
        "kettle", "pot", "pan", "skillet", "wok", "colander", "sieve", "grater", "peeler",
        "chopper", "mixer123", "freezer", "fridge", "sink", "faucet", "drain", "sponge", "rag",
        "broom456", "mop", "dustpan", "vacuum", "trashcan", "bin", "garbage", "compost",
        "recycle789", "paper", "cardboard", "plastic", "metal", "wood", "bamboo", "cork321",
        "clay", "brick", "stone", "gravel", "sand", "dust", "mud", "soil654", "peat", "moss",
        "lichen", "fern", "vine", "ivy", "weed222", "grass", "clover", "dandelion", "thistle",
        "nettle", "bramble", "thorn987", "bark", "twig", "leaf", "petal", "stamen", "pistil",
        "pollen", "nectar123", "honey", "beeswax", "hive", "bee", "wasp", "ant", "beetle",
        "butterfly456", "moth", "dragonfly", "ladybug", "spider", "web", "cocoon", "silk",
        "shell789", "scale", "fin", "gill", "tail", "claw", "paw", "hoof", "horn321", "antler",
        "fur", "feather", "wing", "beak", "talon", "fang", "venom654", "sting", "buzz",
        "chirp", "bark222", "meow", "roar", "growl", "hiss", "croak", "bleat", "moo", "neigh987",
        "bray", "cluck", "crow", "hoot", "tweet", "quack", "grunt", "squeak123", "howl",
        "yelp", "purr", "drone", "hum", "rustle", "crackle", "pop456", "snap", "crunch", "fizz",
        "sizzle", "drip", "splash", "gurgle", "bubble789", "ripple", "wave", "tide", "current",
        "eddy", "whirlpool", "foam", "spray321", "mist", "fog", "haze", "smog", "dew", "frost",
        "ice", "snow654", "sleet", "hail", "drizzle", "downpour", "flood", "drought", "breeze",
        "gust222", "gale", "storm", "tempest", "cyclone", "blizzard", "thunder", "lightning",
        "rainbow987", "cloud", "sky", "horizon", "dawn", "dusk", "twilight", "midday",
        "midnight123", "sunrise", "sunset", "moon", "star", "comet", "asteroid", "meteor",
        "planet456", "orbit", "galaxy", "nebula", "cosmos", "void", "vacuum", "gravity", "mass789",
        "weight", "force", "energy", "power", "heat", "spark", "flame", "ember321", "ash",
        "smoke", "soot", "charcoal", "coal", "oil", "gas", "steam654", "vapor", "mist", "scent",
        "aroma", "fragrance", "odor", "smell", "taste222", "flavor", "spice", "herb", "mint",
        "basil", "thyme", "sage", "parsley987", "dill", "cilantro", "oregano", "fennel", "clove",
        "nutmeg", "cinnamon", "ginger123", "pepper", "salt", "sugar", "syrup", "molasses",
        "jam", "jelly", "marmalade456", "cream", "butter", "cheese", "yogurt", "milk", "curd",
        "whey", "custard789", "pudding", "pie", "tart", "cake", "cookie", "brownie", "muffin",
        "scone321", "bread", "roll", "bun", "bagel", "croissant", "pastry", "dough", "crust654",
        "crumb", "loaf", "slice", "toast", "sandwich", "wrap", "taco", "burrito222", "pizza",
        "pasta", "noodle", "sauce", "gravy", "stew", "soup", "broth987", "salad", "dressing",
        "vinegar", "oil", "mustard", "ketchup", "mayo", "relish123", "pickle", "olive",
        "onion", "garlic", "leek", "shallot", "chive", "celery456", "carrot", "radish",
        "turnip", "beet", "yam", "potato", "cabbage", "lettuce789", "spinach", "kale",
        "arugula", "chard", "broccoli", "cauliflower", "sprout", "bean321", "pea", "lentil",
        "chickpea", "soybean", "tofu", "nut", "almond", "walnut654", "pecan", "hazelnut",
        "cashew", "peanut", "seed", "sesame", "flax", "pumpkin222", "sunflower", "berry",
        "strawberry", "blueberry", "raspberry", "blackberry", "cranberry", "gooseberry987",
        "grape", "raisin", "currant", "fig", "date", "prune", "apricot", "peach123",
        "nectarine", "plum", "cherry", "mango", "papaya", "kiwi", "pineapple", "melon456",
        "watermelon", "cantaloupe", "honeydew", "lemon", "lime", "orange", "grapefruit",
        "tangerine789", "apple", "pear", "quince", "persimmon", "pomegranate", "coconut",
        "avocado", "tomato321", "eggplant", "zucchini", "squash", "pumpkin", "cucumber",
        "pepper", "chili", "jalapeno654", "corn", "wheat", "barley", "oat", "rye", "rice",
        "quinoa", "millet222", "sorghum", "bran", "germ", "flour", "meal", "grits", "porridge",
        "cereal987", "granola", "muesli", "snack", "chip", "cracker", "popcorn", "pretzel",
        "candy123", "chocolate", "fudge456", "adventure", "quest123", "journey", "trip",
        "voyage", "expedition", "trek", "hike", "stroll", "wander", "roam", "explore456",
        "discover", "search", "hunt", "chase", "pursue", "track", "trail789", "path", "route",
        "shortcut", "detour", "map", "compass321", "guide", "landmark", "signpost", "beacon",
        "lighthouse", "tower", "spire", "dome654", "arch", "bridge", "tunnel", "gate", "fence",
        "wall", "barrier222", "hedge", "ditch", "moat", "ramp", "slope", "ridge987", "cliff",
        "canyon", "valley", "plain", "plateau", "mesa", "dune", "oasis123", "swamp", "marsh",
        "bog", "wetland", "reef", "atoll", "island", "peninsula456", "cape", "bay", "harbor",
        "dock", "pier", "jetty", "wharf", "marina789", "shore", "coast", "beach", "cove",
        "inlet", "fjord", "glacier", "iceberg321", "tundra", "prairie", "savanna", "jungle",
        "rainforest", "desert", "steppe", "meadow654", "grove", "orchard", "vineyard", "garden",
        "lawn", "patio", "terrace", "balcony222", "porch", "deck", "gazebo", "shed", "barn",
        "silo", "stable", "pen987", "coop", "kennel", "cage", "nest", "burrow", "den", "lair",
        "hive123", "anthill", "mound", "tunnel", "cave", "cavern", "grotto", "abyss", "chasm456",
        "crater", "volcano", "lava", "magma", "ash", "soot", "cinder", "boulder789", "pebble",
        "gravel", "sand", "silt", "clay", "loam", "dirt", "soil321", "compost", "mulch",
        "manure", "fertilizer", "sprout", "seedling", "sapling", "shrub654", "bush", "hedge",
        "bramble", "thicket", "underbrush", "canopy", "trunk", "branch222", "twig", "bark",
        "sap", "resin", "amber", "cone", "needle", "frond987", "palm", "cactus", "succulent",
        "aloe", "agave", "yucca", "moss", "lichen123", "fungus", "mushroom", "toadstool",
        "mold", "mildew", "yeast", "spore", "pollen456", "nectar", "bud", "bloom", "blossom",
        "flower", "rose", "tulip", "daisy789", "lily", "orchid", "violet", "iris", "peony",
        "poppy", "sunflower", "marigold321", "zinnia", "pansy", "petunia", "snapdragon",
        "daffodil", "hyacinth", "lotus", "waterlily654", "vine", "ivy", "grapevine", "tendril",
        "root", "bulb", "tuber", "rhizome222", "stalk", "stem", "leaf", "blade", "vein",
        "chlorophyll", "photosynthesis", "oxygen987", "carbon", "nitrogen", "mineral",
        "nutrient", "vitamin", "enzyme", "hormone", "gene123", "DNA", "cell", "nucleus",
        "membrane", "cytoplasm", "organelle", "tissue", "organ456", "heart", "liver", "kidney",
        "spleen", "pancreas", "stomach", "intestine", "bladder789", "vein", "artery",
        "capillary", "blood", "plasma", "platelet", "antibody", "antigen321", "immunity",
        "vaccine", "virus", "bacteria", "germ", "infection", "fever", "cough654", "sneeze",
        "rash", "itch", "bruise", "cut", "scrape", "burn", "blister222", "scar", "stitch",
        "bandage", "gauze", "plaster", "sling", "crutch", "wheelchair987", "stretcher",
        "ambulance", "hospital", "clinic", "pharmacy", "medicine", "pill", "capsule123",
        "syrup", "ointment", "cream", "lotion", "spray", "inhaler", "syringe", "needle456",
        "dose", "prescription", "doctor", "nurse", "surgeon", "dentist", "vet", "pharmacist789",
        "therapist", "patient", "ward", "room", "bed", "chart", "monitor", "scanner321", "xray",
        "ultrasound", "surgery", "operation", "recovery", "therapy", "exercise", "stretch654",
        "jog", "sprint", "swim", "cycle", "lift", "pushup", "situp", "plank222", "yoga",
        "meditation", "breath", "pose", "balance", "strength", "flexibility", "endurance987",
        "stamina", "speed", "agility", "reflex", "coordination", "rhythm", "pace", "stride123",
        "leap", "bound", "skip", "hop", "tumble", "flip", "roll", "spin456", "twirl", "twist",
        "bend", "sway", "swing", "dance", "waltz", "tango789", "salsa", "ballet", "tap", "jazz",
        "hiphop", "choreography", "routine", "step321", "move", "gesture", "wave", "nod", "wink",
        "smile", "frown", "grin654", "smirk", "pout", "glare", "stare", "glance", "peek", "gaze",
        "squint222", "vision", "sight", "focus", "blur", "shadow", "reflection", "mirror",
        "lens987", "prism", "beam", "ray", "glow", "sparkle", "shimmer", "glint", "gleam123",
        "flash", "flare", "blaze", "flicker", "candle", "lamp", "bulb", "lantern456", "torch",
        "spotlight", "floodlight", "headlight", "taillight", "signal", "beacon", "flare789",
        "fire", "flame", "ember", "spark", "kindle", "blaze", "inferno", "smoke321", "fog",
        "mist", "vapor", "steam", "haze", "smog", "dust", "pollen654", "ash", "soot", "cinder",
        "charcoal", "coal", "peat", "oil", "gas222", "fuel", "propane", "kerosene", "diesel",
        "gasoline", "battery", "charge", "current987", "volt", "watt", "amp", "circuit", "wire",
        "cable", "plug", "socket123", "switch", "fuse", "breaker", "generator", "turbine",
        "engine", "motor", "piston456", "gear", "lever", "pulley", "belt", "chain", "axle",
        "wheel", "tire789", "rim", "hub", "spoke", "brake", "clutch", "pedal", "handlebar",
        "saddle321", "frame", "fork", "chain", "crank", "sprocket", "derailleur", "spoke",
        "valve654", "pump", "patch", "tube", "rim", "bike", "tricycle", "unicycle", "scooter222",
        "skateboard", "rollerblade", "helmet", "pad", "glove", "vest", "badge", "flag987",
        "banner", "pennant", "streamer", "ribbon", "emblem85", "crest123", "compass547",
        "lantern819", "saddle274", "ribbon632", "pebble105", "breeze483", "petal736",
        "spark291", "meadow408", "horizon372"
    ]

def get_target_password() -> str:
    """Get the target password - embedded for web deployment"""
    return "meadow408"

def get_password_selection_options() -> dict:
    """Get password selection options for different difficulty levels"""
    password_list = get_password_list()
    
    return {
        "Easy (Top of list)": password_list[0],  # "123"
        "Medium (Middle of list)": password_list[len(password_list)//2],  # Middle password
        "Hard (End of list)": password_list[-1],  # "horizon372"
        "Very Hard (Complex)": "meadow408",  # Original target
        "Custom Selection": None  # Will be handled in UI
    }

def read_passwords_from_file(filename: str) -> list[str]:
    """Legacy function - now returns embedded data"""
    return get_password_list()

def get_target(filename: str) -> str:
    """Legacy function - now returns embedded data"""
    return get_target_password()

def create_attack_complexity_graph():
    """Create an interactive graph showing time complexity of different attack methods"""
    
    # Generate data for different password lengths
    password_lengths = np.arange(1, 9)  # 1 to 8 characters
    
    # Dictionary attack complexity (linear - O(n) where n is dictionary size)
    # Assuming dictionary size grows linearly with password length
    dict_complexity = password_lengths * 100  # Simplified model
    
    # Incremental attack complexity (exponential - O(c^n) where c is character set size)
    char_set_size = 36  # a-z + 0-9
    incremental_complexity = char_set_size ** password_lengths
    
    # Create the figure
    fig = go.Figure()
    
    # Add dictionary attack line
    fig.add_trace(go.Scatter(
        x=password_lengths,
        y=dict_complexity,
        mode='lines+markers',
        name='Dictionary Attack',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        hovertemplate='<b>Dictionary Attack</b><br>' +
                     'Password Length: %{x}<br>' +
                     'Complexity: %{y:,.0f}<br>' +
                     'Time Complexity: O(n)<extra></extra>'
    ))
    
    # Add incremental attack line
    fig.add_trace(go.Scatter(
        x=password_lengths,
        y=incremental_complexity,
        mode='lines+markers',
        name='Incremental Attack',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=8),
        hovertemplate='<b>Incremental Attack</b><br>' +
                     'Password Length: %{x}<br>' +
                     'Complexity: %{y:,.0f}<br>' +
                     'Time Complexity: O(c^n)<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Attack Method Time Complexity Comparison',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        xaxis_title='Password Length (characters)',
        yaxis_title='Computational Complexity (log scale)',
        yaxis_type='log',
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.1)',
            title_font_color='white',
            tickfont_color='white'
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.1)',
            title_font_color='white',
            tickfont_color='white'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            font=dict(color='white')
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        height=400
    )
    
    return fig

def create_password_strength_distribution():
    """Create a graph showing password strength distribution in the dictionary"""
    
    # Get password list and analyze strength of each
    password_list = get_password_list()
    strength_scores = []
    
    # Sample passwords for performance (analyze first 100)
    sample_passwords = password_list[:100]
    
    for password in sample_passwords:
        analysis = analyze_password_strength(password)
        strength_scores.append(analysis['score'])
    
    # Create histogram
    fig = px.histogram(
        x=strength_scores,
        nbins=10,
        title='Password Strength Distribution (Sample of 100)',
        labels={'x': 'Strength Score', 'y': 'Number of Passwords'},
        color_discrete_sequence=['#00ff88']
    )
    
    # Update layout for dark theme
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_color='white',
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title_font_color='white',
            tickfont_color='white'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title_font_color='white',
            tickfont_color='white'
        ),
        height=300
    )
    
    return fig



def main(enable_2fa: bool, target_password: str = None, attack_method: str = "dictionary"):
    """Run brute force attack - automatic if 2FA disabled, step-by-step if enabled."""

    # Select password list based on attack method
    if attack_method == "dictionary":
        password_list_array = get_password_list()
    elif attack_method == "incremental":
        password_list_array = generate_incremental_passwords(4)  # Up to 4 characters
    else:
        st.error("❌ Invalid attack method selected.")
        return

    target_word = target_password if target_password else get_target_password()

    if not target_word:
        st.error("❌ Failed: No valid target password found.")
        return
    if len(password_list_array) == 0:
        st.error("❌ Failed: Password list is empty.")
        return

    if not enable_2fa:
        # Original automatic mode - no 2FA
        st.success(f"🎯 Target password loaded: `{target_word}`")
        st.info(f"📋 Testing against {len(password_list_array)} passwords using {attack_method.title()} attack...")
        st.info(f"🎯 **Target:** `{target_word}`")
        
        # Check if attack is paused or finished
        if st.session_state.attack_paused:
            st.warning("⏸️ **Attack Paused** - Click 'Start Brute Force Attack' to resume")
            return
        elif st.session_state.attack_finished:
            st.info("⏹️ **Attack Finished** - Click 'Start Brute Force Attack' to start a new attack")
            return
        
        # Create placeholders for updating
        progress_bar = st.progress(0)
        status_text = st.empty()
        attempt_text = st.empty()
        speed_text = st.empty()
        result_text = st.empty()
        
        start_time = time.time()
        attempt = 0
        found = False
        
        # Loop through passwords automatically
        for word in password_list_array:
            # Check if attack was paused or finished during execution
            if st.session_state.attack_paused or st.session_state.attack_finished:
                st.warning("⏸️ **Attack Interrupted**")
                return
                
            attempt += 1
            
            # Update progress
            progress = attempt / len(password_list_array)
            progress_bar.progress(progress)
            
            # Calculate and display attack speed
            current_time = time.time()
            elapsed_time = current_time - start_time
            speed_metrics = calculate_attack_speed(attempt, elapsed_time)
            
            # Update status
            status_text.write(f"🔍 **Trying password:** `{word}`")
            attempt_text.write(f"📊 **Attempt #{attempt}** of {len(password_list_array)}")
            speed_text.write(f"⚡ **Speed:** {speed_metrics['passwords_per_second']} pwd/sec | {speed_metrics['passwords_per_minute']} pwd/min")
            
            # Check if password matches
            if word == target_word:
                found = True
                end_time = time.time()
                elapsed_time = round(end_time - start_time, 2)
                
                result_text.success(f"🎉 **SUCCESS!** Password found: `{word}`")
                st.balloons()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Result", "Found")
                with col2:
                    st.metric("Attempts", attempt)
                with col3:
                    st.metric("Time", f"{elapsed_time}s")
                with col4:
                    st.metric("Speed", f"{speed_metrics['passwords_per_second']} pwd/sec")
                
                # Mark attack as finished
                st.session_state.attack_finished = True
                break
            
            # Small delay for visual effect
            time.sleep(0.05)
        
        # If not found
        if not found:
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            speed_metrics = calculate_attack_speed(attempt, elapsed_time)
            result_text.error("❌ **FAILED:** Password not found in password list")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Result", "Not Found")
            with col2:
                st.metric("Time", f"{elapsed_time}s")
            with col3:
                st.metric("Speed", f"{speed_metrics['passwords_per_second']} pwd/sec")
            
            # Mark attack as finished
            st.session_state.attack_finished = True
    
    else:
        # 2FA enabled - step-by-step mode
        # Check if attack is paused or finished
        if st.session_state.attack_paused:
            st.warning("⏸️ **Attack Paused** - Click 'Start Brute Force Attack' to resume")
            return
        elif st.session_state.attack_finished:
            st.info("⏹️ **Attack Finished** - Click 'Start Brute Force Attack' to start a new attack")
            return
        
        # Initialize attack state
        st.session_state.setdefault("attempt_index", 0)
        st.session_state.setdefault("start_time", time.time())

        total = len(password_list_array)
        attempt = st.session_state.attempt_index + 1 if st.session_state.attempt_index < total else total

        st.info(f"📋 Testing against {total} passwords using {attack_method.title()} attack...")
        st.info(f"🎯 **Target:** `{target_word}`")

        # Progress/status
        progress = st.session_state.attempt_index / total
        st.progress(progress)

        # Display attack speed for 2FA mode
        if st.session_state.attempt_index > 0:
            elapsed_time = time.time() - st.session_state.start_time
            speed_metrics = calculate_attack_speed(st.session_state.attempt_index, elapsed_time)
            st.info(f"⚡ **Current Speed:** {speed_metrics['passwords_per_second']} pwd/sec | {speed_metrics['passwords_per_minute']} pwd/min")

        # If attack finished previously
        if st.session_state.attempt_index >= total:
            elapsed_time = round(time.time() - st.session_state.start_time, 2)
            speed_metrics = calculate_attack_speed(total, elapsed_time)
            st.error("❌ **FAILED:** Password not found in password list")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Result", "Not Found")
            with col2:
                st.metric("Time", f"{elapsed_time}s")
            with col3:
                st.metric("Speed", f"{speed_metrics['passwords_per_second']} pwd/sec")
            
            # Mark attack as finished
            st.session_state.attack_finished = True
            return

        current_word = password_list_array[st.session_state.attempt_index]
        st.write(f"🔍 **Next attempt:** `{current_word}` (#{attempt} of {total})")

        # Generate new 2FA code for each attempt
        current_2fa_code = str(random.randint(1000, 9999))
        
        # One-attempt form: when submitted, we process exactly one attempt
        form_key = f"attempt_form_{st.session_state.attempt_index}"
        with st.form(form_key, clear_on_submit=True):
            user_pass = st.text_input(f"Enter 2FA code '{current_2fa_code}' to run this attempt:", type="password")
            submitted = st.form_submit_button("Run this attempt")

        if submitted:
            if user_pass != current_2fa_code:
                st.error(f"❌ Wrong code. Enter '{current_2fa_code}' to proceed.")
                return

            # Process the attempt
            if current_word == target_word:
                elapsed_time = round(time.time() - st.session_state.start_time, 2)
                speed_metrics = calculate_attack_speed(attempt, elapsed_time)
                st.success(f"🎉 **SUCCESS!** Password found: `{current_word}`")
                st.balloons()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Result", "Found")
                with col2:
                    st.metric("Attempts", attempt)
                with col3:
                    st.metric("Time", f"{elapsed_time}s")
                with col4:
                    st.metric("Speed", f"{speed_metrics['passwords_per_second']} pwd/sec")
                
                # Mark attack as finished
                st.session_state.attack_finished = True
                return
            else:
                # Advance to next attempt
                st.session_state.attempt_index += 1
                st.rerun()

# Streamlit UI
st.set_page_config(page_title="Brute Force Demo", page_icon="🔓", layout="wide")
st.title("🔓 Brute Force Attack Simulator")

# Generate random 4-digit 2FA code
if "twofa_code" not in st.session_state:
    st.session_state.twofa_code = str(random.randint(1000, 9999))

# Create main layout with two columns
main_col, graph_col = st.columns([2, 1])

with main_col:
    # Password selection
    st.write("**🎯 Select Target Password:**")
    password_options = get_password_selection_options()

    # Create two columns for password selection
    col1, col2 = st.columns([2, 1])

    with col1:
        password_choice = st.selectbox(
            "Choose password difficulty:",
            list(password_options.keys()),
            help="Select from predefined difficulty levels or choose a custom password"
        )

    with col2:
        if password_choice == "Custom Selection":
            password_list = get_password_list()
            custom_index = st.number_input(
                "Select password index (0-2024):",
                min_value=0,
                max_value=len(password_list)-1,
                value=0,
                help=f"Choose any password from the list of {len(password_list)} passwords"
            )
            target_password = password_list[custom_index]
            position = custom_index + 1
            st.info(f"Selected: `{target_password}`")
            st.write(f"📍 Position: {position}/{len(password_list)}")
        else:
            target_password = password_options[password_choice]
            password_list = get_password_list()
            try:
                position = password_list.index(target_password) + 1
                st.info(f"Selected: `{target_password}`")
                st.write(f"📍 Position: {position}/{len(password_list)}")
            except ValueError:
                st.info(f"Selected: `{target_password}`")
                st.write("📍 Position: Not in list (very hard)")

    # Password Strength Analyzer
    st.write("**🔍 Password Strength Analysis:**")
    strength_analysis = analyze_password_strength(target_password)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Strength", strength_analysis["strength"])
    with col2:
        st.metric("Score", strength_analysis["score"])
    with col3:
        st.metric("Entropy", strength_analysis["entropy"])

    # Character type indicators
    char_col1, char_col2, char_col3, char_col4 = st.columns(4)
    with char_col1:
        st.write(f"**Lowercase:** {'✅' if strength_analysis['has_lower'] else '❌'}")
    with char_col2:
        st.write(f"**Uppercase:** {'✅' if strength_analysis['has_upper'] else '❌'}")
    with char_col3:
        st.write(f"**Digits:** {'✅' if strength_analysis['has_digit'] else '❌'}")
    with char_col4:
        st.write(f"**Special:** {'✅' if strength_analysis['has_special'] else '❌'}")

    # Detailed feedback
    with st.expander("📊 Detailed Analysis"):
        for feedback in strength_analysis["feedback"]:
            st.write(feedback)

    # Attack Method Selection
    st.write("**⚔️ Attack Method:**")
    attack_method = st.selectbox(
        "Choose attack method:",
        ["dictionary", "incremental"],
        format_func=lambda x: x.title(),
        help="Dictionary: Tests against common passwords (faster)\nIncremental: Tests all combinations up to 4 characters (slower but more thorough)"
    )

    # Show attack method info
    if attack_method == "dictionary":
        password_list = get_password_list()
        st.info(f"📋 **Dictionary Attack:** Testing against {len(password_list)} common passwords")
    elif attack_method == "incremental":
        incremental_list = generate_incremental_passwords(4)
        st.info(f"📋 **Incremental Attack:** Testing all combinations up to 4 characters ({len(incremental_list)} total)")

    # Show password list info
    with st.expander("📋 Password List Information"):
        if attack_method == "dictionary":
            password_list = get_password_list()
            st.write(f"**Total passwords available:** {len(password_list)}")
            st.write("**Sample passwords:**")
            st.code(f"First: {password_list[0]}\nMiddle: {password_list[len(password_list)//2]}\nLast: {password_list[-1]}")
        else:
            incremental_list = generate_incremental_passwords(4)
            st.write(f"**Total combinations:** {len(incremental_list)}")
            st.write("**Character set:** a-z, 0-9 (36 characters)")
            st.write("**Sample combinations:**")
            st.code(f"1 char: {incremental_list[0]}, {incremental_list[10]}, {incremental_list[35]}\n2 chars: {incremental_list[36]}, {incremental_list[100]}, {incremental_list[500]}\n3 chars: {incremental_list[1296]}, {incremental_list[2000]}, {incremental_list[3000]}")

    # Simple configuration
    enable_2fa = st.checkbox("🔐 Enable 2FA Protection")
    if enable_2fa:
        st.info(f"🔒 You will need to enter the 2FA code: **{st.session_state.twofa_code}**")

    # Session state for flow
    st.session_state.setdefault("attack_requested", False)
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("twofa_error", "")
    st.session_state.setdefault("attack_started", False)
    st.session_state.setdefault("attack_paused", False)
    st.session_state.setdefault("attack_finished", False)

    # Attack control buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🎯 Start Brute Force Attack", type="primary", disabled=st.session_state.attack_started and not st.session_state.attack_paused and not st.session_state.attack_finished):
            st.session_state.attack_requested = True
            st.session_state.attack_paused = False
            st.session_state.attack_finished = False
            st.session_state.twofa_error = ""

    with col2:
        if st.button("⏸️ Pause Attack", disabled=not st.session_state.attack_started or st.session_state.attack_paused or st.session_state.attack_finished):
            st.session_state.attack_paused = True

    with col3:
        if st.button("⏹️ Finish Attack", disabled=not st.session_state.attack_started or st.session_state.attack_finished):
            st.session_state.attack_finished = True
            st.session_state.attack_paused = True

    with col4:
        if st.button("🔄 Reset Attack", disabled=not st.session_state.attack_started):
            st.session_state.attack_started = False
            st.session_state.attack_requested = False
            st.session_state.attack_paused = False
            st.session_state.attack_finished = False
            st.session_state.authenticated = False
            st.session_state.attempt_index = 0
            st.session_state.twofa_error = ""
            st.rerun()

    # If user requested an attack and 2FA is enabled but not authenticated, prompt now
    if st.session_state.attack_requested and enable_2fa and not st.session_state.authenticated:
        st.warning("🔐 **2FA Required**")
        st.info(f"Enter the 2FA code: **{st.session_state.twofa_code}**")

        twofa_input = st.text_input("2FA Code:", type="password", key="twofa_input")
        if st.button("Authenticate"):
            if twofa_input == st.session_state.twofa_code:
                st.session_state.authenticated = True
            else:
                st.session_state.twofa_error = f"Wrong code! Enter {st.session_state.twofa_code}"

        if st.session_state.twofa_error:
            st.error(st.session_state.twofa_error)

    # If attack was requested and (2FA passed or disabled), run the attack
    if st.session_state.attack_requested and (not enable_2fa or st.session_state.authenticated):
        # Start or continue the step-by-step attack
        if not st.session_state.attack_started:
            # Initialize attack state
            st.session_state.attack_started = True
            st.session_state.start_time = time.time()
            st.session_state.attempt_index = 0
            st.session_state.attack_paused = False
            st.session_state.attack_finished = False
        

        main(enable_2fa, target_password, attack_method)

# Right column - Interactive Graphs
with graph_col:
    st.write("**📊 Attack Complexity Analysis**")
    
    # Create and display the attack complexity graph
    complexity_fig = create_attack_complexity_graph()
    st.plotly_chart(complexity_fig, use_container_width=True)
    
    # Add educational information
    with st.expander("ℹ️ About Attack Complexity"):
        st.write("""
        **Dictionary Attack (O(n)):**
        - Linear time complexity
        - Tests against a predefined list of common passwords
        - Fast but limited to known passwords
        
        **Incremental Attack (O(c^n)):**
        - Exponential time complexity
        - Tests all possible character combinations
        - Slower but more thorough
        - c = character set size (36 for a-z, 0-9)
        - n = password length
        """)
    
    # Create and display password strength distribution
    st.write("**📈 Password Strength Distribution**")
    strength_fig = create_password_strength_distribution()
    st.plotly_chart(strength_fig, use_container_width=True)
    
    # Add real-time attack statistics
    if st.session_state.get("attack_started", False):
        st.write("**⚡ Real-time Statistics**")
        
        if st.session_state.get("attempt_index", 0) > 0:
            elapsed_time = time.time() - st.session_state.get("start_time", time.time())
            attempts = st.session_state.get("attempt_index", 0)
            
            if elapsed_time > 0:
                speed = attempts / elapsed_time
                st.metric("Current Speed", f"{speed:.1f} pwd/sec")
                st.metric("Total Attempts", attempts)
                st.metric("Elapsed Time", f"{elapsed_time:.1f}s")
                
                # Estimate time to complete
                if attack_method == "dictionary":
                    total_passwords = len(get_password_list())
                    remaining = total_passwords - attempts
                    if speed > 0:
                        eta = remaining / speed
                        st.metric("ETA", f"{eta:.1f}s")
                else:
                    total_combinations = len(generate_incremental_passwords(4))
                    remaining = total_combinations - attempts
                    if speed > 0:
                        eta = remaining / speed
                        st.metric("ETA", f"{eta:.1f}s")
