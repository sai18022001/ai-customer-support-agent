const API = "/api/v1";
const HEADERS = { "X-API-Key": "dev-api-key-123" };

const INTENT_COLORS = {
    billing: "#3b82f6",
    technical: "#ef4444",
    order_inquiry: "#f59e0b",
    account: "#8b5cf6",
    general: "#6b7280",
    escalate: "#dc2626",
};

async function loadOverview() {
    try {
        const resp = await fetch(`${API}/analytics/overview`, { headers: HEADERS });
        const data = await resp.json();

        document.getElementById("totalSessions").textContent = data.total_sessions;
        document.getElementById("aiResolved").textContent = data.ai_resolved;
        document.getElementById("escalated").textContent = data.escalated;
        document.getElementById("resolutionRate").textContent = data.resolution_rate + "%";
        document.getElementById("avgSatisfaction").textContent = data.avg_satisfaction > 0
            ? data.avg_satisfaction + " / 5" : "N/A";
        document.getElementById("activeSessions").textContent = data.active_sessions;

        renderResolutionChart(data);
    } catch (err) {
        console.error("Failed to load overview:", err);
    }
}

async function loadIntents() {
    try {
        const resp = await fetch(`${API}/analytics/intents`, { headers: HEADERS });
        const data = await resp.json();
        renderIntentChart(data.intents);
    } catch (err) {
        console.error("Failed to load intents:", err);
    }
}

function renderIntentChart(intents) {
    const container = document.getElementById("intentChart");

    if (!intents || intents.length === 0) {
        container.innerHTML = '<div class="no-data">No intent data yet. Start chatting to generate data.</div>';
        return;
    }

    const maxCount = Math.max(...intents.map(i => i.count));

    container.innerHTML = intents.map(i => {
        const width = maxCount > 0 ? (i.count / maxCount) * 100 : 0;
        const color = INTENT_COLORS[i.intent] || "#6b7280";
        return `
            <div class="bar-row">
                <div class="bar-label">${i.intent}</div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:${width}%; background:${color};"></div>
                </div>
                <div class="bar-value">${i.count} <span class="bar-pct">(${i.percentage}%)</span></div>
            </div>`;
    }).join("");
}

function renderResolutionChart(data) {
    const container = document.getElementById("resolutionChart");
    const total = data.total_sessions;

    if (total === 0) {
        container.innerHTML = '<div class="no-data">No sessions yet. Start chatting to generate data.</div>';
        return;
    }

    const resolvedPct = (data.ai_resolved / total) * 100;
    const escalatedPct = (data.escalated / total) * 100;

    container.innerHTML = `
        <div class="donut-wrapper">
            <div class="donut" style="background: conic-gradient(#22c55e ${resolvedPct}%, #f59e0b ${resolvedPct}% 100%);">
                <div class="donut-hole">
                    <div class="donut-value">${Math.round(resolvedPct)}%</div>
                    <div class="donut-label">AI Resolved</div>
                </div>
            </div>
        </div>
        <div class="legend">
            <div class="legend-item">
                <span class="legend-dot" style="background:#22c55e;"></span>
                AI Resolved: ${data.ai_resolved}
            </div>
            <div class="legend-item">
                <span class="legend-dot" style="background:#f59e0b;"></span>
                Escalated: ${data.escalated}
            </div>
        </div>`;
}

loadOverview();
loadIntents();
