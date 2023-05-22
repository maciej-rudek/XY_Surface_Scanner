from enum import Enum
from src.scan_data import ScanSample
from src.scan_data import Status, ScanParam, DwfData, PictureData

class MenuControll:

    @staticmethod
    def param_1(data_params):
        """Nr of Samples [50-10000]"""
        ScanSample.sample = data_params

    @staticmethod
    def param_2(data_params):
        """Scan Area [1-100] """
        ScanParam.area = data_params

    @staticmethod
    def param_3(data_params):
        """Resolution [50-500] """
        ScanParam.resolution = data_params

    @staticmethod
    def param_4(data_params):
        """Show all Logs"""

    @staticmethod
    def param_5(data_params):
        """Save picture"""
        PictureData.save = Status(data_params)
    
    @staticmethod
    def param_6(data_params):
        """Scan-Stop-Exit"""
        ScanParam.scan = Status(data_params)
        
    @staticmethod
    def execute(data_list):
        global MenuControll
        MenuControll_name = '%s%s'%("param_", data_list[0])
        print(MenuControll_name)
        try:
            controller = getattr(MenuControll, MenuControll_name)
        except AttributeError:
            DwfData.logError = "Method not found."
        else:
            if (len(data_list) > 1):
                controller(data_list[1])
            else:
                DwfData.logError = "Empty parameter."

    
    @staticmethod
    def generate_menu():
        print("================================")
        param_methods = [m for m in dir(MenuControll) if m.startswith('param_')]
        
        for method in param_methods:
            print(method[-1], getattr(MenuControll, method).__doc__)
        
        print("--------------------------------")
            #logs
        print("================================")
        print("Insert a number:", end = ' ' )


    @staticmethod
    def run():
        user_input = 0
        # while(ScanParam.scan != Status.EXIT):
        MenuControll.generate_menu()
        user_input = input("Get param: \t ")
        print(user_input)
        if not (user_input == ''):
            data_list = user_input.split()
            MenuControll.execute(data_list)
        else:
            DwfData.logError = "Empty prompt."
            

# test purpuse only
# def main():
    #cwhile(ScanParam.scan != Status.EXIT):
    # MenuControll.run()


# if __name__ == "__main__":
#     main()