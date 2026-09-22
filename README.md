# FedOps Blog & News

Blog and News are published independently from the FedOps homepage. Both sections use Markdown collections in this repository and deploy through GitHub Pages when `main` changes.

- Published Blog articles: `_blog/<slug>.md`
- Published News updates: `_news/<slug>.md`
- Keep unpublished drafts outside this public repository until they are approved for release.
- Shared layout and colors: `_layouts/` and `assets/site.css`

Each published file needs `title`, `summary`, and `category` front matter. News articles also use `display_order` to control the listing order; the 13 imported posts use the exact order of the former FedOps News page (1–13), followed by the existing 1.3 development preview (14). The imported posts retain their original dates, authors, external source links, original page URLs, and Markdown bodies in front matter and content. The filename determines the public slug. Preview locally with `bundle install` and `bundle exec jekyll serve`; the local site uses the configured `/fedops-publications` base path. Images belong in `assets/` and should use `{{ '/assets/file.png' | relative_url }}` in Markdown.

Public sections: `/blog/` and `/news/`. The homepage should link to those public URLs rather than include this repository's Markdown in its own build.
