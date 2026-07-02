"""支付网关管理器 - 统一处理多通道支付"""
import config

# 导入所有网关（按需）
_available_gateways = {}


def _init_gateways():
    """初始化可用的支付网关"""
    global _available_gateways
    _available_gateways = {"simulate": SimulateGateway()}

    if config.EPAY_PID and config.EPAY_KEY:
        from payments.epay import epay
        _available_gateways["epay"] = epay

    if config.NOWPAYMENTS_API_KEY:
        from payments.nowpayments import nowpayments_gateway
        _available_gateways["nowpayments"] = nowpayments_gateway

    if config.STRIPE_API_KEY:
        from payments.stripe_gateway import stripe
        _available_gateways["stripe"] = stripe

    print(f"[Payments] 已加载的网关: {list(_available_gateways.keys())}")


class SimulateGateway:
    """模拟支付（用于测试）"""

    def __repr__(self):
        return "simulate"


def get_gateway(name: str = None):
    """获取支付网关实例"""
    if not _available_gateways:
        _init_gateways()
    if name:
        return _available_gateways.get(name)
    return _available_gateways.get("simulate")


_init_gateways()
