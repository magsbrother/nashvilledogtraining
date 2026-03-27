# Google Search Console Setup

Your site: https://magsbrother.github.io/nashvilledogtraining/

## Step 1: Add Property (5 min)

1. Go to https://search.google.com/search-console
2. Click "Add Property" (top left dropdown)
3. Choose "URL prefix" (right side)
4. Enter: `https://magsbrother.github.io/nashvilledogtraining/`
5. Click "Continue"

## Step 2: Verify Ownership

Choose **HTML tag** method (easiest for GitHub Pages):

1. Copy the meta tag Google gives you (looks like `<meta name="google-site-verification" content="xxxxx">`)
2. Add it to index.html in the `<head>` section
3. Commit and push:
   ```bash
   cd /home/justin-malinow/nashvilledogtraining
   git add index.html
   git commit -m "add google verification"
   git push
   ```
4. Wait 1-2 minutes for GitHub Pages to rebuild
5. Click "Verify" in Search Console

## Step 3: Submit Sitemap

1. In Search Console, go to "Sitemaps" (left sidebar)
2. Enter: `sitemap.xml`
3. Click "Submit"
4. Status should show "Success" within minutes

## Step 4: Request Indexing

1. Go to "URL Inspection" (left sidebar)
2. Enter your homepage URL
3. Click "Request Indexing"
4. Repeat for any additional pages you add later

## Ongoing Monitoring

Check weekly for:
- **Coverage**: Any crawl errors?
- **Performance**: Which keywords are you ranking for?
- **Enhancements**: Any mobile usability or structured data issues?

## Bing Webmaster Tools (Optional but Free)

1. Go to https://www.bing.com/webmasters
2. Sign in with Microsoft account
3. Import from Google Search Console (one click)
4. Bing will auto-verify and import your sitemap

## Expected Timeline

- **Indexing**: 1-7 days after submission
- **Initial rankings**: 2-4 weeks
- **Stable rankings**: 2-3 months (with consistent GBP posts + citations)

---

**Pro tip**: Once indexed, search `site:magsbrother.github.io/nashvilledogtraining` to confirm Google sees your page.
