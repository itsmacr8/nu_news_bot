def write_bot_status(filename, content):
    with open(filename, mode='w', encoding='UTF-8') as file:
        file.write(content)
