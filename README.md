# ML Exercise / Churn Prediction

This Repository Contains a simple example on Churn Prediction

## HOW TO USE:

1. First to transform the existing data and merge it with Label.
command :   python transform_data.py	 

### What It Does

It will generate 'train.csv' and 'merged.csv' file. 'train.csv' file contains  all the transformed attribute.'merged.csv' contains values of 'train.csv' and labels information.

### Transformed the attributes

- customer_id: ID of the customer same as it was given in order.csv file.

- diff_between_last_two_visit: Difference of last two order_date for each customer. Intially, I had planned to take 
difference in first and last order for each customer.

- visited_count:  Number of times each customer ordered, It derived from order_rank

- order_success_count: Count of order which get success for each customer. Intially, I had planned success_ration as transformation.

- voucher_applied_times: Number of times voucher has been used for customer, Intially, I had planned to use voucher_value which has value 0 or 1 (customer had ever used voucher or not).

- delivery_fee_applied_times: Number of times delivery fee has been charged for customer, Intially, I had planned to use delivery_value which has value 0 or 1 (whether customer has been charged for delivery or not).

- avg_of_amount_paid: Average of the total amount paid for every customer. Intially, I had planned to use total_amount for each customer as transformation.

- most_visited_payment_id: Most used payment_id for customer(categorical variables are arranged from sequential order starting from 1 as value was high). Encoding is missing. Discussed below.

- most_visited_platform_id:  Most used plaform_id for platform(categorical variables are arranged from sequential order starting from 1 as value was high)

- most_visited_transmission_id: Most used transmission_id(categorical variables are arranged from sequential order starting from 1 as value was high)

### Dropped other attributes

- order_hour
- order date
- restaurant_id
- city_id

## PREDICTION METHODS:

1. I have tried two models. Random Forest and Support Vector Machine have been used for modelling. 
Random forest has quite fast to train but SVM is very slow to train. I kept Random Forest though. I have uploaded code of both.
   - command: python predict_rf.py
   - command: python predict_svc.py

2. Accuracy using SVM : ~82 %
   Accuracy using Random Forest : ~79%


## DATA FINDINGS

- order_Date values have outlier. It contains date of year 2013 also. I have removed it though. 
And User_rating_value, Delivery_on_time could also be effective in finding better accuracy.
  

## FOR BETTER ACCURACY

1. If I would have time, then I would binary encoded the categorical variable into on hot encoding then feed it into SVM. So, it might have performed better. Also, added or dropped few attributes to see its effectiveness in the accuracy.

2. I would have also tried neural networks(CNN models) on this probelm if I would have time. That also might outperformed others.


# HOW TO RUN CODE:

1. command: python app.py

   It will start the server with port 3004
   for check: http://localhost:3004/ will return 'Hello'

2. Provided API as URL, just have to put customer_id after http://localhost:3004/predict/<customer_id> to get 0,1. It would   use predict.csv to fetch predicted value for customer_id

   For example http://localhost:3004/predict/000133bb597f will return 1

