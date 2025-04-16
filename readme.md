

## OUTPUT FORMAT

```
├── phase_countdowns
|  ├── phase
|  └── phase_ends_in
├── map
|  ├── mode
|  ├── phase
|  ├── round
|  ├── name
|  ├── team_ct
|  |  ├── score
|  |  ├── consecutive_round_losses
|  |  ├── timeouts_remaining
|  |  └── matches_won_this_series
|  ├── team_t
|  |  ├── score
|  |  ├── consecutive_round_losses
|  |  ├── timeouts_remaining
|  |  └── matches_won_this_series
|  └── round_wins
|     ├── 1
|     ├── 2
|     ├── 3
|     ├── 4
|     ├── 5
|     ├── 6
|     ├── 7
|     ├── 8
|     ├── 9
|     ├── 10
|     ├── 11
|     └── 12
├── round
|  └── phase
└── allplayers
   ├── team_t
   |  ├── 0
   |  |  ├── id
   |  |  ├── name
   |  |  ├── observer_slot
   |  |  ├── team
   |  |  ├── position
   |  |  |  ├── x
   |  |  |  ├── y
   |  |  |  └── z
   |  |  ├── forward
   |  |  |  ├── x
   |  |  |  ├── y
   |  |  |  └── z
   |  |  ├── match_stats
   |  |  |  ├── kills
   |  |  |  ├── assists
   |  |  |  ├── deaths
   |  |  |  ├── mvps
   |  |  |  └── score
   |  |  ├── state
   |  |  |  ├── health
   |  |  |  ├── armor
   |  |  |  ├── helmet
   |  |  |  ├── flashed
   |  |  |  ├── smoked
   |  |  |  ├── burning
   |  |  |  ├── money
   |  |  |  ├── round_kills
   |  |  |  ├── round_killhs
   |  |  |  ├── round_totaldmg
   |  |  |  └── equip_value
   |  |  └── weapons
   |  |     ├── weapon_0
   |  |     |  ├── name
   |  |     |  ├── paintkit
   |  |     |  ├── type
   |  |     |  └── state
   |  |     ├── weapon_1
   |  |     |  ├── name
   |  |     |  ├── paintkit
   |  |     |  ├── type
   |  |     |  ├── ammo_clip
   |  |     |  ├── ammo_clip_max
   |  |     |  ├── ammo_reserve
   |  |     |  └── state
   |  |     ├── weapon_2
   |  |     |  ├── name
   |  |     |  ├── paintkit
   |  |     |  ├── type
   |  |     |  ├── ammo_clip
   |  |     |  ├── ammo_clip_max
   |  |     |  ├── ammo_reserve
   |  |     |  └── state
   |  |     └── active
   |  |        ├── name
   |  |        ├── paintkit
   |  |        ├── type
   |  |        ├── ammo_clip
   |  |        ├── ammo_clip_max
   |  |        ├── ammo_reserve
   |  |        └── state
   |  ├── 1
   |  ...
   └── team_ct
      ├── 0
      ...
```

## Default config.ini example
```
[NETWORK]
ip = 127.0.0.1  ;; Local ip of the server or your dns
port = 3000  ;; port used on local server
flask_debug = False  ;; for debug purposes

[DEBUG]
debug_mode = True  ;; determines if the data is pulled from a test json file, not from a game
debug_save = False  ;; determines if the data from the game is saved to a test json file
save_file = tests/1.json  ;; debug file to save/load test data from

[API]
update_period = 1000 ;; time at which game and dashboard send/pull data to/from server

[CSV]
export = True  ;; if data will exported to a .csv format
file_path = exports/output.csv  ;; path to .csv file. If folder or file does not exists - it will be created
delimiter = ,  ;; a symbol used as a delimiter between columns (comma , is a vMix default)

[JSON]
export = True ;; if data will be exported to a .json format
raw = False  ;; determines a format of json outut data:
;; True: {"some_data": {"someotherdata": "value" ...}
;; False: {"some_data.someotherdata": value" ...}
file_path = exports/output.json  ;; path to .json file. If folder or file does not exists - it will be created
indent = 4  ;; amount of spaces used as an indentation

[EXCEL]
export = True  ;; if data will be exported to a .excel format
file_path = exports/output.xlsx  ;; if path to .xlsx file. If folder or file does not exists - it will be created

[LOG]
file_path = logs/latest.log  ;; path to a log file. folders/file will be created if not exists
backup_file_count = 3  ;; amount of additional files created.
;; When one log file exceeds set size, it will be renamed to a more older one. This way the data may be stored for a set size, by removing old logs
max_file_size = 2  ;; Size of one log file in megabytes
export_terminal_logging = True  ;; Output "export" logs to terminal. "Export" logs are ones about saving data to output files
preparation_terminal_logging = True  ;; Output "preparation" logs to terminal. "Preparation" logs are ones that tell how the data from the game is converted to output format
network_terminal_logging = True  ;; Output "network" logs to terminal. "Network" logs are those related to Flask server
terminal_logging_level = INFO ;; DEBUG, INFO, ERROR. Level of logs being output to terminal
file_logging_level = DEBUG ;; DEBUG, INFO, ERROR. Level of logs being written to a log file
```