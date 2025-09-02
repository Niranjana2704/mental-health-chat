const chatEl = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("text");
const resetBtn = document.getElementById("resetBtn");
const exportBtn = document.getElementById("exportBtn");

function addMsg(role, text) {
  const row = document.createElement("div");
  row.className = `msg ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  row.appendChild(bubble);
  chatEl.appendChild(row);
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function fetchHistory() {
  const res = await fetch("/api/history");
  const data = await res.json();
  chatEl.innerHTML = "";
  data.messages.forEach(m => addMsg(m.role, m.content));
}

async function sendText(text) {
  addMsg("user", text);
  input.value = "";
  const btn = form.querySelector("button"); btn.disabled = true;
  try {
    const res = await fetch("/api/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (data.reply) addMsg("assistant", data.reply);
    else addMsg("assistant", data.error || "Something went wrong.");
  } catch (e) {
    addMsg("assistant", "Network error. Is the server running?");
  } finally {
    btn.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  sendText(text);
});

resetBtn.addEventListener("click", async () => {
  if (!confirm("Clear the whole conversation?")) return;
  await fetch("/api/reset", { method: "POST" });
  await fetchHistory();
});

exportBtn.addEventListener("click", async () => {
  const res = await fetch("/api/history");
  const data = await res.json();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `kindwords_history_${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
});

// Initial load
fetchHistory();
input.focus();
