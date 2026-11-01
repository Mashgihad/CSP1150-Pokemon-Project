
# Name: Mashgihad Farhan Tihan
# Student Number: 10735759

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
                raise ValueError("The Pokedex is empty or invalid.")

        except (OSError, ValueError, TypeError) as error:
            tkinter.messagebox.showerror(
                "Pokedex Error",
                "Unable to load Pokemon data: " + str(error)
            )
            return

        # Start with the first Pokemon.
        self.index = 0

        # Create the main window.
        self.main = tkinter.Tk()
        self.main.title("Mashgihad's Pokedex")
        self.main.geometry("430x300")
        self.main.resizable(False, False)
        self.main.configure(bg="#f0f0f0")

        # Create the heading label.
        self.heading = tkinter.Label(
            self.main,
            text="",
            font=("Arial", 15, "bold"),
            bg="#f0f0f0",
            fg="#222222"
        )
        self.heading.pack(pady=(15, 10))

        # Create a frame for navigation and image.
        self.image_frame = tkinter.Frame(
            self.main,
            bg="#f0f0f0"
        )
        self.image_frame.pack(pady=5)

        # Create the Previous button.
        self.previous_button = tkinter.Button(
            self.image_frame,
            text="<",
            width=5,
            font=("Arial", 12),
            command=self.previous
        )
        self.previous_button.grid(
            row=0,
            column=0,
            padx=15
        )

        # Create the Pokemon image label.
        self.image_label = tkinter.Label(
            self.image_frame,
            bg="#f0f0f0"
        )
        self.image_label.grid(
            row=0,
            column=1,
            padx=10
        )

        # Create the Next button.
        self.next_button = tkinter.Button(
            self.image_frame,
            text=">",
            width=5,
            font=("Arial", 12),
            command=self.next
        )
        self.next_button.grid(
            row=0,
            column=2,
            padx=15
        )

        # Create the Pokemon details label.
        self.details_label = tkinter.Label(
            self.main,
            text="",
            justify="center",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#222222"
        )
        self.details_label.pack(pady=(10, 10))

        # Display the first Pokemon.
        self.show_pokemon()

        # Start the GUI main loop.
        tkinter.mainloop()


    def show_pokemon(self):
        # Get the current Pokemon.
        pokemon = self.data[self.index]

        # Display Pokemon name and number.
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

        except (tkinter.TclError, OSError):
            self.photo = None

            self.image_label.config(
                image="",
                text="Image unavailable",
                width=18,
                height=6
            )

        # Prepare Pokemon details.
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
        self.details_label.config(
            text=details
        )

        # Enable or disable navigation buttons.
        if self.index == 0:
            self.previous_button.config(
                state="disabled"
            )
        else:
            self.previous_button.config(
                state="normal"
            )

        if self.index == len(self.data) - 1:
            self.next_button.config(
                state="disabled"
            )
        else:
            self.next_button.config(
                state="normal"
            )


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
