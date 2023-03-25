from datetime import datetime


def ravel(data: list):
    modified = False
    for row in data:
        dict_keys = [key for key in row if type(row[key]) == dict]
        for dict_key in dict_keys:
            for valKey, value in row[dict_key].items():
                row[dict_key + "_" + valKey] = value
            del row[dict_key]
            modified = True
    if modified:
        ravel(data)


def transform_date(data, date_columns):
    for row in data:
        for column in date_columns:
            if column in row:
                row[column] = datetime.fromtimestamp(row[column] / 1000).date()

    return data
