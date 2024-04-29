from flask import request

from lib.storage.db.connection import get_data_from_table


def get_keys_and_values(payload, source, source_key="sys#source"):
    if isinstance(payload, dict):
        for key, value in payload.items():
            if value is not None and isinstance(value, dict) and source_key in value:
                payload[key] = get_hash_key(get_source_value(value[source_key]['key'], source), value[source_key])
            elif value is not None and "@plugin." in value:
                payload[key] = parse_plugin_value(value, None)
            elif value is not None and "{req[" in value:
                payload[key] = get_args([value])[0]
            else:
                if isinstance(value, dict):
                    request.json[key] = payload[key]
                get_keys_and_values(value, source)


def get_insertion_values(result, payload, response, source_key="sys#input"):
    if isinstance(payload, dict):
        for key, value in payload.items():
            if value is not None and isinstance(value, dict) and source_key in value:
                c = value[source_key]
                for item in c if isinstance(c, list) else [c]:
                    if item['key'] not in result:
                        result[item['key']] = {'columns': [], 'values': []}
                    result[item['key']]['columns'].append(item['value'])
                    result[item['key']]['values'].append(response[key])

            # get_input_source_by_key(key, value[source_key], response)
            # payload[key] = get_insertion_attr(get_source_value(value[source_key]['key'], source), response,
            #                                   value[source_key], key)
            elif value is not None and "@plugin." in value:
                payload[key] = parse_plugin_value(value, None)
            elif value is not None and "{req[" in value:
                payload[key] = get_args([value])[0]
            else:
                get_insertion_values(result, value, response)


def incorporate_plugin_input(data, plugin_input):
    for key, input_data in plugin_input.items():
        values = input_data.get('values', [])
        for value in values:
            column, column_value = value.split('=')
            column_value = get_args([column_value])[0]
            if column is not None and column_value is not None:
                data[key]['columns'].append(column)
                data[key]['values'].append(column_value)
                data[key]['config'] = input_data
    return data


def get_input_source_by_key(key_name, key_ref, response):
    if isinstance(key_ref, list):
        result = {_key_ref['key']: {'column': _key_ref['value'], 'value': response[key_name]} for _key_ref in key_ref}
    else:
        result = {key_ref['key']: {'column': key_ref['value'], 'value': response[key_name]}}
    response[key_name] = result


def get_insertion_attr(value, res, _v, _k):
    _res_value = res[_k]
    value['column'] = _v['value']
    res[_k] = {
        'key': _k,
        'value': _res_value,
        'column': _v['value'],
        'ops': value
    }

    return res


def parse_response_data(data):
    result = {}
    if isinstance(data, dict):
        for key, value in data.items():
            for _item in value:
                if _item not in result:
                    result[_item] = {'columns': [], 'values': []}

                result[_item]['columns'].append(value[_item]['column'])
                result[_item]['values'].append(value[_item]['value'])

    return result


def get_hash_key(config, _v):
    column_value = _v['value']

    t_value = get_data_from_table(resolve_usr_condition(config), {'select_column': column_value}, config)
    if "fun" in _v:
        return parse_plugin_value(_v['fun'], [t_value])
    return t_value


def parse_plugin_value(value, _args):
    function_name = value.split('.', 1)[1]
    f_arg = function_name.split('(')
    function_name = f_arg[0]
    args = f_arg[1].replace(')', '')
    args = args.split(',')

    """importing plugin file"""
    import lib.plugin.plugin as plugin

    function = getattr(plugin, function_name)
    # function = globals()[function_name]

    if _args is None:
        _args = get_args(args)

    _args = list(filter(lambda x: x != "", _args))
    if len(_args) > 0:
        return function(*_args)
    return function()


def resolve_usr_condition(value):
    condition = value['condition']
    results = get_args(condition)

    return {'table': value['table'], 'condition': results}


def get_args_v1(args):
    results = []
    for _x in args:
        if request and "{req[" in _x:
            results.append(_x.format(req=request.json))

    if len(results) > 0:
        return results
    else:
        return args


def get_args(args):
    if request:
        results = [_x.format(req=request.json) for _x in args if "{req[" in _x]
        if results:
            return results
    return args


def get_source_value(value, source):
    return source[value]
