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

                    if not line or line.startswith("#"):
                        continue
                    elif not line.startswith(VALID_KEYS):
                        raise ParserError(f"Line {i}: Invalid line")

                    if first_valid_line is None:
                        first_valid_line = line
                        if not first_valid_line.startswith("nb_drones"):
                            raise ParserError(
                                f"Line {i}: First line must be nb_drones"
                            )

                    try:
                        key, value = line.split(":", 1)
                    except ValueError:
                        raise ParserError(f"Line {i}: Missing ':' separator")

                    key = key.strip()
                    value = value.strip()

                    if key not in LIST_KEYS:
                        if key in result:
                            raise ParserError(
                                f"Line {i}: Duplicate key: {key}"
                            )
                        result[key] = value
                        line_numbers[key] = i
                    else:
                        if key not in result:
                            result[key] = []
                        result[key].append((value, i))

        except ParserError as e:
            print(e)
            sys.exit()

        try:
            for key in MUST_HAVE:
                if key not in result:
                    raise ParserError(f"Missing required key: {key}")

            try:
                nb = int(result["nb_drones"])
            except ValueError:
                raise ParserError(
                    f"Line {line_numbers['nb_drones']}: "
                    "nb_drones must be an integer"
                )
            if nb <= 0:
                raise ParserError(
                    f"Line {line_numbers['nb_drones']}: "
                    "Number of drones must be positive"
                )
            result["nb_drones"] = nb

            def parse_hub(value: str, i: int) -> dict:
                """Retorna dict com name, x, y e raw metadata string."""
                if "[" in value and "]" in value:
                    parts = value.split("[", 1)
                    coord_part = parts[0].strip()
                    metadata_str = "[" + parts[1].strip()
                else:
                    coord_part = value
                    metadata_str = None  # type: ignore[assignment]

                tokens = coord_part.split(maxsplit=3)
                if len(tokens) != 3:
                    raise ParserError(
                        f"Line {i}: Hub must have name, x, y"
                    )

                name = tokens[0]
                if "-" in name:
                    raise ParserError(
                        f"Line {i}: Hub name couldn't have '-'"
                    )

                try:
                    x = int(tokens[1])
                    y = int(tokens[2])
                except ValueError:
                    raise ParserError(
                        f"Line {i}: Hub coordinates must be integers"
                    )

                return {
                    "name": name,
                    "x": x,
                    "y": y,
                    "_metadata_str": metadata_str,
                    "line": i,
                }

            def parse_hub_metadata(hub: dict) -> dict:
                """Parseia o metadata de um hub e retorna dict estruturado."""
                line = hub["line"]
                metadata_str = hub.get("_metadata_str")

                zone = "normal"
                color = None
                max_drones = 1

                if metadata_str is not None:
                    inner = metadata_str.strip("[]")
                    parts = inner.split()

                    for p in parts:
                        if p.startswith("zone="):
                            zone = p.split("=", 1)[1]
                            if zone not in VALID_ZONES:
                                raise ParserError(
                                    f"Line {line}: Invalid zone: {zone}"
                                )
                        elif p.startswith("color="):
                            color = p.split("=", 1)[1]
                        elif p.startswith("max_drones="):
                            raw = p.split("=", 1)[1]
                            try:
                                max_drones = int(raw)
                            except ValueError:
                                raise ParserError(
                                    f"Line {line}: max_drones "
                                    "must be a positive integer"
                                )
                            if max_drones <= 0:
                                raise ParserError(
                                    f"Line {line}: max_drones "
                                    "must be a positive integer"
                                )
                        else:
                            raise ParserError(
                                f"Line {line}: Unknown metadata key '{p}'"
                            )

                return {
                    "zone": zone,
                    "color": color,
                    "max_drones": max_drones,
                }

            def apply_metadata(hub: dict) -> dict:
                """Remove campos temporários e aplica metadata estruturado."""
                meta = parse_hub_metadata(hub)
                hub.pop("_metadata_str", None)
                hub.pop("line", None)
                hub["metadata"] = meta
                return hub

            result["start_hub"] = apply_metadata(
                parse_hub(result["start_hub"], line_numbers["start_hub"])
            )
            result["end_hub"] = apply_metadata(
                parse_hub(result["end_hub"], line_numbers["end_hub"])
            )

            parsed_hubs = []
            for val, line_num in result["hub"]:
                parsed_hubs.append(apply_metadata(parse_hub(val, line_num)))
            result["hub"] = parsed_hubs

            defined_hubs = {
                hub["name"]
                for hub in result["hub"]
                + [result["start_hub"], result["end_hub"]]
            }

            def parse_connections_meta(conn_meta: str, line: int) -> dict:
                """Parseia metadata de uma connection."""
                inner = conn_meta.replace("[", "").replace("]", "").strip()
                try:
                    name, value = inner.split("=")
                except ValueError:
                    raise ParserError(
                        f"Line {line}: Invalid metadata format"
                    )
                if name != "max_link_capacity":
                    raise ParserError(
                        f"Line {line}: Invalid connection metadata"
                    )
                try:
                    cap = int(value)
                    if cap <= 0:
                        raise ParserError(
                            f"Line {line}: max_link_capacity "
                            "must be a positive integer"
                        )
                except ValueError:
                    raise ParserError(
                        f"Line {line}: max_link_capacity "
                        "must be a positive integer"
                    )
                return {"max_link_capacity": cap}

            def parse_connections(value: list) -> list:
                """Retorna lista de dicts com zone1, zone2, metadata."""
                parsed = []
                seen = set()

                for item, line in value:
                    parts = item.split('-', maxsplit=1)
                    if len(parts) != 2:
                        raise ParserError(
                            f"Line {line}: Invalid connection format"
                        )

                    zone1 = parts[0].strip()
                    rest = parts[1].split(maxsplit=1)
                    zone2 = rest[0].strip()

                    if zone1 not in defined_hubs:
                        raise ParserError(
                            f"Line {line}: Unknown hub '{zone1}'"
                        )
                    if zone2 not in defined_hubs:
                        raise ParserError(
                            f"Line {line}: Unknown hub '{zone2}'"
                        )

                    conn_key = frozenset([zone1, zone2])
                    if conn_key in seen:
                        raise ParserError(
                            f"Line {line}: Duplicate connection "
                            f"'{zone1}-{zone2}'"
                        )
                    seen.add(conn_key)

                    meta = None
                    if len(rest) == 2:
                        meta = parse_connections_meta(rest[1], line)

                    parsed.append({
                        "zone1": zone1,
                        "zone2": zone2,
                        "metadata": meta,
                    })

                return parsed

            result["connection"] = parse_connections(result["connection"])

        except ParserError as e:
            print(e)
            sys.exit()
        return result
