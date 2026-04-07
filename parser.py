import sys
from custom_errors import ParserError

LIST_KEYS = {"hub", "connection"}
VALID_ZONES = {"normal", "blocked", "restricted", "priority"}
MUST_HAVE = ["start_hub", "end_hub"]
VALID_KEYS = ("nb_drones", "start_hub", "hub", "end_hub", "connection")


class Parser():
    @staticmethod
    def parser(map_txt: str) -> dict:
        """Parseia o arquivo de mapa e retorna um dict com os dados."""
        result = {}
        line_numbers = {}

        try:
            with open(map_txt, 'r') as f:
                first_valid_line = None

                for i, line in enumerate(f, start=1):
                    line = line.strip()
                    # ignorar comentários e linhas vazias e
                    # ver se as linhas são válidas
                    if not line or line.startswith("#"):
                        continue
                    elif not line.startswith(VALID_KEYS):
                        raise ParserError(f"Line {i}: Invalid line")

                    # verificação se a first line começa com "nb_drones"
                    if first_valid_line is None:
                        first_valid_line = line
                        if not first_valid_line.startswith("nb_drones"):
                            raise ParserError(f"Line {i}: First line must be \
nb_drones")

                    # criação de key e value para inserir no dict
                    try:
                        key, value = line.split(":", 1)
                    except ValueError:
                        raise ParserError(f"Line {i}: Missing ':' separator")
                    key = key.strip()
                    value = value.strip()

                    # verificar hub e connection para criar listas
                    # e verificar keys duplicadas
                    if key not in LIST_KEYS:
                        if key in result:
                            raise ParserError(f"Line {i}: Duplicate key: \
{key}")
                        result[key] = value
                        line_numbers[key] = i
                    else:
                        if key not in result:
                            result[key] = []
                        result[key].append((value, i))  # tupla só para listas

        except ParserError as e:
            print(e)
            sys.exit()

        try:
            # verificar se start_hub e end_hub existem
            for key in MUST_HAVE:
                if key not in result:
                    raise ParserError(f"Missing required key: {key}")

            # verificar se nb_drones é um inteiro positivo
            try:
                nb = int(result["nb_drones"])
            except ValueError:
                raise ParserError(f"Line {line_numbers['nb_drones']}: \
nb_drones must be an integer")
            if nb <= 0:
                raise ParserError(f"Line {line_numbers['nb_drones']}: \
Number of drones must be positive")
            result["nb_drones"] = nb

            # função auxiliar para parsear hubs
            def parse_hub(value: str, i: int) -> dict:
                """Retorna dict {'name', 'x', 'y', 'metadata', 'line'}"""
                if "[" in value and "]" in value:
                    parts = value.split("[", 1)
                    coord_part = parts[0].strip()
                    metadata_part = "[" + parts[1].strip()
                else:
                    coord_part = value
                    metadata_part = None

                tokens = coord_part.split(maxsplit=3)
                if len(tokens) != 3:
                    raise ParserError(f"Line {i}: Hub must have name, x, y")
                name = tokens[0]
                if "-" in name:
                    raise ParserError(f"Line {i}: Hub name couldn't have '-'")
                try:
                    x = int(tokens[1])
                    y = int(tokens[2])
                except ValueError:
                    raise ParserError(f"Line {i}: Hub coordinates must \
be integers")
                return {
                    "name": name,
                    "x": x, "y": y,
                    "metadata": metadata_part,
                    "line": i
                }

            # função auxiliar para parsear e validar zones do metadata
            def parse_metadata(metadata: list) -> list:
                """Valida e retorna lista de zones"""
                zones = []
                for item in metadata:
                    if item["metadata"] is None:
                        zones.append(None)
                        continue
                    meta = item["metadata"].strip("[]").split()
                    line = item["line"]

                    zone = None

                    for p in meta:
                        if p.startswith("zone="):
                            zone = p.split("=")[1]
                            break

                    if zone is not None and zone not in VALID_ZONES:
                        raise ParserError(f"Line {line}: Invalid zone: {zone}")
                    zones.append(zone)
                return zones

            # parsear start_hub e end_hub
            result["start_hub"] = parse_hub(result["start_hub"],
                                            line_numbers["start_hub"])
            result["end_hub"] = parse_hub(result["end_hub"],
                                          line_numbers["end_hub"])

            # parsear hubs e desempacotar tupla
            parsed_hubs = []
            for val, line_num in result["hub"]:
                parsed_hubs.append(parse_hub(val, line_num))
            result["hub"] = parsed_hubs

            parse_metadata(result["hub"])

            # função auxiliar para parsear max_link_connections
            def parse_connections_meta(conn_metadata: str, line: int) -> dict:
                conn_metadata = conn_metadata.replace("[", "").replace("]", "")

                try:
                    name, value = conn_metadata.split("=")
                except ValueError:
                    raise ParserError(f"Line {line}: Invalid metadata format")

                if name != "max_link_capacity":
                    raise ParserError(f"Line {line}: Invalid connection \
metadata")

                try:
                    value = int(value)
                    if value <= 0:
                        raise ParserError(f"Line {line}: max_link_capacity \
must be a positive integer")
                except ValueError:
                    raise ParserError(f"Line {line}: Max link capacity must \
be a positive integer")

                return {"max_link_capacity": value}

            #   função auxiliar para parsear connections
            def parse_connections(value: list) -> list:
                """Retorna lista de dicts {zone1, zone2, metadata}"""
                parsed_connections = []

                for item, line in value:  # <-- mantém line aqui
                    try:
                        parts = item.split('-', maxsplit=1)
                        if len(parts) != 2:
                            raise ParserError(f"Line {line}: Invalid \
connection format")

                        zone1 = parts[0].strip()

                        rest = parts[1].split(maxsplit=1)
                        zone2 = rest[0].strip()

                        metadata = None
                        if len(rest) == 2:
                            metadata = parse_connections_meta(rest[1], line)

                        parsed_connections.append({
                            "zone1": zone1,
                            "zone2": zone2,
                            "metadata": metadata
                        })

                    except ParserError as e:
                        raise ParserError(str(e))

                return parsed_connections
            result["connection"] = parse_connections(result["connection"])

            # remover 'line' dos hubs após todas as validações
            for hub in result["hub"]:
                hub.pop("line")
            result["start_hub"].pop("line")
            result["end_hub"].pop("line")
            print(result)

        except ParserError as e:
            print(e)
            sys.exit()

        return result


if __name__ == "__main__":
    Parser.parser("maps/hard/02_capacity_hell.txt")
