import pprint
import uuid
from magic_store.kv_idea.store import Store
from magic_store.db.database import Database

def test():
    store = Store()
    result = store.put("key1", "test text")
    result = store.put("key1", "test text 2", namespace="osiolek")
    result = store.put("key1", "nierozwazna czynnosc")

    x = store.get("key1", namespace="osiolek")
    print(x)
    result = store.delete("key1", namespace="osiolek", guard=x["guard"])
    result = store.put("key1","def", namespace="osiolek")
    # result = store.put("key1", "xxxxxxxxxxxxxxx", guard=x["guard"])

    print(result)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)

    result = store.save()
    print(result)


def testLoad():
    store = Store()
    result = store.load()
    print(result)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)

if __name__ == '__main__':

    database = Database()

    user = {
        "imie": "Weroni",
        "nazwisko": "Lendzi",
        "login": "Werolina"
    }
    database.createUser(user, "id1")
    database.searchUser("id1")

    userUpdate = {
        "imie": "Weronika",
        "nazwisko": "Lendzion",
        "login": "Wersko",
    }

    database.updateUser("id1", userUpdate)

    file1 = {
        "plik": "1.jpg",
        "sciezka": "C:\\5 semestr\\Technical Analitics\\Cwiczenia\\1zajecia\\1.jpg",
    }
    file2 = {
        "plik": "2.xlsx",
        "sciezka": "C:\\5 semestr\\Technical Analitics\\Cwiczenia\\1zajecia\\2.jpg",
    }
    file3 = {
        "plik": "zad2.docx",
        "sciezka": "C:\\5 semestr\\Technical Analitics\\Cwiczenia\\2zajecia\\zad2.docx",
    }

    database.createFile("id1", ["TA", "zdj1"], file1)
    database.createFile("id1", ["TA", "zdj2"], file2)
    database.createFile("id1", ["TA", "zad2"], file3)
    database.createFile("euiwaydia", ["word"], file3)
    #database.deleteUser("id1")

    database.searchFileByTags("id1", ["TA", "zdj1"], 2)
    database.searchFileByTags("id1", ["TA", "euiwaydia"], 2)

    #database.deleteTag("id1", "TA")
    #database.deleteFileFromTag("id1", "TA", "zad2.docx")
    #database.deleteFileFromAllTags("id1", "zad2.docx")

