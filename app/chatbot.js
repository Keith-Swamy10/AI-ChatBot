/**
 * Embeddable Chatbot Widget
 *
 * Usage:
 *   Add this script tag to any HTML page:
 *
 *   <script
 *     src="https://your-domain.com/chatbot.js"
 *     data-api-url="http://localhost:8000/chat"
 *     data-public-key="pk_live_123">
 *   </script>
 *
 *   The chatbot button will appear in the bottom-right corner automatically.
 */
(function () {
  const script =
    document.currentScript ||
    document.querySelector('script[data-api-url]');

  const API_URL = script && script.dataset.apiUrl;
  const PUBLIC_KEY = script && script.dataset.publicKey;

  if (!API_URL) {
    console.error("Chatbot widget: data-api-url attribute is missing on the script tag.");
    return;
  }

  /* ====================== Styles ====================== */
  const style = document.createElement("style");
  style.textContent = `
    /* --- Chatbot Widget Namespace (prefixed to avoid collisions) --- */
    #cw-chat-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: #3276EA;
      color: white;
      border: none;
      cursor: pointer;
      font-size: 24px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      z-index: 9999;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    #cw-chat-btn:hover {
      transform: scale(1.08);
      box-shadow: 0 6px 18px rgba(0,0,0,0.28);
    }

    #cw-chat-panel {
      position: fixed;
      bottom: 90px;
      right: 24px;
      width: 370px;
      height: 520px;
      background: #fff;
      border-radius: 14px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.18);
      display: none;
      flex-direction: column;
      z-index: 9999;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      overflow: hidden;
    }

    #cw-chat-header {
      padding: 14px 16px;
      background: #3276EA;
      color: white;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
      font-size: 15px;
    }

    #cw-chat-messages {
      flex: 1;
      padding: 14px;
      overflow-y: auto;
      background: #f4f6f9;
    }

    .cw-msg {
      margin-bottom: 10px;
      padding: 10px 14px;
      border-radius: 12px;
      max-width: 80%;
      font-size: 14px;
      line-height: 1.5;
      word-wrap: break-word;
    }

    .cw-user {
      background: #3276EA;
      color: white;
      margin-left: auto;
      border-bottom-right-radius: 4px;
    }

    .cw-bot {
      background: #e4e6eb;
      color: #1a1a1a;
      margin-right: auto;
      border-bottom-left-radius: 4px;
    }

    #cw-chat-input-area {
      display: flex;
      padding: 10px;
      border-top: 1px solid #e0e0e0;
      background: #fff;
    }

    #cw-chat-input {
      flex: 1;
      padding: 10px 12px;
      font-size: 14px;
      border: 1px solid #d0d0d0;
      border-radius: 8px;
      outline: none;
      transition: border-color 0.2s ease;
    }

    #cw-chat-input:focus {
      border-color: #3276EA;
    }

    #cw-send-btn {
      margin-left: 8px;
      padding: 10px 16px;
      background: #3276EA;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 600;
      transition: background 0.2s ease;
    }

    #cw-send-btn:hover {
      background: #275ec2;
    }

    #cw-clear-btn {
      background: rgba(255,255,255,0.2);
      border: none;
      color: white;
      cursor: pointer;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      transition: background 0.2s ease;
    }

    #cw-clear-btn:hover {
      background: rgba(255,255,255,0.35);
    }

    /* -------- Typing Indicator -------- */
    .cw-typing {
      display: flex;
      gap: 4px;
      padding: 8px 12px;
      background: #e4e6eb;
      border-radius: 12px;
      width: fit-content;
      margin-bottom: 10px;
    }

    .cw-typing span {
      width: 7px;
      height: 7px;
      background: #888;
      border-radius: 50%;
      animation: cw-blink 1.4s infinite both;
    }

    .cw-typing span:nth-child(2) {
      animation-delay: 0.2s;
    }

    .cw-typing span:nth-child(3) {
      animation-delay: 0.4s;
    }

    @keyframes cw-blink {
      0%   { opacity: 0.2; }
      20%  { opacity: 1;   }
      100% { opacity: 0.2; }
    }

    /* -------- Mobile Responsive -------- */
    @media (max-width: 480px) {
      #cw-chat-panel {
        width: calc(100vw - 24px);
        height: calc(100vh - 120px);
        right: 12px;
        bottom: 80px;
        border-radius: 12px;
      }
    }
  `;
  document.head.appendChild(style);

  /* ====================== UI ====================== */
  const chatBtn = document.createElement("button");
  chatBtn.id = "cw-chat-btn";
  chatBtn.innerHTML = "💬";
  chatBtn.setAttribute("aria-label", "Open chat");

  const panel = document.createElement("div");
  panel.id = "cw-chat-panel";
  panel.innerHTML = `
    <div id="cw-chat-header">
      <span>Chat</span>
      <button id="cw-clear-btn">New Chat</button>
    </div>
    <div id="cw-chat-messages"></div>
    <div id="cw-chat-input-area">
      <input id="cw-chat-input" placeholder="Type a message…" autocomplete="off" />
      <button id="cw-send-btn">Send</button>
    </div>
  `;

  document.body.appendChild(chatBtn);
  document.body.appendChild(panel);

  const messagesDiv = panel.querySelector("#cw-chat-messages");
  const input = panel.querySelector("#cw-chat-input");

  let conversation = [];

  /* ====================== Helpers ====================== */
  function getSessionId() {
    let sessionId = localStorage.getItem("cw_session_id");
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem("cw_session_id", sessionId);
    }
    return sessionId;
  }

  function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `cw-msg cw-${sender}`;
    msg.innerText = text;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function clearConversation() {
    conversation = [];
    messagesDiv.innerHTML = "";
  }

  /* ====================== Typing Indicator ====================== */
  let typingEl = null;

  function showTyping() {
    typingEl = document.createElement("div");
    typingEl.className = "cw-typing";
    typingEl.innerHTML = "<span></span><span></span><span></span>";
    messagesDiv.appendChild(typingEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function hideTyping() {
    if (typingEl) {
      typingEl.remove();
      typingEl = null;
    }
  }

  /* ====================== Send Message ====================== */
  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    input.value = "";
    addMessage(text, "user");
    showTyping();

    try {
      const sessionId = getSessionId();
      const headers = { "Content-Type": "application/json" };
      if (PUBLIC_KEY) headers["X-Public-Key"] = PUBLIC_KEY;

      const res = await fetch(API_URL, {
        method: "POST",
        headers,
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });

      const data = await res.json();
      hideTyping();

      const reply = data.answer || "No response";
      addMessage(reply, "bot");
    } catch (err) {
      hideTyping();
      addMessage("Error connecting to server", "bot");
    }
  }

  /* ====================== Events ====================== */
  chatBtn.onclick = () => {
    const isOpen = panel.style.display === "flex";
    panel.style.display = isOpen ? "none" : "flex";
    chatBtn.innerHTML = isOpen ? "💬" : "✕";
    if (!isOpen) input.focus();
  };

  panel.querySelector("#cw-clear-btn").onclick = clearConversation;
  panel.querySelector("#cw-send-btn").onclick = sendMessage;

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
})();
