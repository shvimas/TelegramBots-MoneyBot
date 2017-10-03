import os


class Container:
    def __init__(self):
        self.categories = []
        self.amounts = dict({cat: 0 for cat in self.categories})

    def find_category(self, category: str) -> (bool, str):
        for inner_name in self.amounts.keys():
            if category.lower() == inner_name.lower():
                return True, inner_name
            if category.lower() == "rest":
                return True, "Restaurants"
        return False, category

    def update_total(self):
        total = 0
        keys = [key for key in self.amounts.keys() if key != "Total"]
        for key in keys:
            total += self.amounts[key]
        self.amounts.update({"Total": total})
        if "Total" not in self.categories:
            self.categories.append("Total")

    def add(self, category: str, amount: str):
        prefix = ""
        try:
            is_set, inner_name = self.find_category(category)
            if is_set:
                if inner_name != "Total":
                    self.amounts[inner_name] += int(amount)
                else:
                    return "Can not update Total"
            else:
                self.categories.append(category)
                self.amounts.update({category: int(amount)})
                prefix = "Added new category: " + category + "\n"
        except ValueError:
            return "Failed to add " + amount + " to " + category
        self.update_total()
        return prefix + "Added " + amount + " to " + inner_name

    def remove(self, cat: str) -> str:
        is_set, inner_name = self.find_category(cat)
        if is_set & (inner_name != "Total"):
            self.categories.remove(inner_name)
            self.amounts.pop(inner_name)
            self.update_total()
            return "Removed " + inner_name
        return "Failed to remove " + cat

    def to_string(self) -> str:
        result = ""
        for cat in self.categories:
            if (cat.lower() != "other") & (cat != "Total"):
                result += cat + " : " + str(self.amounts.get(cat, 0)) + "\n"
        other_set, inner_name = self.find_category("Other")
        if other_set:
            result += inner_name + " : " + str(self.amounts[inner_name]) + "\n"
        total_set, inner_name = self.find_category("Total")
        if total_set:
            result += inner_name + " : " + str(self.amounts[inner_name]) + "\n"
        return result if result != "" else "<empty>\n"

    def empty(self):
        self.categories = []
        self.amounts = {}
        return self

    def is_empty(self) -> bool:
        return self.categories == []


class History:
    def __init__(self):
        self.containers = []

    def __len__(self):
        return len(self.containers)

    def __getitem__(self, item) -> Container:
        return self.containers.__getitem__(item)

    def save(self, cont):
        self.containers.append(cont)

    def restore(self, i) -> Container:
        return self.containers[i]

    def to_string(self) -> str:
        result = ""
        for container in self.containers:
            result += container.to_string() + "\n"
        if result == "":
            result = "<empty>"
        return result


class Users:
    def __init__(self):
        self.users = {}

    def __getitem__(self, item) -> str:
        return self.users.__getitem__(item)

    def get(self, k, default=None):
        return self.users.get(k, default)

    def add_user(self, user_id: int, user: str):
        self.users.update({user_id: user})

    def keys(self):
        return self.users.keys()

    def values(self):
        return self.users.values()


class Nodes:
    def __init__(self):
        self.nodes = {user_id: (Container(), History()) for user_id in Users().users.keys()}

    def __getitem__(self, item) -> (Container, History):
        return self.nodes.__getitem__(item)

    def get(self, k, default=None):
        return self.nodes.get(k, default)

    def items(self):
        return self.nodes.items()

    def add_node(self, user_id: int, cont=Container(), hist=History()):
        self.nodes.update({user_id: (cont, hist)})

    def update(self, d):
        self.nodes.update(d)

    def keys(self):
        return self.nodes.keys()


class Data:
    dump_dir = "dumped"

    def __init__(self):
        self.nodes = Nodes()
        self.users = Users()

    def get_user_container(self, user_id: int) -> Container:
        return self.nodes.get(user_id)[0]

    def get_user_history(self, user_id: int) -> History:
        return self.nodes.get(user_id)[1]
    
    def set_user_container(self, user_id: int, cont: Container):
        history = self.get_user_history(user_id)
        history.save(self.get_user_container(user_id))
        self.nodes.update({self.users[user_id]: (cont, history)})
    
    def register_user(self, message) -> int:
        user_id = message.chat.id
        if user_id not in self.users.keys():
            self.users.add_user(user_id, message.chat.username)
            cont, hist = self.read_node(user_id).get(user_id)
            self.nodes.add_node(user_id, cont, hist)
        return user_id
    
    def get_node_dump_name(self, user_id: int) -> str:
        return str(user_id) + "_" + self.users[user_id] + "_node.txt"

    def dump_node(self, user_id):
        # self.get_user_history(user_id).save(self.get_user_container(user_id))
        out = open(self.dump_dir + "/" + self.get_node_dump_name(user_id), mode="w")
        out.write("Container:\n\t" +
                  "\n\t".join(self.nodes[user_id][0].to_string()[:-1].split("\n")) +
                  "\n\nHistory:\n\t" +
                  "\n\t".join(self.nodes[user_id][1].to_string().split("\n"))
                  .replace("\n\t\n", "\n\n")[:-2])
        out.close()

    def dump_nodes(self):
        for user_id in self.nodes.keys():
            self.dump_node(user_id)

    @staticmethod
    def read_container(file) -> Container:
        container = Container().empty()
        for line in file:
            if line != "\n":
                if line.startswith("\t"):
                    if "<empty>" in line:
                        container = Container().empty()
                    else:
                        try:
                            category, amount = line.split(" : ")[0:2]
                            category = category.replace("\n", "").replace("\t", "").replace(" ", "")
                            amount = amount.replace("\n", "").replace("\t", "").replace(" ", "")
                            container.add(category, amount)
                        except ValueError:
                            print("Warn: failed to read " + line + " in " + file.name)
                            container = Container().empty()
            else:
                break
        return container

    def read_history(self, file) -> History:
        history = History()
        container = self.read_container(file)
        while not container.is_empty():
            history.save(container)
            container = self.read_container(file)
        return history

    def read_node(self, user_id: int) -> {int: (Container, History)}:
        try:
            file = open(self.dump_dir + "/" + self.get_node_dump_name(user_id), "r")
        except FileNotFoundError:
            return {user_id: (Container(), History())}
        container = self.read_container(file)
        history = self.read_history(file)
        file.close()
        return {user_id: (container, history)}

    def read_nodes(self):
        files = [f for f in os.listdir(self.dump_dir) if str(f).endswith(".txt")]
        for filename in files:
            user_id = int(filename.split("_")[0])
            username = filename.split("_")[1]
            self.users.add_user(user_id, username)
            self.nodes.update(self.read_node(user_id))
