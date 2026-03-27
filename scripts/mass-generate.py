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
