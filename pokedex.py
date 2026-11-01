
# Name:Mashgihad Farhan Tihan 
# Student Number:10735759

# CSP1150 Project - pokedex.py

# Import the required modules.
import tkinter
import tkinter.messagebox
import json


class ProgramGUI:
    def __init__(self):
        # Load Pokemon data from the text file.
        try:
            with open("pokemon.txt", "r", encoding="utf-8") as file:
                self.data = json.load(file)

            if not isinstance(self.data, list) or not self.data:
                raise ValueError("The Pokedex is empty or has invalid data.")

        except (OSError, ValueError, TypeError) as error:
            tkinter.messagebox.showerror(
                "Pokedex Error",
                "Unable to load Pokemon data: " + str(error)
            )
            return

        self.index = 0

        # Create the main window.
        self.main = tkinter.Tk()
        self.main.title("My Pokedex")
        self.main.resizable(False, False)

        # Create the heading label.
        self.heading = tkinter.Label(
            self.main,
            font=("Arial", 15, "bold"),
            width=28
        )
        self.heading.grid(
            row=0, column=0, columnspan=3,
            pady=(12, 5)
        )

        # Create the Previous button.
        self.previous_button = tkinter.Button(
            self.main,
            text="<",
            width=5,
            command=self.previous
        )
        self.previous_button.grid(
            row=1, column=0, padx=10
        )

        # Create the image label.
        self.image_label = tkinter.Label(
            self.main,
            width=120,
            height=120
        )
        self.image_label.grid(
            row=1, column=1, padx=8
        )

        # Create the Next button.
        self.next_button = tkinter.Button(
            self.main,
            text=">",
            width=5,
            command=self.next
        )
        self.next_button.grid(
            row=1, column=2, padx=10
        )

        # Create the Pokemon details label.
        self.details_label = tkinter.Label(
            self.main,
            justify="left",
            font=("Arial", 11)
        )
        self.details_label.grid(
            row=2, column=0,
            columnspan=3, pady=(5, 14)
        )

        # Display the first Pokemon.
        self.show_pokemon()

        # Start the GUI.
        tkinter.mainloop()


    def show_pokemon(self):
        # Get the current Pokemon.
        pokemon = self.data[self.index]

        # Display its name and number.
        self.heading.config(
            text="{}\n#{:04d}".format(
                pokemon["name"],
                pokemon["number"]
            )
        )

        # Load the Pokemon image.
        image_path = "images/{}.png".format(
            pokemon["number"]
        )

        try:
            self.photo = tkinter.PhotoImage(
                file=image_path
            )
            self.image_label.config(
                image=self.photo,
                text=""
            )

        except tkinter.TclError:
            self.photo = None
            self.image_label.config(
                image="",
                text="Image unavailable"
            )

        # Prepare the Pokemon details.
        details = "{}\nType: {}\nSize: {}m, {}kg".format(
            pokemon["category"],
            ", ".join(pokemon["types"]),
            pokemon["height"],
            pokemon["weight"]
        )

        # Display evolution details if available.
        if pokemon.get("evolves_from"):
            details += "\nEvolves from {}".format(
                pokemon["evolves_from"]
            )

        # Update the details label.
        self.details_label.config(text=details)


    def previous(self):
        # Move to the previous Pokemon.
        if self.index > 0:
            self.index -= 1
            self.show_pokemon()


    def next(self):
        # Move to the next Pokemon.
        if self.index < len(self.data) - 1:
            self.index += 1
            self.show_pokemon()


# Create an object of the ProgramGUI class.
gui = ProgramGUI()
