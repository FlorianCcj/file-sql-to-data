# A practical Guide to Anonymizing Datasets with Python & Faker
# blog.districtdatalabs.com/a-practical-guide-to-anonymizing-datasets-with-python-faker
# pip install faker unicodecsv

import unicodecsv as csv
from faker import Factory
from collections import defaultdict

def anonymize_rows(rows):
	"""
	Rows is an iterable of dictionaries that contain name and
	email fields that need to be anonymized
	"""

	faker = Factory.create()
	names = defaultdict(faker.name)
	emails = defaultdict(faker.email)

	for row in rows:
		row['name'] = names[row['name']]
		row['email'] = emails[row['email']]

		yield row

def anonymize(source, target):
	"""
	The source argument is a path to a CSV file containing data to anonymize
	while target is a path to write the anonymized CSV data to.
	"""
	with open(source, 'rU') as file:
		with open(target, 'w') as output:
			reader = csv.DictReader(file)
			writer = csv.DictWriter(output, reader.fieldnames)

			for row in anonymize_rows(reader):
				writer.writerow(row)

test = anonymize('firstFile.csv', 'output.csv')