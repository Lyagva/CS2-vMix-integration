from logging_handler import preparation_logger

def prepare_data(data):
    result = {}
    preparation_logger.info('Preparing data')

    if "phase_countdowns" in data:
        result["phase_countdowns"] = {
            "phase": data["phase_countdowns"]["phase"],
            "phase_ends_in": data["phase_countdowns"]["phase_ends_in"],
        }
    else:
        preparation_logger.debug('No phase countdowns')

    if "map" in data:
        preparation_logger.debug('Preparing map')
        result["map"] = {
            "mode": data["map"]["mode"],
            "phase": data["map"]["phase"],
            "round": data["map"]["round"],
            "name": data["map"]["name"],
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
        if "round_wins" in data["map"]:
            preparation_logger.debug('Preparing round results history')
            result["map"]["round_wins"] = {num: result for num, result in data["map"]["round_wins"].items()}
        else:
            preparation_logger.debug('No round results history yet')
    else:
        preparation_logger.debug('No map entries')

    if "round" in data:
        preparation_logger.debug('Preparing round')
        result["round"] = {"phase": data["round"]["phase"]}
    else:
        preparation_logger.debug('No round')

    if "bomb" in data:
        preparation_logger.debug('Preparing bomb information')
        result["bomb"] = {
            "state": data["bomb"]["state"],
            "position": flatten_vector_3(data["bomb"]["position"]),
        }
        if "player" in data["bomb"]:
            preparation_logger.debug('Preparing player holding bomb id')
            result["bomb"]["player"] = data["bomb"]["player"]
        else:
            preparation_logger.debug('No player holding bomb')
    else:
        preparation_logger.debug('No bomb found')

    if "allplayers" in data:
        preparation_logger.debug('Preparing all players')
        players = [generate_player(id, item) for id, item in data["allplayers"].items()]
        result["allplayers"] = {
            "team_t": {i: player for i, player in enumerate(sorted([i for i in players if i["team"] == "T"],
                             key=lambda item: item["match_stats"]["score"]))},
            "team_ct": {i: player for i, player in enumerate(sorted([i for i in players if i["team"] == "CT"],
                             key=lambda item: item["match_stats"]["score"]))},
        }
    else:
        preparation_logger.debug('No players found')

    return result


def generate_player(id, player):
    result = {
        "id": id,
        "name": player["name"],
        "observer_slot": player["observer_slot"],
        "team": player["team"],
        "position": flatten_vector_3(player["position"]),
        "forward": flatten_vector_3(player["forward"]),
        "match_stats": {
            "kills": player["match_stats"]["kills"],
            "assists": player["match_stats"]["assists"],
            "deaths": player["match_stats"]["deaths"],
            "mvps": player["match_stats"]["mvps"],
            "score": player["match_stats"]["score"],
        },
        "state": {
            "health": player["state"]["health"],
            "armor": player["state"]["armor"],
            "helmet": player["state"]["helmet"],
            "flashed": player["state"]["flashed"],
            "smoked": player["state"]["smoked"],
            "burning": player["state"]["burning"],
            "money": player["state"]["money"],
            "round_kills": player["state"]["round_kills"],
            "round_killhs": player["state"]["round_killhs"],
            "round_totaldmg": player["state"]["round_totaldmg"],
            "equip_value": player["state"]["equip_value"],
        },
        "weapons": player["weapons"],
    }
    preparation_logger.debug('Preparing player: {}'.format(player["name"]))

    active_weapons = [i for i in player["weapons"].values() if i["state"] == "active"]
    if active_weapons:
        result["weapons"]["active"] = active_weapons[0]
        preparation_logger.debug('Active weapon: {}'.format(active_weapons))
    else:
        preparation_logger.debug('No active weapons found')

    return result


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


def flatten_vector_3(vector, char=", "):
    vector = vector.split(char)
    return {
        "x": vector[0],
        "y": vector[1],
        "z": vector[2],
    }