from enum import Enum
from scan_data import Status, ScanParam, print_class

class MenuControll:

    @staticmethod
    def param_1():
        """a1"""
        print("jestem tutaj")
        print_class(ScanParam)

    @staticmethod
    def param_2():
        """A2"""
        print("Doing 2")

    @staticmethod
    def param_3():
        """A3"""
        print("Doing 3")

    @staticmethod
    def param_4():
        """A4"""
        print("Doing 4")

    @staticmethod
    def param_5():
        """A5"""
        print("Doing 5")

    @staticmethod
    def param_6():
        """A6"""
        print("Doing 6..")
    
        
    @staticmethod
    def execute(data_list):
        global MenuControll
        MenuControll_name = '%s%s'%("param_", data_list[0])
        print(MenuControll_name)
        try:
            controller = getattr(MenuControll, MenuControll_name)
        except AttributeError:
            print("Method not found")
        else:
            controller()

    
    @staticmethod
    def generate_menu():
        print("================================")
        param_methods = [m for m in dir(MenuControll) if m.startswith('param_')]
        
        for method in param_methods:
            print(method[-1], getattr(MenuControll, method).__doc__)
        
        print("================================")
        print("Insert a number:", end = ' ' )


    @staticmethod
    def run():
        user_input = 0
        while(ScanParam.scan != Status.EXIT):
            MenuControll.generate_menu()
            user_input = input("Get param: \t ")
            print(user_input)
            if not (user_input == ''):
                data_list = user_input.split()
                MenuControll.execute(data_list)
            

# test purpuse only
def main():
    MenuControll.run()


if __name__ == "__main__":
    main()