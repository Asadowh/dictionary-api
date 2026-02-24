const form = document.getElementById("search-form");
const input = document.getElementById("word-input");
const resultEl = document.getElementById("result");

function setState({ loading = false, error = null, data = null }) {
  resultEl.classList.toggle("result--loading", loading);
  resultEl.classList.toggle("result--empty", !loading && !error && !data);

  if (loading) {
    resultEl.innerHTML = '<p class="muted">Looking up your word…</p>';
    return;
  }

  if (error) {
    resultEl.innerHTML = `<p class="error">${error}</p>`;
    return;
  }

  if (!data) {
    resultEl.innerHTML = '<p class="muted">Type a word and hit search to see its definition.</p>';
    return;
  }

  const hasSynonyms = Array.isArray(data.synonyms) && data.synonyms.length > 0;
  const hasAntonyms = Array.isArray(data.antonyms) && data.antonyms.length > 0;

  let chipsHtml = "";
  if (hasSynonyms) {
    const items = data.synonyms.join("</span><span class='chip chip--accent'>");
    chipsHtml = `
      <div class="definition-label">Synonyms</div>
      <div class="chips">
        <span class="chip chip--accent">${items}</span>
      </div>
    `;
  } else if (hasAntonyms) {
    const items = data.antonyms.join("</span><span class='chip'>");
    chipsHtml = `
      <div class="definition-label">Antonyms</div>
      <div class="chips">
        <span class="chip">${items}</span>
      </div>
    `;
  }

  resultEl.innerHTML = `
    <div class="header-row">
      <span class="word">${data.word}</span>
      <span class="pronunciation">${data.pronunciation || ""}</span>
    </div>
    <div>
      <div class="definition-label">Definition</div>
      <div class="definition">${data.definition}</div>
    </div>
    ${chipsHtml}
  `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const word = input.value.trim();
  if (!word) return;

  setState({ loading: true });

  try {
    // Adjust base URL if your FastAPI app runs on a different host/port.
    const response = await fetch(`/words/${encodeURIComponent(word)}`);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("No such word was found.");
      }
      throw new Error("Something went wrong while contacting the server.");
    }

    const data = await response.json();
    setState({ data });
  } catch (err) {
    setState({ error: err.message || "Unexpected error" });
  }
});

