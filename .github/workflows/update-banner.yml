name: Update Hero Banner

on:
  schedule:
    - cron: "*/30 * * * *"   # every 30 minutes
  workflow_dispatch:          # allow manual run from the Actions tab

jobs:
  update-banner:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests

      - name: Update banner with live time & weather
        run: python3 scripts/update_banner.py

      - name: Commit and push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add siddik_hero_banner.svg
          git diff --staged --quiet || git commit -m "chore: update banner time/weather [skip ci]"
          git push
