from fastapi.testclient import TestClient
from database import Base  # Adjust the import according to your project structure
from main import app  # Import your FastAPI app


client = TestClient(app)

def test_get_credit_value():
    response = client.put("/credits/1", json={
        "loans": [
            {
                "loan_amount": 10000,
                "taken_on": "2023-05-01",
                "loan_bank_provider": "Bank A",
                "loan_status": "DUE"
            },
            {
                "loan_amount": 30000,
                "taken_on": "2023-06-01",
                "loan_bank_provider": "Bank B",
                "loan_status": "PAID"
            }
        ],
        "annual_turnover": [
            {
                "annual_turnover": 50000,
                "profit": 10000,
                "fiscal_year": "2023",
                "reported_by_company_date": "2023-06-01"
            }
        ]
    })
    assert response.status_code == 200 
    data = response.json() 
    assert "credit_value" in data, "credit_value key not found in response"
    assert data["credit_value"] == 40000, f"Expected credit_value of 40000, but got {data['credit_value']}"

    print("Test Get Credit Value: PASSED")
