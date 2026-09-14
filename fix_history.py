import os

filepath = r"dashboard\static\app.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Update addChatMessage to handle sessionStorage
old_addmsg = """window.addChatMessage = (speaker, text) => {
  let x = document.createElement('div'), user = /YOU|USER/i.test(speaker);
  x.className = `msg ${user ? 'user' : ''}`;
  x.innerHTML = `<strong>${user ? 'YOU' : 'J.A.R.V.I.S'}</strong> ${esc(text)}`;
  $('chat-feed').append(x);
  $('chat-feed').scrollTop = 999999;
};"""

new_addmsg = """let seenMsgIds = new Set();
let chatHistory = JSON.parse(sessionStorage.getItem('jarvis_chat_history') || '[]');

window.addChatMessage = (speaker, text, msgId = null, save = true) => {
  let id = msgId || (speaker + ':' + text);
  if (seenMsgIds.has(id)) return;
  seenMsgIds.add(id);

  let x = document.createElement('div'), user = /YOU|USER/i.test(speaker);
  x.className = `msg ${user ? 'user' : ''}`;
  x.innerHTML = `<strong>${user ? 'YOU' : 'J.A.R.V.I.S'}</strong> ${esc(text)}`;
  
  let typingInd = $('chat-typing-indicator');
  if (typingInd) {
    $('chat-feed').insertBefore(x, typingInd);
  } else {
    $('chat-feed').append(x);
  }
  $('chat-feed').scrollTop = 999999;
  
  if (save) {
    chatHistory.push({speaker, text, id});
    sessionStorage.setItem('jarvis_chat_history', JSON.stringify(chatHistory));
  }
};

window.loadChatHistory = () => {
  chatHistory.forEach(m => addChatMessage(m.speaker, m.text, m.id, false));
};
"""
html = html.replace(old_addmsg, new_addmsg)

# Update receive to pass msgId
old_receive = """function receive(m) {
  if (m.state || m.type === 'state') updateAIState(m.state || m.type);
  if (m.speaker || ['log', 'speech_recognized', 'assistant_response', 'sys'].includes(m.type)) {
    let who = (m.speaker || (m.type === 'speech_recognized' ? 'USER' : 'J.A.R.V.I.S')).toUpperCase(), text = m.text || '';
    if (text) {
      addChatMessage(who, text);
      addMemoryLog(`${who}: ${text}`);
      if (/J.A.R.V.I.S|ASSISTANT/.test(who)) showToast('J.A.R.V.I.S VOICE', text);
    }
  }
"""

new_receive = """function receive(m) {
  if (m.state || m.type === 'state') updateAIState(m.state || m.type);
  if (m.speaker || ['log', 'speech_recognized', 'assistant_response', 'sys'].includes(m.type)) {
    let who = (m.speaker || (m.type === 'speech_recognized' ? 'USER' : 'J.A.R.V.I.S')).toUpperCase(), text = m.text || '';
    if (text) {
      let msgId = m.ts || (who + ':' + text);
      if (!seenMsgIds.has(msgId)) {
        addChatMessage(who, text, msgId);
        addMemoryLog(`${who}: ${text}`);
        if (/J.A.R.V.I.S|ASSISTANT/.test(who)) showToast('J.A.R.V.I.S VOICE', text);
      }
    }
  }
"""
html = html.replace(old_receive, new_receive)

# Call loadChatHistory in the init section
old_init = """updateAIState('LISTENING');
connect();"""

new_init = """updateAIState('LISTENING');
loadChatHistory();
connect();"""
html = html.replace(old_init, new_init)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated app.html with session history")
