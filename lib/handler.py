from lib.parser import get_insertion_values, incorporate_plugin_input
from lib.storage.db.connection import get_data_from_table


def process_response(response, plugin_response):
    result = {}
    get_insertion_values(result, plugin_response['response']['success'], response, "sys#input")
    processed_data = incorporate_plugin_input(result, plugin_response['input'])
    return assign_to_db_processor(processed_data)


def assign_to_db_processor(data):
    result = []
    for key, value in data.items():
        select_column = {'select_column': value['values'][0]}
        result.extend(get_data_from_table(value, select_column, value['config']))
    return result
