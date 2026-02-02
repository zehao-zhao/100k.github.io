document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach((link) => {
        link.addEventListener("click", (event) => {
            const targetId = link.getAttribute("href").slice(1);
            const target = document.getElementById(targetId);
            if (!target) {
                return;
            }
            event.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });

    const runButton = document.querySelector("[data-run-pipeline]");
    const statusBox = document.querySelector(".automation-status");
    const resultsList = document.querySelector(".automation-results ul");
    const form = document.querySelector(".automation-form");

    if (runButton && statusBox && resultsList && form) {
        runButton.addEventListener("click", () => {
            const formData = new FormData(form);
            const focus = formData.get("focus");
            const runtime = formData.get("runtime");
            const sources = formData.getAll("sources");
            const apiKey = formData.get("apiKey");

            if (!focus) {
                statusBox.innerHTML = "<p>Please enter a research focus before running.</p>";
                return;
            }

            if (apiKey) {
                localStorage.setItem("researchApiKey", apiKey.toString());
            }

            const sourceLabel = sources.length ? sources.join(", ") : "no sources selected";
            statusBox.innerHTML = `
                <p><strong>Running...</strong></p>
                <ul>
                    <li>Searching ${sourceLabel} for “${focus}”.</li>
                    <li>Ranking results by novelty + relevance.</li>
                    <li>Summarizing with ${runtime} model runtime.</li>
                    <li>Drafting updated research directions.</li>
                </ul>
            `;

            resultsList.innerHTML = "";

            const demoIdeas = [
                `Design an evaluation suite for ${focus} with stress-test scenarios and failure analysis.`,
                `Build a lightweight “research memory” service that auto-updates ${focus} with weekly digests.`,
                `Prototype a pilot study on ${focus} that measures impact on decision quality and trust.`,
            ];

            setTimeout(() => {
                demoIdeas.forEach((idea) => {
                    const item = document.createElement("li");
                    item.textContent = idea;
                    resultsList.appendChild(item);
                });
                statusBox.innerHTML = `
                    <p><strong>Complete.</strong> Stored your API key locally (if provided) and generated fresh ideas.</p>
                    <p>Next: wire the pipeline to your local scripts or API endpoints.</p>
                `;
            }, 800);
        });
    }
});
