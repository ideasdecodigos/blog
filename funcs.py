

def cipherAbb(number):
    if number >= 1000000000:
        number = number / 1000000000
        number = f'{number:.1f}'
        return "{}{}".format(number, 'B')
    elif number >= 1000000:
        number = number / 1000000
        number = f'{number:.1f}'
        return "{}{}".format(number, 'M')
    elif number >= 1000:
        number = number / 1000
        number = f'{number:.1f}'
        return "{}{}".format(number, 'K')
    else:
        return number
        
    