def input_number():
    print("Введите число:")
    num = int(input())
    while True:
        if num < 0 or num >= 256:
            print("Ошибка ввода. ВВедите заново число")
            num = int(input())
            continue
        else:
            break
    return num


def element_gf(num):
    str_num = str(bin(num))[2:]
    print(str_num)
    power = len(str_num) - 1
    result = ""
    for s in str_num:
        if s == "1":
            if power == 0:
                result += "+1"
            elif power == 1:
                result += "+x"
            elif power == len(str_num) - 1:
                result += "x^{0}".format(power)
            else:
                result += "+x^{0}".format(power)
        power -= 1
    print(result)


def degree(num):
    return num.bit_length()-1


def add_sub(num1, num2):
    return num1 ^ num2


def mult_polynoms(num1, num2):
    result = 0
    while num2:
        if num2 & 1:
            result ^= num1
        num1 <<= 1
        num2 >>= 1
    return result


def multEleventGF (num1,num2, prim):
    result = 0
    while num2:
        if num2 & 1:
            result ^= num1
        num1 <<= 1
        if num1 & 0x100:
            num1 ^= prim
        num2 >>= 1
    #print(result)
    return result


def mult_element(num1, num2, poly):
    result = mult_polynoms(num1, num2)
    result = mod(result, poly)

    return result

def div(dividend, divider):
    if dividend == 0:
        return 0
    if divider == 1:
        return dividend
    if dividend == 1:
        return 0
    result = 0
    while degree(dividend) >= degree(divider):
        result = add_sub(result, 1 << (degree(dividend)-degree(divider)))
        dividend = add_sub(dividend, divider << (degree(dividend)-degree(divider)))
    return result

def mod(dividend, divider):
    if dividend == 0:
        return 0
    if dividend == 1:
        if divider == 1:
            return 0
        return 1
    while(degree(dividend) >= degree(divider)):
        dividend =  add_sub(dividend, divider << (degree(dividend) - degree(divider)))
    return dividend

def extandEuclid(num1, num2):
    x, xx, y, yy = 1, 0, 0, 1
    while num2:
        q = div(num1, num2)
        num1, num2 = num2, mod(num1, num2)
        x, xx = xx, x ^ multEleventGF(xx, q, 0x11b)
        y, yy = yy, y ^ multEleventGF(yy, q, 0x11b)
    return x

def potentition(num):
    if num == 0:
        return num
    res = 1
    deg = 254
    while deg > 0:
        if (deg & 1) == 1:
            res = multEleventGF(res, num, 283)
        res = multEleventGF(res, res, 283)
        deg >>= 1
    return res