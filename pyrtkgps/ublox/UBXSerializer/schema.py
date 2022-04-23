VAL_SET = {
    "type": "array",
    "items": {
        "type": "object",
        "patternProperties": {
            "^.*$": {
                "type": "integer"
            }
        }
    }
}

VAL_GET = {
    "type": "array",
    "items": {
        "anyOf": [
            {"type": "integer"},
            {"type": "string"}
        ]
    }
}


VAL_DEL = VAL_GET


schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "RAM": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "UBX-CFG-VALGET": VAL_GET,
                "UBX-CFG-VALSET": VAL_SET
            }
        },
        "BBR": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "UBX-CFG-VALGET": VAL_GET,
                "UBX-CFG-VALSET": VAL_SET,
                "UBX-CFG-VALDEL": VAL_DEL
            }
        },
        "Flash": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "UBX-CFG-VALGET": VAL_GET,
                "UBX-CFG-VALSET": VAL_SET,
                "UBX-CFG-VALDEL": VAL_DEL
            }
        },
        "Default": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "UBX-CFG-VALGET": VAL_GET
            }
        },
    }
}
