# goit-web-hw-03


## Перша частина для потоків
* Напишіть програму обробки директорії "Хлам", яка 
	- копіює файли з заданої директорії (та всіх її піддиректорій) до цільової директорії, сортуючи їх за розширеннями. 
	- Програма повинна використовувати багатопотоковість для ефективної обробки великих обсягів файлів та піддиректорій.

Програма приймає два аргументи командного рядка:
* шлях до директорії з файлами для обробки.
* шлях до директорії, де будуть розміщені відсортовані файли. 
    За замовчуванням використовується директорія dist

Вона має рекурсивно обходити всі піддиректорії джерельної директорії. 

Наприклад маємо наступну структуру директорій та файлів.
📂picture
 ┣ 📂icons
 ┃ ┣ 📜e-learning_icon.jpg
 ┃ ┗ 📜mongodb.jpg
 ┣ 📂Logo
 ┃ ┣ 📜IBM+Logo.png
 ┃ ┣ 📜ibm.svg
 ┃ ┗ 📜logo-tm.png
 ┣ 📂Other
 ┃ ┣ 📂Icons
 ┃ ┃ ┗ 📜1600.png
 ┃ ┣ 📜golang.png
 ┃ ┣ 📜hqdefault.jpg
 ┃ ┗ 📜nodejslogo.png
 ┣ 📂wallpaper
 ┃ ┣ 📜js.png
 ┃ ┗ 📜node-wallpaper.jpg
 ┣ 📜bot-icon.png
 ┗ 📜javascript_encapsulation.jpg

Кожен файл має бути скопійований у піддиректорію цільової директорії, назва якої відповідає розширенню файлу. 
І після сортування це має виглядати наступним чином.

📂dist
 ┣ 📂jpg
 ┃ ┣ 📜e-learning_icon.jpg
 ┃ ┣ 📜hqdefault.jpg
 ┃ ┣ 📜javascript_encapsulation.jpg
 ┃ ┣ 📜mongodb.jpg
 ┃ ┗ 📜node-wallpaper.jpg
 ┣ 📂png
 ┃ ┣ 📜1600.png
 ┃ ┣ 📜bot-icon.png
 ┃ ┣ 📜golang.png
 ┃ ┣ 📜IBM+Logo.png
 ┃ ┣ 📜js.png
 ┃ ┣ 📜logo-tm.png
 ┃ ┗ 📜nodejslogo.png
 ┗ 📂svg
   ┗ 📜ibm.svg

Пришвидшіть обробку великих каталогів з великою кількістю вкладених директорій та файлів за рахунок паралельного виконання обходу всіх директорій в окремих потоках. 
Найбільш витратним за часом буде перенесення файлу та отримання списку файлів у директорії (ітерація по вмісту каталогу). 

Щоб прискорити перенесення файлів, його можна виконувати в окремому потоці чи пулі потоків. Це тим зручніше, що результат цієї операції ви в програмі не обробляєте та можна не збирати жодних результатів. Щоб прискорити обхід вмісту каталогу з кількома рівнями вкладеності, ви можете обробку кожного підкаталогу виконувати в окремому потоці або передавати обробку в пул потоків.

---------------------------------
## Друга частина для процесів
* Напишіть реалізацію функції factorize, яка приймає список чисел та повертає список чисел, на які числа з вхідного списку поділяються без залишку.
* Реалізуйте синхронну версію та виміряйте час виконання.
* Потім покращіть продуктивність вашої функції, реалізувавши використання кількох ядер процесора для паралельних обчислень і замірьте час виконання знову. 
    Для визначення кількості ядер на машині використовуйте функцію cpu_count() з пакета multiprocessing

Для перевірки правильності роботи алгоритму самої функції можете скористатися тестом:
def factorize(*number):
    # YOUR CODE HERE
    raise NotImplementedError() # Remove after implementation


a, b, c, d  = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

------
**NOTE**
коли запускаю перший раз, то асинхроний розрахунок виконується швидше
Sync approach - duration: 1.24 sec
Async approach 1 -  duration: 1.14 sec
Async approach 2 -  duration: 0.77 sec
Async approach 3 -  duration: 0.88 sec

коли запускаю тругий раз
Sync approach - duration: 0.44 sec
Async approach 1 -  duration: 0.58 sec
Async approach 2 -  duration: 0.53 sec
Async approach 3 -  duration: 0.73 sec

* чомусь асинхронна версія відпрацьовує довше ніж синхронна. 
    очікував що буде навпаки, але схоже що все-таки обслуговування потоків також потребує ресурс + мабуть шось ще кешується
    реалізував 3 різні асинзронні способи розпаралелити розрахунок, все рівно синзронна версія швидше відпрацьовує.
--------------------