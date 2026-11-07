import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

def read_transactions(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"transaction_id", "amount"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path}: required columns are transaction_id,amount")
        result = defaultdict(list)
        for line, row in enumerate(reader, start=2):
            key = (row["transaction_id"] or "").strip()
            if not key:
                raise ValueError(f"{path}:{line}: missing transaction_id")
            try:
                amount = Decimal((row["amount"] or "").strip())
                if not amount.is_finite():
                    raise InvalidOperation()
            except InvalidOperation:
                raise ValueError(f"{path}:{line}: invalid amount")
            result[key].append(amount)
    return result

def reconcile(left, right):
    issues = []
    for key in sorted(set(left) | set(right)):
        a, b = left.get(key, []), right.get(key, [])
        if len(a) > 1 or len(b) > 1:
            status = "duplicate_id"
        elif not a:
            status = "missing_in_left"
        elif not b:
            status = "missing_in_right"
        elif a[0] != b[0]:
            status = "amount_mismatch"
        else:
            status = "matched"
        issues.append({
            "transaction_id": key,
            "left_amount": str(sum(a)) if a else "",
            "right_amount": str(sum(b)) if b else "",
            "status": status
        })
    return issues

def main(argv=None):
    parser = argparse.ArgumentParser(description="Reconcile two transaction CSV files without modifying them")
    parser.add_argument("left")
    parser.add_argument("right")
    parser.add_argument("--output", default="reconciliation_report.csv")
    args = parser.parse_args(argv)
    try:
        results = reconcile(read_transactions(args.left), read_transactions(args.right))
        output = Path(args.output)
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["transaction_id","left_amount","right_amount","status"])
            writer.writeheader()
            writer.writerows(results)
        summary = {s: sum(row["status"] == s for row in results) for s in
                   ("matched","amount_mismatch","missing_in_left","missing_in_right","duplicate_id")}
        print(json.dumps({"report": str(output), "summary": summary}, indent=2))
    except (OSError, ValueError) as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()
