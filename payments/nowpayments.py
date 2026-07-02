"""NOWPayments 加密货币支付网关"""
import hashlib
import hmac
import httpx
import config


class NOWPaymentsGateway:
    """NOWPayments 比特币/USDT 支付"""

    BASE_URL = "https://api.nowpayments.io/v1"
    SANDBOX_BASE = "https://api.sandbox.nowpayments.io/v1"

    def __init__(self):
        self.api_key = config.NOWPAYMENTS_API_KEY
        self.is_sandbox = config.NOWPAYMENTS_SANDBOX
        self.base_url = self.SANDBOX_BASE if self.is_sandbox else self.BASE_URL
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def create_payment(self,
                             amount: float,
                             currency: str = "usd",
                             pay_currency: str = "btc",
                             order_id: str = "",
                             description: str = "") -> dict:
        """创建支付"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/payment",
                headers=self.headers,
                json={
                    "price_amount": amount,
                    "price_currency": currency,
                    "pay_currency": pay_currency,
                    "order_id": order_id,
                    "order_description": description,
                    "success_url": config.NOWPAYMENTS_SUCCESS_URL,
                    "cancel_url": config.NOWPAYMENTS_CANCEL_URL,
                    "is_fee_paid_by_user": False,
                },
                timeout=30,
            )
            return resp.json()

    async def get_payment_status(self, payment_id: str) -> dict:
        """获取支付状态"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/payment/{payment_id}",
                headers=self.headers,
                timeout=10,
            )
            return resp.json()

    def verify_ipn(self, received_signature: str, body: bytes) -> bool:
        """验证 IPN 回调签名"""
        expected = hmac.new(
            self.api_key.encode(),
            body,
            hashlib.sha512,
        ).hexdigest()
        return hmac.compare_digest(expected, received_signature)


nowpayments_gateway = NOWPaymentsGateway()
