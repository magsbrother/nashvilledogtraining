#!/usr/bin/env python3
"""
Mass SEO Blog Post Generator for Nashville Dog Training
Generates 50 SEO-optimized HTML blog posts per run.
Tracks used topics in a JSON file to avoid duplicates.
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).resolve().parent.parent
BLOG_DIR    = REPO_ROOT / "blog"
TRACKER     = REPO_ROOT / "scripts" / "used-topics.json"
SITEMAP     = REPO_ROOT / "sitemap.xml"
SITE_URL    = "https://nashvilledogtraining.com"

POSTS_PER_RUN = 50

# ── topic pool ─────────────────────────────────────────────────────────────
TOPICS = [
    # Obedience basics
    ("how-to-teach-your-dog-to-sit",          "How to Teach Your Dog to Sit: A Step-by-Step Guide for Nashville Owners"),
    ("how-to-teach-your-dog-to-stay",         "How to Teach Your Dog to Stay: Tips from Nashville's Top Trainers"),
    ("how-to-teach-your-dog-to-come",         "Recall Training: How to Teach Your Dog to Come Every Time"),
    ("how-to-teach-down-command",             "How to Teach the Down Command to Your Dog"),
    ("how-to-teach-heel-command",             "Teaching Your Dog to Heel: A Complete Nashville Guide"),
    ("how-to-teach-leave-it-command",         "Leave It! How to Train Your Dog to Ignore Distractions"),
    ("how-to-teach-drop-it-command",          "Drop It Command: Keep Your Dog Safe with This Simple Skill"),
    ("how-to-teach-place-command",            "The 'Place' Command: The Most Underrated Dog Training Skill"),
    ("how-to-teach-dog-to-wait",              "Wait vs Stay: Teaching Your Dog Both Commands"),
    ("how-to-teach-dog-off-command",          "Off! Teaching Your Dog Not to Jump on People"),
    # Leash & walking
    ("stop-dog-pulling-on-leash",             "Stop Your Dog Pulling on the Leash for Good"),
    ("loose-leash-walking-guide",             "Loose-Leash Walking: The Complete Nashville Dog Owner's Guide"),
    ("best-harness-vs-collar-for-training",   "Harness vs Collar: Which Is Best for Dog Training in Nashville?"),
    ("how-to-walk-two-dogs-at-once",          "How to Walk Two Dogs at Once Without Losing Your Mind"),
    ("dog-pulling-solutions-nashville",       "5 Proven Solutions for Dogs That Pull in Nashville Parks"),
    # Puppy topics
    ("puppy-training-basics-nashville",       "Puppy Training Basics for Nashville New Dog Owners"),
    ("how-to-potty-train-a-puppy",            "How to Potty Train a Puppy: Nashville's Complete Guide"),
    ("puppy-socialization-guide",             "Puppy Socialization: Why the First 16 Weeks Are Critical"),
    ("puppy-biting-how-to-stop",              "How to Stop Puppy Biting: Bite Inhibition Training"),
    ("crate-training-puppy-guide",            "Crate Training Your Puppy the Right Way"),
    ("puppy-schedule-daily-routine",          "The Ideal Daily Schedule for Your New Puppy"),
    ("best-age-to-start-dog-training",        "What's the Best Age to Start Training Your Dog?"),
    ("puppy-first-week-home-tips",            "Your Puppy's First Week Home: Survival Tips for Nashville Families"),
    # Behavior problems
    ("how-to-stop-dog-barking",               "How to Stop Excessive Barking: A Nashville Dog Trainer's Guide"),
    ("dog-separation-anxiety-solutions",      "Dog Separation Anxiety: Causes, Signs, and Real Solutions"),
    ("how-to-stop-dog-jumping-guests",        "Stop Your Dog Jumping on Guests Once and For All"),
    ("dog-aggression-training-nashville",     "Dog Aggression Training in Nashville: What You Need to Know"),
    ("reactive-dog-training-tips",            "Reactive Dog Training: How to Help a Dog That Lunges and Barks"),
    ("dog-resource-guarding-solutions",       "Resource Guarding in Dogs: How to Safely Address It"),
    ("how-to-stop-destructive-chewing",       "How to Stop Destructive Chewing in Dogs"),
    ("dog-counter-surfing-fix",               "Counter Surfing: How to Keep Your Dog Off the Kitchen Counter"),
    ("dog-door-manners-training",             "Door Manners: Stop Your Dog Bolting Out the Front Door"),
    ("fear-based-behavior-dog-training",      "Understanding and Training Fear-Based Behaviors in Dogs"),
    # Local Nashville content
    ("dog-training-nashville-tn",             "Dog Training in Nashville, TN: What to Expect"),
    ("dog-trainer-franklin-tn",               "Finding the Right Dog Trainer in Franklin, TN"),
    ("dog-training-brentwood-tn",             "In-Home Dog Training in Brentwood, TN: Is It Worth It?"),
    ("dog-training-murfreesboro-tn",          "Dog Training Services in Murfreesboro, TN"),
    ("dog-training-hendersonville-tn",        "Dog Training in Hendersonville, TN: Local Guide"),
    ("dog-training-mt-juliet-tn",             "Dog Trainer in Mt. Juliet, TN: Everything You Need to Know"),
    ("best-dog-parks-nashville",              "Best Dog Parks in Nashville: A Trainer's Review"),
    ("dog-friendly-restaurants-nashville",    "Dog-Friendly Restaurants in Nashville: Tips for Well-Behaved Dogs"),
    ("dog-training-spring-hill-tn",           "Dog Training in Spring Hill, TN: In-Home Options"),
    ("dog-training-smyrna-tn",                "Dog Training in Smyrna, TN: What Nashville Area Trainers Offer"),
    # In-home training
    ("in-home-dog-training-benefits",         "In-Home Dog Training: 7 Reasons It Outperforms Group Classes"),
    ("how-in-home-dog-training-works",        "How In-Home Dog Training Works: Nashville Owner's Guide"),
    ("in-home-vs-board-and-train",            "In-Home Training vs Board and Train: Which Is Right for Your Dog?"),
    ("in-home-training-cost-nashville",       "How Much Does In-Home Dog Training Cost in Nashville?"),
    # Breed-specific
    ("golden-retriever-training-tips",        "Golden Retriever Training Tips for Nashville Families"),
    ("labrador-training-guide-nashville",     "Labrador Retriever Training Guide for Nashville Dog Owners"),
    ("german-shepherd-training-nashville",    "German Shepherd Training in Nashville: Breed-Specific Tips"),
    ("french-bulldog-training-tips",          "French Bulldog Training: What Nashville Owners Need to Know"),
    ("doodle-dog-training-guide",             "Goldendoodle & Labradoodle Training: Nashville Doodle Guide"),
    ("pitbull-training-tips-nashville",       "Pit Bull Training Tips: Busting Myths in Nashville"),
    ("small-dog-training-tips",               "Small Dog Training: Why Little Dogs Need Training Too"),
    ("rescue-dog-training-guide",             "Rescue Dog Training: A Nashville Guide to the First 90 Days"),
    # Methods & philosophy
    ("balanced-dog-training-explained",       "Balanced Dog Training Explained: What It Means and Why It Works"),
    ("positive-reinforcement-training",       "Positive Reinforcement Dog Training: A Nashville Trainer's Guide"),
    ("e-collar-training-facts",               "E-Collar Training: Facts, Myths, and Safe Use in Nashville"),
    ("marker-training-dogs-guide",            "Marker Training for Dogs: How to Use a Clicker or Word Marker"),
    ("dog-training-consistency-tips",         "Why Consistency Is the #1 Dog Training Rule"),
    # Health & lifestyle
    ("exercise-needs-by-dog-breed",           "Exercise Needs by Dog Breed: Nashville Owner's Reference Guide"),
    ("mental-stimulation-for-dogs",           "Mental Stimulation for Dogs: 10 Ideas Nashville Trainers Love"),
    ("dog-nutrition-training-connection",     "How Your Dog's Diet Affects Their Training Performance"),
    ("dog-enrichment-activities-nashville",   "Dog Enrichment Activities for Nashville's Active Pet Owners"),
    ("how-much-exercise-does-a-dog-need",     "How Much Exercise Does Your Dog Really Need?"),
    # Advanced skills
    ("off-leash-training-guide",              "Off-Leash Training: Is Your Dog Ready? Nashville Guide"),
    ("dog-distraction-proofing-training",     "Distraction Proofing: Train Your Dog to Focus Anywhere"),
    ("advanced-obedience-training-nashville", "Advanced Obedience Training in Nashville: Next-Level Skills"),
    ("dog-impulse-control-training",          "Impulse Control Training: Calm Your Dog's Excitement"),
    ("dog-training-real-world-scenarios",     "Real-World Dog Training: Why Context Matters"),
    # FAQs & guides
    ("how-long-does-dog-training-take",       "How Long Does Dog Training Take? Honest Nashville Answers"),
    ("how-to-choose-a-dog-trainer-nashville", "How to Choose a Dog Trainer in Nashville: 7 Key Questions"),
    ("dog-training-cost-guide-nashville",     "Dog Training Cost in Nashville: What You Should Expect to Pay"),
    ("group-class-vs-private-training",       "Group Dog Classes vs Private Training: Which Is Better?"),
    ("dog-training-mistakes-owners-make",     "10 Dog Training Mistakes Nashville Owners Commonly Make"),
    ("when-to-hire-professional-dog-trainer", "When Should You Hire a Professional Dog Trainer?"),
    ("dog-training-schedule-for-owners",      "Building a Dog Training Schedule That Fits Your Nashville Life"),
    # Kids & dogs
    ("dog-training-with-kids-in-home",        "Dog Training with Kids: How to Keep Your Home Safe and Happy"),
    ("teaching-kids-to-interact-with-dogs",   "Teaching Kids to Interact Safely with Dogs"),
    ("family-dog-training-tips-nashville",    "Family Dog Training Tips for Nashville Households"),
    # Seasonal
    ("summer-dog-training-tips-nashville",    "Summer Dog Training Tips for Nashville's Hot Weather"),
    ("holiday-dog-training-tips",             "Holiday Dog Training: Prep Your Dog for Guests and Chaos"),
    ("spring-dog-training-refresh",           "Spring Dog Training Refresh: Reset Your Dog's Manners"),
    ("winter-indoor-dog-training-ideas",      "Winter Dog Training: Keeping Skills Sharp Indoors"),
    # Multi-dog
    ("training-multiple-dogs-guide",          "Training Multiple Dogs: Nashville's Guide to a Harmonious Pack"),
    ("introducing-new-dog-to-resident-dog",   "How to Introduce a New Dog to Your Resident Dog"),
    # Special situations
    ("dog-training-after-having-baby",        "Dog Training After Having a Baby: Nashville Family Guide"),
    ("senior-dog-training-tips",              "Senior Dog Training: It's Never Too Late to Learn"),
    ("dog-training-for-first-time-owners",    "Dog Training for First-Time Nashville Dog Owners"),
    ("training-a-rescue-with-unknown-history","Training a Rescue Dog with an Unknown History"),
    ("dog-training-apartment-nashville",      "Dog Training in a Nashville Apartment: Making It Work"),
    # Trust & testimonials
    ("why-choose-nashville-dog-training",     "Why Nashville Dog Training: Our Approach and Promise"),
    ("nashville-dog-training-results",        "Real Results: Nashville Dog Training Success Stories"),
    ("dog-training-free-consultation",        "Free Dog Training Consultation in Nashville: What to Expect"),
]


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").title()


def load_used() -> set:
    if TRACKER.exists():
        with open(TRACKER) as f:
            return set(json.load(f))
    return set()


def save_used(used: set):
    with open(TRACKER, "w") as f:
        json.dump(sorted(used), f, indent=2)


# ── HTML template ──────────────────────────────────────────────────────────

def build_post_html(slug: str, title: str, date_str: str) -> str:
    """Generate a full SEO-optimized HTML blog post."""

    # derive a meta description from the title
    meta_desc = f"{title} | Expert advice from Nashville's trusted in-home dog trainers."

    # Build body content paragraphs keyed off the slug topic
    h2_sections = build_sections(slug, title)

    sections_html = ""
    for h2, paragraphs in h2_sections:
        sections_html += f"    <h2>{h2}</h2>\n"
        for p in paragraphs:
            sections_html += f"    <p>{p}</p>\n"

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "datePublished": date_str,
        "dateModified": date_str,
        "author": {
            "@type": "Organization",
            "name": "Nashville Dog Training"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Nashville Dog Training",
            "url": SITE_URL
        },
        "url": f"{SITE_URL}/blog/{slug}/",
        "description": meta_desc
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Nashville Dog Training</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{SITE_URL}/blog/{slug}/">
<meta name="geo.region" content="US-TN">
<meta name="geo.placename" content="Nashville">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE_URL}/blog/{slug}/">
<script type="application/ld+json">
{schema}
</script>
<style>
  body {{ font-family: Georgia, serif; max-width: 780px; margin: 0 auto; padding: 1.5rem; color: #222; line-height: 1.75; }}
  h1 {{ font-size: 2rem; color: #1a3c5e; margin-bottom: .25rem; }}
  h2 {{ font-size: 1.35rem; color: #1a3c5e; margin-top: 2rem; }}
  .meta {{ color: #666; font-size: .9rem; margin-bottom: 2rem; }}
  .cta-box {{ background: #1a3c5e; color: #fff; padding: 1.5rem; border-radius: 8px; text-align: center; margin: 2.5rem 0; }}
  .cta-box a {{ background: #f0a500; color: #fff; padding: .75rem 1.75rem; border-radius: 5px; text-decoration: none; font-weight: bold; font-size: 1.1rem; }}
  nav a {{ color: #1a3c5e; margin-right: 1rem; }}
  footer {{ border-top: 1px solid #ddd; margin-top: 3rem; padding-top: 1rem; color: #666; font-size: .85rem; }}
</style>
</head>
<body>
<nav><a href="/">Home</a><a href="/blog/">Blog</a></nav>
<article>
  <h1>{title}</h1>
  <p class="meta">By Nashville Dog Training &bull; {datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")} &bull; Nashville, TN</p>

{sections_html}
  <div class="cta-box">
    <p style="font-size:1.15rem;margin-bottom:1rem;">Ready to transform your dog's behavior? We serve Nashville, Franklin, Brentwood, Murfreesboro, and surrounding areas.</p>
    <a href="/">Book a Free Consultation</a>
  </div>
</article>
<footer>
  <p>&copy; {datetime.now().year} Nashville Dog Training &bull; In-home dog training serving Greater Nashville, TN</p>
  <p><a href="/">Home</a> &bull; <a href="/blog/">Blog</a></p>
</footer>
</body>
</html>
"""


def build_sections(slug: str, title: str):
    """Return a list of (h2_heading, [paragraph, ...]) tuples based on slug keywords."""

    # Generic structured content built from the title/slug
    topic_words = slug.replace("-", " ")
    location_rotation = [
        "Nashville", "Franklin", "Brentwood", "Murfreesboro",
        "Hendersonville", "Mt. Juliet", "Spring Hill", "Smyrna"
    ]

    sections = [
        (
            f"Why {title.split(':')[0]} Matters",
            [
                f"Whether you're a first-time dog owner or a seasoned pro, mastering {topic_words} is one of the "
                f"most impactful things you can do for your dog's quality of life. At Nashville Dog Training we work "
                f"with hundreds of families across the greater Nashville metro every year, and this topic comes up "
                f"constantly in our in-home consultations.",
                f"Dogs thrive on structure, clear communication, and consistent expectations. Understanding the "
                f"fundamentals behind {topic_words} gives you the foundation to build a relationship based on "
                f"mutual trust — not frustration."
            ]
        ),
        (
            "The Science Behind the Skill",
            [
                "Modern dog training is grounded in behavioral science. Dogs learn primarily through operant "
                "conditioning — they repeat behaviors that are rewarded and avoid behaviors that lead to "
                "unpleasant outcomes. Timing, consistency, and clear criteria are the three pillars of every "
                "successful training session.",
                f"When we address {topic_words} in our Nashville in-home programs, we tailor the approach to "
                "your dog's individual temperament, age, and history. A fearful rescue responds differently than "
                "a confident working-breed puppy, and a skilled trainer knows how to adjust."
            ]
        ),
        (
            "Step-by-Step: Getting Started",
            [
                "Start every session with a calm, focused dog. Keep initial sessions short — 5 to 10 minutes "
                "is ideal for most dogs. End on a success, even if you have to make it easy.",
                f"For {topic_words}, break the skill down into the smallest possible steps. Reward each "
                "tiny improvement (called 'shaping'). Once the dog is offering the behavior reliably in a low-"
                "distraction environment, gradually add duration, distance, and distractions — in that order.",
                "Use a consistent marker word ('yes!') or clicker at the exact moment the correct behavior "
                "occurs, then follow immediately with a high-value reward. Precision in timing is more important "
                "than the value of the treat."
            ]
        ),
        (
            "Common Mistakes Nashville Dog Owners Make",
            [
                "Inconsistency is the number-one training killer. If the rule is 'no jumping,' that rule must "
                "apply with every family member, every guest, every time — or the dog learns that jumping "
                "sometimes works, which makes it much harder to extinguish.",
                f"When working on {topic_words}, avoid repeating commands. Say it once, clearly, and help the "
                "dog succeed if needed. Repeating 'sit, sit, sit' teaches your dog to wait for the third cue.",
                "Finally, don't train when you're frustrated. Dogs read your emotional state. If a session "
                "isn't going well, end it on a simple win and come back tomorrow."
            ]
        ),
        (
            f"{topic_words.title()} in Real-World Nashville Environments",
            [
                f"Practicing {topic_words} at home is a great start, but the real test is out in the world. "
                f"Nashville has excellent options for proofing your dog's skills: Shelby Bottoms Greenway, "
                f"Centennial Dog Park, Edwin Warner Park, and busy neighborhood streets in East Nashville or "
                f"12South are all fantastic training grounds.",
                "Start at a distance from distractions and gradually close the gap as your dog's skills improve. "
                "A dog that ignores a squirrel from 50 feet away isn't ready to ignore one from 5 feet — work "
                "up to it systematically."
            ]
        ),
        (
            "When to Call a Professional Nashville Dog Trainer",
            [
                "Some behaviors are best addressed with professional guidance, especially aggression, severe "
                "reactivity, or deep-rooted fear. Attempting to work through these without experience can "
                "inadvertently make them worse.",
                f"Our in-home trainers serve all of the greater Nashville area — including {', '.join(location_rotation[:5])} "
                f"and beyond. We offer a free consultation so you can see our approach before committing. "
                f"Most owners are surprised how quickly they see results when they have expert guidance.",
                "Don't wait until a behavior becomes dangerous. Early intervention is almost always faster, "
                "easier, and less expensive than trying to fix a deeply ingrained problem later."
            ]
        ),
        (
            "Frequently Asked Questions",
            [
                f"<strong>How long will it take to see results with {topic_words}?</strong> Most dogs show "
                "noticeable improvement within the first 1–3 sessions when owners apply what they learn "
                "consistently between visits.",
                "<strong>Do you use punishment-based methods?</strong> We use a balanced approach — "
                "positive reinforcement drives the majority of our teaching, with clear, fair consequences "
                "when needed. We never use methods that cause fear, pain, or shut down a dog's personality.",
                f"<strong>Can you train my dog even if we live outside Nashville proper?</strong> Yes — "
                f"we travel throughout the greater Nashville metro. Reach out to confirm coverage for your area."
            ]
        ),
    ]
    return sections


# ── sitemap updater ────────────────────────────────────────────────────────

def update_sitemap(new_slugs: list[str], date_str: str):
    content = SITEMAP.read_text()
    insert_before = "</urlset>"
    new_entries = ""
    for slug in new_slugs:
        url = f"{SITE_URL}/blog/{slug}/"
        if url not in content:
            new_entries += (
                f"  <url>\n"
                f"    <loc>{url}</loc>\n"
                f"    <lastmod>{date_str}</lastmod>\n"
                f"    <changefreq>monthly</changefreq>\n"
                f"    <priority>0.7</priority>\n"
                f"  </url>\n"
            )
    if new_entries:
        content = content.replace(insert_before, new_entries + insert_before)
        SITEMAP.write_text(content)


# ── blog index updater ─────────────────────────────────────────────────────

BLOG_INDEX = BLOG_DIR / "index.html"

def rebuild_blog_index():
    posts = sorted(BLOG_DIR.glob("*/index.html"))
    items = ""
    for post_path in reversed(posts):
        slug = post_path.parent.name
        # read title from file
        html = post_path.read_text()
        m = re.search(r"<h1>(.*?)</h1>", html)
        title = m.group(1) if m else slug_to_title(slug)
        m2 = re.search(r"<meta name=\"description\" content=\"(.*?)\"", html)
        desc = m2.group(1) if m2 else ""
        m3 = re.search(r"By Nashville Dog Training &bull; (.*?) &bull;", html)
        date_display = m3.group(1) if m3 else ""
        items += (
            f'  <li>\n'
            f'    <a href="/blog/{slug}/"><strong>{title}</strong></a>\n'
            f'    <span class="date">{date_display}</span>\n'
            f'    <p>{desc}</p>\n'
            f'  </li>\n'
        )

    BLOG_INDEX.write_text(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dog Training Blog | Nashville Dog Training Tips & Guides</title>
<meta name="description" content="Nashville Dog Training blog: expert tips, how-to guides, and local insights for Nashville, TN dog owners.">
<link rel="canonical" href="{SITE_URL}/blog/">
<style>
  body {{ font-family: Georgia, serif; max-width: 780px; margin: 0 auto; padding: 1.5rem; color: #222; line-height: 1.75; }}
  h1 {{ color: #1a3c5e; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ border-bottom: 1px solid #eee; padding: 1rem 0; }}
  a {{ color: #1a3c5e; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .date {{ color: #888; font-size: .85rem; margin-left: .5rem; }}
  p {{ margin: .3rem 0 0; color: #555; font-size: .95rem; }}
  nav a {{ margin-right: 1rem; }}
</style>
</head>
<body>
<nav><a href="/">Home</a><a href="/blog/">Blog</a></nav>
<h1>Nashville Dog Training Blog</h1>
<p>Expert tips, how-to guides, and local Nashville insights for dog owners across the greater Nashville metro.</p>
<ul>
{items}</ul>
</body>
</html>
""")


# ── main ───────────────────────────────────────────────────────────────────

def main():
    BLOG_DIR.mkdir(exist_ok=True)

    used = load_used()
    available = [(s, t) for s, t in TOPICS if s not in used]

    if not available:
        print("All topics exhausted — no new posts generated.")
        sys.exit(0)

    to_generate = available[:POSTS_PER_RUN]
    base_date = datetime.now()
    new_slugs = []

    for i, (slug, title) in enumerate(to_generate):
        post_date = (base_date - timedelta(days=len(to_generate) - 1 - i)).strftime("%Y-%m-%d")
        post_dir = BLOG_DIR / slug
        post_dir.mkdir(exist_ok=True)
        html = build_post_html(slug, title, post_date)
        (post_dir / "index.html").write_text(html)
        used.add(slug)
        new_slugs.append(slug)
        print(f"  [{i+1:02d}/{len(to_generate)}] {slug}")

    save_used(used)
    update_sitemap(new_slugs, base_date.strftime("%Y-%m-%d"))
    rebuild_blog_index()

    print(f"\nDone. {len(new_slugs)} posts written to {BLOG_DIR}")
    print(f"Topics remaining: {len([s for s, _ in TOPICS if s not in used])} / {len(TOPICS)}")


if __name__ == "__main__":
    main()
