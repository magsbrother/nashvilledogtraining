# Nashville Dog Training Website

Static website for Nashville Dog Training, deployed via GitHub Pages.

## Deployment Instructions

### 1. Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name the repository `nashvilledogtraining`
3. Leave it empty (do not initialize with README)
4. Click "Create repository"

### 2. Push Code to GitHub

Run these commands from the project directory:

```bash
git remote add origin git@github.com:YOUR_USERNAME/nashvilledogtraining.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Build and deployment":
   - Source: **GitHub Actions**
5. The workflow will automatically deploy on push to main

### 4. Access Your Site

After the workflow completes, your site will be available at:

```
https://YOUR_USERNAME.github.io/nashvilledogtraining/
```

## Custom Domain (Optional)

To use a custom domain:

1. Add your domain to the `CNAME` file
2. In your domain registrar, add DNS records:
   - For apex domain: A records pointing to GitHub Pages IPs
   - For subdomain: CNAME record pointing to `YOUR_USERNAME.github.io`
3. Enable "Enforce HTTPS" in repository Settings > Pages

See [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) for details.

## Making Updates

After making changes to `index.html` or other files:

```bash
./deploy.sh "Describe your changes"
```

Or manually:

```bash
git add -A
git commit -m "Your commit message"
git push origin main
```

The site will automatically redeploy via GitHub Actions.

## Project Structure

```
nashvilledogtraining/
├── index.html              # Main website
├── seo-assets/             # SEO and meta assets
├── CNAME                   # Custom domain (empty until configured)
├── deploy.sh               # Quick deploy script
├── README.md               # This file
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions deployment
```
