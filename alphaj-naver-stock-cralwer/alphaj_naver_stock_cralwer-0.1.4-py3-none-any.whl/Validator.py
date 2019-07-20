def check_valid_stock_code(stock_code):
    if stock_code.isdigit() and stock_code[-1] == '0':
        return True
    
    return False

def check_valid_stock_name(stock_name):
    
    name_len = len(stock_name)

    if stock_name[name_len-2:] == "스팩":
        return False
    if stock_name[name_len-2:] == "우B":
        return False
    if stock_name[name_len-1:] == "우":
        return False
    if stock_name[name_len-3:] == "우선주":
        return False
    if stock_name[name_len-1:] == ")":
        return False
    if stock_name[name_len-2:] == "1호":
        return False
    if stock_name[name_len-2:] == "2호":
        return False
    if stock_name[name_len-2:] == "3호":
        return False
    if stock_name[name_len-2:] == "4호":
        return False
    if stock_name[name_len-2:] == "5호":
        return False
    if stock_name[name_len-2:] == "6호":
        return False
    if stock_name[name_len-2:] == "7호":
        return False
    if stock_name[name_len-2:] == "8호":
        return False
    if stock_name[name_len-2:] == "9호":
        return False
    if stock_name[name_len-4:] == "SPAC":
        return False

    return True