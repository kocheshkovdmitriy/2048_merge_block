import json

class LogRecords():
    def __init__(self):
        with open("data_file.json", "r") as read_file:
            self.record = json.load(read_file)

    def add_result(self, name: str, score: int, game: str):
        self.record[game][name] = score
        with open("data_file.json", "w") as write_file:
            json.dump(self.record, write_file, indent=2)

    def get_top(self, game):
        top = sorted([item for item in self.record[game].items()], key=lambda x: (-int(x[1]), x[0]))
        top.extend([(None, 0) for _ in range(10 - len(top))])
        return top[:10]

    def get_now_place(self, name, score, game):
        temp = [item for item in self.record[game].items()]
        if self.record.get(name, 0) == score:
            return sorted(temp, key=lambda x: (-int(x[1]), x[0])).index((name, score)) + 1
        temp.append((name, score))
        temp.sort(key=lambda x: (-int(x[1]), x[0]))
        return temp.index((name, score)) + 1


if __name__ == '__main__':
    LogRecords()


