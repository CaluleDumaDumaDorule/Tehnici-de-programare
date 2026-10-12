import argparse
from webtools import site_report

parser = argparse.ArgumentParser()
parser.add_argument("url")

args = parser.parse_args()

site_report(args.url)
