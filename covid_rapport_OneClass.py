from datetime import datetime, timedelta

data = {}


# function that loads the data from the data file
def load_data(filename, classnumber):
    with open(f'classroom_{classnumber}_data.txt', 'r') as f:
        # skip the header
        next(f)
        for line in f:
            line = line.strip().split(',')
            if line[0] not in data:
                data[line[0]] = [line[1:]]
            else:
                data[line[0]].append(line[1:])


# function that checks if input idrfid is in the data
def check_idrfid(idrfid):
    if idrfid in data:
        return True
    else:
        return False


# function that will search throught the data for any students that were at least 15 minutes with the infected student
def get_infected_students(idrfid):
    infected_students = []
    if check_idrfid(idrfid):
        # loop through every class entry of the infected student
        for i in range(len(data[idrfid])):
            date = data[idrfid][i][0].strip()
            intime = data[idrfid][i][1].strip()
            outtime = data[idrfid][i][2].strip()

            # convert the intime and outtime into a datetime object
            in_datetime = datetime.strptime(date + ' ' + intime, '%Y-%m-%d %H:%M:%S')
            out_datetime = datetime.strptime(date + ' ' + outtime, '%Y-%m-%d %H:%M:%S')

            threshold = timedelta(minutes=15)

            # loop through every student in the data
            for student in data:
                if student != idrfid:
                    # loop through every class entry of the student
                    for j in range(len(data[student])):
                        other_date = data[student][j][0].strip()
                        other_intime = data[student][j][1].strip()
                        other_outtime = data[student][j][2].strip()

                        # convert the intime and outtime into a datetime object
                        other_in_datetime = datetime.strptime(other_date + ' ' + other_intime, '%Y-%m-%d %H:%M:%S')
                        other_out_datetime = datetime.strptime(other_date + ' ' + other_outtime, '%Y-%m-%d %H:%M:%S')

                        # check if the student was at least 15 minutes with the infected student
                        if (in_datetime <= other_out_datetime and out_datetime >= other_in_datetime and
                                (min(out_datetime, other_out_datetime) - max(in_datetime, other_in_datetime)) >= threshold):
                            infected_students.append(student)
                            break
    return infected_students


# function that will ask for the class number and covid cases
def getlistofstudents():
    class_number = input('Enter the class number (1-5): ')
    # check if class number is from 1-5
    if class_number not in ['1', '2', '3', '4', '5']:
        print('Invalid input')
        return
    # load the data from the data file
    load_data(f'classroom_{class_number}_data.txt', class_number)
    # ask for covid cases
    while True:
        try:
            covid_cases = input('Were there any covid cases today? (y/n): ')
            if covid_cases == 'y':
                # ask for idrfid
                idrfid = input('Enter the idrfid of the infected student: ')
                # check if idrfid is in the data
                if check_idrfid(idrfid):
                    print('The list of infected students is: ', get_infected_students(idrfid))
                    break
                else:
                    print('The idrfid is not in the data')
            elif covid_cases == 'n':
                print('No infected students')
                break
            else:
                print('Invalid input')
        except:
            print('Invalid input')


if __name__ == '__main__':
    getlistofstudents()
