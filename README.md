# 100k.github.io

This repository is a static, single-page site (`index.html`) with supporting CSS and JavaScript. You can access it locally by opening the HTML file or by running a small local web server.

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
