#!/usr/bin/env python3
"""One-command updater for the homepage image slider.

Usage:
    python3 update_slider.py              # regenerate slider HTML, commit, push
    python3 update_slider.py --export     # also re-export jpegs from the pptx first
    python3 update_slider.py --no-push    # do everything except git push

Replaces the old manual flow (export from PowerPoint, run
generate_images_html.py, paste output into index.html, git add/commit/push).
The 'photos never showed up' failure mode was untracked jpegs:
`git commit -a` does NOT pick up brand-new files. This script always
`git add`s the image directory explicitly and refuses to push if index.html
references an image that isn't committed.
"""

import argparse
import glob
import os
import random
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(REPO, "header_images", "photos_for_website")
IMG_DIR_REL = "header_images/photos_for_website"
INDEX = os.path.join(REPO, "index.html")
PPTX = os.path.abspath(os.path.join(REPO, "..", "photos_for_website.pptx"))
START_MARK = "<!-- REPLACE HERE WITH SCRIPT OUTPUT FROM GENERATE_IMAGES_HTML.PY-->"
STOP_MARK = "<!-- STOP REPLACE HERE WITH SCRIPT OUTPUT-->"


def run(cmd, **kw):
    print("  $", " ".join(cmd))
    return subprocess.run(cmd, cwd=REPO, check=True, **kw)


def export_from_pptx():
    """Export every slide of the pptx as jpegs via PowerPoint (macOS)."""
    if not os.path.exists(PPTX):
        sys.exit(f"pptx not found: {PPTX}")
    script = f'''
    tell application "Microsoft PowerPoint"
        open POSIX file "{PPTX}"
        save active presentation in POSIX file "{IMG_DIR}" as save as JPG file format
        close active presentation saving no
    end tell
    '''
    print(f"Exporting slides from {os.path.basename(PPTX)} via PowerPoint...")
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except subprocess.CalledProcessError:
        sys.exit(
            "PowerPoint export failed. Export manually instead:\n"
            "  File > Export... > JPEG > save into header_images/photos_for_website/\n"
            "then re-run this script without --export."
        )
    # PowerPoint may write .JPG/.jpg — normalize everything to .jpeg
    for f in glob.glob(os.path.join(IMG_DIR, "*")):
        base, ext = os.path.splitext(f)
        if ext.lower() in (".jpg", ".jpeg") and ext != ".jpeg":
            os.replace(f, base + ".jpeg")


def slide_number(path):
    m = re.search(r"(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0


def regenerate_index():
    files = sorted(glob.glob(os.path.join(IMG_DIR, "*.jpeg")), key=slide_number)
    if not files:
        sys.exit(f"No .jpeg files found in {IMG_DIR_REL}/")
    random.shuffle(files)
    block = "\n"
    for f in files:
        rel = f"./{IMG_DIR_REL}/{os.path.basename(f)}"
        block += (
            '<div class="swiper-slide">\n'
            f'    <img src="{rel}" alt="">\n'
            "</div>\n\n"
        )
    with open(INDEX) as fh:
        html = fh.read()
    if START_MARK not in html or STOP_MARK not in html:
        sys.exit("Marker comments not found in index.html — cannot splice slider block.")
    pre, rest = html.split(START_MARK, 1)
    _, post = rest.split(STOP_MARK, 1)
    with open(INDEX, "w") as fh:
        fh.write(pre + START_MARK + "\n" + block + STOP_MARK + post)
    print(f"Wrote {len(files)} slides into index.html")
    return files


def commit_and_push(push=True):
    run(["git", "add", IMG_DIR_REL, "index.html"])
    # Verify every image referenced by index.html is now staged/tracked
    tracked = subprocess.run(
        ["git", "ls-files", IMG_DIR_REL], cwd=REPO,
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    with open(INDEX) as fh:
        referenced = re.findall(rf"{IMG_DIR_REL}/(\S+?\.jpeg)", fh.read())
    missing = [r for r in referenced if f"{IMG_DIR_REL}/{r}" not in tracked]
    if missing:
        sys.exit(f"ABORT: index.html references images not tracked by git: {missing}")

    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=REPO
    ).returncode != 0
    if not staged:
        print("Nothing changed — no commit needed.")
        return
    run(["git", "commit", "-m", "update header slider images"])
    if push:
        run(["git", "push"])
        print("\nDone — pushed. Site updates in ~1 min: https://mb2448.github.io")
    else:
        print("\nCommitted but not pushed (--no-push). Run `git push` when ready.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--export", action="store_true",
                   help="re-export jpegs from ../photos_for_website.pptx via PowerPoint first")
    p.add_argument("--no-push", action="store_true", help="commit but do not push")
    args = p.parse_args()
    if args.export:
        export_from_pptx()
    regenerate_index()
    commit_and_push(push=not args.no_push)
