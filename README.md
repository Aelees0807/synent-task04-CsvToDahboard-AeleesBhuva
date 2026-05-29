# Netflix Analytics Dashboard

0. Add `netflix_titles.csv` to the repository root (next to `task-4.py`).
1. Commit and push this repository to GitHub.
2. On Streamlit Community Cloud, create a new app and connect the GitHub repository and branch.

Important:

- The app will automatically load `netflix_titles.csv` if present in the repo root.
- If the dataset is not present, the app shows a sidebar file uploader so users can upload a CSV manually.

Quick commands:

```bash
git init
git add .
git commit -m "Add Streamlit app and dataset"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

After pushing, go to https://share.streamlit.io and follow the prompts to deploy.