import io
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont
import httpx

def run_e2e_suite():
    client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=15.0)
    print("=================================================================")
    print("  AFFORDABILITY ANALYZER — FULL END-TO-END VERIFICATION SUITE   ")
    print("=================================================================")

    # 1. Health Checks
    r = client.get("/health")
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    print("[PASS] 1. Backend Server Health & Diagnostics: 200 OK")

    # 2. Frontend HTML Pages
    pages = ["/", "/analyze.html", "/budget.html", "/result.html", "/history.html", "/ppp-manager.html"]
    for page in pages:
        res = client.get(page)
        assert res.status_code == 200, f"Page {page} returned status {res.status_code}"
        assert "<!DOCTYPE html>" in res.text or "<html" in res.text, f"Page {page} is not valid HTML"
    print(f"[PASS] 2. All 6 HTML Web Application Pages ({len(pages)}/6) Verified 200 OK")

    # 3. Static Assets (CSS & JS)
    css_files = ["/css/style.css", "/css/components.css", "/css/responsive.css"]
    js_files = ["/js/app.js", "/js/upload.js", "/js/ocr.js", "/js/budget.js", "/js/charts.js", "/js/analysis.js", "/js/history.js"]
    for css in css_files:
        res = client.get(css)
        assert res.status_code == 200, f"CSS {css} not found"
    for js in js_files:
        res = client.get(js)
        assert res.status_code == 200, f"JS {js} not found"
    print(f"[PASS] 3. All CSS Design Tokens & JS Interactive Modules ({len(css_files)+len(js_files)} files) Verified 200 OK")

    # 4. Currency Exchange API
    curr_res = client.get("/api/currencies")
    assert curr_res.status_code == 200
    currencies = curr_res.json()
    assert len(currencies) >= 5
    print(f"[PASS] 4. Currency Metadata API: {len(currencies)} Currencies Loaded")

    rate_res = client.get("/api/exchange-rate", params={"from": "USD", "to": "INR"})
    assert rate_res.status_code == 200
    rate_data = rate_res.json()
    assert rate_data["rate"] > 0
    print(f"[PASS] 5. Real-Time Exchange Rate: 1 USD = {rate_data['rate']:.4f} INR (Source: {rate_data['source']})")

    # 5. PPP Service
    ppp_res = client.get("/api/ppp", params={"country": "India", "category": "Electronics"})
    assert ppp_res.status_code == 200
    ppp_data = ppp_res.json()
    assert ppp_data["ppp_factor"] == 0.82
    print(f"[PASS] 6. Category-Aware PPP Lookup: India/Electronics PPP Factor = {ppp_data['ppp_factor']}")

    # 6. Budget Management
    budget_payload = {
        "user_id": 1,
        "monthly_income": 45000.0,
        "fixed_expenses": 20000.0,
        "variable_expenses": 8000.0,
        "commitments": 5000.0,
        "currency": "INR"
    }
    b_res = client.post("/api/budget", json=budget_payload)
    assert b_res.status_code == 200
    b_data = b_res.json()
    assert b_data["disposable_budget"] == 12000.0
    print(f"[PASS] 7. Budget Profile Save: Income ₹{b_data['monthly_income']} -> Disposable Budget ₹{b_data['disposable_budget']}")

    # 7. OCR Processing with Dynamic Image
    img = Image.new("RGB", (600, 300), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((50, 50), "Sony Wireless Headphones", fill=(0, 0, 0))
    d.text((50, 120), "$49.99 USD", fill=(0, 0, 0))
    d.text((50, 180), "Category: Electronics", fill=(0, 0, 0))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    files = {"file": ("test_product.png", img_bytes, "image/png")}
    ocr_res = client.post("/api/ocr/analyze", files=files)
    assert ocr_res.status_code == 200
    ocr_data = ocr_res.json()
    print(f"[PASS] 8. OCR Image Pipeline: Raw Text Detected = '{ocr_data['raw_text'][:30]}...', Price = {ocr_data['price']}, Currency = {ocr_data['currency']}")

    # 8. Complete Analysis Pipeline (Demo Scenario from Section 35)
    analysis_req = {
        "user_id": 1,
        "product_name": "Sony Wireless Headphones",
        "category": "Electronics",
        "subcategory": "Audio",
        "original_price": 49.99,
        "original_currency": "USD",
        "target_currency": "INR",
        "country": "India",
        "monthly_income": 40000.0,
        "disposable_budget": 10000.0,
        "raw_ocr_text": "Sony Wireless Headphones $49.99 USD"
    }
    a_res = client.post("/api/analysis", json=analysis_req)
    assert a_res.status_code == 201
    a_data = a_res.json()
    analysis_id = a_data["id"]

    assert a_data["affordability_score"] > 0
    assert a_data["budget_impact"] > 0
    assert a_data["decision"] in ("BUY", "CONSIDER", "WAIT", "NOT RECOMMENDED")
    assert a_data["safe_budget_price"] == 2000.0
    assert len(a_data["calculation_breakdown"]["breakdown_steps"]) == 5

    print(f"[PASS] 9. Complete 11-Step Analysis Pipeline Execution:")
    print(f"       • Original Price: {a_data['original_price']} {a_data['original_currency']}")
    print(f"       • Converted Price: {a_data['converted_price']} {a_data['target_currency']}")
    print(f"       • Effective Value: {a_data['effective_value']} {a_data['target_currency']}")
    print(f"       • Budget Impact: {a_data['budget_impact']}%")
    print(f"       • Affordability Score: {a_data['affordability_score']}/100 ({a_data['affordability_status']})")
    print(f"       • Purchase Decision: {a_data['decision']}")
    print(f"       • Safe Budget Price: {a_data['safe_budget_price']} {a_data['target_currency']}")
    print(f"       • Mathematical Steps: {len(a_data['calculation_breakdown']['breakdown_steps'])} steps verified")

    # 9. History Retrieval & Item Details
    hist_res = client.get("/api/analysis/history", params={"user_id": 1})
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 1
    print(f"[PASS] 10. History Retrieval: {len(hist_res.json())} Analysis Records Found")

    single_res = client.get(f"/api/analysis/{analysis_id}")
    assert single_res.status_code == 200
    print(f"[PASS] 11. Individual Report by ID #{analysis_id}: Verified 200 OK")

    # 10. PPP Admin Extensibility (CRUD)
    create_ppp = client.post("/api/ppp", json={
        "country": "Testland",
        "currency": "TST",
        "category": "Electronics",
        "ppp_factor": 0.77,
        "source": "E2E Automated Verification Test"
    })
    assert create_ppp.status_code == 201
    new_ppp_id = create_ppp.json()["id"]

    update_ppp = client.put(f"/api/ppp/{new_ppp_id}", json={"ppp_factor": 0.88})
    assert update_ppp.status_code == 200
    assert update_ppp.json()["ppp_factor"] == 0.88

    delete_ppp = client.delete(f"/api/ppp/{new_ppp_id}")
    assert delete_ppp.status_code == 200
    print(f"[PASS] 12. PPP Admin Factor Extensibility (Create, Update, Delete): Fully Operational")

    print("\n=================================================================")
    print("  ALL 12 END-TO-END INTEGRATION TEST SUITES PASSED FLAWLESSLY!   ")
    print("=================================================================")

if __name__ == "__main__":
    run_e2e_suite()
