#!/usr/bin/env python3
"""
Mass generator - creates thousands of SEO posts via topic combinations
"""

import re
import random
from datetime import datetime
from pathlib import Path

# Base templates that get combined with modifiers
PROBLEMS = [
    "jumping", "barking", "biting", "pulling", "lunging", "chewing",
    "digging", "whining", "growling", "aggression", "anxiety", "fear",
    "reactivity", "leash pulling", "counter surfing", "door dashing",
    "food guarding", "toy guarding", "nipping", "mouthing"
]

SITUATIONS = [
    "on walks", "at home", "around guests", "around other dogs",
    "around kids", "at the door", "during meals", "at night",
    "when alone", "in the car", "at the vet", "at the groomer",
    "in public", "off leash", "on leash", "around strangers"
]

BREEDS = [
    "german shepherd", "golden retriever", "labrador", "pit bull",
    "rottweiler", "husky", "beagle", "bulldog", "poodle", "boxer",
    "dachshund", "chihuahua", "yorkie", "shih tzu", "great dane",
    "doberman", "australian shepherd", "border collie", "corgi",
    "french bulldog", "maltese", "cocker spaniel", "bernese mountain dog",
    "cavalier king charles", "miniature schnauzer", "boston terrier",
    "havanese", "pomeranian", "shetland sheepdog", "vizsla",
    "weimaraner", "rhodesian ridgeback", "akita", "alaskan malamute",
    "basset hound", "bloodhound", "bichon frise", "cane corso",
    "english mastiff", "irish setter", "jack russell terrier",
    "papillon", "samoyed", "scottish terrier", "west highland terrier"
]

AGES = [
    "puppy", "8 week old", "10 week old", "12 week old", "4 month old",
    "6 month old", "1 year old", "2 year old", "adult", "senior",
    "older dog", "young dog", "adolescent"
]

NASHVILLE_AREAS = [
    "nashville", "franklin", "brentwood", "murfreesboro", "hendersonville",
    "gallatin", "spring hill", "mt juliet", "smyrna", "la vergne",
    "lebanon", "goodlettsville", "white house", "antioch", "bellevue",
    "green hills", "hermitage", "madison", "nolensville", "thompsons station",
    "clarksville", "dickson", "columbia", "east nashville", "west nashville",
    "germantown nashville", "the gulch", "sylvan park", "12 south",
    "berry hill", "oak hill", "forest hills", "belle meade",
    "donelson", "old hickory", "inglewood", "east nashville", "bordeaux",
    "joelton", "whites creek", "pegram", "kingston springs", "fairview",
    "pleasant view", "greenbrier", "springfield", "portland", "westmoreland",
    "hartsville", "carthage", "watertown", "smithville", "mcminnville",
    "tullahoma", "shelbyville", "lewisburg", "chapel hill", "eagleville",
    "rockvale", "christiana", "lascassas", "woodbury", "manchester",
    "37201", "37203", "37204", "37205", "37206", "37207", "37208", "37209",
    "37210", "37211", "37212", "37214", "37215", "37216", "37217", "37218",
    "37219", "37220", "37221", "37027", "37064", "37067", "37069"
]

SERVICES = [
    "puppy training", "obedience training", "behavior modification",
    "aggression training", "anxiety training", "leash training",
    "crate training", "potty training", "off leash training",
    "protection dog training", "service dog training", "therapy dog training",
    "board and train", "private lessons", "group classes",
    "in home training", "online dog training", "virtual dog training"
]

COMMANDS = [
    "sit", "stay", "come", "heel", "down", "place", "off", "leave it",
    "drop it", "wait", "go to bed", "touch", "shake", "roll over",
    "speak", "quiet", "fetch", "bring it", "release", "free"
]

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:60]

def generate_title_variations():
    """Generate thousands of unique titles"""
    titles = []

    # Pattern: how to stop [breed] from [problem]
    for breed in BREEDS:
        for problem in PROBLEMS[:10]:
            titles.append(f"how to stop {breed} from {problem}")

    # Pattern: [breed] [problem] [situation]
    for breed in BREEDS[:20]:
        for problem in PROBLEMS[:10]:
            for situation in SITUATIONS[:5]:
                titles.append(f"{breed} {problem} {situation}")

    # Pattern: [age] [breed] training tips
    for age in AGES:
        for breed in BREEDS:
            titles.append(f"{age} {breed} training tips")

    # Pattern: dog training [nashville area]
    for area in NASHVILLE_AREAS:
        titles.append(f"dog training {area}")
        titles.append(f"puppy training {area}")
        titles.append(f"dog obedience classes {area}")
        titles.append(f"in home dog training {area}")
        titles.append(f"private dog trainer {area}")
        titles.append(f"best dog trainer {area}")
        titles.append(f"affordable dog training {area}")

    # Pattern: how to teach [breed] to [command]
    for breed in BREEDS[:15]:
        for command in COMMANDS:
            titles.append(f"how to teach {breed} to {command}")

    # Pattern: why does my [breed] [problem]
    for breed in BREEDS[:20]:
        for problem in PROBLEMS:
            titles.append(f"why does my {breed} {problem}")

    # Pattern: [problem] in [age] dogs
    for problem in PROBLEMS:
        for age in AGES:
            titles.append(f"{problem} in {age} dogs")

    # Pattern: [service] [nashville area]
    for service in SERVICES:
        for area in NASHVILLE_AREAS:
            titles.append(f"{service} {area}")

    # Pattern: [breed] [service] near me
    for breed in BREEDS[:25]:
        for service in SERVICES[:8]:
            titles.append(f"{breed} {service} near me")

    # Pattern: best [service] for [breed]
    for service in SERVICES[:10]:
        for breed in BREEDS[:20]:
            titles.append(f"best {service} for {breed}")

    # Pattern: [age] dog [problem] help
    for age in AGES:
        for problem in PROBLEMS:
            titles.append(f"{age} dog {problem} help")

    # Pattern: how much does [service] cost
    for service in SERVICES:
        titles.append(f"how much does {service} cost")
        titles.append(f"{service} prices nashville")

    # NEW Pattern 1: is [breed] easy to train
    for breed in BREEDS:
        titles.append(f"is {breed} easy to train")
        titles.append(f"is {breed} hard to train")
        titles.append(f"how to train a {breed} for beginners")

    # NEW Pattern 2: rescued [breed] training / adopted dog training
    for breed in BREEDS:
        titles.append(f"rescued {breed} training tips")
        titles.append(f"adopted {breed} behavior problems")
        titles.append(f"training a rescue {breed}")

    # NEW Pattern 3: [breed] training mistakes
    for breed in BREEDS[:25]:
        titles.append(f"{breed} training mistakes to avoid")
        titles.append(f"common {breed} training mistakes")

    # NEW Pattern 4: how to train [breed] with positive reinforcement
    for breed in BREEDS:
        titles.append(f"how to train {breed} with positive reinforcement")
        titles.append(f"reward based training for {breed}")

    # NEW Pattern 5: [breed] off leash training
    for breed in BREEDS:
        titles.append(f"{breed} off leash training nashville")
        titles.append(f"how to train {breed} off leash")

    # NEW Pattern 6: [problem] after adopting a dog
    for problem in PROBLEMS:
        titles.append(f"{problem} after adopting a dog")
        titles.append(f"newly adopted dog {problem} help")
        titles.append(f"rescue dog {problem} solutions")

    # NEW Pattern 7: dog training tips for [season/occasion]
    OCCASIONS = [
        "the holidays", "christmas", "thanksgiving", "fourth of july",
        "new years", "halloween", "summer", "winter", "spring", "fall",
        "thunderstorms", "fireworks", "house guests", "moving to a new home",
        "having a baby", "introducing a new pet", "camping", "travel"
    ]
    for occasion in OCCASIONS:
        titles.append(f"dog training tips for {occasion}")
        titles.append(f"how to calm dog during {occasion}")
        titles.append(f"dog anxiety during {occasion}")

    # NEW Pattern 8: [breed] not listening help
    for breed in BREEDS:
        titles.append(f"{breed} not listening help")
        titles.append(f"why wont my {breed} listen")
        titles.append(f"{breed} ignoring commands")

    # NEW Pattern 9: how long does it take to train a [breed]
    for breed in BREEDS:
        titles.append(f"how long does it take to train a {breed}")
        titles.append(f"how long to potty train a {breed}")
        titles.append(f"{breed} training timeline")

    # NEW Pattern 10: [breed] socialization tips
    for breed in BREEDS:
        titles.append(f"{breed} socialization tips")
        titles.append(f"how to socialize a {breed}")
        titles.append(f"{breed} socialization nashville")

    # NEW Pattern 11: [breed] daily training routine / training schedule
    for breed in BREEDS:
        titles.append(f"{breed} daily training routine")
        titles.append(f"{breed} training schedule for beginners")
        titles.append(f"how often should you train a {breed}")

    # NEW Pattern 12: [age] [breed] potty training tips
    for age in AGES[:6]:
        for breed in BREEDS:
            titles.append(f"{age} {breed} potty training")
            titles.append(f"how to potty train a {age} {breed}")

    # NEW Pattern 13: [breed] training in an apartment / small space
    LIVING_SITUATIONS = [
        "apartment", "small house", "condo", "townhouse", "with kids",
        "with cats", "with other dogs", "without a yard", "in a city"
    ]
    for breed in BREEDS[:20]:
        for situation in LIVING_SITUATIONS:
            titles.append(f"training a {breed} in a {situation}")
            titles.append(f"{breed} training tips for {situation} living")

    # NEW Pattern 14: crate training [breed] / how to crate train a [breed]
    for breed in BREEDS:
        titles.append(f"crate training a {breed}")
        titles.append(f"how to crate train a {breed}")
        titles.append(f"{breed} crate training problems")

    # NEW Pattern 15: [breed] separation anxiety help
    for breed in BREEDS:
        titles.append(f"{breed} separation anxiety help")
        titles.append(f"how to help {breed} with separation anxiety")
        titles.append(f"{breed} alone time training")

    # NEW Pattern 16: how to calm a [breed] / [breed] calming techniques
    for breed in BREEDS:
        titles.append(f"how to calm a {breed}")
        titles.append(f"{breed} calming techniques")
        titles.append(f"how to calm an anxious {breed}")

    # NEW Pattern 17: [breed] first week home tips / new puppy checklist
    for breed in BREEDS:
        titles.append(f"first week home with a {breed}")
        titles.append(f"bringing home a new {breed} checklist")
        titles.append(f"what to expect first week with {breed}")

    # NEW Pattern 18: [breed] leash manners / loose leash walking
    for breed in BREEDS:
        titles.append(f"{breed} loose leash walking tips")
        titles.append(f"how to teach {breed} leash manners")
        titles.append(f"{breed} heel training nashville")

    # NEW Pattern 19: [problem] during [life event]
    LIFE_EVENTS = [
        "pregnancy", "baby coming home", "moving houses", "adding a new pet",
        "divorce", "working from home", "returning to office", "long work hours",
        "vacation", "boarding", "daycare"
    ]
    for problem in PROBLEMS[:10]:
        for event in LIFE_EVENTS:
            titles.append(f"dog {problem} during {event}")
            titles.append(f"managing dog {problem} when {event}")

    # NEW Pattern 20: [breed] aggression toward [target] help
    AGGRESSION_TARGETS = [
        "other dogs", "strangers", "kids", "men", "women",
        "cats", "small animals", "visitors", "mail carrier", "joggers"
    ]
    for breed in BREEDS[:20]:
        for target in AGGRESSION_TARGETS:
            titles.append(f"{breed} aggression toward {target} help")
            titles.append(f"{breed} reactive toward {target} nashville")

    # NEW Pattern 21: [breed] fear of [stimulus]
    FEAR_STIMULI = [
        "thunder", "fireworks", "strangers", "other dogs", "loud noises",
        "cars", "children", "men", "vacuum cleaner", "water"
    ]
    for breed in BREEDS:
        for stimulus in FEAR_STIMULI:
            titles.append(f"{breed} fear of {stimulus}")
            titles.append(f"helping {breed} overcome fear of {stimulus}")

    # NEW Pattern 22: how to introduce [breed] to [new thing]
    INTRODUCTIONS = [
        "cats", "a baby", "other dogs", "children", "small animals",
        "a new home", "a new family member", "another dog"
    ]
    for breed in BREEDS:
        for thing in INTRODUCTIONS:
            titles.append(f"how to introduce {breed} to {thing}")
            titles.append(f"introducing a {breed} to {thing}")

    # NEW Pattern 23: [breed] [command] training step by step
    for breed in BREEDS[:20]:
        for command in COMMANDS[:10]:
            titles.append(f"{breed} {command} training step by step")
            titles.append(f"teaching {breed} to {command} step by step")

    # NEW Pattern 24: when to start training / best age to train
    for breed in BREEDS:
        titles.append(f"when to start training a {breed} puppy")
        titles.append(f"best age to start training a {breed}")
        titles.append(f"at what age can you train a {breed}")

    # NEW Pattern 25: mental stimulation for [breed]
    for breed in BREEDS:
        titles.append(f"mental stimulation for {breed}")
        titles.append(f"brain games for {breed}")
        titles.append(f"how to mentally stimulate a {breed}")

    # NEW Pattern 26: [breed] body language guide
    for breed in BREEDS:
        titles.append(f"{breed} body language guide")
        titles.append(f"reading {breed} body language")
        titles.append(f"understanding {breed} body language")

    # NEW Pattern 27: [breed] recall training
    for breed in BREEDS:
        titles.append(f"{breed} recall training tips")
        titles.append(f"how to improve {breed} recall")
        titles.append(f"{breed} wont come when called help")

    # NEW Pattern 28: [breed] tricks to teach
    TRICK_LEVELS = [
        "at home", "for beginners", "in 5 minutes", "for kids to teach",
        "to impress friends", "for mental stimulation"
    ]
    for breed in BREEDS[:25]:
        for level in TRICK_LEVELS:
            titles.append(f"{breed} tricks to teach {level}")

    # NEW Pattern 29: best training tools for [breed]
    TRAINING_TOOLS = [
        "collar", "harness", "leash", "clicker", "treats", "crate"
    ]
    for breed in BREEDS[:20]:
        for tool in TRAINING_TOOLS:
            titles.append(f"best training {tool} for {breed}")
            titles.append(f"{breed} training {tool} recommendations")

    # NEW Pattern 30: [breed] training progress milestones
    for breed in BREEDS:
        titles.append(f"{breed} training milestones by age")
        titles.append(f"{breed} puppy training progress week by week")
        titles.append(f"what should a trained {breed} know")

    # NEW Pattern 31: stubborn [breed] training
    for breed in BREEDS:
        titles.append(f"stubborn {breed} training tips")
        titles.append(f"how to train a stubborn {breed}")
        titles.append(f"why is my {breed} so stubborn")

    # NEW Pattern 32: [breed] training without treats
    for breed in BREEDS:
        titles.append(f"{breed} training without treats")
        titles.append(f"how to train {breed} without food rewards")
        titles.append(f"lure free training for {breed}")

    # NEW Pattern 33: dog training games and mental stimulation for [breed]
    for breed in BREEDS:
        titles.append(f"dog training games for {breed}")
        titles.append(f"mental stimulation activities for {breed}")
        titles.append(f"fun training exercises for {breed}")

    # NEW Pattern 34: best collar and harness for [breed] training
    for breed in BREEDS:
        titles.append(f"best training collar for {breed}")
        titles.append(f"best harness for {breed} training")
        titles.append(f"{breed} collar vs harness training")

    # NEW Pattern 35: fearful and anxious [breed] training
    for breed in BREEDS:
        titles.append(f"fearful {breed} training tips")
        titles.append(f"how to train a scared {breed}")
        titles.append(f"{breed} fear aggression training nashville")

    # NEW Pattern 36: [breed] impulse control and self-control training
    for breed in BREEDS:
        titles.append(f"{breed} impulse control training")
        titles.append(f"how to teach {breed} self control")
        titles.append(f"{breed} impulse control exercises")

    # NEW Pattern 37: [breed] recall and off-leash reliability
    for breed in BREEDS:
        titles.append(f"{breed} recall training tips")
        titles.append(f"how to teach {breed} reliable recall")
        titles.append(f"{breed} off leash recall nashville")

    # NEW Pattern 38: when and what age to start training [breed]
    for breed in BREEDS:
        titles.append(f"when to start training a {breed}")
        titles.append(f"what age to start training {breed}")
        titles.append(f"best age to train a {breed}")

    # NEW Pattern 39: [breed] training for specific activities
    ACTIVITIES = [
        "hiking", "running", "swimming", "camping", "agility",
        "dock diving", "nose work", "flyball", "hunting", "therapy work"
    ]
    for breed in BREEDS[:20]:
        for activity in ACTIVITIES:
            titles.append(f"{breed} training for {activity}")
            titles.append(f"how to train {breed} for {activity}")

    # NEW Pattern 40: [breed] keeps [problem] no matter what / despite training
    for breed in BREEDS[:25]:
        for problem in PROBLEMS[:8]:
            titles.append(f"{breed} keeps {problem} no matter what")
            titles.append(f"{breed} still {problem} despite training")

    # NEW Pattern 41: [breed] resource guarding solutions
    for breed in BREEDS:
        titles.append(f"{breed} resource guarding solutions")
        titles.append(f"how to stop {breed} resource guarding")
        titles.append(f"{breed} resource guarding nashville trainer")

    # NEW Pattern 42: dog training cost in [Nashville area]
    for area in NASHVILLE_AREAS:
        titles.append(f"dog training cost in {area}")
        titles.append(f"how much does dog training cost in {area}")

    # NEW Pattern 43: [age] [breed] obedience training
    for age in AGES:
        for breed in BREEDS[:22]:
            titles.append(f"{age} {breed} obedience training")

    # NEW Pattern 44: [breed] training tips for first time owners
    for breed in BREEDS:
        titles.append(f"{breed} training tips for first time owners")
        titles.append(f"first time {breed} owner training guide")

    # NEW Pattern 45: how to exercise a [breed] / [breed] exercise needs
    for breed in BREEDS:
        titles.append(f"how to exercise a {breed}")
        titles.append(f"{breed} exercise requirements and training")

    # NEW Pattern 46: hyperactive [breed] and zoomies help
    for breed in BREEDS:
        titles.append(f"hyperactive {breed} training tips")
        titles.append(f"how to calm a hyperactive {breed}")
        titles.append(f"{breed} zoomies what to do")

    # NEW Pattern 47: [problem] control training tips
    for problem in PROBLEMS:
        titles.append(f"how to train dog to stop {problem} on command")
        titles.append(f"{problem} control training tips nashville")

    # NEW Pattern 48: [breed] door manners and boundary training
    for breed in BREEDS:
        titles.append(f"{breed} door manners training")
        titles.append(f"how to train {breed} door boundaries")

    # NEW Pattern 49: dog training for [specific scenario]
    SCENARIOS = [
        "reactive dogs", "fearful dogs", "aggressive dogs", "anxious dogs",
        "rescue dogs", "senior dogs", "deaf dogs", "blind dogs",
        "dogs with trauma", "high drive dogs", "working dogs", "sporting dogs"
    ]
    for scenario in SCENARIOS:
        titles.append(f"dog training for {scenario}")
        titles.append(f"tips for training {scenario}")
        titles.append(f"nashville trainer specializing in {scenario}")

    # NEW Pattern 50: [service] benefits and effectiveness
    for service in SERVICES:
        titles.append(f"benefits of {service} for your dog")
        titles.append(f"does {service} really work")
        titles.append(f"{service} results and success stories nashville")

    # NEW Pattern 51: [breed] training for [owner type]
    OWNER_TYPES = [
        "seniors", "busy families", "first responders", "athletes",
        "remote workers", "veterans", "apartment dwellers", "large families"
    ]
    for breed in BREEDS:
        for owner in OWNER_TYPES:
            titles.append(f"{breed} training for {owner}")
            titles.append(f"{breed} training advice for {owner}")

    # NEW Pattern 52: does [training method] work for [breed]
    TRAINING_METHODS = [
        "e-collar training", "prong collar training",
        "positive reinforcement only training", "clicker training",
        "balanced training", "alpha training", "force free training",
        "marker training"
    ]
    for breed in BREEDS:
        for method in TRAINING_METHODS:
            titles.append(f"does {method} work for {breed}")

    # NEW Pattern 53: what to do about [breed] [problem]
    for breed in BREEDS[:25]:
        for problem in PROBLEMS:
            titles.append(f"what to do about {breed} {problem}")
            titles.append(f"tips for dealing with {breed} {problem}")

    # NEW Pattern 54: [age] [breed] [problem] causes and solutions
    for age in AGES[:5]:
        for breed in BREEDS[:20]:
            for problem in PROBLEMS[:6]:
                titles.append(f"{age} {breed} {problem} causes and solutions")

    # NEW Pattern 55: is it too late to train a [age] [breed]
    OLDER_AGES = ["adult", "senior", "older dog", "2 year old", "1 year old", "adolescent"]
    for age in OLDER_AGES:
        for breed in BREEDS:
            titles.append(f"is it too late to train a {age} {breed}")
            titles.append(f"can you train a {age} {breed}")
            titles.append(f"training a {age} {breed} is it possible")

    # NEW Pattern 56: dog behaviorist / certified trainer in [area]
    for area in NASHVILLE_AREAS:
        titles.append(f"dog behaviorist {area}")
        titles.append(f"certified dog trainer {area}")
        titles.append(f"dog behavior consultant {area}")
        titles.append(f"reactive dog specialist {area}")

    # NEW Pattern 57: [breed] training on a budget
    for breed in BREEDS:
        titles.append(f"{breed} training on a budget")
        titles.append(f"cheap dog training for {breed}")
        titles.append(f"free dog training tips for {breed}")
        titles.append(f"affordable {breed} obedience training")

    # NEW Pattern 58: how to choose a dog trainer for [breed]
    for breed in BREEDS:
        titles.append(f"how to choose a dog trainer for {breed}")
        titles.append(f"what to look for in a {breed} trainer")
        titles.append(f"questions to ask a {breed} dog trainer")

    # NEW Pattern 59: [problem] in multi-dog households
    for problem in PROBLEMS:
        titles.append(f"{problem} in multi dog households")
        titles.append(f"managing {problem} with multiple dogs nashville")
        titles.append(f"training two dogs {problem} solutions")
        titles.append(f"how to stop {problem} in a multi dog home")

    # NEW Pattern 60: [breed] enrichment and mental stimulation activities
    ENRICHMENT_TYPES = [
        "puzzle feeders", "nose work", "agility", "trick training",
        "scent work", "sniff walks", "fetch games", "tug games"
    ]
    for breed in BREEDS[:20]:
        for enrichment in ENRICHMENT_TYPES:
            titles.append(f"{breed} enrichment with {enrichment}")
            titles.append(f"how to use {enrichment} for {breed} mental stimulation")

    return list(set(titles))

def create_post(title, output_dir):
    """Create a single blog post"""
    slug = slugify(title)
    output_path = output_dir / f"{slug}.html"

    if output_path.exists():
        return None

    # Read template
    template_path = output_dir / "template.html"
    if not template_path.exists():
        return None

    template = template_path.read_text()

    # Generate content
    display_title = title.title().replace("Tn", "TN")
    date = datetime.now().strftime("%B %d, %Y")
    meta_desc = f"Expert guide to {title}. Professional dog training tips from Nashville's trusted trainers. Free consultation available."[:160]
    keywords = f"dog training, {title}, Nashville dog training, {title.split()[0]} training"

    content = f"""<p>If you're searching for help with {title}, you've come to the right place. This is one of the most common challenges we help Nashville dog owners overcome.</p>

<p>In this comprehensive guide, we'll break down exactly what's causing the issue and give you practical, actionable steps to fix it. These are the same techniques we use in our in-home training sessions throughout Nashville, Franklin, Brentwood, and the greater Middle Tennessee area.</p>

<h2>Understanding the Issue</h2>
<p>The first step to solving any training challenge is understanding why it's happening. Dogs don't misbehave out of spite - there's always an underlying cause, whether it's lack of training, anxiety, overexcitement, or simply not understanding what we want from them.</p>

<h2>The Solution</h2>
<p>Here's what we recommend for addressing {title.lower()}:</p>
<ol>
<li><strong>Identify the trigger</strong> - What specifically sets off the behavior?</li>
<li><strong>Manage the environment</strong> - Set your dog up for success by controlling the situation</li>
<li><strong>Train an alternative</strong> - Give your dog something appropriate to do instead</li>
<li><strong>Be consistent</strong> - Everyone in the household follows the same rules</li>
<li><strong>Be patient</strong> - Real behavior change takes 2-4 weeks of consistent practice</li>
</ol>

<h2>When to Get Professional Help</h2>
<p>While many issues can be addressed at home with consistent training, some situations benefit from professional guidance. If you're in the Nashville area and want faster results with expert support, our in-home training sessions are designed for exactly these challenges.</p>

<p>We serve Nashville, Franklin, Brentwood, Murfreesboro, Hendersonville, and the entire Middle Tennessee region. Contact us for a free consultation to discuss your specific situation.</p>"""

    # Fill template
    html = template.replace("{{TITLE}}", display_title)
    html = html.replace("{{META_DESCRIPTION}}", meta_desc)
    html = html.replace("{{KEYWORDS}}", keywords)
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{DATE}}", date)
    html = html.replace("{{SHORT_TITLE}}", display_title[:40])
    html = html.replace("{{CONTENT}}", content)

    output_path.write_text(html)
    return {"slug": slug, "title": display_title, "url": f"https://magsbrother.github.io/nashvilledogtraining/blog/{slug}.html"}

def main():
    blog_dir = Path(__file__).parent.parent / "blog"
    titles = generate_title_variations()
    print(f"Generated {len(titles)} unique title combinations")

    created = 0
    for title in titles:
        result = create_post(title, blog_dir)
        if result:
            created += 1
            if created % 100 == 0:
                print(f"Created {created} posts...")

    print(f"\nTotal new posts created: {created}")

    # Update sitemap
    sitemap_path = Path(__file__).parent.parent / "sitemap.xml"
    posts = list(blog_dir.glob("*.html"))
    posts = [p for p in posts if p.name not in ["template.html", "index.html"]]

    urls = set()
    urls.add("https://magsbrother.github.io/nashvilledogtraining/")
    urls.add("https://magsbrother.github.io/nashvilledogtraining/blog/")
    for post in posts:
        urls.add(f"https://magsbrother.github.io/nashvilledogtraining/blog/{post.name}")

    header = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    entries = []
    for url in sorted(urls):
        priority = '1.0' if 'blog' not in url else '0.7'
        entries.append(f'''  <url>
    <loc>{url}</loc>
    <lastmod>2026-03-27</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>''')
    footer = '</urlset>'
    sitemap_path.write_text(header + '\n' + '\n'.join(entries) + '\n' + footer)
    print(f"Updated sitemap with {len(urls)} URLs")

    # Update blog index
    post_items = []
    for post in sorted(posts, key=lambda x: x.stat().st_mtime, reverse=True)[:500]:
        content = post.read_text()
        title_match = re.search(r'<h1>(.+?)</h1>', content)
        title = title_match.group(1) if title_match else post.stem.replace("-", " ").title()
        post_items.append(f'<li><a href="{post.name}">{title}</a></li>')

    index_path = blog_dir / "index.html"
    index_content = index_path.read_text()
    # Update just the list
    new_list = "\n".join(post_items)
    index_content = re.sub(r'<ul>.*?</ul>', f'<ul>\n{new_list}\n</ul>', index_content, flags=re.DOTALL)
    index_path.write_text(index_content)
    print(f"Updated blog index")

if __name__ == "__main__":
    main()
