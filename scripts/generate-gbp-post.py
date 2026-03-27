#!/usr/bin/env python3
"""
GBP Post Generator for Nashville Dog Training

Generates ready-to-post content for Google Business Profile.
Run weekly to get fresh content ideas.

Usage:
    python generate-gbp-post.py
    python generate-gbp-post.py --type tip
    python generate-gbp-post.py --type success
    python generate-gbp-post.py --type faq
"""

import argparse
import random
from datetime import datetime

# Post templates by type
TIPS = [
    {
        "title": "3-Second Rule for Treats",
        "body": """Your dog has about 3 seconds to connect a reward with a behavior.

Timing matters more than the treat itself. Mark the exact moment they do it right with "yes!" then treat immediately.

Nashville dog owners: this one change will 10x your training results.""",
        "cta": "Book Now",
        "photo_idea": "Trainer giving treat to attentive dog"
    },
    {
        "title": "The Power of 'Place'",
        "body": """The 'place' command is the most underrated skill your dog can learn.

- Guests arrive? Place.
- Cooking dinner? Place.
- Kids running around? Place.

One command that solves a dozen problems. We teach this in every Nashville training program.""",
        "cta": "Learn More",
        "photo_idea": "Dog calmly on bed/mat while activity happens"
    },
    {
        "title": "Why Your Dog Pulls on Leash",
        "body": """Dogs pull because it works. Every step forward while pulling = reward.

The fix: become a tree. Stop completely when they pull. Walk only on a loose leash.

Boring? Yes. Effective? Absolutely. Most Nashville dogs improve within days.""",
        "cta": "Book Now",
        "photo_idea": "Side-by-side: pulling vs loose leash"
    },
    {
        "title": "Mental Exercise > Physical Exercise",
        "body": """A tired dog is a good dog. But physical exercise alone won't cut it.

15 minutes of training = 1 hour at the dog park (mentally).

Nose work, puzzle toys, obedience drills - these tire your dog's brain AND build your bond.""",
        "cta": "Contact Us",
        "photo_idea": "Dog doing puzzle toy or nose work"
    },
    {
        "title": "Stop Saying 'No'",
        "body": """'No' tells your dog what NOT to do. It doesn't tell them what TO do.

Instead of 'no jumping' → 'sit'
Instead of 'no barking' → 'quiet' + redirect
Instead of 'no pulling' → 'heel'

Give your dog a job. They want to please you.""",
        "cta": "Book Now",
        "photo_idea": "Dog in sit position looking at owner"
    },
]

SUCCESS_STORIES = [
    {
        "title": "From Reactive to Relaxed",
        "body": """This Brentwood family was about to rehome their dog. Lunging, barking, couldn't walk past another dog.

6 sessions later? Calm walks through the neighborhood. The whole family is in tears (happy ones).

Don't give up on your dog. We specialize in reactive behavior in Nashville.""",
        "cta": "Book Now",
        "photo_idea": "Calm dog on walk or happy family with dog"
    },
    {
        "title": "Puppy to Pro in 8 Weeks",
        "body": """Started with a wild 4-month-old Golden in Franklin. Biting, jumping, zero focus.

8 weeks of in-home training later:
- Solid sit, down, stay
- Loose leash walks
- Calm greetings

Puppy training done right = years of easy living.""",
        "cta": "Learn More",
        "photo_idea": "Well-behaved Golden Retriever"
    },
    {
        "title": "Senior Dog, New Tricks",
        "body": """'He's 7 years old, it's too late.'

That's what this Murfreesboro owner thought. But in just 4 sessions, their 'stubborn' Lab learned:
- Reliable recall
- Door manners
- Leash walking

It's never too late. Book your consultation.""",
        "cta": "Book Now",
        "photo_idea": "Older dog looking happy and engaged"
    },
]

FAQS = [
    {
        "title": "How Many Sessions Will I Need?",
        "body": """Honest answer: it depends on your goals.

- Basic obedience: 4-6 sessions
- Moderate behavior issues: 6-8 sessions
- Severe reactivity/aggression: 8-12 sessions

Every dog is different. That's why we start with a free consultation to assess YOUR dog.""",
        "cta": "Get Quote",
        "photo_idea": "Trainer evaluating dog"
    },
    {
        "title": "Do You Train All Breeds?",
        "body": """Yes! We've trained:
- Chihuahuas to Great Danes
- 'Easy' breeds and 'stubborn' breeds
- Rescues with unknown histories
- Purebreds with championship lines

There are no bad breeds. Just dogs who need the right training approach.""",
        "cta": "Contact Us",
        "photo_idea": "Collage of different breeds"
    },
    {
        "title": "Why In-Home vs Group Classes?",
        "body": """Group classes teach your dog to behave at the training facility.

In-home training teaches your dog to behave:
- At YOUR front door
- On YOUR couch
- In YOUR backyard

Real life doesn't happen in a training center. We train where it matters.""",
        "cta": "Book Now",
        "photo_idea": "Trainer working in client's living room"
    },
]

LOCATIONS = [
    "Nashville", "Franklin", "Brentwood", "Murfreesboro",
    "Hendersonville", "Mt. Juliet", "Smyrna", "Spring Hill",
    "Gallatin", "La Vergne", "East Nashville", "Green Hills",
    "Belle Meade", "Bellevue", "Hermitage"
]

def generate_post(post_type=None):
    """Generate a random GBP post."""

    if post_type == "tip":
        posts = TIPS
        category = "Training Tip"
    elif post_type == "success":
        posts = SUCCESS_STORIES
        category = "Success Story"
    elif post_type == "faq":
        posts = FAQS
        category = "FAQ"
    else:
        # Random type
        all_posts = [("Training Tip", TIPS), ("Success Story", SUCCESS_STORIES), ("FAQ", FAQS)]
        category, posts = random.choice(all_posts)

    post = random.choice(posts)
    location = random.choice(LOCATIONS)

    print("=" * 60)
    print(f"GBP POST - {category.upper()}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    print(f"TITLE: {post['title']}")
    print()
    print("BODY:")
    print("-" * 40)
    print(post['body'])
    print("-" * 40)
    print()
    print(f"CTA BUTTON: {post['cta']}")
    print(f"PHOTO IDEA: {post['photo_idea']}")
    print()
    print(f"LOCATION TAG SUGGESTION: Mention '{location}' if not already in post")
    print()
    print("=" * 60)
    print("TO POST: Go to business.google.com > Posts > Add Update")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate GBP posts for Nashville Dog Training")
    parser.add_argument("--type", choices=["tip", "success", "faq"],
                        help="Type of post to generate (random if not specified)")
    args = parser.parse_args()

    generate_post(args.type)
