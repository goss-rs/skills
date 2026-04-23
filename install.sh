#!/usr/bin/env bash
# Install go-teaching-skills to Cursor user skills directory

SKILLS_DIR="$HOME/.cursor/skills"
TARGET_DIR="$SKILLS_DIR/go-teaching-skills"
REPO_URL="https://github.com/goss-rs/skills.git"

if [ -d "$TARGET_DIR" ]; then
  echo "go-teaching-skills already installed at $TARGET_DIR"
  echo "Pulling latest changes..."
  git -C "$TARGET_DIR" pull
else
  mkdir -p "$SKILLS_DIR"
  echo "Cloning $REPO_URL -> $TARGET_DIR"
  git clone "$REPO_URL" "$TARGET_DIR"
fi

echo ""
echo "Done. Skills available in all Cursor projects."
echo "To sync the go-lesson-plan knowledge corpus, run from your Go teaching repo:"
echo "  python .cursor/skills/go-teaching-skills/go-lesson-plan/scripts/sync_skill_knowledge.py"
