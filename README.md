# Fraud Detection Model

## 0.1 Data

The data used in this challenge are two csv files containing incoming and outgoing transactions between
’2018-06-19 11:08:59.049229’ and ’2018-11-25 11:02:46.357596’. Both the incoming and outgoing
tables have the same number of columns and column names:

  * transaction_id - unique ID for the transaction
  * transaction_timestamp - date-time when the transaction has occurred
  * amount - amount of money incoming or outgoing for that transaction
  * user_id - unique ID for the client
  * transaction_type - transaction type (i.e. ’AE’, ’AV’, ’AR’,...)
  * bank_balance_impact - impact on the bank balance after the transaction. If incoming then should be positive (or void), if outgoing then it should be negative.
  * tx_status - FRAUD or NOT_FRAUD decision per transaction
  
  
## 0.2 Directory
The project directory is set up the following way:

```
FraudDetection
│   README.md
|   run.py
│
└─── data
│   │   incoming.csv
│   │   outgoing.csv
|   |   example.csv
│   
└─── src
    │   pipeline.py
    │   dataloader.py
```
