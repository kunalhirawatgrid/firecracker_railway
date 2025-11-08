# Scripts

## seed_data.py

Creates sample assessment data for testing the platform.

### Usage

```bash
python scripts/seed_data.py
```

This will create:
- 1 assessment (ID: 1) for candidate_1
- 3 questions:
  1. Two Sum (easy)
  2. Reverse String (easy)
  3. Fibonacci Number (easy)
- Multiple test cases for each question (sample and hidden)

### Access the Assessment

After running the script, you can access the assessment at:
- Frontend: http://localhost:5173/assessment/1?candidate_id=candidate_1
- API: http://localhost:8000/api/v1/assessments/1?candidate_id=candidate_1

