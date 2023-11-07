def format_date(data):
    try:
        data_clean = data.split(' 00:00')[0]
        data_splitted = data_clean.split('/')
        formatted_data = data_splitted[2] + '-' + data_splitted[1] + '-' + data_splitted[0]
        return formatted_data
    except Exception as error:
        print(error, flush=True)
