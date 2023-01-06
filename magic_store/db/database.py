from ..kv_idea.store import Store
from ..constants import MESSAGES
import pprint
import uuid

class Database:
    def __init__(self, namespace=None):
        self.store = Store()
        self.namespace = namespace
        self.store.save()

        #self.FOREACH_TAG_SEARCH_TYPE = 1
        #self.ALL_TAG_SEARCH_TYPE = 2

    def _getId(self):
        return uuid.uuid4().hex

    def _printDb(self):

        self.store = Store()
        result = self.store.load()
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.store._store)
    
    def _getAllUserKeys(self, userKey):

        self.store = Store()
        result = self.store.load()
        
        namespace = self.namespace
        if namespace == None:
            namespace = "__default__"
        
        tags = []
        for key in self.store._store[namespace].keys():
            if key.split(".")[0] == userKey:
                tags.append(key)
        return tags


    def createUser(self, information, key):  #tworze nowego usera

        self.store = Store()
        result = self.store.load()
        
        result = self.store.get(key, namespace=self.namespace)

        if result["success"] == False:
            id = self._getId()
            information["_id"] = id
            result = self.store.put(key, information, namespace=self.namespace)
            result = self.store.save()
            print(MESSAGES.USER_ADDED)
        else:
            print(MESSAGES.USER_EXISTS)
            return

    
    def searchUser(self, key):

        self.store = Store()
        result = self.store.load()
        result = self.store.get(key, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        print(result)

    def updateUser(self, key, user): #user jest slownikiem
        # klucz identyfikatorem

        self.store = Store()
        result = self.store.load()
        if "_id" in user.keys(): #zakaz zmiany
            print(MESSAGES.ID_CHANGE_NOT_ALLOWED)
            return
        data = self.store.get(key, namespace=self.namespace)
        if data["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        id = data["value"]["_id"]#dodaje id do slownika
        user["_id"] = id
        result = self.store.put(key, user, namespace=self.namespace, guard=data["guard"])
        result = self.store.save()
        print(MESSAGES.USER_UPDATED)                

    def deleteUser(self, key):

        self.store = Store()
        result = self.store.load()
        result = self.store.get(key, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return

        userKeys = self._getAllUserKeys(key) #przeszukuje przestrzenie i zwraca klucze usera
        for userKey in userKeys:
            data = self.store.get(userKey, namespace=self.namespace)
            result = self.store.delete(userKey, namespace=self.namespace, guard=data["guard"])
        
        result = self.store.save()
        print(MESSAGES.USER_DELETED)
        # self._printDb()

    def createFile(self, userKey, tags, document): #tags - list

        self.store = Store()
        result = self.store.load()
        
        result = self.store.get(userKey, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        document["_id"] = self._getId() #tworze id
        
        for tag in tags:
            data = self.store.get(userKey + "." + tag, namespace=self.namespace)
            if data["success"] == False:
                result = self.store.put(userKey + "." + tag, [document], namespace=self.namespace)
            else:
                data["value"].append(document)
                result = self.store.put(userKey + "." + tag, data["value"], namespace=self.namespace, guard=data["guard"])
        
        result = self.store.save()
        print(MESSAGES.FILE_ADDED)


    def searchFileByTags(self, userKey, tags, type): #tags = lista, typ - 1 (dla kazdego z listy) albo 2 (dla wszystkich)

        self.store = Store()
        result = self.store.load()
        if type == 1:
            for tag in tags:
                result = self.store.get(userKey + "." + tag, namespace=self.namespace)
                if result['success'] == False:
                    print(MESSAGES.TAG_NOT_EXISTS)

                else:
                    print("tag =",tag, result)
        elif type == 2:
            files = {}
            for tag in tags:
                data = self.store.get(userKey + "." + tag, namespace=self.namespace)
                if data['success'] == False:
                    print(MESSAGES.TAG_NOT_EXISTS)
                    return
                for file in data["value"]:
                    if file["_id"] in files.keys():
                        files[file["_id"]]["count"] += 1
                    else:
                        files[file["_id"]] = {
                            "count": 1,
                            "plik": file
                        }
            result = []
            for file in files.values():
                if file["count"] == len(tags):
                    result.append(file["plik"])
            if len(result)==0:
                print(MESSAGES.NO_MATCH)
                return
            print(MESSAGES.FILES_FOUND)
            print(result)

    def deleteTag(self, userKey, tag):
        
        self.store = Store()
        result = self.store.load()
        result = self.store.get(userKey + "." + tag, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.TAG_NOT_EXISTS)
            return

        result = self.store.delete(userKey + "." + tag, namespace=self.namespace, guard=result["guard"])
        result = self.store.save()
        print(MESSAGES.TAG_DELETED)

    def deleteFileFromTag(self, userKey, tag, name):

        self.store = Store()
        result = self.store.load()
        result = self.store.get(userKey + "." + tag, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.TAG_NOT_EXISTS)
            return
        files = result["value"]
        for file in files:
            if file["plik"] == name:
                files.remove(file)
                result = self.store.put(userKey + "." + tag, files, namespace=self.namespace, guard=result["guard"])
                result = self.store.save()
                print(MESSAGES.FILE_DELETED)
                return
        print(MESSAGES.FILE_NOT_EXISTS)
        return

    def deleteFileFromAllTags(self, userKey, name):

        count = 0
        self.store = Store()
        result = self.store.load()
        result = self.store.get(userKey, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        userKeys = self._getAllUserKeys(userKey)
        for key in userKeys:
            if key == userKey:
                continue
            data = self.store.get(key, namespace=self.namespace)
            
            if data["success"] == False:
                continue
            
            files = data["value"]
            for file in files:
                if file["plik"] == name:
                    files.remove(file)
                    result = self.store.put(key, files, namespace=self.namespace, guard=data["guard"])
                    result = self.store.save()
                    count += 1
        if count == 0:
            print(MESSAGES.FILE_NOT_EXISTS)
            return
        print(MESSAGES.FILE_DELETED)







