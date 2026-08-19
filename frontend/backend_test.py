"""
Backend API tests for Cozinha Lucrativa - Mercado Pago Integration
Tests all backend endpoints through the public URL
"""
import requests
import json
import time
import hmac
import hashlib
from datetime import datetime

# Public URL from .env
BASE_URL = "https://mercado-pago-staging-1.preview.emergentagent.com"

def test_mp_config():
    """Test 1: GET /api/payments/mercadopago/config"""
    print("\n" + "="*80)
    print("TEST 1: MP Config Endpoint")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/payments/mercadopago/config"
        print(f"GET {url}")
        
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("enabled") == False and data.get("price") == 57.0 and data.get("currency") == "BRL":
                print("✅ PASS: Config returns enabled=false, price=57.0, currency=BRL")
                return True
            else:
                print(f"❌ FAIL: Unexpected config data: {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_mp_preference_without_token():
    """Test 2a: POST /api/payments/mercadopago/preference without token (should return 503)"""
    print("\n" + "="*80)
    print("TEST 2a: MP Preference Creation Without Token")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/payments/mercadopago/preference"
        print(f"POST {url}")
        
        payload = {
            "email": "buyer_test@example.com",
            "ref": "A01"
        }
        print(f"Payload: {json.dumps(payload)}")
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 503:
            print("✅ PASS: Returns 503 gracefully without MP_ACCESS_TOKEN")
            return True
        else:
            print(f"❌ FAIL: Expected 503, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_mp_preference_invalid_email():
    """Test 2b: POST /api/payments/mercadopago/preference with invalid email (should return 422)"""
    print("\n" + "="*80)
    print("TEST 2b: MP Preference Creation With Invalid Email")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/payments/mercadopago/preference"
        print(f"POST {url}")
        
        payload = {
            "email": "invalid-email",
            "ref": "A01"
        }
        print(f"Payload: {json.dumps(payload)}")
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ PASS: Returns 422 for invalid email validation")
            return True
        else:
            print(f"❌ FAIL: Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_webhook_non_payment():
    """Test 3a: POST /api/mercadopago/webhook with non-payment type (should return 200)"""
    print("\n" + "="*80)
    print("TEST 3a: MP Webhook Non-Payment Type")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/mercadopago/webhook"
        print(f"POST {url}")
        
        payload = {"type": "test"}
        print(f"Payload: {json.dumps(payload)}")
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("received") == True:
                print("✅ PASS: Non-payment webhook returns 200 with received=true")
                return True
            else:
                print(f"❌ FAIL: Unexpected response: {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_webhook_invalid_signature():
    """Test 3b: POST /api/mercadopago/webhook with invalid signature (should return 401)"""
    print("\n" + "="*80)
    print("TEST 3b: MP Webhook Invalid Signature")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/mercadopago/webhook"
        print(f"POST {url}")
        
        payload = {
            "type": "payment",
            "data": {"id": "999"}
        }
        print(f"Payload: {json.dumps(payload)}")
        
        headers = {
            "x-signature": "ts=123,v1=deadbeef",
            "x-request-id": "abc"
        }
        print(f"Headers: {json.dumps(headers)}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ PASS: Invalid signature returns 401")
            return True
        else:
            print(f"❌ FAIL: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_webhook_valid_signature():
    """Test 3c: POST /api/mercadopago/webhook with valid signature (should return 200)"""
    print("\n" + "="*80)
    print("TEST 3c: MP Webhook Valid Signature")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/mercadopago/webhook"
        print(f"POST {url}")
        
        # Generate valid signature
        data_id = "12345"
        request_id = "req-xyz"
        ts = str(int(time.time()))
        secret = "cl_test_webhook_secret_dummy"
        
        # Manifest format: id:{data_id};request-id:{request_id};ts:{ts};
        manifest = f"id:{data_id};request-id:{request_id};ts:{ts};"
        print(f"Manifest: {manifest}")
        
        # HMAC-SHA256
        signature = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
        print(f"Signature: {signature}")
        
        payload = {
            "type": "payment",
            "data": {"id": data_id}
        }
        print(f"Payload: {json.dumps(payload)}")
        
        headers = {
            "x-signature": f"ts={ts},v1={signature}",
            "x-request-id": request_id
        }
        print(f"Headers: {json.dumps(headers)}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("received") == True:
                print("✅ PASS: Valid signature returns 200 with received=true (no access granted without MP_ACCESS_TOKEN)")
                return True
            else:
                print(f"❌ FAIL: Unexpected response: {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_affiliate_validate():
    """Test 4a: GET /api/affiliates/validate"""
    print("\n" + "="*80)
    print("TEST 4a: Affiliate Validate Endpoint")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/affiliates/validate"
        print(f"GET {url}?code=TESTCODE")
        
        response = requests.get(url, params={"code": "TESTCODE"}, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            # Should return valid=false for non-existent code
            if "valid" in data:
                print("✅ PASS: Affiliate validate endpoint is reachable and working")
                return True
            else:
                print(f"❌ FAIL: Unexpected response format: {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_affiliate_track():
    """Test 4b: GET /api/affiliates/track"""
    print("\n" + "="*80)
    print("TEST 4b: Affiliate Track Endpoint")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/affiliates/track"
        print(f"GET {url}?code=TESTCODE")
        
        response = requests.get(url, params={"code": "TESTCODE"}, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            # Should return ok=false for non-existent code
            if "ok" in data:
                print("✅ PASS: Affiliate track endpoint is reachable and working")
                return True
            else:
                print(f"❌ FAIL: Unexpected response format: {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_access_code_validate():
    """Test 5: POST /api/access-codes/validate"""
    print("\n" + "="*80)
    print("TEST 5: Access Code Validate Endpoint")
    print("="*80)
    
    try:
        url = f"{BASE_URL}/api/access-codes/validate"
        print(f"POST {url}")
        
        payload = {
            "code": "TESTCODE",
            "base_price": 57.0
        }
        print(f"Payload: {json.dumps(payload)}")
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            # Should return valid=false for non-existent code
            if "valid" in data:
                print("✅ PASS: Access code validate endpoint is reachable and working")
                return True
            else:
                print(f"❌ FAIL: Unexpected response format: {data}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def test_general_api_health():
    """Test 6: Check if FastAPI is accessible through Next.js proxy"""
    print("\n" + "="*80)
    print("TEST 6: General API Health Check")
    print("="*80)
    
    try:
        # Test the root endpoint of FastAPI (should be proxied)
        url = f"{BASE_URL}/api/payments/mercadopago/config"
        print(f"GET {url} (testing proxy)")
        
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ PASS: FastAPI endpoints are accessible through Next.js proxy")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")
        return False


def main():
    """Run all backend tests"""
    print("\n" + "="*80)
    print("BACKEND API TESTS - COZINHA LUCRATIVA")
    print("Testing Mercado Pago Integration")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().isoformat()}")
    
    results = {}
    
    # Run all tests
    results["MP Config"] = test_mp_config()
    results["MP Preference Without Token"] = test_mp_preference_without_token()
    results["MP Preference Invalid Email"] = test_mp_preference_invalid_email()
    results["Webhook Non-Payment"] = test_webhook_non_payment()
    results["Webhook Invalid Signature"] = test_webhook_invalid_signature()
    results["Webhook Valid Signature"] = test_webhook_valid_signature()
    results["Affiliate Validate"] = test_affiliate_validate()
    results["Affiliate Track"] = test_affiliate_track()
    results["Access Code Validate"] = test_access_code_validate()
    results["General API Health"] = test_general_api_health()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*80)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*80)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
