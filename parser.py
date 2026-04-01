import sys
from custom_errors import ParserError


LIST_KEYS = {"hub", "connection"}
MUST_HAVE = ["start_hub", "end_hub"]


class Parser():
    @staticmethod
    def parser(map_txt: str):
        result = {}
        line_numbers = {}
        try:
            with open(map_txt, 'r') as f:
                first_valid_line = None

                for i, line in enumerate(f, start=1):
                    line = line.strip()
# ignorar comentários no documento lido
                    if not line or line.startswith("#"):
                        continue
# verificação se a first line começa com "nb_drones", como pedido no subject
                    if first_valid_line is None:
                        first_valid_line = line
                        if not first_valid_line.startswith("nb_drones"):
                            raise ParserError(f"Line {i}: \
First line must be nb_drones")

# criação de key e value para inserir no dict
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()

# verificar hub e connection para criar listas e verificar keys duplicadas
                    if key in LIST_KEYS:
                        if key not in result:
                            result[key] = []
                        result[key].append(value)
                        line_numbers[key] = i
                    else:
                        if key in result:
                            raise ParserError(f"Line {1}: Duplicate key: \
{key}")
                        result[key] = value
                        line_numbers[key] = i
        except ParserError as e:
            print(e)
            sys.exit()

        try:
            # verificar se start_hub e end_hub existem
            for key in MUST_HAVE:
                if key not in result:
                    raise ParserError(f"Missing required key: {key}")

            for k in result:
                # verificar se nb_drones é um inteiro
                if k == "nb_drones":
                    try:
                        nb = int(result["nb_drones"])
                    except ValueError:
                        raise ParserError(f"Line {line_numbers["nb_drones"]}: \
nb_drones must be an integer")
                    if nb <= 0:
                        raise ParserError(f"Line {line_numbers["nb_drones"]}: \
Number of drones must be a positive integer")

# Parsear o value dos hubs — extrair name, x, y e metadata [...] separadamente
            parsed_hubs = []
            for hub_value in result["hub"]:
                value = hub_value
                if "[" in value and "]" in value:
                    parts = value.split("[", 1)
                    coords = parts[0].strip()
                    metadata = "[" + parts[1].strip()
                else:
                    coords = value
                    metadata = None
                coords_token = coords.split()
                if len(coords_token) != 3:
                    raise ParserError(f"Line {i}: Hub must have name, x, y")
                name = coords_token[0]
                try:
                    x = int(coords_token[1])
                    y = int(coords_token[2])
                except ValueError:
                    raise ParserError(f"Line {i}: Hub coordinates must be \
integers")
                hub_dict = {
                    "name": name,
                    "x": x,
                    "y": y,
                    "metadata": metadata
                }
                parsed_hubs.append(hub_dict)
            result["hub"] = parsed_hubs
            print(result)

        except ParserError as e:
            print(e)
            sys.exit()


if __name__ == "__main__":
    Parser.parser("maps/easy/01_linear_path.txt")
