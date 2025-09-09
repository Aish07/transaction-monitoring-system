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

---

## Scalability & Future Options

The current implementation is designed to handle **up to 1M transactions** in-memory using Pandas.  
This is feasible because:

- Each transaction record is ~100 bytes on average (user_id, timestamp, merchant, amount).  
- 1M rows ≈ **100 MB**, which fits comfortably within the memory of modern laptops and servers.  
- All five rules are linear-time (`O(n)`), making them efficient for this dataset size.  


### Future Scalability Options

As transaction volumes grow (tens or hundreds of millions per day), the system can be extended in several ways:

1. **Batch Scaling with Chunked Processing**  
   - Use `pandas.read_csv(chunksize=...)` to stream the file in smaller chunks.  
   - Each chunk is processed independently, results are merged at the end.  
   - Prevents memory overload for files larger than RAM.

2. **Distributed DataFrames (Horizontal Scaling)**  
   - Replace Pandas with **Apache Spark** for parallel processing.  
   - Enables processing of hundreds of millions of rows across a cluster.  

3. **Database Integration (Hybrid Scaling)**  
   - Store transactions in a **SQL/NoSQL database** (PostgreSQL, MongoDB, Cassandra).  
   - Fraud rules can be applied via optimized queries with indexes on `user_id` and `timestamp`.  
   - Supports multiple applications sharing the same transaction data.  

4. **Real-Time Stream Processing**  
   - Integrate with **Apache Kafka** for ingestion and **Apache Flink/Spark Streaming** for rule execution.  
   - Enables continuous fraud detection with sub-second latency.  
   - Ideal for real-time flagging (e.g., blocking a suspicious payment instantly).  

5. **Machine Learning Augmentation**  
   - Extend beyond rule-based checks with ML anomaly detection models.  
   - Use features like transaction velocity, merchant diversity, and time-of-day patterns.  
   - Improves detection of novel fraud patterns that static rules might miss.  

