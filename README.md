# 100k.github.io

This repository is a static, single-page site (`index.html`) with supporting CSS and JavaScript. You can access it locally by opening the HTML file or by running a small local web server.

## Automated research update workflow
The site now includes an **Automated Research Update Pipeline** section with a one-click UI to simulate a real-time run. Under the hood, the repo ships a set of local scripts you can run on your computer to:

1. **Search online sources** (arXiv, news via GDELT, GitHub repos).
2. **Summarize with open-source APIs or local LLMs** (OpenRouter/Together/Fireworks or Ollama).
3. **Synthesize updated research ideas** that refresh your brainstorms.

### Local scripts (logic programs)
Run these scripts from the repo root:

```bash
python3 tools/research_fetch.py --query "trustworthy agents" --limit 10 --sources arxiv,news,github
python3 tools/research_summarize.py --input research_results.json --runtime local --model llama3.1:8b
python3 tools/research_synthesize.py --input research_summaries.json --runtime local --model llama3.1:8b
```

**Open-source API runtime (OpenRouter/Together/Fireworks)**:
```bash
export OPENROUTER_API_KEY="your_key_here"
python3 tools/research_summarize.py --runtime open-source --model meta-llama/llama-3.1-70b-instruct
python3 tools/research_synthesize.py --runtime open-source --model meta-llama/llama-3.1-70b-instruct
```

### UI instructions
Open the site, scroll to **Automated Research Update Pipeline**, enter your research focus, pick a runtime, and click **Run real-time update**. The UI shows the pipeline steps and outputs sample updated ideas. Wire the UI to your own backend endpoints if you want real-time data in the browser.

## Access the site locally (quickest)
1. Open your file explorer in this repository.
2. Double‑click `index.html` to open it in your default browser.
3. The page should load immediately with all content and styling.

## Access the site via a local web server (recommended for testing)
1. Open a terminal and navigate to the repository root.
2. Run a simple web server. For example:
   ```bash
   python3 -m http.server 8000
   ```
3. Open your browser and go to:
   ```
   http://localhost:8000
   ```
4. You should see the homepage. Refresh the page after edits to see changes.

## Step‑by‑step walkthrough of what you’re doing
1. **Locate the entry point**: The page starts at `index.html`, which references `styles.css` and `scripts.js`.
2. **Load the page**:
   - Opening `index.html` directly loads the HTML and pulls in the CSS/JS files from the same folder.
   - Running a local server simulates how the page would be served on a website.
3. **View the content**: The browser renders the layout, sections, and cards based on the HTML structure and CSS styles.
4. **Iterate**: Edit HTML/CSS/JS, save, then refresh the browser to review changes.
