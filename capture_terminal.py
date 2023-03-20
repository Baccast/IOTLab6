import random
import datetime

# set the start and end times for the classroom
start_time = datetime.time(13, 0)
end_time = datetime.time(18, 0)

# define the number of classrooms and students
num_classrooms = 5
num_students = 20

# load the list of valid rfid identifiers from the students.txt file
with open("students.txt", "r") as f:
    valid_ids = [line.strip() for line in f]


# define a function to generate a random datetime within the classroom hours
def random_datetime():
    date = datetime.date.today()
    time = datetime.time(
        hour=random.randint(start_time.hour, end_time.hour - 1),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )
    return datetime.datetime.combine(date, time)


# generate a data file for each classroom
for i in range(num_classrooms):
    # generate a unique filename for each data file
    filename = f"classroom_{i + 1}_data.txt"

    # open the file and write the header
    with open(filename, "w") as f:
        f.write("idrfid, date, intime, outtime\n")

        # generate random data for each student
        for j in range(num_students):
            # randomly select a valid rfid identifier
            idrfid = random.choice(valid_ids)

            # randomly generate the check-in and check-out times
            intime = random_datetime()
            outtime = intime + datetime.timedelta(hours=1)

            # write the data to the file
            f.write(f"{idrfid}, {intime.date()}, {intime.time()}, {outtime.time()}\n")
