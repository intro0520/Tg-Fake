"""易支付网关"""
import hashlib
import urllib.parse
import httpx
import config


class EPAYGateway:
    """易支付（国内常见虚拟支付）"""

    def create_order(self,
                    order_id: str,
                    amount: float,
                    title: str = "商品",
                    notify_url: str = "") -> dict:
        """创建支付订单"""
        params = {
            "pid": config.EPAY_PID,
            "type": "alipay",
            "out_trade_no": order_id,
            "notify_url": notify_url or f"http://localhost:{config.WEB_PORT}/webhook/epay",
            "return_url": "",
            "name": title,
            "money": f"{amount:.2f}",
        }
        # 签名
        params["sign"] = self._sign(params)
        params["sign_type"] = "MD5"

        pay_url = f"{config.EPAY_URL}?{urllib.parse.urlencode(params)}"
        return {
            "success": True,
            "pay_url": pay_url,
            "order_id": order_id,
        }

    def _sign(self, params: dict) -> str:
        """MD5 签名"""
        sorted_params = sorted(params.items())
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        sign_str += config.EPAY_KEY
        return hashlib.md5(sign_str.encode()).hexdigest()

    def verify_callback(self, params: dict) -> bool:
        """验证回调"""
        received_sign = params.pop("sign", "")
        return self._sign(params) == received_sign


epay = EPAYGateway()
