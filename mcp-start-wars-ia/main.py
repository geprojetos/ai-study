from tools import search_characters, search_planets, search_films, get_character_by_id, list_all_films
import sys

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SWAPI CLI - Star Wars API Tools")
    subparsers = parser.add_subparsers(dest="command")

    parser_char = subparsers.add_parser("search_characters")
    parser_char.add_argument("--search", required=True, help="Nome do personagem para buscar")

    parser_planet = subparsers.add_parser("search_planets")
    parser_planet.add_argument("--search", required=True, help="Nome do planeta para buscar")

    parser_film = subparsers.add_parser("search_films")
    parser_film.add_argument("--search", required=True, help="Título do filme para buscar")

    parser_char_id = subparsers.add_parser("get_character_by_id")
    parser_char_id.add_argument("--id", required=True, type=int, help="ID do personagem")

    parser_films = subparsers.add_parser("list_all_films")

    args = parser.parse_args()

    if args.command == "search_characters":
        search_characters(args.search)
    elif args.command == "search_planets":
        search_planets(args.search)
    elif args.command == "search_films":
        search_films(args.search)
    elif args.command == "get_character_by_id":
        get_character_by_id(args.id)
    elif args.command == "list_all_films":
        list_all_films()
    else:
        parser.print_help()
