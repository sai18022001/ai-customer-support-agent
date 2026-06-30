import json
import logging

from groq import Groq

from app.config import settings

logger = logging.getLogger(__name__)

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are an AI customer support agent for a SaaS company. Your role is to help
customers with their questions about orders, billing, accounts, and technical issues.

You have access to the customer's information and recent orders. Use this context to provide
personalized, helpful responses.

RULES:
- Be professional, empathetic, and concise.
- If you can resolve the issue, do so directly.
- If the customer is angry or the issue is complex, recommend escalation.
- Never make up information. If you don't know, say so.
- Always reference specific order IDs or account details when available.
"""

CLASSIFICATION_PROMPT = """Analyze this customer support message and return a JSON object with:
- "intent": one of [billing, technical, order_inquiry, account, general, escalate]
- "sentiment": one of [positive, neutral, negative, angry]
- "confidence": a float between 0.0 and 1.0
- "suggested_actions": a list of actions from [lookup_order, lookup_customer, create_case, update_account, escalate_to_human]
- "requires_escalation": boolean (true if customer is very angry, asking for a manager, or the issue is beyond AI capability)

Customer message: "{message}"

Return ONLY valid JSON, no other text."""


class AIEngine:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = Groq(api_key=settings.groq_api_key)
        return self._client

    def classify_message(self, message: str) -> dict:
        try:
            client = self._get_client()
            prompt = CLASSIFICATION_PROMPT.format(message=message)
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300,
            )
            text = response.choices[0].message.content.strip()

            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                text = text.rsplit("```", 1)[0]

            return json.loads(text)
        except Exception as exc:
            logger.warning("AI classification failed: %s", exc)
            return {
                "intent": "general",
                "sentiment": "neutral",
                "confidence": 0.5,
                "suggested_actions": ["create_case"],
                "requires_escalation": False,
            }

    def generate_response(
        self,
        message: str,
        customer_context: dict,
        conversation_history: list[dict],
        classification: dict,
    ) -> str:
        try:
            client = self._get_client()

            history_text = ""
            for msg in conversation_history[-6:]:
                role_label = "Customer" if msg["role"] == "customer" else "Agent"
                history_text += f"{role_label}: {msg['content']}\n"

            user_prompt = f"""CUSTOMER CONTEXT:
- Name: {customer_context.get('customer_name', 'Unknown')}
- Tier: {customer_context.get('customer_tier', 'basic')}
- Company: {customer_context.get('company', 'N/A')}
- Recent Orders: {json.dumps(customer_context.get('recent_orders', []), indent=2)}

DETECTED INTENT: {classification.get('intent', 'general')}
DETECTED SENTIMENT: {classification.get('sentiment', 'neutral')}

CONVERSATION SO FAR:
{history_text}

Customer: {message}

Respond helpfully and concisely. Do not use markdown formatting."""

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logger.warning("AI response generation failed: %s", exc)
            return (
                "I apologize, but I'm having trouble processing your request right now. "
                "Let me connect you with a human agent who can help you immediately."
            )


ai_engine = AIEngine()
