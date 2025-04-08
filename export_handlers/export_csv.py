import json


def write_csv(data, path="test.csv"):
    result = {
        "phase_countdowns": {
            "phase": data["phase_countdowns"]["phase"],
            "phase_ends_in": data["phase_countdowns"]["phase_ends_in"],
        },
        "map": {
            "mode": data["map"]["mode"],
            "phase": data["map"]["phase"],
            "round": data["map"]["round"],
            "name": data["map"]["name"],
            "round_wins": {num: result for num, result in data["map"]["round_wins"].items()},
            "team_ct": {
                "score": data["map"]["team_ct"]["score"],
                "consecutive_round_losses": data["map"]["team_ct"]["consecutive_round_losses"],
                "timeouts_remaining": data["map"]["team_ct"]["timeouts_remaining"],
                "matches_won_this_series": data["map"]["team_ct"]["matches_won_this_series"],
            },
            "team_t": {
                "score": data["map"]["team_t"]["score"],
                "consecutive_round_losses": data["map"]["team_t"]["consecutive_round_losses"],
                "timeouts_remaining": data["map"]["team_t"]["timeouts_remaining"],
                "matches_won_this_series": data["map"]["team_t"]["matches_won_this_series"],
            }
        }
    }

    result = flatten_dict(result)
    with open(path, mode="w+") as file:
        headers = ",".join(result.keys())
        values = ",".join(map(str, result.values()))

        file.write(headers + "\n")
        file.write(values)


def flatten_dict(d, parent_key='', sep='.'):
    """
    Flatten a nested dictionary.

    :param d: The dictionary to flatten.
    :param parent_key: The base key string for recursion (used internally).
    :param sep: The separator between keys.
    :return: A flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


if __name__ == "__main__":
    write_csv(json.load(open("../tests/1.json", mode="r")))