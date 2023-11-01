def format_date(data):
    try:
        data_splitted = data.split('/')
        year = data_splitted[2].split('00:00:00')
        formatted_data = year[0].strip() + '-' + data_splitted[1] + '-' + data_splitted[0]
        return formatted_data
    except Exception as error:
        print(error, flush=True)