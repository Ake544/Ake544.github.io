/* SCROLL ANIMATIONS */
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); } });
}, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

/* ── CONFIG ─────────────────────────────────────────────────── */
const API_BASE_URL = 'https://aklilu-portfolio-api.onrender.com';

/* ── FLOATING CHAT ──────────────────────────────────────────── */
let chatOpen = false;
function toggleChat() {
    chatOpen = !chatOpen;
    const popup = document.getElementById('chatPopup');
    const icon = document.getElementById('chatFabIcon');
    const notif = document.getElementById('chatNotif');
    if (chatOpen) {
        popup.classList.add('open');
        notif.style.display = 'none';
        icon.innerHTML = '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>';
        setTimeout(() => { document.getElementById('chatInput').focus(); }, 300);
    } else {
        popup.classList.remove('open');
        icon.innerHTML = '<path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>';
    }
}

/* ── CHATBOT ────────────────────────────────────────────────── */
let conversationHistory = [];

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';
    appendMessage('user', msg);
    conversationHistory.push({ role: 'user', content: msg });
    showTyping();
    const sendBtn = document.getElementById('chatSend');
    sendBtn.disabled = true;
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: msg,
                history: conversationHistory.slice(0, -1) // send history without the last user message
            })
        });
        removeTyping();
        const data = await response.json();
        const reply = data.reply || "Having trouble connecting right now. Please reach out directly at aklilwassie@email.com.";
        appendMessage('ai', reply);
        conversationHistory.push({ role: 'assistant', content: reply });
    } catch (e) {
        removeTyping();
        appendMessage('ai', "Connection issue — feel free to reach out directly at aklilwassie@email.com.");
    }
    sendBtn.disabled = false;
}

function appendMessage(role, text) {
    const msgs = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'chat-msg ' + role;
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble';
    bubble.textContent = text;
    div.appendChild(bubble);
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
    const msgs = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'chat-msg ai'; div.id = 'typing-indicator';
    div.innerHTML = '<div class="chat-bubble" style="background:var(--bg3);border:1px solid var(--line);"><div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div></div>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

function removeTyping() {
    const t = document.getElementById('typing-indicator');
    if (t) t.remove();
}

function sendSuggestion(text) {
    document.getElementById('chatInput').value = text;
    sendMessage();
}

document.getElementById('chatInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
});

/* ── CONTACT FORM ───────────────────────────────────────────── */
async function handleFormSubmit(e) {
    e.preventDefault ? e.preventDefault() : null;
    const btn = e.target;

    // Store original button HTML for restoration
    const originalBtnHTML = btn.innerHTML;

    // Use IDs for reliable field selection
    const firstName = document.getElementById('firstName')?.value || '';
    const lastName = document.getElementById('lastName')?.value || '';
    const email = document.getElementById('email')?.value || '';
    const subject = document.getElementById('subject')?.value || '';
    const message = document.getElementById('message')?.value || '';

    if (!firstName || !lastName || !email || !subject || !message) {
        alert('Please fill in all fields.');
        return;
    }

    btn.innerHTML = '<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg> Sending...';
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                subject: subject,
                message: message
            })
        });

        const data = await response.json();
        if (data.status === 'sent') {
            btn.innerHTML = '<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></svg> ✓ Message Sent';
            btn.style.background = '#3b6d11';
            // Clear form
            ['firstName', 'lastName', 'email', 'subject', 'message'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.value = '';
            });
        } else {
            btn.innerHTML = '<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg> Sent (email not configured)';
            btn.style.background = '#b8860b';
        }
    } catch (err) {
        btn.innerHTML = '<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" y2="12"/><line x1="12" y1="16" y2="16"/></svg> Error - try email directly';
        btn.style.background = '#8b0000';
    }

    btn.disabled = false;
    setTimeout(() => {
        btn.innerHTML = originalBtnHTML;
        btn.style.background = '';
    }, 4000);
}
