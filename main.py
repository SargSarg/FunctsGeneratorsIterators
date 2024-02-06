def fid():
    a, b = 0, 1
    yield a
    yield b

    while True:
        a, b = b, a + b
        yield b
c = fid()
print(c)

# для примера возьмём строку
str_ = "my tst"
str_iter = iter(str_)

print(type(str_))  # строка
print(type(str_iter))  # итератор строки
print(next(str_iter))  # m

# Получим ещё несколько элементов последовательности
print(next(str_iter))  # y
print(next(str_iter))  #
print(next(str_iter))  # t
print(next(str_iter))  # s
print(next(str_iter))  # t

#Функции высшего порядка
def my_func(inside_func):
    ...
    inside_func()  # Вызов функции принятой в качестве аргумента
    ...

def a():
    def b():
        pass
    return b


def twice_func(inside_func):
    """Функция, выполняющая дважды функцию принятую в качестве аргумента"""
    inside_func()
    inside_func()
def hello():
    print("Hello")
test = twice_func(hello)


#Замыкание функций
def make_adder(x):
   def adder(n):
       return x + n # захват переменной "x" из nonlocal области
   return adder  # возвращение функции в качестве результата

# функция, которая будет к любому числу прибавлять пятёрку
add_5 = make_adder(5)
print(add_5(10))  # 15
print(add_5(100))  # 105

#Декораторы
def my_decorator(a_function_to_decorate):
    # Здесь мы определяем новую функцию - «обертку». Она нам нужна, чтобы выполнять
    # каждый раз при вызове оригинальной функции, а не только один раз
    def wrapper():
        # здесь поместим код, который будет выполняться до вызова, потом вызов
        # оригинальной функции, потом код после вызова
        print("Я буду выполнен до основного вызова!")

        result = a_function_to_decorate()  # не забываем вернуть значение исходной функции

        print("Я буду выполнен после основного вызова!")
        return result

    return wrapper
def my_function():
   print("Я - оборачиваемая функция!")
   return 0

print(my_function())
# Я - оборачиваемая функция!
# 0

decorated_function = my_decorator(my_function)  # декорирование функции
print(decorated_function())
# Я буду выполнен до основного вызова!
# Я - оборачиваемая функция!
# Я буду выполнен после основного вызова!
# 0
#Замерим время
import time
def decorator_time(fn):
   def wrapper():
       print(f"Запустилась функция {fn}")
       t0 = time.time()
       result = fn()
       dt = time.time() - t0
       print(f"Функция выполнилась. Время: {dt:.10f}")
       return dt  # задекорированная функция будет возвращать время работы
   return wrapper

def pow_2():
   return 10000000 ** 2

def in_build_pow():
   return pow(10000000, 2)

pow_2 = decorator_time(pow_2)
in_build_pow = decorator_time(in_build_pow)

pow_2()
# Запустилась функция <function pow_2 at 0x7f938401b158>
# Функция выполнилась. Время: 0.0000011921

in_build_pow()
# Запустилась функция <function in_build_pow at 0x7f938401b620>
# Функция выполнилась. Время: 0.0000021458


#Отдельное задание
import time
N = 100
def decorator_time(fn):
   def wrapper():
       t0 = time.time()
       result = fn()
       dt = time.time() - t0
       return dt
   return wrapper

def pow_2():
   return 10000000 ** 2
def in_build_pow():
   return pow(10000000, 2)
pow_2 = decorator_time(pow_2)
in_build_pow = decorator_time(in_build_pow)

mean_pow_2 = 0
mean_in_build_pow = 0
for _ in range(N):
   mean_pow_2 += pow_2()
   mean_in_build_pow += in_build_pow()
print(f"Функция {pow_2} выполнялась {N} раз. Среднее время: {mean_pow_2 / N:.10f}")
print(f"Функция {in_build_pow} выполнялась {N} раз. Среднее время: {mean_in_build_pow / 100:.10f}")



#Синтаксический сахар
def my_decorator(fn):
   def wrapper():
       fn()
   return wrapper  # возвращается задекорированная функция, которая заменяет исходную
# выведем незадекорированную функцию
def my_function():
   pass
print(my_function)  # <function my_function at 0x7f938401ba60>

# выведем задекорированную функцию
@my_decorator
def my_function():
   pass
print(my_function)  # <function my_decorator.<locals>.wrapper at 0x7f93837059d8>



# декоратор, в котором встроенная функция умеет принимать аргументы
def do_it_twice(func):
   def wrapper(*args, **kwargs):
       func(*args, **kwargs)
       func(*args, **kwargs)
   return wrapper
@do_it_twice
def say_word(word):
   print(word)
say_word("Oo!!!")
# Oo!!!
# Oo!!!


#Универсальный шаблон для декоратора
def my_decorator(fn):
    print("Этот код будет выведен один раз в момент декорирования функции")
    def wrapper(*args, **kwargs):
        print('Этот код будет выполняться перед каждым вызовом функции')
        result = fn(*args, **kwargs)
        print('Этот код будет выполняться после каждого вызова функции')
        return result
    return wrapper

#Декоратор может сохранять результат декорируемой функции в словаре назовем его кеш
def cache(func):
   cache_dict = {}
   def wrapper(num):
       nonlocal cache_dict
       if num not in cache_dict:
           cache_dict[num] = func(num)
           print(f"Добавление результата в кэш: {cache_dict[num]}")
       else:
           print(f"Возвращение результата из кэша: {cache_dict[num]}")
       print(f"Кэш {cache_dict}")
       return cache_dict[num]
   return wrapper