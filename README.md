
## Здравствуйте!) В этом файле есть две функции: для нахождения номера договора в тексте и для классификации разговора. 
Первая использует модель find_dogovor_model.bin, а вторая - classiffication_model.bin.

### Чтобы найти номер договора, вызовем функцию `find_nomer_dogovora(text)`. 
```python
from functions import find_nomer_dogovora
text = "Мой номер договора 90-029. А, нет, 90-025"
result = find_nomer_dogovora(text)
print(result)
```
Функция выведет:
```python
90-029, 90-025
```
### Чтобы классифицировать разговор, вызовем функцию `classify_text(text)`. Она возрвращает номер категории и ее текстовое значение. 

```python
from functions import classify_text
text = "На линии сейчас авария"
label_number, label_text=classify_text(text)
print(label_number, label_text)
```
Функция выведет:
```python
9 Авария
``` 
## Есть такие категории звонков и их номера:<br>
1: Входящий юр. лицо<br>
2: Входящий физ. лицо<br>
3: Передать контакт менеджеру/перезвонить или написать клиенту<br>
4: Оплата<br>
5: Информация по заявке<br>
6: Еще не подключают<br>
7: Заявка для техников<br>
8: Техподдержка от менеджера<br>
9: Авария<br>
10: Звонят из другой компании/Спам<br>
11: Непонятно<br>

Здесь можно попробовать эти функции в Google Colab:
https://colab.research.google.com/drive/1eQiV1uSwX7M9hByd5w00as1LNggz8mK6?usp=sharing

## Если возникает ошибка "model cannot be opened for loading, то советуют в файле functions.py указать самый полный путь в моделям .bin"
Если что пишите мне в телеграм @hozyaikaaa

