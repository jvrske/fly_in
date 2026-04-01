from custom_errors import ParserError


LIST_KEYS = {"hub", "connection"}
MUST_HAVE = ["start_hub", "end_hub"]


class Parser():
    @staticmethod
    def parser(map_txt: str):
        result: dict = {}
        try:
            with open(map_txt, 'r') as f:
                first_valid_line = None

                for line in f.readlines():
                    line = line.strip()
# ignorar comentários no documento lido
                    if not line or line.startswith("#"):
                        continue
# verificação se a first line começa com "nb_drones", como pedido no subject
                    if first_valid_line is None:
                        first_valid_line = line
                        if not first_valid_line.startswith("nb_drones"):
                            raise ParserError("First line must be nb_drones")

# criação de key e value para inserir no dict
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()

# verificar hub e connection para criar listas e keys duplicadas
                    if key in LIST_KEYS:
                        if key not in result:
                            result[key] = []
                        result[key].append(value)
                    else:
                        if key in result:
                            raise ParserError(f"Duplicate key: {key}")
                        result[key] = value
        except ParserError as e:
            print(e)

        try:
            # verificar se start_hub e end_hub existem
            for key in MUST_HAVE:
                if key not in result:
                    raise ParserError(f"{key} must exist")
            for k in result:
                # verificar se nb_drones é um inteiro
                if k == "nb_drones":
                    try:
                        nb = int(result["nb_drones"])
                    except ValueError:
                        raise ParserError("nb_drones must be an integer")
                    if nb <= 0:
                        raise ParserError("Number of drones must be a \
positive integer")
        except ParserError as e:
            print(e)


if __name__ == "__main__":
    Parser.parser("maps/easy/01_linear_path.txt")
