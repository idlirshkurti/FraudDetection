# Fraud Detection Model

## Data

The data used in this challenge are two csv files containing incoming and outgoing transactions between
’2018-06-19 11:08:59.049229’ and ’2018-11-25 11:02:46.357596’. Both the incoming and outgoing
tables have the same number of columns and column names:

  * __transaction_id__ - unique ID for the transaction
  * __transaction_timestamp__ - date-time when the transaction has occurred
  * __amount__ - amount of money incoming or outgoing for that transaction
  * __user_id__ - unique ID for the client
  * __transaction_type__ - transaction type (i.e. ’AE’, ’AV’, ’AR’,...)
  * __bank_balance_impact__ - impact on the bank balance after the transaction. If incoming then should be positive (or void), if outgoing then it should be negative.
  * __tx_status__ - FRAUD or NOT_FRAUD decision per transaction
  
  
## Repository structure
The project directory is set up the following way:

```
FraudDetection
│   README.md
|   run.py
│
└─── data
│   └-- incoming.csv
│   └-- outgoing.csv
|   └-- example.csv
│   
└─── src
    └-- pipeline.py
    └-- dataloader.py
```


The __dataloader.py__ script in the src folder contains functions which read the data from the ./data
directory.

The __pipeline.py__ script contains the ABT class which creates an Analytics Base Table necessary for
model building. This will use the dataloader.py functions to retrieve the data and build the full table. Each
function within the ABT class will add a different variable to the ABT table. The data scientist could
use a similar format if he/she wishes to add further variables to the model. These functions contain some
error-handling checks which can also be used for future functions.


In order run the project, one has to run the __run.py__ script in the home directory. Note: Please set the
working directory to the home directory of the project in line 13 of the run script. The model building part
of the script starts from line 27. If the data scientist needs to build the model first, then the model_building
variable in line 28 should be changed to ’True’. If ```model_building = True``` then the script will create the
ABT table and calculate all the features necessary for model building using the pipeline.py script functions.
After this the data scients could build a machine learning model to detect fraud using the new ABT table
with the filled in variables.

Then the following lines will calulate the features for the new, incoming, example datapoint and append
it to the ABT table. Before the new datapoint is appended to the ABT table, the already built machine
learning model could make a prediction here to see if the transaction is fraudulent.

```python
tmp = df.abt.loc[df.abt['user_id'] == example_id]
example['ratio'] = tmp. incoming_outgoing.sum()/tmp.shape[0]
example['prev_trans_time'] = example.iloc[0].transaction_timestamp - tmp.iloc[-1].transaction_timestamp
example ['average_time'] = tmp.append(example).reset_index().transaction_timestamp.diff().dropna().mean()

# NOTE: use a machine learning model here to make prediction
# append the new extended datapoint to ABT table
df.abt = df.abt.append(example).reset_index()
```


However if ```model_building = False```, then the variables of the ABT table will not be calculated. In
this scenario the model is already built and only the prediction for the new datapoint is required. The
ABT table will be called and only the variables of the new incoming transaction will be calculated. In this
scenario, the new extended transaction datapoint is appended to the ABT table, however it would make
sense if this is appended to a table in a (time-series) database. SQL queries could be a lot faster in this
scenario and improve any bottlenecks in the future once the data grows.



## Unit testing

In order to test if a certain feature is calculated correctly, the data scientist could use unit tests on the
functions of the pipeline.py script in order to give a few inputs and check if the output is the one expected.
The 'unittest' library could be used to make this possible.


## Efficiency


It is fair to say that the current method for building the ABT table is not the most efficient possible since
it uses loops. However if the features are calculated for every incoming transaction, the rows should be
appended to the ABT table. At the moment this seems to be fairly quick and efficient. In order to check
where the bottlenecks are in the code, time functions should be used in order to find which computations
are really the ones taking the longest time. i.e. if the datetime calculations are taking long to compute,
maybe different queries, technologies could be used to speed this up when the data grows.

__Note:__
1. If the data grows significantly and for some reason the ABT table needs to be re-run frequently, it
wouldn’t be smart to re-run the pipeline.py script every time. Maybe PySpark could come in handy
here in order to speed up the process by using a paralellised framework.

2. In this example python seems to be satisfactory for ETL purposes, however there are other options.
SQL queries could be faster for certain pre-processing/loading reasons. Also technologies like NiFi or
Informatica could be used for data flow automation and easier error diagnosis.

## A/B testing
Assuming the new model has been created and tested by the data scientists and seems to outperform the existing
model in some pre-specified criteria on a test set, both models should then be deployed simultaneously
to check real-life performance. I believe, initially, containers should be created around the models to ensure
stability. Both models should be given the same resources (maybe Hadoop Yarn or something equivalent
could be used to fix this). As mentioned in the previous section, a data flow automation technology such as
NiFi or Informatica could be used to run the pipelines for both models and save certain interesting outcomes
such as: prediction results, run time, etc. The time period necessary for A/B testing should be defined prior
to running the tests. Also the criteria which is interesting for the data scientists to check after the test
(scope of the test) should be priorly defined. This could be an improvement in prediction acurracy, quicker
prediction running time for incoming transaction or quicker re-training time for machine learning model.
