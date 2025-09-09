# Transaction Monitoring Subsystem

This subsystem monitors transactions for potential fraud and flags suspicious transactions based on multiple rules. It is designed to process transaction lists with up to **1 million rows**.

---

## Problem Statement

**Input:**  
A CSV file containing user transactions with the following columns:

- `user_id`: Unique identifier for the user  
- `timestamp`: Date and time of the transaction  
- `merchant_name`: Name of the merchant  
- `amount`: Transaction amount  

**Output:**  
A list of flagged transactions for each fraud rule.

**Objective:**  
Detect unusual or potentially fraudulent activity in a transaction dataset using automated rules.

---

## Fraud Detection Rules

The system uses 5 rules to flag suspicious transactions:

### **Rule 1: High-Value Transactions**
Flags any transaction above a fixed high-value threshold (e.g., $7,000).  
**Reason:** Large transactions are often anomalous and require review.

### **Rule 2: Rapid Small Transactions**
Flags users performing 5 or more transactions within 2 minutes.  
**Reason:** Rapid transactions in a short window can indicate automated fraud or card misuse.

### **Rule 3: Same-Merchant Transactions**
Flags 3 or more transactions at the same merchant within 90 seconds.  
**Reason:** Rapid repeated activity at a merchant may indicate test transactions or fraudulent behavior.

### **Rule 4: Unusual Time-of-Day Transactions**
Flags transactions that occur outside a user's typical transaction hours (mean ± 2 standard deviations).  
**Reason:** Fraud often occurs at unusual times compared to normal user behavior.

### **Rule 5: High-Frequency User Transactions**
Flags users if the number of transactions in a 3-hour window is at least twice their average transactions per hour and at least 3 transactions occur.  
**Reason:** Sudden spikes in activity may indicate fraudulent behavior or compromised accounts.

---

## Implementation Notes

- Implemented in Python using **pandas** for data manipulation.  
- All rules are designed to work on datasets of up to 1M rows efficiently.  
- Sliding time windows and per-user statistics are used for dynamic thresholds.

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/transaction-monitoring-system.git
cd transaction-monitoring-system
```

2. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Activate the virtual environment:

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```
---

## Usage

Run all rules on the default input file (data/input.csv):
```bash
python -m src.run_all_rules
```

Run on a custom CSV file:
```bash
python -m src.run_all_rules --file path/to/your/file.csv
```

The script outputs flagged transactions for each rule along with counts.

---

## Testing

Run all unit tests to ensure rules behave as expected:
```bash
python -m unittest discover -s tests
```

Unit tests cover both happy paths (transactions that should be flagged) and sad paths (transactions that should not be flagged).

---

## Example Output

```text
Processing file: data/input.csv

Rule 1 - High-value transactions: 1 flagged
Rule 2 - Rapid small transactions: 5 flagged
Rule 3 - Same-merchant transactions: 8 flagged
Rule 4 - Unusual time transactions: 0 flagged
Rule 5 - High-frequency transactions: 16 flagged
```
