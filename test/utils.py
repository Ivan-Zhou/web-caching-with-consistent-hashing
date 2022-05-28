import pandas as pd


def get_test_urls(n):
	df = pd.read_csv("test/test_data.csv")[:n]
	return df["url"].tolist()
