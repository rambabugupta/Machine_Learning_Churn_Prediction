import csv
import numpy
import operator
from datetime import datetime
import pandas as pd


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

# first we need to transform some fields into small numericals:
# payment_id
# platform_id
# transmission_id

csv_path = "machine_learning_challenge_order_data.csv"
column_names = []
unique_payment_id_dict = {}
unique_platform_id_dict = {}
unique_transmission_id_dict = {}
number_of_rows=0;

def modify_dict(dict):
	numeric = 1;
	for key in sorted(dict.iterkeys()):
		dict[key] = numeric;
		numeric = numeric + 1;

with open(csv_path, "rb") as f_obj:
	reader=csv.reader(f_obj)
	column_names = reader.next()
	
	# index of fields which should be normalized
	# to smaller numericals
	payment_idx = column_names.index('payment_id')
	platform_idx = column_names.index('platform_id')
	transmission_idx = column_names.index('transmission_id')

	for row in reader:
		number_of_rows = number_of_rows + 1;
		# for payment_id
		if row[payment_idx] not in unique_payment_id_dict:
			unique_payment_id_dict[row[payment_idx]] = -1

		if row[platform_idx] not in unique_platform_id_dict:
			unique_platform_id_dict[row[platform_idx]] = -1

		if row[transmission_idx] not in unique_transmission_id_dict:
			unique_transmission_id_dict[row[transmission_idx]] = -1


modify_dict(unique_payment_id_dict)
modify_dict(unique_platform_id_dict)
modify_dict(unique_transmission_id_dict)


print 'payment_id_map', unique_payment_id_dict
print 'platform_id_map', unique_platform_id_dict
print 'transmission_id_map', unique_transmission_id_dict

customers_transform_info = [];
customer_info = {}
payment_info = {};
platform_info = {};
transmission_info = {};
prev_row = {};

cus_idx = column_names.index('customer_id')
date_idx = column_names.index('order_date')
order_rank_idx = column_names.index('customer_order_rank')
is_failed_idx = column_names.index('is_failed')
voucher_idx = column_names.index('voucher_amount')
delivery_idx = column_names.index('delivery_fee')
amount_idx = column_names.index('amount_paid')
payment_idx = column_names.index('payment_id')
platform_idx = column_names.index('platform_id')
transmission_idx = column_names.index('transmission_id')

modified_column_lists = ['customer_id', 'diff_between_last_two_visit', 
'visited_count','order_success_count', 'voucher_applied_times', 
'delivery_fee_applied_times', 'avg_of_amount_paid', 'most_visited_payment_id', 
'most_visited_platform_id', 'most_visited_transmission_id']



with open(csv_path, "rb") as f_obj:
	reader=csv.reader(f_obj)
	skip=reader.next()
	for row in reader:
		number_of_rows = number_of_rows - 1;
		#first time
		if customer_info == {}:
			customer_info['customer_id'] = row[cus_idx]
			customer_info['diff_between_last_two_visit'] = -1
			customer_info['visited_count'] = 1
			customer_info['order_success_count'] = 0
			customer_info['voucher_applied_times'] = 0
			customer_info['delivery_fee_applied_times'] = 0
			if (int(row[is_failed_idx]) == 0):
				customer_info['order_success_count'] = 1
			if (float(row[voucher_idx])!=0):
				customer_info['voucher_applied_times'] = 1
			if (float(row[delivery_idx]) != 0):
				customer_info['delivery_fee_applied_times'] = 1
			
			customer_info['sum_amount'] = float(row[amount_idx])
			payment_info[row[payment_idx]] = 1
			platform_info[row[platform_idx]] =1;
			transmission_info[row[transmission_idx]]=1
			prev_row = row;

		elif 'customer_id' in customer_info.keys() and row[cus_idx] == customer_info['customer_id']:
			customer_info['diff_between_last_two_visit'] = days_between(row[date_idx],prev_row[date_idx])
			customer_info['visited_count'] = customer_info['visited_count'] + 1
			
			if (int(row[is_failed_idx]) == 0):
				customer_info['order_success_count'] = customer_info['order_success_count'] + 1

			if (float(row[voucher_idx])!=0):
				customer_info['voucher_applied_times'] = customer_info['voucher_applied_times'] + 1

			if (float(row[delivery_idx]) != 0):
				customer_info['delivery_fee_applied_times'] = customer_info['delivery_fee_applied_times'] + 1

			customer_info['sum_amount'] = float(row[amount_idx]) + customer_info['sum_amount']
			
			if row[payment_idx] in payment_info:
				payment_info[row[payment_idx]] = payment_info[row[payment_idx]] + 1
			else:
				payment_info[row[payment_idx]] = 1

			if row[platform_idx] in platform_info:
				platform_info[row[platform_idx]] = platform_info[row[platform_idx]] + 1
			else:
				platform_info[row[platform_idx]] = 1

			if row[transmission_idx] in transmission_info:
				transmission_info[row[transmission_idx]] = transmission_info[row[transmission_idx]] + 1
			else:
				transmission_info[row[transmission_idx]] = 1
			prev_row = row
			if number_of_rows == 0:
				sorted_payment = sorted(payment_info.items(), key=operator.itemgetter(1))
				sorted_platform = sorted(platform_info.items(), key=operator.itemgetter(1))
				sorted_transmission = sorted(transmission_info.items(), key=operator.itemgetter(1))
				customer_info['most_visited_payment_id'] = unique_payment_id_dict[sorted_payment[-1][0]]
				customer_info['most_visited_platform_id'] = unique_platform_id_dict[sorted_platform[-1][0]]
				customer_info['most_visited_transmission_id'] = unique_transmission_id_dict[sorted_transmission[-1][0]]
				if (customer_info['order_success_count']):
					customer_info['avg_of_amount_paid'] = int(customer_info['sum_amount']/customer_info['order_success_count'])
				else:
					customer_info['avg_of_amount_paid']=0
				del customer_info['sum_amount']
				customers_transform_info.append(customer_info)
				
		else:
			sorted_payment = sorted(payment_info.items(), key=operator.itemgetter(1))
			sorted_platform = sorted(platform_info.items(), key=operator.itemgetter(1))
			sorted_transmission = sorted(transmission_info.items(), key=operator.itemgetter(1))
			customer_info['most_visited_payment_id'] = unique_payment_id_dict[sorted_payment[-1][0]]
			customer_info['most_visited_platform_id'] = unique_platform_id_dict[sorted_platform[-1][0]]
			customer_info['most_visited_transmission_id'] = unique_transmission_id_dict[sorted_transmission[-1][0]]
			if (customer_info['order_success_count']):
				customer_info['avg_of_amount_paid'] = int(customer_info['sum_amount']/customer_info['order_success_count'])
			else:
				customer_info['avg_of_amount_paid']=0
			del customer_info['sum_amount']
			customers_transform_info.append(customer_info)

			customer_info = {}
			payment_info = {}
			platform_info = {}
			transmission_info = {}
			
			customer_info['customer_id'] = row[cus_idx]
			customer_info['diff_between_last_two_visit'] = -1
			customer_info['visited_count'] = 1
			customer_info['order_success_count'] = 0
			customer_info['voucher_applied_times'] = 0
			customer_info['delivery_fee_applied_times'] = 0
			if (int(row[is_failed_idx]) == 0):
				customer_info['order_success_count'] = 1
			if (float(row[voucher_idx])!=0):
				customer_info['voucher_applied_times'] = 1
			if (float(row[delivery_idx]) != 0):
				customer_info['delivery_fee_applied_times'] = 1
			
			customer_info['sum_amount'] = float(row[amount_idx])
			payment_info[row[payment_idx]] = 1
			platform_info[row[platform_idx]] =1;
			transmission_info[row[transmission_idx]]=1
			prev_row = row;
			if number_of_rows == 0:
				sorted_payment = sorted(payment_info.items(), key=operator.itemgetter(1))
				sorted_platform = sorted(platform_info.items(), key=operator.itemgetter(1))
				sorted_transmission = sorted(transmission_info.items(), key=operator.itemgetter(1))
				customer_info['most_visited_payment_id'] = unique_payment_id_dict[sorted_payment[-1][0]]
				customer_info['most_visited_platform_id'] = unique_platform_id_dict[sorted_platform[-1][0]]
				customer_info['most_visited_transmission_id'] = unique_transmission_id_dict[sorted_transmission[-1][0]]
				if (customer_info['order_success_count']):
					customer_info['avg_of_amount_paid'] = int(customer_info['sum_amount']/customer_info['order_success_count'])
				else:
					customer_info['avg_of_amount_paid']=0
				del customer_info['sum_amount']
				customers_transform_info.append(customer_info)

target_csv = 'train.csv'
keys = modified_column_lists;

with open(target_csv, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(customers_transform_info)


first = pd.read_csv('train.csv')
second = pd.read_csv('machine_learning_challenge_labeled_data.csv')

merged = pd.merge(first, second, how='left', on='customer_id')
merged.to_csv('merged.csv', index=False)












