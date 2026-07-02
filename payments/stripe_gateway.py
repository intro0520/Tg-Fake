"""Stripe 信用卡支付网关"""
import httpx
import config


class StripeGateway:
    """Stripe 国际信用卡支付"""

    BASE_URL = "https://api.stripe.com/v1"

    def __init__(self):
        self.api_key = config.STRIPE_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    async def create_checkout_session(self,
                                     order_id: str,
                                     amount: float,
                                     description: str = "",
                                     success_url: str = "",
                                     cancel_url: str = "") -> dict:
        """创建 Checkout Session"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/checkout/sessions",
                headers=self.headers,
                data={
                    "payment_method_types[]": "card",
                    "line_items[0][price_data][currency]": "usd",
                    "line_items[0][price_data][unit_amount]": int(amount * 100),
                    "line_items[0][price_data][product_data][name]": description,
                    "line_items[0][quantity]": "1",
                    "mode": "payment",
                    "success_url": success_url,
                    "cancel_url": cancel_url,
                    "client_reference_id": order_id,
                },
                timeout=30,
            )
            result = resp.json()
            return {
                "success": True,
                "pay_url": result["url"],
                "session_id": result["id"],
            }

    async def create_payment_intent(self,
                                    amount: float,
                                    currency: str = "usd",
                                    description: str = "") -> dict:
        """创建 PaymentIntent（直接在前端 elements 中使用）"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/payment_intents",
                headers=self.headers,
                data={
                    "amount": int(amount * 100),
                    "currency": currency,
                    "description": description,
                    "payment_method_types[]": "card",
                    "automatic_payment_methods[enabled]": "true",
                },
                timeout=30,
            )
            result = resp.json()
            return {
                "success": True,
                "client_secret": result["client_secret"],
                "id": result["id"],
            }


stripe = StripeGateway()
