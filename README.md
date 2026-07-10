This is the professional website of Michael Bottom.

Live at https://mb2448.github.io

## Updating the header slider photos

1. Edit the PowerPoint one directory up: `../photos_for_website.pptx` (one photo per slide).
2. Export the slides as JPEGs into `header_images/photos_for_website/`:
   - In PowerPoint: **File > Export... > JPEG**
   - **Set Width to 1920** — the default (720) looks blurry on the site.
   - Save into `header_images/photos_for_website/`, replacing the existing files.
3. Run:

   ```
   python3 update_slider.py
   ```

That's it. The script:
- regenerates the slider HTML in `index.html` (spliced between the `REPLACE HERE` marker comments) with the slides in random order,
- `git add`s the image folder explicitly, so brand-new photos can't be silently left behind (`git commit -a` does not pick up untracked files — this once caused broken images on the live site),
- aborts if any image is narrower than 1500px (catches a forgotten Width=1920 in the export dialog),
- aborts if `index.html` references an image git isn't tracking,
- commits and pushes. The site updates in about a minute.

Options: `--no-push` to commit without pushing, `--export` to attempt an automated PowerPoint export via AppleScript first (may export at low resolution, in which case the width check will tell you to export manually).

If the site still looks wrong after a push, hard-refresh the browser (Cmd+Shift+R) — GitHub Pages caches images for 10 minutes.

## Other content updates

Everything else (publications, group members, etc.) is edited directly in `index.html`, then committed and pushed.
