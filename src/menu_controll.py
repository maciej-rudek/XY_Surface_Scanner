


class MenuControll:

    @staticmethod
    def param_1():
        """a1"""
        print("Doing 1")

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
        """A6 exit"""
        print("Exiting..")
        
        
    @staticmethod
    def execute(user_input):
        # MenuControll_name = "param_"{user_input}
        MenuControll_name = '%s%d'%("param_", user_input)
        print(MenuControll_name)
        try:
            MenuControll = getattr(MenuControll, MenuControll_name)
        except AttributeError:
            print("Method not found")
        else:
            MenuControll()
            
    
    @staticmethod
    def generate_menu():
        print("================================")
        param_methods = [m for m in dir(MenuControll) if m.startswith('param_')]
        # for method in param_methods:
        #     print(method[-1], getattr(MenuControll, method).__doc__)
        
        menu_string = "\n".join([' '.join([method[-1], (getattr(MenuControll, method).__doc__)]) for method in param_methods])

        # menu_string = "\n".join(
            # [{method[-1]}. {getattr(MenuControll, method).__doc__} for method in param_methods])
        print(menu_string)
        print("================================")
        print("Insert a number:", end = ' ' )


    @staticmethod
    def run():
        user_input = 0
        while(user_input != 6):
            MenuControll.generate_menu()
            user_input = int(input())
            MenuControll.execute(user_input)
        print("Program stopped.")


# test purpuse only
def main():
    MenuControll.run()


if __name__ == "__main__":
    main()