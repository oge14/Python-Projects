"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
StudentId: 151237366
Name:      Oskari Kuisma
Email:     oskari.kuisma@tuni.fi

PROJECT 4: Warehouse Inventory

This is a simple program of a to help with warehouse inventory.
This program has atrributes that can print, delete, change,
combibe and set sale on products. The program is also coded in a way that
gives the user error messages for bad inputs.
"""

class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock):
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock
        self.__original_price = price


    def __str__(self):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests.
        """

        lines = [
            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)


    def __eq__(self, other):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests since the read_database function will
        stop working correctly.
        """

        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price


    def modify_stock_size(self, amount):
        """
        YOU SHOULD NOT MODIFY THIS METHOD since read_database
        relies on its behavior and might stop working as a result.

        Allows the <amount> of items in stock to be modified.
        This is a very simple method: it does not check the
        value of <amount> which could possibly lead to
        a negative amount of items in stock. Caveat emptor.

        :param amount: int, how much to change the amount in stock.
                       Both positive and negative values are accepted:
                       positive value increases the stock and vice versa.
        """

        if amount < 0:
            self.__stock -= abs(amount)
        else:
            self.__stock += abs(amount)


    def check_stock(self):
        """
        Checks if the product has stock.
        :return: True if the product has stock /
        False if it doesn't and the product can be deleted.
        """

        if self.__stock > 0:
            return True
        else:
            return False


    def check_low_stock(self):
        """
        Checks if the product stock is 30 or lower.
        :return: True if the stock is 30 or lower -> prints the product.
                 False if the stock is higher than 30 -> doesn't print.
        """
        if self.__stock <= 30:
            return True
        else:
            return False


    def combine_product(self, product):
        """
        Tests if the product object's category and the price are the
        same as the self object's category and price.
        :param product: Product object.
        :return: True and adds the product object's stock to the self object's stock /
                 False if the tests fail.
        """

        if self.__category != product.__category:
            print(f"Error: combining items of different categories '{self.__category}' and '{product.__category}'.")
            return False

        if self.__price != product.__price:
            print(f"Error: combining items with different prices {self.__price}€ and {product.__price}€.")
            return False

        if self.__price == product.__price:
            self.__stock += product.__stock
            return True

        else:
            return False


    def set_sale(self, sale, category):
        """
        Set's the sale on the products in the wanted category.
        Returns the price to the normal price if the sale percentage is 0 %.
        :param sale: Sale percent.
        :param category: The category for the sale to be added to.
        :return: True if the sale is applied / False if not.
        """

        if sale == 0:
            self.__price = self.__original_price
            return True

        elif self.__category == category:
            self.__price = self.__original_price * (100-float(sale))/100
            return True

        else:
            return False


def _read_lines_until(fd, last_line):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION since read_database
    relies on its behavior and might stop working as a result.

    Reads lines from <fd> until the <last_line> is found.
    Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if
    file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#'
    and everything after it on a line).

    You don't need to understand this function works as it is
    only used as a helper function for the read_database function.

    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """

    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)


def read_database(filename):

    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:
                lines = _read_lines_until(fd, "BEGIN PRODUCT")
                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")
                if lines is None:
                    print(f"Error: premature end of file while reading '{filename}'.")
                    return None

                print(f"TEST: {lines=}")

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(maxsplit=1)  # ValueError possible

                    print(f"TEST: {keyword=} {value=}")

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible

                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.

                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible

                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(f"Error: a product block is missing one or more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                print(product)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def delete_product(warehouse, parameters):
    """
    This function deletes the wanted product if there is no stock.
    It calls the check_stock method which returns a bool value.
    :param warehouse: Warehouse dictionary.
    :param parameters: The parameters of the user input.
    """

    parameters_list = parameters.split()
    try:
        if len(parameters_list) > 1:
        # Error message if there are more than 1 parameters
            print(f"Error: product '{parameters}' can not be deleted as it does not exist.")
        # Error message if the product has stock
        elif warehouse[int(parameters_list[0])].check_stock():
            print(f"Error: product '{parameters_list[0]}' can not be deleted as stock remains.")
        # Deletes the product if conditions are met
        else:
            del warehouse[int(parameters_list[0])]

    except KeyError:
        print(f"Error: product '{parameters}' can not be deleted as it does not exist.")
    except ValueError:
        print(f"Error: product '{parameters}' can not be deleted as it does not exist.")
    except IndexError:
        print(f"Error: product '{parameters}' can not be deleted as it does not exist.")


def change_stock(warehouse, parameters):
    """
    This function changes the stock amount by how
    much the user wants. It calls the modify stock size method,
    which changes the stock size.
    :param warehouse: Warehouse dictionary.
    :param parameters: The parameters of the user input.
    """
    parameters_list = parameters.split()
    try:
        if int(parameters_list[0]) not in warehouse:
        # Error message if the product isn't in the dictionary
            print(f"Error: stock for '{parameters_list[0]}' can not be changed as it does not exist.")
        # Error message if more than 2 parameters are given
        elif len(parameters_list) > 2:
            print(f"Error: bad parameters '{parameters}' for change command.")
        # Calls the modify stock size method, which changes the stock size
        else:
            warehouse[int(parameters_list[0])].modify_stock_size(int(parameters_list[1]))

    except KeyError:
        print(f"Error: bad parameters '{parameters}' for change command.")
    except ValueError:
        print(f"Error: bad parameters '{parameters}' for change command.")
    except IndexError:
        print(f"Error: bad parameters '{parameters}' for change command.")


def print_one_product(warehouse, parameters):
    """
    This function prints the information of one product.
    :param warehouse: Warehouse dictionary.
    :param parameters: The parameters of the user input.
    """
    try:
        print(warehouse[int(parameters)])
    except ValueError:
        print(f"Error: product '{parameters}' can not be printed as it does not exist.")
    except KeyError:
        print(f"Error: product '{parameters}' can not be printed as it does not exist.")


def combine_products(warehouse, parameters):
    """
    This function combines two products if the
    correct requirements are met. Calls the combine product
    method, which checks if the combination is possible.
    :param warehouse: Warehouse dictionary.
    :param parameters: The parameters of the user input.
    """
    parameters_list = parameters.split()
    try:
        # Error message if the products are the same
        if int(parameters_list[0]) == int(parameters_list[1]):
            print(f"Error: bad parameters '{parameters}' for combine command.")
        # Calls the combine product method
        if warehouse[int(parameters_list[0])].combine_product(warehouse[int(parameters_list[1])]):
            # Deletes the second product if the combination was possible
            del warehouse[int(parameters_list[1])]

    except KeyError:
        print(f"Error: bad parameters '{parameters}' for combine command.")
    except ValueError:
        print(f"Error: bad parameters '{parameters}' for combine command.")
    except IndexError:
        print(f"Error: bad parameters '{parameters}' for combine command.")


def apply_sale(warehouse, parameters):
    """
    This function applies the sale to the products
    in the wanted category. Calls the set sale method,
    which applies the sale.
    :param warehouse: Warehouse dictionary.
    :param parameters: The parameters of the user input.
    """
    parameters_list = parameters.split()
    try:
        sale_category = parameters_list[0]
        sale = parameters_list[1]
        count = 0
        # Calls the set sale method and counts how many times the sale was applied.
        for code in warehouse:
            if warehouse[code].set_sale(sale, sale_category):
                count += 1
        print(f"Sale price set for {count} items.")
    except ValueError:
        print(f"Error: bad parameters '{parameters}' for sale command.")


def main():

    filename = input("Enter database name: ")

    warehouse = read_database(filename)

    if warehouse is None:
        return

    while True:
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        if "print".startswith(command) and parameters == "":
            for code in sorted(warehouse):
                print(warehouse[code])

        elif "print".startswith(command) and parameters != "":
            print_one_product(warehouse, parameters)

        elif "delete".startswith(command) and parameters != "":
            delete_product(warehouse, parameters)

        elif "change".startswith(command) and parameters != "":
            change_stock(warehouse, parameters)

        elif "low".startswith(command) and parameters == "":
            for code in sorted(warehouse):
                # Calls the check low stock method which returns true
                # if the stock is 30 or lower.
                if warehouse[code].check_low_stock():
                    print(warehouse[code])

        elif "combine".startswith(command) and parameters != "":
           combine_products(warehouse, parameters)

        elif "sale".startswith(command) and parameters != "":
            apply_sale(warehouse, parameters)

        else:
            print(f"Error: bad command line '{command_line}'.")

if __name__ == "__main__":
    main()
