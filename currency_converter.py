#!/usr/bin/python3

"""
Usage:
    currency_converter.py [--amount=<amount>] [--input_currency=<input_currency>] [--output_currency=<output_currency>]

Options:
    --amount=<amount>                       Amount
    --input_currency=<input_currency>       inputCurrency
    --output_currency=<output_currency>     outputCurrency
"""

import json
import re

import requests
from docopt import docopt

with open('currency_code.json') as data_file:
    currency_code = json.load(data_file)


def check_currency_code(currency_code, currency, total_code):
    for i in range(total_code):
        if currency == currency_code['code'][i]['symbol']:
            currency = currency_code['code'][i]['letter']
            break
    return currency


def convert_currency(input_currency, output_currency, amount):
    r = requests.get(
        'https://www.google.com/finance/converter?a={}&from={}&to={}'.format(amount, input_currency, output_currency))
    if r.status_code == 200:
        data = r.text  # Changed .content to .text
        try:
            fetch_result = re.findall('<span class=bld>(.*?) ' + output_currency + '</span>', data, re.DOTALL)
            conversion_result = float("".join(fetch_result).replace('\n', ' '))
            return conversion_result
        except:
            return 'enter another output currency'
    else:
        return 'try again later'


def main():
    arguments = docopt(__doc__)
    amount = arguments.get('--amount')
    input_currency = arguments.get('--input_currency')
    output_currency = arguments.get('--output_currency')

    total_code = len(currency_code['code'])
    if input_currency.isalpha() == False or len(input_currency) < 3:
        input_currency = check_currency_code(currency_code, input_currency, total_code)
    result = {
        "input": {
            "amount": amount,
            "currency": input_currency  # Removed str() around input_currency
        },
        "output": {
        }
    }
    if output_currency:
        if output_currency.isalpha() == False or len(output_currency) < 3:
            output_currency = check_currency_code(currency_code, output_currency, total_code)
        conversion_result = convert_currency(input_currency, output_currency, amount)
        result['output'].update({output_currency: conversion_result})  # Removed str() around output_currency
        print(json.dumps(result, sort_keys=True, indent=4))  # Added print() to output the JSON result
    else:
        for i in range(total_code):
            output_currency = currency_code['code'][i]['letter']
            if output_currency != input_currency:
                conversion_result = convert_currency(input_currency, output_currency, amount)
                result['output'].update({output_currency: conversion_result})  # Removed str() around output_currency
        print(json.dumps(result, sort_keys=True, indent=4))  # Added print() to output the JSON result


if __name__ == '__main__':
    main()
