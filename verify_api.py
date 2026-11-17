import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import httpx
import json

def verify_all():
    client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=10.0)
    
    # 1. Health
    h = client.get("/health")
    print("[1] Health Status:", h.status_code, h.json())

    # 2. Exchange Rate
    r = client.get("/api/exchange-rate", params={"from": "USD", "to": "INR"})
    print("\n[2] Exchange Rate USD->INR:", r.status_code, json.dumps(r.json(), indent=2))

    # 3. PPP Factor
    p = client.get("/api/ppp", params={"country": "India", "category": "Electronics", "currency": "INR"})
    print("\n[3] PPP Factor India/Electronics:", p.status_code, json.dumps(p.json(), indent=2))

    # 4. Budget
    b = client.get("/api/budget", params={"user_id": 1})
    print("\n[4] User Budget Profile:", b.status_code, json.dumps(b.json(), indent=2))

    # 5. Complete Analysis for $49.99 USD Sony Headphones -> INR
    analysis_payload = {
        "user_id": 1,
        "product_name": "Sony Wireless Headphones",
        "category": "Electronics",
        "subcategory": "Audio",
        "original_price": 49.99,
        "original_currency": "USD",
        "target_currency": "INR",
        "country": "India",
        "monthly_income": 40000.0,
        "disposable_budget": 10000.0
    }
    a = client.post("/api/analysis", json=analysis_payload)
    print("\n[5] Complete Analysis Endpoint Response:", a.status_code)
    res_data = a.json()
    print(" - Original:", f"{res_data['original_price']} {res_data['original_currency']}")
    print(" - Converted:", f"{res_data['converted_price']} {res_data['target_currency']} (Rate: {res_data['exchange_rate']})")
    print(" - Effective Value:", f"{res_data['effective_value']} {res_data['target_currency']} (PPP Factor: {res_data['ppp_factor']})")
    print(" - Budget Impact:", f"{res_data['budget_impact']}%")
    print(" - Affordability Score:", f"{res_data['affordability_score']}/100 ({res_data['affordability_status']})")
    print(" - Decision:", res_data['decision'])
    print(" - Safe Budget Price:", f"{res_data['safe_budget_price']} (Difference: {res_data['price_difference_safe']})")
    print(" - Recommendation:", res_data['recommendation'])

    # 6. History
    hist = client.get("/api/analysis/history", params={"user_id": 1})
    print(f"\n[6] History Count: {len(hist.json())} items")

if __name__ == "__main__":
    verify_all()
