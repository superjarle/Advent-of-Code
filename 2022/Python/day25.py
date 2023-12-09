puzzleinput = '202225.txt'

with open(puzzleinput, 'r') as file:
    snafu_numbers = file.readlines()


def decimal_to_snafu(decimal):
  
    if decimal == 0:
        return '0'

    snafu_digits = []
    while decimal > 0:
        remainder = decimal % 5
        if remainder == 4:
            snafu_digit = '-'
            decimal += 1 
        elif remainder == 3:
            snafu_digit = '='
            decimal += 2
        else:
            snafu_digit = str(remainder)
        snafu_digits.append(snafu_digit)
        decimal //= 5

    return ''.join(reversed(snafu_digits))

snafu_sum = decimal_to_snafu(total_decimal)
snafu_sum