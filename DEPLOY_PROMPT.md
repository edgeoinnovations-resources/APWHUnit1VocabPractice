# Deployment prompt — paste this into Claude Code on your Mac

Claude Code runs on your computer, so it can do the two things this chat can't:
reach your 100 local audio files, and use your own GitHub sign-in to publish. Copy
everything in the block below into Claude Code, fill in the two spots marked
`<...>`, and run it.

---

You are helping me publish a static vocabulary website to GitHub Pages.

Context you can rely on:
- The website files are already on disk in this folder (index.html, hub.html, games/, assets/, data/, tools/, and an empty audio/unit1/). Do not rewrite them.
- My 100 Unit 1 audio files are in this folder on my Mac:
  `<PATH TO YOUR AUDIO FOLDER, e.g. /Users/paulstrootman/Desktop/APWH Unit 1 Vocab/words>`
- The GitHub repository I want to publish to is:
  `<YOUR REPO — either the URL to clone, or "this folder is already the repo">`

Please do the following, pausing to show me the output of each step:

1. If this folder is not already a git repo connected to my GitHub repo, help me get
   the site files into a local clone of it (copy them into the clone). Otherwise stay here.

2. Copy my audio into the site, renamed to the clean web-safe names the site expects.
   Run the helper script (it is non-destructive — it copies, it does not touch my originals):
   ```
   python3 tools/rename_audio.py "<PATH TO YOUR AUDIO FOLDER>" audio/unit1
   ```
   Confirm it prints "All 100 files matched and copied." If any file is reported missing,
   stop and show me the list so I can check the source folder.

3. Show me a quick local preview so I can click through before publishing:
   ```
   python3 -m http.server 8000
   ```
   Tell me to open http://localhost:8000 and try the games (especially the audio and the
   region map). Wait for me to say it looks good. Then stop the server.

4. Commit and push:
   ```
   git add -A
   git commit -m "Add AP World Unit 1 vocabulary site with audio"
   git push
   ```
   Use my existing GitHub authentication. If git asks for credentials, prompt ME to enter
   them — do not hard-code or store any token. (I am rotating my credentials, so use a
   freshly created token or SSH, never an old one.)

5. Help me turn on GitHub Pages: in the repo on github.com, Settings → Pages → "Deploy
   from a branch" → branch `main`, folder `/ (root)` → Save. Then give me the published
   URL (usually `https://<my-username>.github.io/<repo>/`) and remind me it can take a
   minute to go live.

Do not enter any passwords, tokens, or financial information on my behalf at any point.
```
