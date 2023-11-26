from random import shuffle
import json
import random

# SecretSanta class for handling Secret Santa operations
class SecretSanta:
    # Initialize SecretSanta with data and email service
    def __init__(self, data, email_service):
        # Store the data and email service
        self.data = data
        self.email_service = email_service

        # Open and read the categories.json file
        with open("categories.json", "r") as file:
            # Load categories from the json file
            self.categories = json.load(file)

        # Make a copy of the categories to available_categories
        self.available_categories = self.categories.copy()

    # Function to assign Secret Santa and send emails
    def assign_and_send_emails(self):
        # Shuffle the players to ensure random assignment
        shuffle(self.data["players"])

        # Loop through each player
        for index, player in enumerate(self.data["players"]):
            # Pick a duo for gifting
            gifter, receiver = self.pick_duo(index)

            # Pick a category for the gift
            category = self.pick_category()

            # Create a link for the gift
            link = self.create_link(gifter["name"], receiver["name"], category)

            # Send email to the gifter
            self.email_service.send_email(gifter["email"], "Secret Santa!", link)

    # Function to pick a duo for gifting
    def pick_duo(self, index):
        # Get the list of players
        players = self.data["players"]

        # Return a pair of players for gifting
        return players[index], players[(index + 1) % len(players)]

    # Function to pick a category for the gift
    def pick_category(self):
        # If there are no available categories, refill the list
        if not self.available_categories:
            self.available_categories = self.categories.copy()

        # Choose a random category
        category = random.choice(self.available_categories)

        # Remove the chosen category from available_categories
        self.available_categories.remove(category)

        # Return the chosen category
        return category

    # Function to create a link for the gift
    def create_link(self, gifter_name, receiver_name, category):
        # Return the created link
        return f'https://example.com/giftDetail?gifter={gifter_name}&receiver={receiver_name}&category={category}'