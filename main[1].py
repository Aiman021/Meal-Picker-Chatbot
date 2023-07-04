'''
Name:           Aiman Haroon
Course:         Cpsc 46000-003
Assignment:     Final Project: Meal Picker Chatbot
Description:    This project is about a Chatbot that helps user pick recipes if the user search by recipe name,
                category, cooking time, or ingredients(s). It also handles user general inquires about recipes based
                on the matching keywords. This programs works by creating a Gui interface, creating a chatbot that
                handles user inquires based on the option they select and, finally readiing the recipes data
                from an external text file.
'''

from tkinter import *
import nltk

# menu options display on Gui
global menu
menu = "\n\n[1] Search by Recipe Names: \n[2] Search by Cooking Time\n" \
       "[3] Search by Ingredients\n[4] Search by Category\n[5] Exit\n"


# ~~~~~~~~~~~Methods~~~~~~~~~~~~~~


# method to parse the text file using NLP and nltk to list of individual recipes in a dictionary(key: value)

def parse_recipe_file(file_path):
    recipes = []

    with open(file_path, 'r') as file:
        # create a dictionary
        recipe = {}
        for line in file:
            line = line.strip()

            if line.startswith('name:'):
                recipe['name'] = line[5:].strip()
            elif line.startswith('category:'):
                recipe['category'] = line[9:].strip()
            elif line.startswith('steps:'):
                recipe['steps'] = nltk.sent_tokenize(line[6:].strip())
            elif line.startswith('ingredients:'):
                recipe['ingredients'] = [ingredient.strip() for ingredient in line[12:].split(',')]
            elif line.startswith('quantities:'):
                recipe['quantities'] = [quantity.strip() for quantity in line[11:].split(',')]
            elif line.startswith('cooking_time:'):
                recipe['cooking_time'] = int(line[13:].strip())
            elif line.startswith('serving_size:'):
                recipe['serving_size'] = int(line[13:].strip())

            if 'name' in recipe and 'category' in recipe and 'steps' in recipe \
                    and 'ingredients' in recipe and 'quantities' in recipe \
                    and 'cooking_time' in recipe and 'serving_size' in recipe:
                recipes.append(recipe)
                recipe = {}

    return recipes


# onEnter method bound to textfield

def onEnter(event):
    # get user input
    question = questionField.get().lower()

    if question == '5' or question == 'exit':

        textarea.insert(END, "\nYou: " + question)
        textarea.insert(END, "\nBot: Good Bye")
        #scroll down at the end
        textarea.yview_moveto(1.0)
        # display the text for 1 second and exit the program

        questionField.delete(0, END)
        root.after(1000, root.quit)


    elif question == '1' or question == "search by recipe name" or question == 'recipe name':

        # unbind the "<Return>" event on the questionField
        questionField.unbind("<Return>")

        # bind the "<Return>" event to a new function that handles recipe name input
        questionField.bind("<Return>", onEnter_recipeName)

        textarea.insert(END, '\nYou: ' + question + '')
        textarea.insert(END, "\nBot: Please enter a Recipe Name: ")
        #scroll down at the end
        textarea.yview_moveto(1.0)
        questionField.delete(0, END)

    elif question == '2' or question == "search by cooking time" or question == 'cooking time':
        # unbind the "<Return>" event on the questionField
        questionField.unbind("<Return>")

        # bind the "<Return>" event to a new function that handles recipe name input
        questionField.bind("<Return>", onEnter_cookingTime)

        textarea.insert(END, '\nYou: ' + question + '')
        textarea.insert(END, "\nBot: Please enter the cooking time in minutes: ")
        #scroll down at the end
        textarea.yview_moveto(1.0)
        questionField.delete(0, END)


    elif question == '3' or question == "search by ingredients" or question == 'ingredients':
        # unbind the "<Return>" event on the questionField
        questionField.unbind("<Return>")

        # bind the "<Return>" event to a new function that handles recipe name input
        questionField.bind("<Return>", onEnter_recipeIngredients)

        textarea.insert(END, '\nYou: ' + question + '')
        textarea.insert(END, "\nBot: Please enter the Recipe Ingredients separated by a Space: ")

        #scroll down at the end
        textarea.yview_moveto(1.0)
        questionField.delete(0, END)


    elif question == '4' or question == "search by category" or question == 'category':
        # unbind the "<Return>" event on the questionField
        questionField.unbind("<Return>")

        # bind the "<Return>" event to a new function that handles recipe name input
        questionField.bind("<Return>", onEnter_recipeCategory)

        textarea.insert(END, '\nYou: ' + question + '')
        textarea.insert(END, "\nBot: Please enter the Recipe Category to display its recipes: ")
        textarea.insert(END, "\nAvailable Categories: Breakfast, Lunch, Dinner\n")

        #scroll down at the end
        textarea.yview_moveto(1.0)
        questionField.delete(0, END)

    else:
        # unbind the "<Return>" event on the questionField
        questionField.unbind("<Return>")

        textarea.insert(END, "\nYou: " + question)
        #scroll down at the end
        textarea.yview_moveto(1.0)
        #get user input
        user_input = questionField.get().lower()
        #call a method that deals with general inquiries and store in results
        general_inquiries(user_input)


# Method to display menu again and return to previous method
def return_to_menu(event_name):
    # display menu
    textarea.insert(END, menu)
    # clear textfield
    questionField.delete(0, END)
    # unbind the "<Return>" event on the questionField
    questionField.unbind("<Return>")
    # bind the "<Return>" event to a new function that handles recipe name input
    questionField.bind("<Return>", event_name)


# method to search the recipes by providing the exact name match
def onEnter_recipeName(event):

    # take user input and tokenize it
    user_input = questionField.get().lower()
    textarea.insert(END, '\nYou: ' + user_input + '')
    user_input_tokenize = nltk.word_tokenize(user_input)

    # Initialize flag variable
    recipe_found = False

    # tokenize recipe names
    for recipe in recipes:
        recipe_name = recipe['name'].lower()

        # find match
        match_all_tokens = True
        for t in user_input_tokenize:
            if t not in recipe_name:
                match_all_tokens = False
                break

        if match_all_tokens:
            textarea.insert(END, "\nBot: Recipe(s) found!\n"
                                 "\nName- \t\t" + recipe['name'] + "\n"
                                 "Category- \t\t" + recipe['category'] + "\n"
                                 "Ingredients- \t\t" + ", ".join(recipe['ingredients']) + "\n"
                                 "Cooking time- \t\t" + str(recipe['cooking_time']) + " mins" "\n"
                                 "Serving size- \t\t" + str(recipe['serving_size']) + "\n"
                                 "Quantities- \t\t" + ", ".join(recipe['quantities']) + "\n"
                                 "Steps- \t\t" + " ".join(recipe['steps']) + "\n")

            # Set flag variable to True
            recipe_found = True

    # If recipe not found, print message
    if not recipe_found:
        textarea.insert(END, "\nBot: Recipe not found.")

    # return to menu
    return_to_menu(onEnter)


# Method to print recipes by cooking time
def onEnter_cookingTime(event):
    # user input
    user_input = questionField.get().lower()
    textarea.insert(END, '\nYou: ' + user_input + '')

    found_match = False
    recipes_text = ""

    for recipe in recipes:
        if int(recipe['cooking_time']) <= int(user_input):
            recipes_text += "\n" + recipe['name'] + ": \t\t" + str(recipe['cooking_time']) + " mins"
            found_match = True

    if found_match:
        textarea.insert(END, "\nBot: The following recipes match your desired cooking time: " + recipes_text)
    else:
        textarea.insert(END, "\nBot: No recipes found with a cooking time equal to " + str(user_input) + " minutes.")

    # return to menu
    return_to_menu(onEnter)


# method to print recipes by their ingredients
def onEnter_recipeIngredients(event):
    # user input
    user_input = questionField.get().lower()
    textarea.insert(END, '\nYou: ' + user_input + '')

    # Tokenize user input
    user_tokens = nltk.word_tokenize(user_input.lower())

    # empty dictionary {key (recipe Name) : Value (matched ingredient(s))}
    matched_recipes = {}

    for recipe in recipes:
        recipe_ingredients = ", ".join(recipe['ingredients']).lower()
        recipe_ingredients_tokens = nltk.word_tokenize(recipe_ingredients)

        # Check if any token is in recipe_ingredients_tokens
        matched_tokens = []
        for t in user_tokens:
            if t in recipe_ingredients_tokens:
                matched_tokens.append(t)

        if len(matched_tokens) > 0:
            # Add recipe to matched_recipes dictionary
            if recipe['name'] not in matched_recipes:
                matched_recipes[recipe['name']] = matched_tokens
            else:
                matched_recipes[recipe['name']].extend(matched_tokens)

    if len(matched_recipes) == 0:
        textarea.insert(END, "\nBot: Sorry, I couldn't find any recipes matching these ingredients.")
    else:
        textarea.insert(END, "\nBot: I found the following recipes that match your ingredients\n\n")
        for recipe_name, matched_tokens in matched_recipes.items():
            matched_tokens_str = ", ".join(set(matched_tokens))
            textarea.insert(END, f"- {recipe_name} (matched with: {matched_tokens_str})\n")


    # scroll down at the end
    textarea.yview_moveto(1.0)
    # return to menu
    return_to_menu(onEnter)


# method to search the recipes by providing the category
def onEnter_recipeCategory(event):
    # user input
    user_input = questionField.get().lower()
    textarea.insert(END, '\nYou: ' + user_input + '')

    if user_input == 'breakfast' or user_input == 'lunch' or user_input == 'dinner':
        textarea.insert(END, "\nBot: Here are all the recipes that fall under " + user_input + " Category\n")
        for recipe in recipes:
            if recipe['category'].lower() == user_input.lower():
                textarea.insert(END, recipe['name'] + "\n")
    else:
        textarea.insert(END, "\nBot: Unrecognized Category!")

    # return to menu
    return_to_menu(onEnter)

# method to check for general inquiries if no menu options was selected
def general_inquiries(user_input):

    # Tokenize user input
    tokens = nltk.word_tokenize(user_input)

    matched_tokens = []
    recipe_found = False

    # Check each recipe for matches
    matched_recipes = []
    for recipe in recipes:
        # Combine all text fields except steps and quantities in recipe
        recipe_text = recipe['name'].lower() + ' ' + recipe['category'].lower() + ' ' + ' '.join(
            recipe['ingredients']).lower() + ' ' + str(recipe['cooking_time']) + ' ' + str(recipe['serving_size'])
        recipe_text_tokens = nltk.word_tokenize(recipe_text)



        # Check if any user token also found in recipe_text_tokens
        for t in tokens:
            if t in recipe_text_tokens:
                matched_tokens.append(t)

        # find match
        match_all_tokens = True
        if not matched_tokens:
            match_all_tokens = False
        else:
            for t in matched_tokens:
                if t not in recipe_text_tokens:
                    match_all_tokens = False
                    break

        if match_all_tokens:
            textarea.insert(END, "\nBot: Recipe(s) found!\n"
                                 "\nName- \t\t" + recipe['name'] + "\n"
                                 "Category- \t\t" + recipe['category'] + "\n"
                                 "Ingredients- \t\t" + ", ".join(recipe['ingredients']) + "\n"
                                 "Cooking time- \t\t" + str(recipe['cooking_time']) + " mins" "\n"
                                 "Serving size- \t\t" + str(recipe['serving_size']) + "\n")
            recipe_found = True

    # If recipe not found, print message
    if not recipe_found:
        textarea.insert(END, "\nBot: Recipe not found.")

    return_to_menu(onEnter)


# ~~~~~~~~~~~Designing the Gui~~~~~~~~~~~~~`

root = Tk()

# width and height of the window
root.geometry('700x700+100+30')

# title
root.title('Meal Picker ChatBot: Aiman Haroon')

# colors
root.config(bg='gold')

# insering logo pic to window
chatbot_logo = PhotoImage(file='robotpic.png')
chatbot_logo_resized = chatbot_logo.subsample(3, 3)

# placing the picture in the upper left corner
chatbot_logoLabel = Label(root, image=chatbot_logo_resized, bg='silver')
chatbot_logoLabel.place(x=10, y=10, anchor='nw')

# text labels next to the picture
text_label = Label(root, text='Meal Picker Chatbot', font=('Arial', 18), bg='gold')
text_label.place(x=200, y=50, anchor='nw')

text_label2 = Label(root, text='Let me help you decide\nyour delicious Meals!', font=('Arial', 12), bg='gold')
text_label2.place(x=200, y=100, anchor='nw')

# more elements to Gui
center_frame = Frame(width=700, height=360)
center_frame.pack_propagate(False)  # prevent the frame from expanding
center_frame.place(relx=0.5, rely=0.5, anchor='center')

scrollbar = Scrollbar(center_frame)
scrollbar.pack(side=RIGHT, fill=Y)

textarea = Text(center_frame, font=('times new roman', 16), height=30, yscrollcommand=scrollbar.set
                , wrap='word')

textarea.insert(END, "Hi there!\n"
                     "I am here to help you pick your meals\n"
                     "For your convenience, Choose an option: \n"
                     "[1] Search by Recipe Names: \n"
                     "[2] Search by Cooking Time\n"
                     "[3] Search by Ingredients\n"
                     "[4] Search by Category\n"
                     "[5] Exit")

textarea.pack(side=LEFT)

# scroll to the end of the text widget
textarea.yview_moveto(1.0)

questionField = Entry(root, font=('verdana', 16, 'bold'))
questionField.pack(side=BOTTOM, fill=X, padx=10, pady=100)
questionField.bind('<Return>', onEnter)

askPic = PhotoImage(file='enter.png')
askLabel = Label(root, image=askPic)
askLabel.place(relx=0.5, rely=1, anchor='s', height=50, width=200, bordermode='outside', y=-20)

# Disable the ability to resize the window
root.resizable(False, False)

# parsing the file into dictionary
recipes = parse_recipe_file('recipes_data.txt')

# displays WINDOW:
root.mainloop()
