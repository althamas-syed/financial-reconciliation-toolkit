# Financial Reconciliation Toolkit

Lightweight open-source Python toolkit for comparing two transaction ledgers and producing reconciliation exceptions.

## Features
- Exact transaction-ID matching
- Decimal arithmetic for money
- Amount mismatch detection
- Missing transaction detection
- Duplicate-ID detection
- CSV exception report

## Quick start
```bash
python -m pip install -e .
reconcile-csv examples/sales.csv examples/payments.csv --output report.csv
python -m unittest discover -s tests -v
```

Current version does not automatically handle partial payments, many-to-one matching, currency conversion or date tolerances.

## License
MIT
