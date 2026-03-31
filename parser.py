from custom_errors import ParserError


class Parser():
    @staticmethod
    def parser(map_txt: str):
        result = {}
        try:
            with open(map_txt, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line.startswith("#") and line:
                        key, value = line.split(":", 1)
                        if result[key] == "hub":
                            ...
                        result[key] = value
                print(result)

        except ParserError as e:
            print(e)


if __name__ == "__main__":
    Parser.parser("maps/easy/01_linear_path.txt")
