
# Name:Mashgihad Farhan Tihan 
# Student Number:10735759

# CSP1150 Project - admin.py
# Semester 2, 2026

# Import necessary module(s).
import json
import urllib.request
import os


# This function repeatedly prompts for input until
# something other than whitespace is entered.
def input_something(prompt):
    value = input(prompt).strip()

    while value == "":
        print("Please enter something.")
        value = input(prompt).strip()

    return value


# This function finds the desired English text
# from a list of dictionaries.
def extract_english(entries, key):
    for entry in entries:
        if entry["language"]["name"] == "en":
            return entry[key]

    return ""


# This function repeatedly prompts for input until
# a valid Pokemon number is entered.
def choose_pokemon(prompt, data):
    while True:
        number = input_something(prompt)

        if number.isdigit():
            number = int(number)

            for pokemon in data:
                if pokemon["number"] == number:
                    return pokemon

        print("Invalid Pokemon number. Please try again.")


# This function saves the data in JSON format.
def save_data(data):
    with open("pokemon.txt", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# Try to load existing Pokemon data.
try:
    with open("pokemon.txt", "r", encoding="utf-8") as file:
        data = json.load(file)

except (FileNotFoundError, ValueError):
    data = []


# Print welcome message.
print("Welcome to the Pokédex Administration Program.")

while True:
    print("\nChoose [a]dd, [l]ist, [s]earch, [v]iew, [d]elete or [q]uit.")
    choice = input("> ").lower().strip()

    if choice == "a":
        # Add a new Pokemon.

        name = input_something("Enter a Pokemon name: ")

        name = name.lower()
        name = name.replace(".", "")
        name = name.replace("'", "")
        name = name.replace(":", "")
        name = name.replace(" ", "-")

        url = (
            "http://pokeapi.co/api/v2/"
            "pokemon-species/" + name
        )

        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "STUDENT_NUM"}
            )

            response = urllib.request.urlopen(request)
            species = json.load(response)
            response.close()

        except (urllib.error.URLError, ValueError):
            print("Unable to find this Pokemon.")
            continue

        number = species["id"]

        already_added = False

        for pokemon in data:
            if pokemon["number"] == number:
                already_added = True

        if already_added:
            print("This Pokemon is already in the Pokedex.")
            continue

        pokemon_name = extract_english(
            species["names"], "name"
        )

        category = extract_english(
            species["genera"], "genus"
        )

        evolves_from = None

        if species["evolves_from_species"] is not None:
            previous_name = species[
                "evolves_from_species"
            ]["name"]

            previous_url = (
                "http://pokeapi.co/api/v2/"
                "pokemon-species/" + previous_name
            )

            try:
                request = urllib.request.Request(
                    previous_url,
                    headers={"User-Agent": "STUDENT_NUM"}
                )

                response = urllib.request.urlopen(request)
                previous_species = json.load(response)
                response.close()

                evolves_from = extract_english(
                    previous_species["names"], "name"
                )

            except (urllib.error.URLError, ValueError):
                evolves_from = previous_name

        # Get additional Pokemon details.
        pokemon_url = (
            "http://pokeapi.co/api/v2/pokemon/"
            + str(number)
        )

        try:
            request = urllib.request.Request(
                pokemon_url,
                headers={"User-Agent": "STUDENT_NUM"}
            )

            response = urllib.request.urlopen(request)
            details = json.load(response)
            response.close()

        except (urllib.error.URLError, ValueError):
            print("Unable to retrieve Pokemon details.")
            continue

        height = details["height"] / 10
        weight = details["weight"] / 10

        types = []

        for item in details["types"]:
            type_name = item["type"]["name"]
            types.append(type_name.title())

        # Download the Pokemon image.
        if not os.path.exists("images"):
            os.mkdir("images")

        image_url = details["sprites"]["front_default"]

        image_path = (
            "images/" + str(number) + ".png"
        )

        if image_url is not None:
            try:
                image_request = urllib.request.Request(
                    image_url,
                    headers={"User-Agent": "STUDENT_NUM"}
                )

                image_response = urllib.request.urlopen(
                    image_request
                )

                image_data = image_response.read()
                image_response.close()

                with open(image_path, "wb") as image_file:
                    image_file.write(image_data)

            except (urllib.error.URLError, OSError):
                print("Unable to download Pokemon image.")

        # Create a dictionary for the Pokemon.
        new_pokemon = {
            "name": pokemon_name,
            "number": number,
            "category": category,
            "height": height,
            "weight": weight,
            "types": types,
            "evolves_from": evolves_from
        }

        data.append(new_pokemon)

        # Sort Pokemon by Pokedex number.
        data.sort(key=lambda pokemon: pokemon["number"])

        save_data(data)

        print(pokemon_name + " added to Pokedex.")


    elif choice == "l":
        # List current Pokemon.

        if len(data) == 0:
            print("Your Pokedex is empty.")

        else:
            print("Your Pokedex contains:")

            for pokemon in data:
                number = pokemon["number"]
                name = pokemon["name"]

                print(
                    "#" + str(number).zfill(4)
                    + ": " + name
                )


    elif choice == "s":
        # Search current Pokemon.

        if len(data) == 0:
            print("Your Pokedex is empty.")

        else:
            search = input_something(
                "Enter a search term: "
            ).lower()

            results = []

            for pokemon in data:
                name = pokemon["name"].lower()
                category = pokemon["category"].lower()

                if search in name or search in category:
                    results.append(pokemon)

            if len(results) == 0:
                print("No matching Pokemon found.")

            else:
                print("Search results:")

                for pokemon in results:
                    print(
                        "#" + str(
                            pokemon["number"]
                        ).zfill(4)
                        + ": " + pokemon["name"]
                    )


    elif choice == "v":
        # View details of a Pokemon.

        if len(data) == 0:
            print("Your Pokedex is empty.")

        else:
            pokemon = choose_pokemon(
                "Pokemon number to view: ",
                data
            )

            print(
                pokemon["name"]
                + " [#"
                + str(pokemon["number"]).zfill(4)
                + "]"
            )

            print(pokemon["category"])

            print(
                "Type: " + ", ".join(pokemon["types"])
            )

            print(
                "Size: "
                + str(pokemon["height"])
                + "m, "
                + str(pokemon["weight"])
                + "kg"
            )

            if pokemon["evolves_from"] is not None:
                print(
                    "Evolves from "
                    + pokemon["evolves_from"]
                )


    elif choice == "d":
        # Delete a Pokemon.

        if len(data) == 0:
            print("Your Pokedex is empty.")

        else:
            pokemon = choose_pokemon(
                "Pokemon number to delete: ",
                data
            )

            data.remove(pokemon)

            image_path = (
                "images/"
                + str(pokemon["number"])
                + ".png"
            )

            if os.path.exists(image_path):
                os.remove(image_path)

            save_data(data)

            print(
                pokemon["name"]
                + " deleted from Pokedex."
            )


    elif choice == "q":
        # Quit the program.

        print(
            "Goodbye! Made by  Mashgihad Farhan Tihan "
            "(10735759)."
        )
        break


    else:
        # Print invalid choice message.
        print("Invalid choice. Please try again.")
