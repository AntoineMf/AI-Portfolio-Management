import json

data_stock={
    "start_date":"2019-01-22",
    "end_date":"2019-06-30",
    "host":"127.0.0.1",
    "port":5432,
    "user":"postgres",
    "password":"pw",
    "database":"stock_pi2",
    "nb_indivi":30,
    "min_share":1,
    "max_share":500,
    "nb_asset":15,
    "n_random_select":25,
    "n_random_tickers":5,
    "t":0,
    "T":30,
    "sig0":5,
    "nb_asset_select":12,
    "epsilon":0.01
}

def ReadJsonFile(file_path):

    with open(file_path) as json_file:
        data = json.load(json_file)
        
        print('start date: ' + data['start_date'])
        print('end date: ' + data['end_date'])
        print('epsilon:', data['epsilon'])
        print('')
    return data

def WriteJsonFile(file_path,data):

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


WriteJsonFile("./Json/config_overwritten.json",data_stock)
ReadJsonFile("./Json/config.json")
