

def to_dast_config_models(configs:list) -> list:
    models = list()
    for config in configs:
        model = {}
        model["scantNodeXpath"] = config[0]
        # optional entries can be set to None and 
        # are skipped in the model
        if config[1]:
            model["scantNodeNewValue"] = config[1]
            if len(config) > 2 and config[2]:
                model["encryptNodeValue"] = config[2]
            models.append(model)

    return models

