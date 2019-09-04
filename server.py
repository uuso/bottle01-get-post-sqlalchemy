from bottle import route, run, HTTPError, request, HTTPResponse
import album

"""
Requirements:
    1. Веб-сервер принимает GET-запросы по адресу /albums/<artist> и выводит на экран 
    сообщение с количеством альбомов исполнителя artist и списком названий этих альбомов.

    2. Веб-сервер принимает POST-запросы по адресу /albums/ и сохраняет переданные пользователем 
    данные об альбоме. Данные передаются в формате веб-формы. Если пользователь пытается передать 
    данные об альбоме, который уже есть в базе данных, обработчик запроса отвечает 
    HTTP-ошибкой 409 и выводит соответствующее сообщение.

    3. Набор полей в передаваемых данных полностью соответствует схеме таблицы album базы данных.

    [id:INTEGER, year:INTEGER, artist:TEXT, genre:TEXT, album:TEXT]

    4. В качестве исходной базы данных использовать файл albums.sqlite3.

    5. До попытки сохранить переданные пользователем данные, нужно провалидировать их. 
    Проверить, например, что в поле "год выпуска" передан действительно год.
"""


def valid_data(album_data):
    """
    Description:
        Получает словарь album, который проверяет на наличие всех полей из списка required_items, а также на соответствие некоторым проверкам на валидность вводимой информации. Подведёт словарь к некоторому стандарту и возвратит его в случае успешных проверок. Иначе - вернёт текст ошибки.
    
    Returns:
        Возвратит раскрытый список: результат в виде булевого значения; значение ошибки / валидный словарь.
    """
    for item in album.required_items:
        if not album_data.get(item):
            return False, 'Missing attribute "%s".' % item
    try:
        album_data["year"] = int(album_data["year"])
    except ValueError:
        return False, 'Incorrect "year" attribute (not a number).'
    else:
        if album_data["year"] < 1860 or album_data["year"] > 2020:
            return False, 'Incorrect "year" attribute (it can\'t be real).'

    for item in album_data:
        # some editing here...
        pass
        # if item != "year":
        #     album_data[item] = str(album_data[item])
    return True, album_data

@route('/albums/<artist>')
def get_albums(artist):
    """
    Description:
        Возвратит строку с заголовком, а также нумерованый список альбомов (при наличии).
        Если альбомов исполнителя нет в базе - веведет 404 с соответствующим сообщением.
    """
    album_list = album.find(artist)
    if not album_list:
        return HTTPError(404, "There are no %s albums in the database." % artist)

    header = "<h1>%s albums [%d]:</h1>" % (album_list[0].artist, len(album_list)) # album_list[0].artist -- берём оригинальное имя из базы, с учётом заглавных букв
    album_names = ["{} ({})".format(album.album, album.year) for album in album_list]
    list_elements = ["<li>%s</li><br>" % name for name in album_names]
    albums_html = "<ol><br>\n" + '\n'.join(list_elements) + "</ol>"
    return header + albums_html

    

@route('/albums/', method = "POST")
def add_album():
    """
    Description:
        Обрабатывает POST-запросы на добавление альбома по адресу HOSTPORT/albums/.
        Параметры запроса считываются из полей передаваемой формы. Если введённые параметры 
        не пройдут валидацию - вернёт ошибку 404 с указанием причины. Если данный альбом 
        уже находится в базе (совпатают поля исполнителя, года и названия) - ответит
        ошибкой 409 с указанием причины.
    """
    album_data = {}
    for item in album.required_items:
        album_data[item] = request.forms.get(item)
    valid, data = valid_data(album_data)
    if not valid:
        return HTTPResponse(data, 400)
    if album.album_exists(data):
        return HTTPResponse("This album is already in the database.", 409)
    else:
        album.add(data)
        return "Database updated."



if __name__ == "__main__":
    run(host = "localhost", port = 8080, debug = True)