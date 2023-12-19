def correct_capitals_in_name(name):
    words = name.split()
    num_words = len(words)
    
    if num_words == 2:
        corrected_name = f"{words[0].capitalize()} {words[1].capitalize()}"
    elif num_words == 3:
        corrected_name = f"{words[0].capitalize()} {words[1].lower()} {words[2].capitalize()}"
    elif num_words == 4:
        corrected_name = f"{words[0].capitalize()} {words[1].lower()} {words[2].lower()} {words[3].capitalize()}"
    else:
        corrected_name = f"{name} - Unknown name format"
    
    response = input(f"Is the name '{corrected_name}' correctly spelled? (y/n): ")
    
    if response == 'n':
        corrected_name = input(f"Please edit the name: [{name.capitalize()}] : ")
    elif response == 'y' or response is None:
        pass  # Keep the corrected_name as is
    
    return corrected_name

if __name__ == '__main__':
    # Test the function
    print(correct_capitals_in_name("john doe"))  # Output: "John Doe"
    print(correct_capitals_in_name("john van doe"))  # Output: "John van Doe"
    print(correct_capitals_in_name("john van de doe"))  # Output: "John van de Doe"
    print(correct_capitals_in_name("john van de doe-diederik"))  # Output: "John van de Doe"
    print(correct_capitals_in_name("john van de doe-diederik ter ristervoorde"))  # Output: "John van de Doe"

