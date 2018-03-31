
# Ближайшие бары  
  
Загружает и анализирует данные о московских барах с сайта [data.mos.ru](https://data.mos.ru/) в формате `json` 
Данные доступны по этой [ссылке](http://data.mos.ru/opendata/7710881420-bary).

  
# Как запустить  
  
Скрипт требует для своей работы установленного интерпретатора Python версии 3.5  
  
Запуск на Linux:  
  
```bash  
  
$ python3.5 bars.py # possibly requires call of python3 executive instead of just python  
Введите имя файла с информацией  о барах или путь к нему (по-умолчанию bars.json) -> bars.json
Самый большой бар: Спорт бар «Красная машина» с: 450 мест
Наименьший бар: БАР. СОКИ с: 0 мест
Введите координаты, разделенные запятой в формате: долгота, широта
 например: 37.621, 55.76536 -> 37.621, 55.765
Ближайший бар: Глобал бар НК с долготой: 37.62122454797518 и широтой: 55.76514637303136

  
```  
  
Запуск на Windows происходит аналогично.  
  
# Цели проекта  
  
Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)