from datetime import datetime, time


DATE_FORMAT = '%m/%d/%Y'

# Dict keys
KEY_DATE = 'Date'
KEY_DESCRIPTION = 'Description'
KEY_ORIGINAL_DESCRIPTION = 'Original Description'
KEY_AMOUNT = 'Amount'
KEY_TRANSACTION_TYPE = 'Transaction Type'
KEY_CATEGORY = 'Category'
KEY_ACCOUNT_NAME = 'Account Name'
KEY_LABELS = 'Labels'
KEY_NOTES = 'Notes'


class TransactionFilter():
    def __init__(self, key, expected_value):
        self.key = key
        self.expected_value = expected_value

    def matches(self, transaction):
        return transaction[self.key] == self.expected_value


def to_dict(record):
    date_object = datetime.strptime(record[KEY_DATE], DATE_FORMAT)

    converted = {}
    converted[KEY_DATE] = date_object,
    converted[KEY_AMOUNT] = float(record[KEY_AMOUNT])
    copy_values(
        [
            KEY_DESCRIPTION,
            KEY_ORIGINAL_DESCRIPTION,
            KEY_TRANSACTION_TYPE,
            KEY_CATEGORY,
            KEY_ACCOUNT_NAME,
            KEY_LABELS,
            KEY_NOTES
        ],
        record,
        converted
    )

    return converted


def copy_values(keys, source, destination):
    for key in keys:
        destination[key] = source[key]


def group_by(transactions, key):
    grouping = {}
    for transaction in transactions:
        val = transaction[key]
        if val not in grouping:
            grouping[val] = []
        grouping[val].append(transaction)

    return grouping


def sum_transactions(transactions):
    return sum([float(tx[KEY_AMOUNT]) for tx in transactions])


def filter_transactions(transactions, filters, filter_type='ALL'):
    # The alternative to 'ALL' is 'ANY'
    op = all if filter_type == 'ALL' else any
    filtered = []
    for transaction in transactions:
        if op([filt.matches(transaction) for filt in filters]):
            filtered.append(transaction)

    return filtered


def filter_transactions_by_date_range(
        transactions, start_date=None, end_date=None):
    date_format = '%m/%d/%Y'
    if start_date:
        start_date = datetime.strptime(start_date, date_format)
    else:
        start_date = datetime(1900, 1, 1)
    if end_date:
        end_date = datetime.strptime(end_date, date_format)
    else:
        end_date = datetime(3000, 1, 1)

    filtered = []
    for transaction in transactions:
        if (start_date
                <= datetime.strptime(transaction[KEY_DATE], date_format)
                <= end_date):
            filtered.append(transaction)

    return filtered


def get_credit_card_account_filters():
    return [
        TransactionFilter(KEY_ACCOUNT_NAME, '<REDACTED>'),
    ]


def get_cash_and_venmo_filters():
    return [
        TransactionFilter(KEY_ACCOUNT_NAME, 'Cash'),
        TransactionFilter(KEY_ACCOUNT_NAME, 'Venmo'),
    ]


def get_food_category_filters():
    return [
        TransactionFilter(KEY_CATEGORY, 'Coffee Shops'),
        TransactionFilter(KEY_CATEGORY, 'Food & Dining'),
        TransactionFilter(KEY_CATEGORY, 'Groceries'),
        TransactionFilter(KEY_CATEGORY, 'Fast Food'),
        TransactionFilter(KEY_CATEGORY, 'Restaurants'),
        TransactionFilter(KEY_CATEGORY, 'Snacks'),
    ]


def get_known_equivalencies():
    return


def bucketize_by_amount(transactions, bin_edges):
    bin_edges = list(sorted(set(bin_edges)))
    bins = [[] for _ in range(len(bin_edges) + 1)]
    for tx in transactions:
        tx_amount = float(tx[KEY_AMOUNT])

        # If transaction amount is greater than greatest bin edge
        if tx_amount >= bin_edges[-1]:
            bins[-1].append(tx)
            continue

        # If transaction amount is less than greatest bin edge
        for idx, edge in enumerate(bin_edges):
            if tx_amount < edge:
                bins[idx].append(tx)
                break  # move on to next transaction

    return bins


def mint_date_to_key(date):
    # Dates are in the form of MM/DD/YYYY
    # Use 'YYYY-MM' as the grouping key
    fmted_date = '-'.join([date.split('/')[i] for i in (2, 0)])
    return datetime.strptime(fmted_date, '%Y-%m')


def group_by_month(transactions):
    groupings = {}
    for tx in transactions:
        key = mint_date_to_key(tx[KEY_DATE])
        if key not in groupings:
            groupings[key] = []
        groupings[key].append(tx)

    return groupings
