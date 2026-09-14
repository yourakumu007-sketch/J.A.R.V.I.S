import os

filepath = r"dashboard\static\app.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace <input> with <textarea> and update styling/events
old_input = """<input id="chat-input-field" class="input" placeholder="Enter a request or command" onkeydown="if(event.key==='Enter')sendChatMessage()">"""
new_input = """<textarea id="chat-input-field" class="input" placeholder="Enter a request or command" rows="1" style="resize:none; overflow:hidden;" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'" onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); sendChatMessage(); }"></textarea>"""
html = html.replace(old_input, new_input)

# 2. Disable logic in JS
old_send = """window.sendChatMessage = () => {
  let input = $('chat-input-field'), t = input.value.trim();
  if (t) {
    addChatMessage('YOU', t);
    input.value = '';
    updateAIState('THINKING');
    sendBackendCommand(t);
  }
};"""

new_send = """window.sendChatMessage = () => {
  let input = $('chat-input-field'), btn = input.nextElementSibling;
  let t = input.value.trim();
  if (t && !input.disabled) {
    addChatMessage('YOU', t);
    input.value = '';
    input.style.height = '';
    updateAIState('THINKING');
    
    // Disable inputs while processing
    input.disabled = true;
    btn.disabled = true;
    
    sendBackendCommand(t).finally(() => {
      input.disabled = false;
      btn.disabled = false;
      input.focus();
    });
  }
};"""
html = html.replace(old_send, new_send)

# 3. Update sendBackendCommand to return a Promise and handle errors
old_sendcmd = """window.sendBackendCommand = t => {
  if (!t) return;
  document.title = 'CMD:' + t;
  if (ws?.readyState === 1) ws.send(JSON.stringify({ type: 'command', text: t }));
  else if (!local) fetch('/api/command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(token !== '__TOKEN__' ? { Authorization: `Bearer ${token}` } : {}) },
    body: JSON.stringify({ text: t })
  }).catch(() => {});
};"""

new_sendcmd = """window.sendBackendCommand = async t => {
  if (!t) return;
  document.title = 'CMD:' + t;
  try {
    if (ws?.readyState === 1) {
      ws.send(JSON.stringify({ type: 'command', text: t }));
      return Promise.resolve();
    } else if (!local) {
      let res = await fetch('/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token !== '__TOKEN__' ? { Authorization: `Bearer ${token}` } : {}) },
        body: JSON.stringify({ text: t })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
    }
  } catch (err) {
    addChatMessage('SYSTEM', `API Error: ${err.message}. Connection failed.`);
    updateAIState('LISTENING');
  }
};"""
html = html.replace(old_sendcmd, new_sendcmd)

# 4. Add typing indicator HTML inside the feed
old_feed = """<div id="chat-feed" class="feed"><div class="msg"><strong>J.A.R.V.I.S</strong> Command channel synchronized.</div></div>"""
new_feed = """<div id="chat-feed" class="feed"><div class="msg"><strong>J.A.R.V.I.S</strong> Command channel synchronized.</div><div id="chat-typing-indicator" class="msg" style="display:none; color: var(--r);"><strong>J.A.R.V.I.S</strong> <span class="blink">Processing neural response...</span></div></div>"""
html = html.replace(old_feed, new_feed)

# 5. Show/hide typing indicator based on AI state
old_update = """  $('voice-bar').style.setProperty('--v', s === 'SPEAKING' ? '96%' : s === 'LISTENING' ? '64%' : s === 'THINKING' ? '45%' : s === 'EMERGENCY' ? '0%' : '18%');
  window.__jarvisState = s;"""
new_update = """  $('voice-bar').style.setProperty('--v', s === 'SPEAKING' ? '96%' : s === 'LISTENING' ? '64%' : s === 'THINKING' ? '45%' : s === 'EMERGENCY' ? '0%' : '18%');
  
  let typingInd = $('chat-typing-indicator');
  if (typingInd) {
    typingInd.style.display = (s === 'THINKING' || s === 'PROCESSING') ? 'block' : 'none';
    if (s === 'THINKING' || s === 'PROCESSING') $('chat-feed').scrollTop = 999999;
  }
  
  window.__jarvisState = s;"""
html = html.replace(old_update, new_update)

# 6. Make Escape close modal and auto-focus chat
old_openModal = """window.openModal = id => {
  $(id).classList.add('active');
  if (id === 'files') refreshFiles();
};"""
new_openModal = """window.openModal = id => {
  $(id).classList.add('active');
  if (id === 'files') refreshFiles();
  if (id === 'chat') setTimeout(() => $('chat-input-field')?.focus(), 50);
};"""
html = html.replace(old_openModal, new_openModal)

# 7. Add simple blinking animation for the typing indicator
old_style = """@keyframes scan{0%{top:0}50%{top:100%}100%{top:0}}"""
new_style = """@keyframes scan{0%{top:0}50%{top:100%}100%{top:0}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
.blink{animation:blink 1.5s infinite;}
.input:disabled, .btn:disabled { opacity: 0.5; cursor: not-allowed; }"""
html = html.replace(old_style, new_style)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated app.html with chat enhancements.")
