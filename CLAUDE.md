# JOKESSHOTS

Photography portfolio website for **Joker**.

## Design References
- **Hero video**: Lena Harrer (lenaharrer.com) — fullscreen dark hero, autoplay video, subtle parallax
- **UI/Navigation**: Gakuyen (gakuyen.com) — Inter typography, clean nav, light content sections, 1200px container
- **Gallery**: Mix of both — 2-column grid (Harrer) with Gakuyen spacing, hover overlay with title/category
- **Mobile-first** responsive design

## Tech Stack
- Static HTML/CSS/JS — no framework
- Inter font (Google Fonts)
- IntersectionObserver scroll reveals
- CSS-only animations
- Lightbox with keyboard navigation

## Project Structure
```
jokesshots/
  src/
    index.html          # Main single-page portfolio
    css/styles.css      # Mobile-first stylesheet
    js/main.js          # Interactions (nav, lightbox, scroll reveal, parallax)
    assets/
      photos/           # Portfolio images + placeholders
      showreel.mp4      # Hero video (not yet provided)
  build/                # Production output (future)
```

## Placeholder Content
All photos are dark gray placeholder images. Replace with Joker's actual work.
Hero video source (`assets/showreel.mp4`) needs to be provided.

## To Customize
- Replace placeholder images in `src/assets/photos/`
- Add `showreel.mp4` to `src/assets/`
- Update project titles/categories in gallery HTML
- Update About section bio, clients, city
- Update contact email and Instagram handle
