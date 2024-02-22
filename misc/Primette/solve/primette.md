# Solver Coquette

La solución de este reto tiene dos partes diferenciadas. La primera es encontrar el valor perdido de la semilla. Esto se puede hacer tomando, por ejemplo, los 5 primeros valores del fichero output.txt. Generando números de 1024 bits con el método n_bit_random proporcionado en el challenge, se puede ir iterando con distintos valores de la semilla (el bueno es 10, para que no se pierda mucho tiempo en esta parte), y en cuanto se obtienen los 5 primeros valores seguidos, se puede entender que el valor de la semilla se ha encontrado. Una vez encontrado el valor, sólo hay que encontrar un primo de bajo nivel con el método proporcionado, pero el problema es que no se garantiza la primalidad de los números generados. Aplicando el test de miller-rabin se pueden ir generando primos con el méotodo dado hasta encontrar el primo de 1024 bits con el que se hace XOR (se garantiza que es el primero que pase el test una vez encontrada la semilla, por cómo está planteado el código) y bruteforcear los bytes hasta recuperar el zip con la flag. 

El código que lo resuelve se puede encontrar en el fichero solver.py y a continuación:

```python3
import random

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def n_bit_random(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def getLowLevelPrime(n):
    while True:
        pc = n_bit_random(n)
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
                print("pc:", pc)
                break
        else:
            return pc


def is_miller_rabin_passed(mrc):
    max_divisions_by_two = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        max_divisions_by_two += 1
    assert (2 ** max_divisions_by_two * ec == mrc - 1)

    def trial_composite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(max_divisions_by_two):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    number_of_rabin_trials = 20
    for i in range(number_of_rabin_trials):
        round_tester = random.randrange(2, mrc)
        if trial_composite(round_tester):
            return False
    return True

def find_prime():
    values = [
        121801052297658028091777076506445143193065101178144372882196128909897866332438422565688398220182131195200015710061040139683639767479864483141606628224838341699237057452367041152968465108187249409929095720450658473624350235695103663251998400585620402131556598873685794575789216195478299765023121924089717420244,
        138093857911392463945029613822522802600069105973234019206788034668526076809028461255031254837856593916298012112801503042867878338390612151994754376792406698715059840981301702034025636498867653603716437151906310311210568549328472344618937214040917263369352398108446408200917304001434370059359364679054887284234,
        172962139495122689266196588834067308877709597324651313683901393950973739512788259236807367333790431731082645680753080118811231197103951796080355082855436552022683636381581137387323758694284359910548640317081624358904129885479683940365182769670539704666177591482721693973091277989904121477386104337660114614223,
        136791590018981995380375896663642191921239405327343323637193359048627323615416863388532224199479266334021421104244864089771508654507384856068508169518568885198473673954723675994673180329022265411842609969138507249124005385053835116912340618255274325442358142600509643622671667329457620698570742372314519274837,
        126269292321846508390256591302973708369426920033326931048919825078137301017406842637479681757695160602973962555713939595636732723211984686957689174658820262882042297658481723696526563950242304112670551426412621296184499988784699194089452683442460598994658993344630225149745852587795636063378257028508304774338,
        124743748562912234147039086233548397825593272057908304286855253240484717622022433349874992175876723314821276321021164457828293266596549811709885688780749617170796592333878167470305448397144779600780496845220758102925931358821349074259104087773502518575998045896931153368087158162535208199418607341455719896861,
        159509442517420132465381367425760108100720695077974110504893406093492427829130184384190196217678394684873738827619827690551849102467319800976525564499531299194012084383448146396113219875153419430059950572371425345905799101491365136621648574539585311902508145258312920391379787388007257388470978623316960071408]

    for i in range(100):
        random.seed(i)
        last_found_value = 0
        test = n_bit_random(1024)
        if test == values[0]:
            while last_found_value < len(values) and test == values[last_found_value]:
                last_found_value += 1
                test = n_bit_random(1024)
            if last_found_value == len(values):
                break
    while True:
        n = 1024
        prime_candidate = getLowLevelPrime(n)
        if is_miller_rabin_passed(prime_candidate):
            return prime_candidate


def brute_force(p, b):
    for i in range(256):
        if ((i * p) % 256) ^ 0xff == b:
            return i
    return False


def decode(file_bytes):
    original_bytes = b""

    p = find_prime()

    print("Found p:", p)
    for b_index in range(len(file_bytes)):
        if b_index % 2 == 0:
            original_bytes += ((file_bytes[b_index] - 8) % 256).to_bytes(1, 'little')
        else:
            decoded_byte = brute_force(p, file_bytes[b_index]).to_bytes(1, 'little')
            original_bytes += decoded_byte

    with open('solved.zip', 'wb') as s:
        s.write(original_bytes)


if __name__ == '__main__':
    with open('flag.enc', 'rb') as e:
        decode(e.read())
```