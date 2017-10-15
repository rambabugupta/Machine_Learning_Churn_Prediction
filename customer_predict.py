import csv


def get_customer_status_from_csv(customer_id):
	csv_path = "predict_rf.csv"
	cus_id_idx = -1
	status_idx = -1
	skip = True
	with open(csv_path, "rb") as f_obj:
		reader=csv.reader(f_obj)
		for row in reader:
			if skip:
				skip = False
				cus_id_idx = row.index('customer_id');
				status_idx = row.index('predict_result');
			else:
				if row[cus_id_idx] == str(customer_id):
					return row[status_idx]
				else:
					continue;
	return 'customer id does not exist'


def get_customer_return_status(customer_id):
	status = get_customer_status_from_csv(customer_id);
	return  status

