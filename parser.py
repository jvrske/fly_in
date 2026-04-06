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
                    if not line or line.startswith("#"):
                        continue

                    # Validar primeira linha
                    if first_valid_line is None:
                        first_valid_line = line
                        if not first_valid_line.startswith("nb_drones"):
                            raise ParserError(f"Line {i}: First line must be \
nb_drones")

                    # Separar key e value
                    try:
                        key, value = line.split(":", 1)
                    except ValueError:
                        raise ParserError(f"Line {i}: Missing ':' separator")
                    key = key.strip()
                    value = value.strip()

                    # Validar duplicados para keys únicas
                    if key not in LIST_KEYS:
                        if key in result:
                            raise ParserError(f"Line {i}: Duplicate key: \
{key}")
                        result[key] = value
                        line_numbers[key] = i
                    else:
                        if key not in result:
                            result[key] = []
                            line_numbers[key] = i
                        result[key].append(value)

        except ParserError as e:
            print(e)
            sys.exit()

        # Validações pós-leitura
        try:
            # Verificar keys obrigatórias
            for key in MUST_HAVE:
                if key not in result:
                    raise ParserError(f"Missing required key: {key}")

            # Validar nb_drones
            try:
                nb = int(result["nb_drones"])
            except ValueError:
                raise ParserError(f"Line {line_numbers['nb_drones']}: \
nb_drones must be an integer")
            if nb <= 0:
                raise ParserError(f"Line {line_numbers['nb_drones']}: \
Number of drones must be positive")

            # Função auxiliar para parsear hubs
            def parse_hub(value, i):
                """Retorna dict {'name', 'x', 'y', 'metadata'}"""
                if "[" in value and "]" in value:
                    parts = value.split("[", 1)
                    coord_part = parts[0].strip()
                    metadata_part = "[" + parts[1].strip()
                else:
                    coord_part = value
                    metadata_part = None

                tokens = coord_part.split(maxsplit=3)
                if not tokens[1].isdigit():
                    raise ParserError(f"Line {i}: Hub name couldn't have '-' \
or spaces")
                if len(tokens) != 3:
                    raise ParserError(f"Line {i}: Hub must have name, x, y")
                name = tokens[0]
                if "-" in name:
                    raise ParserError("Hub name couldn't have '-' or spaces")
                try:
                    x = int(tokens[1])
                    y = int(tokens[2])
                except ValueError:
                    raise ParserError(f"Line {i}: Hub coordinates must \
be integers")
                return {
                    "name": name,
                    "x": x, "y": y,
                    "metadata": metadata_part}

            # Parsear start_hub
            result["start_hub"] = parse_hub(result["start_hub"],
                                            line_numbers["start_hub"])
            # Parsear end_hub
            result["end_hub"] = parse_hub(result["end_hub"],
                                          line_numbers["end_hub"])
            # Parsear hubs
            parsed_hubs = []
            for val in result["hub"]:
                parsed_hubs.append(parse_hub(val, line_numbers["hub"]))
            result["hub"] = parsed_hubs

            print(result)

        except ParserError as e:
            print(e)
            sys.exit()


if __name__ == "__main__":
    Parser.parser("maps/easy/01_linear_path.txt")
