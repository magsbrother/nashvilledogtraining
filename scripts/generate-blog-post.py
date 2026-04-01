#!/usr/bin/env python3
"""
Blog Post Generator for Nashville Dog Training

Generates SEO-optimized blog posts targeting long-tail keywords.
Run locally or via scheduled trigger.

Usage:
    python generate-blog-post.py
    python generate-blog-post.py --topic "leash training tips"
    python generate-blog-post.py --batch 10
"""

import argparse
import os
import re
import random
from datetime import datetime
from pathlib import Path

# Topic categories for SEO targeting
TOPIC_CATEGORIES = {
    "behavioral": [
        "how to stop dog from jumping on guests",
        "why does my dog bark at other dogs",
        "dog separation anxiety solutions",
        "how to stop dog from pulling on leash",
        "dog aggression toward strangers",
        "why does my dog growl at family members",
        "how to calm an anxious dog",
        "dog resource guarding food bowl",
        "why does my dog bite the leash",
        "how to stop dog from chasing cars",
        "dog reactivity on walks",
        "why does my dog destroy things when alone",
        "how to stop excessive barking",
        "dog fear of loud noises",
        "why does my dog nip at heels",
        "how to stop dog from eating poop",
        "dog mounting behavior fix",
        "why does my dog lick everything",
        "dog obsessive behavior help",
        "how to stop dog from begging",
        "dog whining for attention",
        "why does my dog follow me everywhere",
        "dog territorial aggression",
        "how to stop leash aggression",
        "dog fear of strangers",
        "why does my dog shake",
        "dog pacing at night",
        "how to calm hyperactive dog",
        "dog wont stop licking paws",
        "why does my dog hide",
    ],
    "training_basics": [
        "how to teach dog to sit",
        "how to teach dog to stay",
        "how to teach reliable recall",
        "how to crate train a dog",
        "how to potty train a puppy fast",
        "how to teach dog to heel",
        "how to teach dog place command",
        "best age to start dog training",
        "how long does dog training take",
        "positive reinforcement vs balanced training",
        "how to use treats in dog training",
        "clicker training for beginners",
        "how to teach dog to drop it",
        "how to teach dog to leave it",
        "how to teach dog off command",
        "how to teach dog to shake",
        "how to teach dog to roll over",
        "how to teach dog to speak",
        "how to teach dog to wait",
        "how to teach dog down command",
        "how to teach dog to fetch",
        "how to teach dog to come every time",
        "e collar training guide",
        "prong collar training tips",
        "marker training for dogs",
        "how to phase out treats in training",
        "training dog with hand signals",
        "verbal commands vs hand signals dogs",
        "how to proof dog commands",
        "training dog around distractions",
    ],
    "puppy": [
        "puppy biting how to stop",
        "puppy socialization checklist",
        "when to start training a puppy",
        "puppy crate training schedule",
        "how to stop puppy from jumping",
        "puppy potty training apartment",
        "puppy leash training first time",
        "best puppy training treats",
        "puppy fear periods explained",
        "how to stop puppy crying at night",
        "8 week old puppy training",
        "12 week old puppy training",
        "16 week old puppy training",
        "puppy first week home tips",
        "puppy chewing everything help",
        "puppy wont sleep through night",
        "how to socialize shy puppy",
        "puppy growling when picked up",
        "puppy wont eat from bowl",
        "puppy scared of everything",
        "puppy barking at other dogs",
        "how to stop puppy zoomies",
        "puppy humping problem",
        "puppy resource guarding toys",
        "raising confident puppy",
    ],
    "breed_specific": [
        "training tips for german shepherds",
        "how to train a golden retriever",
        "labrador training guide",
        "pit bull training tips",
        "training stubborn dog breeds",
        "high energy dog training",
        "small dog training tips",
        "herding dog training basics",
        "working dog training at home",
        "rescue dog training tips",
        "australian shepherd training guide",
        "border collie training tips",
        "husky training challenges",
        "beagle training stubborn",
        "rottweiler training guide",
        "doberman training tips",
        "french bulldog training",
        "boxer dog training guide",
        "dachshund training tips",
        "great dane puppy training",
        "poodle training guide",
        "shih tzu training tips",
        "yorkie training challenges",
        "chihuahua behavior training",
        "corgi training herding instinct",
        "bulldog training tips",
        "cocker spaniel training",
        "australian cattle dog training",
        "bernese mountain dog training",
        "maltese training guide",
    ],
    "local_nashville": [
        "best dog training nashville tn",
        "in home dog training nashville",
        "dog trainers franklin tn",
        "brentwood dog training services",
        "murfreesboro dog obedience classes",
        "dog training near me nashville",
        "nashville puppy training classes",
        "affordable dog training nashville",
        "private dog training lessons nashville",
        "dog behavior specialist nashville",
        "dog training hendersonville tn",
        "mt juliet dog trainers",
        "dog training spring hill tn",
        "smyrna tn dog training",
        "gallatin dog training services",
        "dog training antioch tn",
        "dog training bellevue nashville",
        "dog training green hills nashville",
        "dog training hermitage tn",
        "dog training madison tn",
        "dog training nolensville tn",
        "dog training thompsons station tn",
        "dog training la vergne tn",
        "dog training goodlettsville tn",
        "dog training white house tn",
        "dog training lebanon tn",
        "dog training columbia tn",
        "dog training dickson tn",
        "dog training clarksville tn",
        "williamson county dog training",
        "davidson county dog trainers",
        "rutherford county dog training",
        "sumner county dog trainers",
        "wilson county dog training",
    ],
    "specific_problems": [
        "dog wont come when called",
        "dog pulls so hard on leash",
        "dog barks at doorbell",
        "dog jumps on counter",
        "dog steals food from table",
        "dog runs away at dog park",
        "dog lunges at other dogs",
        "dog afraid of car rides",
        "dog wont walk on leash",
        "dog ignores commands outside",
        "dog only listens with treats",
        "dog wont listen to husband",
        "dog goes crazy when guests arrive",
        "dog marks inside house",
        "dog digs in yard constantly",
        "dog chases cat in house",
        "dog wont let you trim nails",
        "dog bites when grooming",
        "dog aggressive on leash only",
        "dog barks at neighbors",
        "dog escapes yard constantly",
        "dog wont go in crate",
        "dog bolts out front door",
        "dog wont eat unless hand fed",
        "dog guards couch from people",
        "dog protective of owner",
        "dog attacks vacuum cleaner",
        "dog hates being alone",
        "dog wont go outside to potty",
        "dog reverse sneezing anxiety",
    ],
    "situations": [
        "training dog for apartment living",
        "training dog around babies",
        "training dog around toddlers",
        "introducing dog to new baby",
        "training two dogs at once",
        "training older dog new tricks",
        "training dog after moving",
        "training dog after adoption",
        "training dog with deaf owner",
        "training dog for elderly owner",
        "dog training after trauma",
        "training nervous rescue dog",
        "training dog from shelter",
        "training dog around chickens",
        "training dog not to chase cats",
        "dog training for first time owners",
        "training dog in small apartment",
        "training dog without yard",
        "training dog for off leash",
        "training dog for hiking",
    ],
    "cost_questions": [
        "how much does dog training cost",
        "is dog training worth it",
        "private dog training vs group classes",
        "board and train vs in home training",
        "how many dog training sessions needed",
        "dog training packages explained",
        "why is dog training so expensive",
        "free dog training tips",
        "diy dog training vs professional",
        "when to hire a dog trainer",
    ],
}

# Article templates for structure
ARTICLE_STRUCTURES = [
    {
        "type": "how_to",
        "sections": ["intro", "why_it_happens", "step_by_step", "common_mistakes", "when_to_get_help", "conclusion"]
    },
    {
        "type": "listicle",
        "sections": ["intro", "tip_1", "tip_2", "tip_3", "tip_4", "tip_5", "pro_tip", "conclusion"]
    },
    {
        "type": "problem_solution",
        "sections": ["intro", "understanding_the_problem", "root_causes", "the_solution", "implementation", "conclusion"]
    },
    {
        "type": "guide",
        "sections": ["intro", "what_you_need", "preparation", "the_process", "troubleshooting", "next_steps", "conclusion"]
    },
]

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:60]

def generate_meta_description(topic, location="Nashville"):
    """Generate SEO meta description."""
    templates = [
        f"Learn {topic} with expert tips from {location}'s trusted dog trainers. Proven methods that work. Free consultation available.",
        f"Struggling with {topic}? Our {location} dog training experts share proven solutions. Get results in weeks, not months.",
        f"Expert guide to {topic} from professional dog trainers serving {location}. Real solutions for real dog owners.",
        f"Discover how to handle {topic} with our step-by-step guide. Trusted by {location} dog owners. Free consultation.",
    ]
    return random.choice(templates)[:160]

def generate_keywords(topic, category):
    """Generate relevant keywords."""
    base_keywords = [
        "dog training", "Nashville dog training", "dog trainer Nashville TN",
        "in-home dog training", "dog obedience", topic
    ]

    category_keywords = {
        "behavioral": ["dog behavior", "behavior modification", "dog psychology"],
        "training_basics": ["obedience training", "basic commands", "dog commands"],
        "puppy": ["puppy training", "puppy classes", "new puppy"],
        "breed_specific": ["breed training", "dog breed behavior"],
        "local_nashville": ["Nashville TN", "Middle Tennessee", "Franklin TN", "Brentwood TN"],
        "specific_problems": ["dog problems", "fix dog behavior", "stop dog from"],
    }

    keywords = base_keywords + category_keywords.get(category, [])
    return ", ".join(keywords[:10])

def generate_placeholder_content(topic, structure):
    """Generate placeholder content structure."""
    title = topic.title().replace("Tn", "TN")

    content_parts = []

    # Intro
    content_parts.append(f"""<p>If you're dealing with {topic.lower()}, you're not alone. This is one of the most common challenges Nashville dog owners face, and the good news is it's completely fixable with the right approach.</p>

<p>In this guide, we'll cover exactly what's causing the problem and give you actionable steps to solve it. These are the same techniques we use in our in-home training sessions throughout Nashville, Franklin, Brentwood, and the surrounding areas.</p>""")

    # Main sections based on structure
    if structure["type"] == "how_to":
        content_parts.append("""<h2>Why This Happens</h2>
<p>Understanding the root cause is the first step to fixing any behavior issue. Dogs don't do things to spite us - there's always an underlying reason, whether it's lack of training, anxiety, overexcitement, or simply not knowing what we expect from them.</p>

<h2>Step-by-Step Solution</h2>
<p>Here's the exact process we use with our Nashville training clients:</p>
<ol>
<li><strong>Assess the trigger</strong> - Identify exactly what causes the behavior to happen</li>
<li><strong>Manage the environment</strong> - Set your dog up for success by controlling the situation</li>
<li><strong>Train an alternative behavior</strong> - Give your dog something else to do instead</li>
<li><strong>Practice consistently</strong> - Repetition is key to making the new behavior stick</li>
<li><strong>Gradually increase difficulty</strong> - Slowly add distractions once the basics are solid</li>
</ol>

<h2>Common Mistakes to Avoid</h2>
<ul>
<li>Punishing after the fact (dogs only connect consequences to what they're doing RIGHT NOW)</li>
<li>Inconsistency between family members</li>
<li>Moving too fast before the basics are solid</li>
<li>Giving up too soon - real change takes 2-4 weeks minimum</li>
</ul>""")

    elif structure["type"] == "listicle":
        content_parts.append("""<h2>1. Start With Management</h2>
<p>Before you can train, you need to prevent the unwanted behavior from being practiced. Every time your dog rehearses a behavior, it gets stronger. Set up your environment to make success easy.</p>

<h2>2. Use High-Value Rewards</h2>
<p>Regular kibble won't cut it for tough behavior challenges. Use real meat, cheese, or whatever makes your dog light up. The reward needs to be worth more than the behavior you're competing against.</p>

<h2>3. Keep Sessions Short</h2>
<p>5-10 minutes of focused training beats an hour of unfocused practice. Dogs learn best in short bursts with plenty of breaks.</p>

<h2>4. Be Consistent</h2>
<p>Everyone in the household needs to follow the same rules. Mixed signals confuse dogs and slow down progress.</p>

<h2>5. Practice in Real Situations</h2>
<p>Training in your living room is a start, but your dog needs to learn to perform around real distractions. Gradually add difficulty once the basics are solid.</p>

<h3>Pro Tip</h3>
<p>The best time to train is when your dog is slightly hungry and has had a chance to burn off some energy. Too hyper and they can't focus; too tired and they won't be motivated.</p>""")

    else:
        content_parts.append("""<h2>Understanding the Problem</h2>
<p>This behavior usually stems from one of three root causes: lack of training, anxiety/stress, or the behavior has been accidentally reinforced over time. Understanding which category your dog falls into will determine the best approach.</p>

<h2>The Solution</h2>
<p>The fix involves three components: management (preventing the behavior), training (teaching an alternative), and consistency (making sure everyone follows the same rules). Skip any of these and you'll struggle to see lasting results.</p>

<h2>How to Implement</h2>
<p>Start by controlling the environment so your dog can't practice the unwanted behavior. Then, train a replacement behavior that's incompatible with the problem. Finally, be patient - real behavior change takes 2-4 weeks of consistent practice.</p>

<h2>When Progress Stalls</h2>
<p>If you've been consistent for 2-3 weeks and aren't seeing improvement, it's time to reassess. You might be missing a trigger, moving too fast, or dealing with an underlying anxiety issue that needs professional help.</p>""")

    # Conclusion with local CTA
    content_parts.append("""<h2>When to Call a Professional</h2>
<p>While many behavior issues can be solved with consistent training at home, some situations benefit from professional guidance. If you're dealing with aggression, severe anxiety, or simply want faster results with expert support, that's where we come in.</p>

<p>Our in-home training sessions are designed for exactly these situations. We come to you, work in your environment, and train both you and your dog. Serving Nashville, Franklin, Brentwood, Murfreesboro, and the entire Middle Tennessee area.</p>""")

    return "\n\n".join(content_parts)

def create_blog_post(topic, category, output_dir):
    """Create a single blog post file."""
    slug = slugify(topic)
    structure = random.choice(ARTICLE_STRUCTURES)

    # Read template
    template_path = Path(__file__).parent.parent / "blog" / "template.html"
    if not template_path.exists():
        print(f"Template not found at {template_path}")
        return None

    template = template_path.read_text()

    # Generate content
    title = topic.title().replace("Tn", "TN").replace(" Tн", " TN")
    content = generate_placeholder_content(topic, structure)
    meta_desc = generate_meta_description(topic)
    keywords = generate_keywords(topic, category)
    date = datetime.now().strftime("%B %d, %Y")
    short_title = title[:40] + "..." if len(title) > 40 else title

    # Fill template
    html = template.replace("{{TITLE}}", title)
    html = html.replace("{{META_DESCRIPTION}}", meta_desc)
    html = html.replace("{{KEYWORDS}}", keywords)
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{DATE}}", date)
    html = html.replace("{{SHORT_TITLE}}", short_title)
    html = html.replace("{{CONTENT}}", content)

    # Write file
    output_path = output_dir / f"{slug}.html"
    output_path.write_text(html)

    return {
        "slug": slug,
        "title": title,
        "path": str(output_path),
        "url": f"https://magsbrother.github.io/nashvilledogtraining/blog/{slug}.html"
    }

def generate_batch(count, output_dir):
    """Generate multiple blog posts."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect all topics
    all_topics = []
    for category, topics in TOPIC_CATEGORIES.items():
        for topic in topics:
            all_topics.append((topic, category))

    # Shuffle and take requested count
    random.shuffle(all_topics)
    topics_to_generate = all_topics[:count]

    results = []
    for topic, category in topics_to_generate:
        result = create_blog_post(topic, category, output_dir)
        if result:
            results.append(result)
            print(f"Created: {result['title']}")

    return results

def update_sitemap(blog_posts, sitemap_path):
    """Update sitemap with new blog posts."""
    sitemap_path = Path(sitemap_path)

    # Read existing sitemap
    content = sitemap_path.read_text()

    # Find insertion point (before closing </urlset>)
    insert_point = content.rfind("</urlset>")

    # Generate new entries
    new_entries = []
    today = datetime.now().strftime("%Y-%m-%d")
    for post in blog_posts:
        entry = f"""  <url>
    <loc>{post['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""
        new_entries.append(entry)

    # Insert new entries
    new_content = content[:insert_point] + "".join(new_entries) + content[insert_point:]
    sitemap_path.write_text(new_content)
    print(f"Updated sitemap with {len(blog_posts)} new posts")

def create_blog_index(blog_dir):
    """Create blog index page."""
    blog_dir = Path(blog_dir)
    posts = list(blog_dir.glob("*.html"))
    posts = [p for p in posts if p.name not in ["template.html", "index.html"]]

    # Generate post list
    post_items = []
    for post in sorted(posts, key=lambda x: x.stat().st_mtime, reverse=True):
        # Extract title from file
        content = post.read_text()
        title_match = re.search(r'<h1>(.+?)</h1>', content)
        title = title_match.group(1) if title_match else post.stem.replace("-", " ").title()

        post_items.append(f'<li><a href="{post.name}">{title}</a></li>')

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dog Training Blog | Nashville Dog Training</title>
<meta name="description" content="Expert dog training tips, guides, and advice from Nashville's trusted in-home dog trainers. Learn how to solve common behavior problems.">
<link rel="canonical" href="https://magsbrother.github.io/nashvilledogtraining/blog/">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
body {{ font-family: 'Outfit', sans-serif; background: #FBF8F1; color: #2D2A26; line-height: 1.7; margin: 0; }}
.nav {{ background: #1B3A2D; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }}
.nav a {{ color: #FBF8F1; text-decoration: none; font-family: 'DM Serif Display', serif; }}
.nav-cta {{ background: #D4A745; color: #1B3A2D !important; padding: 10px 20px; border-radius: 50px; font-family: 'Outfit', sans-serif !important; font-weight: 600; }}
.container {{ max-width: 800px; margin: 0 auto; padding: 40px 24px; }}
h1 {{ font-family: 'DM Serif Display', serif; color: #1B3A2D; margin-bottom: 24px; }}
ul {{ list-style: none; padding: 0; }}
li {{ padding: 16px 0; border-bottom: 1px solid #e0ddd5; }}
li a {{ color: #2A5A45; text-decoration: none; font-size: 1.1rem; }}
li a:hover {{ color: #D4A745; }}
</style>
</head>
<body>
<nav class="nav">
  <a href="../">Nashville Dog Training</a>
  <a href="../#consult" class="nav-cta">Free Consultation</a>
</nav>
<div class="container">
<h1>Dog Training Tips & Guides</h1>
<p>Expert advice from Nashville's trusted in-home dog trainers. Browse our articles to solve common behavior problems and build a better relationship with your dog.</p>
<ul>
{"".join(post_items)}
</ul>
</div>
</body>
</html>"""

    index_path = blog_dir / "index.html"
    index_path.write_text(index_html)
    print(f"Created blog index with {len(posts)} posts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SEO blog posts for Nashville Dog Training")
    parser.add_argument("--topic", help="Specific topic to write about")
    parser.add_argument("--batch", type=int, default=1, help="Number of posts to generate")
    parser.add_argument("--category", choices=list(TOPIC_CATEGORIES.keys()), help="Topic category")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    blog_dir = script_dir.parent / "blog"
    sitemap_path = script_dir.parent / "sitemap.xml"

    if args.topic:
        category = args.category or "specific_problems"
        result = create_blog_post(args.topic, category, blog_dir)
        if result:
            print(f"\nCreated: {result['url']}")
            update_sitemap([result], sitemap_path)
    else:
        results = generate_batch(args.batch, blog_dir)
        if results:
            update_sitemap(results, sitemap_path)
            create_blog_index(blog_dir)
            print(f"\nGenerated {len(results)} posts")
