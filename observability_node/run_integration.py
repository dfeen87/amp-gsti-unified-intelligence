#!/usr/bin/env python3
"""
Integration test for Global Observability Node
==============================================

Tests all endpoints and verifies read-only behavior.
"""

import sys
import requests
import time


BASE_URL = "http://localhost:8081"


def test_endpoint(method, endpoint, expected_status=200, should_fail=False):
    """Test a single endpoint."""
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing {method} {endpoint}...", end=" ")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json={})
        elif method == "PUT":
            response = requests.put(url, json={})
        elif method == "DELETE":
            response = requests.delete(url)
        elif method == "PATCH":
            response = requests.patch(url, json={})
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        if response.status_code == expected_status:
            print(f"✓ (status {response.status_code})")
            return True
        else:
            print(f"✗ Expected {expected_status}, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("Global Observability Node - Integration Tests")
    print("=" * 70)
    
    # Give server time to start
    print("\nWaiting for server to be ready...")
    time.sleep(2)
    
    # Test connectivity
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Server is responding (status {response.status_code})")
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        print("\nPlease start the observability node first:")
        print("  python -m observability_node.run")
        return 1
    
    print("\n" + "=" * 70)
    print("Testing GET Endpoints (should all succeed)")
    print("=" * 70)
    
    results = []
    
    # Test all GET endpoints
    results.append(test_endpoint("GET", "/"))
    results.append(test_endpoint("GET", "/health"))
    results.append(test_endpoint("GET", "/api/system_state"))
    results.append(test_endpoint("GET", "/api/gsti_state", expected_status=503))  # No DB
    results.append(test_endpoint("GET", "/api/amp_state", expected_status=503))   # No DB
    results.append(test_endpoint("GET", "/api/forecast_state", expected_status=503))  # No DB
    results.append(test_endpoint("GET", "/api/audit_summary", expected_status=503))   # No DB
    
    print("\n" + "=" * 70)
    print("Testing Write Operations (should all be rejected with 405)")
    print("=" * 70)
    
    # Test that write operations are rejected
    results.append(test_endpoint("POST", "/health", expected_status=405))
    results.append(test_endpoint("PUT", "/api/system_state", expected_status=405))
    results.append(test_endpoint("DELETE", "/api/gsti_state", expected_status=405))
    results.append(test_endpoint("PATCH", "/api/amp_state", expected_status=405))
    
    print("\n" + "=" * 70)
    print("Testing Error Handling")
    print("=" * 70)
    
    # Test 404 handling
    results.append(test_endpoint("GET", "/nonexistent", expected_status=404))
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
