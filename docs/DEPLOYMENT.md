# GitHub Pages Deployment Guide

This guide explains how to deploy the Ludicé documentation to GitHub Pages.

## Setup Complete ✅

The documentation site is now configured and ready for deployment to GitHub Pages.

### What's Been Set Up

1. **Docusaurus Configuration** (`docs/my-docs/docusaurus.config.js`)
   - Site title: "Ludicé Documentation"
   - Base URL: `/Ludice/`
   - Organization: `LudiceTeam`
   - GitHub repository integration

2. **Documentation Files Copied**
   - Introduction (`intro.md`)
   - Setup Guide (`setup-guide.md`)
   - Technical Architecture (`technical-architecture.md`)
   - API Documentation (`api-documentation.md`)
   - Development Guide (`development-guide.md`)
   - Legal documents (`legal/`)

3. **Sidebar Navigation** (`docs/my-docs/sidebars.js`)
   - Getting Started section
   - Technical Documentation section
   - Legal section

4. **GitHub Actions Workflow** (`.github/workflows/deploy-docs.yml`)
   - Automated deployment on push to `main` branch
   - Builds and deploys to GitHub Pages

## How to Deploy

### First-Time Setup on GitHub

1. **Enable GitHub Pages** in your repository settings:
   - Go to: `https://github.com/LudiceTeam/Ludice/settings/pages`
   - Under "Source", select: **GitHub Actions**
   - Save

2. **Push your changes** to the `main` branch:
   ```bash
   git add .
   git commit -m "docs: add Docusaurus documentation site"
   git push origin main
   ```

3. **GitHub Actions will automatically**:
   - Build the Docusaurus site
   - Deploy to GitHub Pages
   - Your site will be available at: `https://LudiceTeam.github.io/Ludice/`

### Manual Deployment

You can also deploy manually using Docusaurus:

```bash
cd docs/my-docs

# Build the site
npm run build

# Deploy to GitHub Pages (requires git authentication)
GIT_USER=<Your GitHub Username> npm run deploy
```

## Local Development

To preview the documentation locally:

```bash
cd docs/my-docs

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

The site will open at `http://localhost:3000/Ludice/`

## Build and Test

To build and test the production version locally:

```bash
cd docs/my-docs

# Build the site
npm run build

# Serve the built site
npm run serve
```

## Updating Documentation

### Adding a New Page

1. Create a new `.md` file in `docs/my-docs/docs/`
2. Add it to the sidebar in `docs/my-docs/sidebars.js`
3. Build and test locally
4. Push to `main` branch

### Updating Existing Pages

1. Edit the `.md` file in `docs/my-docs/docs/`
2. Test locally with `npm start`
3. Push to `main` branch
4. GitHub Actions will auto-deploy

## Troubleshooting

### Build Fails on GitHub Actions

- Check the Actions tab in your GitHub repository
- Review the build logs for errors
- Common issues:
  - Broken links (check with `npm run build`)
  - Missing dependencies
  - Invalid Markdown syntax

### Site Not Updating

- Clear your browser cache
- Wait 2-3 minutes for GitHub Pages to update
- Check GitHub Actions to ensure deployment succeeded

### Broken Links

The configuration is set to `onBrokenLinks: 'warn'` to allow builds with warnings. To find broken links:

```bash
npm run build
# Review warning messages
```

## Configuration Files

### Key Files

- `docs/my-docs/docusaurus.config.js` - Main configuration
- `docs/my-docs/sidebars.js` - Sidebar navigation
- `docs/my-docs/package.json` - Dependencies
- `.github/workflows/deploy-docs.yml` - CI/CD pipeline

### Environment Variables

No environment variables are needed for GitHub Pages deployment. The site is publicly accessible.

## Next Steps

1. Push your changes to the `main` branch
2. Enable GitHub Pages in repository settings
3. Wait for GitHub Actions to complete
4. Visit `https://LudiceTeam.github.io/Ludice/`

## Resources

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Last Updated:** January 2025
