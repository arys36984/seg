def is_prime(number):

    if type(number) != int or number < 1:
        raise ValueError("Number must be a positive integer")

    if number == 1:
        return False

    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    else:
        return True