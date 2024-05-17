from collections import UserDict

                                                                # classes for work with adress book 
class Field:                                                    # present generic field in contact record
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):                                              # present name field in contact record
    pass

class Phone(Field):
    def __init__(self, value):                                  # present phone number field in contact record
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)

class Record:                                                   # present contact record
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):                                 
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):                 # replace old_phone to new_phone
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError("Phone number not found")          # if not -> Raise error msg
    
    def __str__(self):                                          # convert object into string
        phones_str = ', '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found")


                                                                # functionality of assistant # initialition of decorator for different exceptions during using bot
def input_error(func):                                          
    def inner(*args, **kwargs):                                 
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command arguments."
    return inner

@input_error
def add_contact(address_book, name, phone):                    # extract name and phone number from args and add to dictionary
    record = address_book.find(name)
    if not record:
        record = Record(name)
        address_book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(address_book, name, old_phone, new_phone):  # extract name and phone number from args and update dictionary
    record = address_book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    else:
        return "Contact not found."

@input_error
def show_phone(address_book, name):                             # extract name from args and look up phone number in dictionary
    record = address_book.find(name)
    if record:
        return ', '.join(p.value for p in record.phones)
    else:
        return "Contact not found."

@input_error
def show_all(address_book):                                     # show all contacts in dictionary
    return '\n'.join(str(record) for record in address_book.values())

def parse_input(user_input):
    if not user_input.strip():                                  # empty enter check
        return "Invalid command.", []
    cmd, *args = user_input.split()                             # split input into command and arguments
    cmd = cmd.strip().lower()                                   # convert to lowercase for case insensitivity
    return cmd, args

def main():
    address_book = AddressBook()                                # create new clean dictionary
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
                                                                # commands block
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) < 2:
                print("Give me name and phone please.")
            elif len(args[1]) != 10 or not args[1].isdigit():
                print("Phone number must be a 10-digit number")
            else:
                name, phone = args
                print(add_contact(address_book, name, phone))
        elif command == "change":
            if len(args) < 3:
                print("Give me name, old phone, and new phone please.")
            else:
                name, old_phone, new_phone = args
                print(change_contact(address_book, name, old_phone, new_phone))
        elif command == "phone":
            if len(args) < 1:
                print("Enter the name for the command")
            else:
                name = args[0]
                result = show_phone(address_book, name)
                if result:
                    print(f'Phone number for contact {name}: {result}')
                else:
                    print('Contact not found.')
        elif command == "all":
            print(show_all(address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
