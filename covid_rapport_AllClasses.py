from datetime import datetime, timedelta
import glob

data = {}


# function that loads the data from the data file
def load_data():
    for filename in glob.glob('classroom_*.txt'):
        with open(filename, 'r') as f:
            # skip the header
            next(f)
            for line in f:
                line = line.strip().split(',')
                if line[0] not in data:
                    data[line[0]] = [(line[1:], filename)]
                else:
                    data[line[0]].append((line[1:], filename))


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
            date = data[idrfid][i][0][0].strip()
            intime = data[idrfid][i][0][1].strip()
            outtime = data[idrfid][i][0][2].strip()

            # convert the intime and outtime into a datetime object
            in_datetime = datetime.strptime(date + ' ' + intime, '%Y-%m-%d %H:%M:%S')
            out_datetime = datetime.strptime(date + ' ' + outtime, '%Y-%m-%d %H:%M:%S')

            threshold = timedelta(minutes=15)

            # loop through every student in the data
            for student in data:
                # loop through every class entry of the student
                for j in range(len(data[student])):
                    other_date = data[student][j][0][0].strip()
                    other_intime = data[student][j][0][1].strip()
                    other_outtime = data[student][j][0][2].strip()

                    # convert the intime and outtime into a datetime object
                    other_in_datetime = datetime.strptime(other_date + ' ' + other_intime, '%Y-%m-%d %H:%M:%S')
                    other_out_datetime = datetime.strptime(other_date + ' ' + other_outtime, '%Y-%m-%d %H:%M:%S')

                    # check if the student was at least 15 minutes with the infected student
                    if (in_datetime <= other_out_datetime and out_datetime >= other_in_datetime and
                            (min(out_datetime, other_out_datetime) - max(in_datetime, other_in_datetime)) >= threshold):
                        if student not in infected_students:
                            infected_students.append(student)
                        break
    return infected_students


if __name__ == '__main__':
    load_data()

    # ask the user if any students have covid y/n catch invalid input
    while True:
        try:
            covid = input('Do any students have covid? (y/n): ')
            if covid == 'y' or covid == 'n':
                break
            else:
                print('Invalid input')
        except ValueError:
            print('Invalid input')

    # if any students have covid ask for the idrfid of the infected student
    if covid == 'y':
        while True:
            try:
                idrfid = input('Enter the idrfid of the infected student: ')
                if check_idrfid(idrfid):
                    break
                else:
                    print('Invalid idrfid')
            except ValueError:
                print('Invalid idrfid')

        # print the infected students
        infected_students = get_infected_students(idrfid)
        print('The following students have been infected:')
        for student in infected_students:
            print(student)
    else:
        print('No students have been infected')
