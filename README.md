
# Ближайшие бары  
  
Загружает и анализирует данные о московских барах с сайта [data.mos.ru](https://data.mos.ru/) в формате `json` 
Данные доступны по этой [ссылке](http://data.mos.ru/opendata/7710881420-bary).

  
# Как запустить  
  
Скрипт требует для своей работы установленного интерпретатора Python версии 3.5  
  
Запуск на Linux:  
  
```bash  
  
$ python3.5 bars.py # possibly requires call of python3 executive instead of just python  
Enter file name or path to file with bars info (default bars.json) -> bars.json
The biggest bar is named: Спорт бар «Красная машина» with: 450 seats
The smallest bar is named: БАР. СОКИ with: 0 seats
Enter geo coordinates separeted by comma in format: longitude, latitude
 for example: 37.621, 55.76536 -> 37.621, 55.76536
The closest bar is named: Глобал бар НК with longitude: 37.62122454797518 and latitude: 55.76514637303136
 
  
```  
  
Запуск на Windows происходит аналогично.  
  
# Цели проекта  
  
Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)