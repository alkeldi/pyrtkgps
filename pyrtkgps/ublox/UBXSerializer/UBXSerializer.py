import yaml
import jsonschema
from pyubx2 import UBXMessage
from schema import schema


def validate(config):
    try:
        error = None
        jsonschema.validate(config, schema)
    except jsonschema.ValidationError as e:
        while e.parent:
            e = e.parent
        path_entries = [str(entry) for entry in e.path]
        path_entries.insert(0, "<root>")
        path = "/".join(path_entries)
        error = f"\n{path}: {e.message}"

    if error:
        raise ValueError(error)


def cleanup(config):
    for layer_name in config:
        layer = config[layer_name]
        for method_name in layer:
            raw_data = layer[method_name]
            cleaned_data = []
            for item in raw_data:
                if isinstance(item, dict):
                    key = list(item.keys())[0].replace("-", "_")
                    value = list(item.values())[0]
                    cleaned_data.append((key, value))
                elif isinstance(item, str):
                    key = item.replace("-", "_")
                    cleaned_data.append(key)
                else:
                    cleaned_data.append(item)
            layer[method_name] = cleaned_data
    return config


def ubx_cfg_valget(cfg_data, layer):
    memory_layer_to_code = {"RAM": 0, "BBR": 1, "Flash": 2, "Default": 7}
    layer_data = memory_layer_to_code[layer]
    return UBXMessage.config_poll(layer_data, 0, cfg_data).serialize()


def ubx_cfg_valset(cfg_data, layer):
    memory_layer_to_code = {"RAM": 1, "BBR": 2, "Flash": 4}
    layer_data = memory_layer_to_code[layer]
    return UBXMessage.config_set(layer_data, 0, cfg_data).serialize()


def ubx_cfg_valdel(cfg_data, layer):
    memory_layer_to_code = {"BBR": 2, "Flash": 4}
    layer_data = memory_layer_to_code[layer]
    return UBXMessage.config_del(layer_data, 0, cfg_data).serialize()


def to_binary(config):
    result = b""
    for layer_name in config:
        layer = config[layer_name]
        for method_name in layer:
            method_data = layer[method_name]
            if method_name == 'UBX-CFG-VALSET':
                result += ubx_cfg_valset(method_data, layer_name)
            elif method_name == 'UBX-CFG-VALDEL':
                result += ubx_cfg_valdel(method_data, layer_name)
            elif method_name == 'UBX-CFG-VALGET':
                result += ubx_cfg_valget(method_data, layer_name)
            else:
                raise ValueError(f"invalid configuration method {method_name}")
    return result


class UBXSerializer:
    @staticmethod
    def serialize(ubx_config):
        config = yaml.safe_load(ubx_config)
        validate(config)
        config = cleanup(config)
        bin_data = to_binary(config)
        return bin_data
