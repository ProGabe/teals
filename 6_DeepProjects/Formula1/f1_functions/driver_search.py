'''
    Driver Search:

    This function supports searching for drivers by:

    1. -l : Last name of a driver
            Lists all drivers with the same last name
    2. -y : A year of F1. Lists all the drivers that were involved
            in the championship that year. 
    3. -q : A query. Valid query fields are those found in the drivers.csv
            data file headers.
    4.    : No arguments returns all drivers who ever drove. 

    Order of precedence, when one is hit that is the result
        -q
        -l
        -y
'''
import json
from multi_command_utils.data_file import column_data
from multi_command_utils.interface import IFunction, argument_definition
from Formula1.f1_functions.constants import F1DataConstants

class DriverSearch(IFunction):
    def __init__(self, datasets):
        super().__init__(
            datasets,
            # Define the arguments you will accept, -h is a default for all.
            [
            argument_definition('-l',False, 'Last name of driver'),
            argument_definition('-y',False, 'Formula 1 season (year)')
            ])

    def execute(self, args):
        try:
            # This call validates inputs. If a required arg isn't there 
            # or an additional, unexpected, arg is present it will except.
            execute_args = super()._parse_execute_arguments(args)

            if IFunction.GLOBAL_HELP in execute_args.keys():
                # Regardless of anything else, if help is there, show it and quit
                self.get_help(1)
            else:
                # At this point, you're clear and ready to go. 
                # This is where all your logic goes. 
                driver_data = self.datasets[F1DataConstants.DRIVER_DATA]
                race_data = self.datasets[F1DataConstants.RACE_DATA]
                results_data = self.datasets[F1DataConstants.RESULTS_DATA]
                driver_info = None

                search_header = "Search All Drivers:"
                if IFunction.GLOBAL_QUERY in execute_args.keys():
                    # Search by query
                    # EX: list drivers -q surname=Senna;forename=Bruno
                    #     list drivers -q nationality=Brazilian
                    search_header = "Search Drivers By Query {}:".format(json.dumps(execute_args[IFunction.GLOBAL_QUERY]))
                    search_fields = []
                    for query_field in execute_args[IFunction.GLOBAL_QUERY].keys():
                        search_fields.append(column_data(query_field,execute_args[IFunction.GLOBAL_QUERY][query_field]))
                    driver_info = driver_data.find(search_fields)

                elif '-l' in execute_args.keys():
                    # Search by last name
                    search_header = "Search Drivers By Last Name {}:".format(execute_args['-l'])
                    driver_info = driver_data.get_by_name(None,execute_args['-l'])
                elif '-y' in execute_args.keys():
                    # Search by year
                    search_header = "Search Drivers By Year {}:".format(execute_args['-y'])
                    races = race_data.get_by_race_year(execute_args['-y'])
                    driver_id_list = []
                    driver_info = []
                    print("Races", len(races))
                    for race in races:
                        race_results = results_data.get_by_race_id(race.raceId)
                        for race_result in race_results:
                            if race_result.driverId not in driver_id_list:
                                driver_id_list.append(race_result.driverId)
                                current_driver = driver_data.get_by_driver_id(race_result.driverId)
                                driver_info.extend(current_driver)
                else:
                    # Get all
                    driver_info = driver_data.get_by_name(None,None)

                # Now dump out what we found
                count = len(driver_info) if driver_info else 0
                print("{}: {} drivers".format(search_header, count))
                print("%s" % ("-".ljust(85,'-') ))
                print("%s | %s | %s | %s | %s" % (
                    "Driver ID".center(10), 
                    "First Name".center(18), 
                    "Last Name".center(18), 
                    "DOB".center(15),
                    "Nationality".center(17)) )
                print("%s" % ("-".ljust(85,'-') ))

                driver_iterations = driver_info if driver_info else []
                for driver in driver_iterations:
                    print("%s | %s | %s | %s | %s" % (
                        driver.driverId.center(10), 
                        driver.forename.center(18), 
                        driver.surname.center(18), 
                        driver.dob.center(15),
                        driver.nationality.center(17)) )

        except Exception as ex:
            print(str(ex))
            raise ex