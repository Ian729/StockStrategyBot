
import re
import json

ALLOWED_ACTIONS = {"invest", "sell", "hold"}
MAX_INVEST = 1000
TARGETS = ["Nasdaq", "Nikkei 225", "S&P 500", "Gold"]

def validate_and_format(raw_text):
    """
    校验模型输出，要求严格的JSON格式：
    [
      {"target": "Nasdaq", "action": "invest", "amount": 500, "reason": "..."},
      ...
    ]
    若不合规，fallback为持有观望并打标。
    """
    try:
        suggestions = json.loads(raw_text)
        if not isinstance(suggestions, list):
            raise ValueError("Not a list")
        result = []
        for s in suggestions:
            if (
                not isinstance(s, dict)
                or s.get("target") not in TARGETS
                or s.get("action") not in ALLOWED_ACTIONS
            ):
                raise ValueError("Invalid target or action")
            if s["action"] == "invest":
                if not (isinstance(s.get("amount"), int) and 0 < s["amount"] <= MAX_INVEST):
                    raise ValueError("Invalid invest amount")
            else:
                if "amount" in s and s["amount"]:
                    raise ValueError("Non-invest action should not have amount")
            # reason可选
            result.append(s)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        # fallback: 全部持有观望并打标
        fallback = [
            {"target": t, "action": "hold", "reason": f"auto-fallback: {str(e)}"}
            for t in TARGETS
        ]
        return json.dumps(fallback, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # 示例用法
    example = '[{"target": "Nasdaq", "action": "invest", "amount": 500, "reason": "positive news"}, {"target": "Nikkei 225", "action": "hold"}, {"target": "S&P 500", "action": "sell", "reason": "negative trend"}, {"target": "Gold", "action": "invest", "amount": 1000}]'
    print(validate_and_format(example))
