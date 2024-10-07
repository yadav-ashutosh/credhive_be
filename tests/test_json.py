test_credits_put = {
  "loans": [
    {
      "loan_amount": 15000,
      "taken_on": "2023-01-15",
      "loan_bank_provider": "Bank A",
      "loan_status": "DUE"
    },
    {
      "loan_amount": 25000,
      "taken_on": "2023-03-20",
      "loan_bank_provider": "Bank B",
      "loan_status": "PAID"
    }
  ],
  "annual_turnover": [
    {
      "annual_turnover": 80000,
      "profit": 12000,
      "fiscal_year": "2020",
      "reported_by_company_date": "2023-06-01"
    },
    {
      "annual_turnover": 60000,
      "profit": 12000,
      "fiscal_year": "2022",
      "reported_by_company_date": "2023-06-01"
    },
    {
      "annual_turnover": 70000,
      "profit": 15000,
      "fiscal_year": "2023",
      "reported_by_company_date": "2023-07-01"
    }
  ]
}
test_company_post = {
  "name": "Test Company",
  "company_id": "U82990DL2023PTC423897",
  "address": "1234 Test Address",
  "registration_date": "2023-05-15",
  "num_employees": 50,
  "contact_number": "+1234567890",
  "contact_email": "test@company.com",
  "company_website": "https://www.testcompany.com"
}
test_company_put ={
  "name": "Updated Test Company",
  "company_id": "U82990DL2023PTC423897", 
  "address": "4567 Updated Address",
  "registration_date": "2023-06-01",
  "num_employees": 75,
  "contact_number": "+0987654321",
  "contact_email": "updated@company.com",
  "company_website": "https://www.updatedcompany.com"
}