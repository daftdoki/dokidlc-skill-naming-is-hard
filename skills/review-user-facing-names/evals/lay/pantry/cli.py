"""Every command, flag, and setting a Pantry user types."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pantry", description="Your recipes, on your laptop.")
    sub = p.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add-recipe", help="Save a new recipe, typed in or from a web page.")
    add.add_argument("--url", help="Copy the recipe from this web page.")
    add.add_argument("--with-photos", action="store_true",
                     help="Also save the photos from the web page.")

    find = sub.add_parser("find-recipes", help="Find recipes that mention a word.")
    find.add_argument("word")

    show = sub.add_parser("show-recipe", help="Print one recipe.")
    show.add_argument("recipe")

    delete = sub.add_parser("delete-recipe", help="Remove one recipe.")
    delete.add_argument("recipe")

    shop = sub.add_parser("make-shopping-list",
                          help="Add up the ingredients of the recipes you name into one list.")
    shop.add_argument("recipes", nargs="+")

    imp = sub.add_parser("import-recipes", help="Add every recipe from a file another app exported.")
    imp.add_argument("file")

    rate = sub.add_parser("rate-recipe", help="Give a recipe one to five stars.")
    rate.add_argument("recipe")
    rate.add_argument("stars", type=int, choices=range(1, 6))

    lst = sub.add_parser("list", help="Print the names of all your recipes.")
    lst.add_argument("--nuke", action="store_true",
                     help="Delete every recipe instead of listing them.")

    sub.add_parser("reindex", help="Rebuild the word list find-recipes searches, "
                                   "when a recipe you saved does not show up.")

    sub.add_parser("gc", help="Delete photos that no recipe uses any more.")

    sub.add_parser("sync", help="Write all your recipes into one PDF you can print.")

    info = sub.add_parser("info", help="Print the ingredients of one recipe, "
                                       "scaled to the number of people you cook for.")
    info.add_argument("recipe")
    info.add_argument("people", type=int)

    conv = sub.add_parser("recipe-ingredient-quantity-unit-convert",
                          help="Change a recipe's amounts between cups and grams.")
    conv.add_argument("recipe")

    sub.add_parser("munge", help="Tidy ingredient names, so 'Tomatoes' and 'tomato' "
                                 "count as one on a shopping list.")

    # Settings: bare, they print the value; given one value, they set it.
    for name, help_text in [
        ("font-size", "How big the text is: small, medium, or large."),
        ("measurement-units", "Show amounts in metric or US units."),
        ("set-dark-mode", "Light text on a dark screen: on or off."),
        ("scaling-coeff", "How many people a recipe is for when you do not say."),
        ("cron", "The day Pantry emails you next week's meal plan, as a cron line "
                 "such as '0 9 * * 0'."),
    ]:
        s = sub.add_parser(name, help=help_text)
        s.add_argument("value", nargs="?")

    return p
