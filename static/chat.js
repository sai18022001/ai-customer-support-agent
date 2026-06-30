const API = "/api/v1";
const HEADERS = { "X-API-Key": "dev-api-key-123", "Content-Type": "application/json" };

let currentCustomerId = null;
let currentSessionId = null;
let customers = [];

const customerSelect = document.getElementById("customerSelect");
const customerInfo = document.getElementById("customerInfo");
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const newSessionBtn = document.getElementById("newSessionBtn");
const escalationBanner = document.getElementById("escalationBanner");

async function loadCustomers() {
    const resp = await fetch(`${API}/customers`, { headers: HEADERS });
    customers = await resp.json();
    customers.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c.id;
        opt.textContent = `${c.name} (${c.tier})`;
        customerSelect.appendChild(opt);
    });
}

function selectCustomer(customerId) {
    currentCustomerId = customerId;
    currentSessionId = null;
    escalationBanner.style.display = "none";

    const c = customers.find(x => x.id === customerId);
    if (c) {
        document.getElementById("custName").textContent = c.name;
        document.getElementById("custEmail").textContent = c.email;
        document.getElementById("custTier").textContent = c.tier;
        document.getElementById("custTier").className = `badge badge-${c.tier}`;
        document.getElementById("custCompany").textContent = c.company || "N/A";
        customerInfo.style.display = "block";
        messageInput.disabled = false;
        sendBtn.disabled = false;
        chatMessages.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">&#x1f44b;</div>
                <h3>Chat as ${c.name}</h3>
                <p>Type a message to start the conversation</p>
            </div>`;
    }
}

function addMessage(role, content, meta) {
    const emptyState = chatMessages.querySelector(".empty-state");
    if (emptyState) emptyState.remove();

    const wrapper = document.createElement("div");
    wrapper.className = `message-wrapper ${role}`;

    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${role}`;
    bubble.textContent = content;
    wrapper.appendChild(bubble);

    if (meta && role === "agent") {
        const badges = document.createElement("div");
        badges.className = "message-meta";

        const intentBadge = document.createElement("span");
        intentBadge.className = "meta-badge intent";
        intentBadge.textContent = meta.intent;
        badges.appendChild(intentBadge);

        const sentimentBadge = document.createElement("span");
        sentimentBadge.className = `meta-badge sentiment-${meta.sentiment}`;
        sentimentBadge.textContent = meta.sentiment;
        badges.appendChild(sentimentBadge);

        const confBadge = document.createElement("span");
        confBadge.className = "meta-badge confidence";
        confBadge.textContent = `${Math.round(meta.confidence * 100)}%`;
        badges.appendChild(confBadge);

        if (meta.actions && meta.actions.length > 0) {
            meta.actions.forEach(a => {
                const ab = document.createElement("span");
                ab.className = `meta-badge action-${a.status}`;
                ab.textContent = a.action_type;
                badges.appendChild(ab);
            });
        }

        wrapper.appendChild(badges);
    }

    chatMessages.appendChild(wrapper);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const emptyState = chatMessages.querySelector(".empty-state");
    if (emptyState) emptyState.remove();

    const wrapper = document.createElement("div");
    wrapper.className = "message-wrapper agent";
    wrapper.id = "typingIndicator";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble agent typing";
    bubble.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    wrapper.appendChild(bubble);

    chatMessages.appendChild(wrapper);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) indicator.remove();
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !currentCustomerId) return;

    messageInput.value = "";
    sendBtn.disabled = true;
    messageInput.disabled = true;

    addMessage("customer", message);
    showTypingIndicator();

    try {
        const body = {
            customer_id: currentCustomerId,
            message: message,
        };
        if (currentSessionId) body.session_id = currentSessionId;

        const resp = await fetch(`${API}/chat`, {
            method: "POST",
            headers: HEADERS,
            body: JSON.stringify(body),
        });
        const data = await resp.json();

        removeTypingIndicator();

        currentSessionId = data.session_id;

        addMessage("agent", data.reply, {
            intent: data.detected_intent,
            sentiment: data.detected_sentiment,
            confidence: data.confidence_score,
            actions: data.executed_actions,
        });

        if (data.was_escalated) {
            escalationBanner.style.display = "flex";
        }
    } catch (err) {
        removeTypingIndicator();
        addMessage("agent", "Failed to reach the server. Please try again.");
    }

    sendBtn.disabled = false;
    messageInput.disabled = false;
    messageInput.focus();
}

customerSelect.addEventListener("change", (e) => {
    if (e.target.value) selectCustomer(e.target.value);
});

sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

newSessionBtn.addEventListener("click", () => {
    if (currentCustomerId) {
        currentSessionId = null;
        escalationBanner.style.display = "none";
        const c = customers.find(x => x.id === currentCustomerId);
        chatMessages.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">&#x1f504;</div>
                <h3>New Session</h3>
                <p>Start a fresh conversation with ${c ? c.name : "customer"}</p>
            </div>`;
    }
});

loadCustomers();
