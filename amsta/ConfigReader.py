class ConfigReader:

    @staticmethod
    def get_value(val):
        file = open("config.txt")
        for x in file:
            if x.split("=")[0] == val:

                # Removing unnececery characters
                x = x.replace('\n', '')
                x = x.replace('\r', '')

                if x.split("=")[1].lower() == "false":
                    # if value is false return a false boolean
                    return False
                elif x.split("=")[1].lower() == "true":
                    # if value is false return a true boolean
                    return True
                else:
                    try:
                        # If value is able to convert to an int return the int
                        return int(x.split("=")[1])
                    except ValueError:
                        # If a value error ocures return a string
                        return x.split("=")[1]
        return None
