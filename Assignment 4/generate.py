from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker("en_US")
fake.add_provider(VehicleProvider)

num = 1
userNum = input("How many rows? :")
with open('output.csv', 'w') as file:
    line = "Make,Model,Year,Color,Miles,MPG,Odo,Date,Amount,Desc,Mechanic,Address,Phone"
    print(line, file=file)
    for x in range(0, int(userNum)):
        line = ""
        # Vehicle Table
        fakeV = fake.vehicle_object()
        make = fakeV["Make"]
        model = fakeV["Model"]
        year = fakeV["Year"]
        line += make + ","
        line += model + ","
        line += str(year) + ","
        color = fake.color_name()
        line += color + ","
        miles = fake.random_int()
        line += str(miles) + ","
        mpgCombined = fake.random_int(0, 60)
        line += str(mpgCombined) + ","

        # Invoice Table
        odo = miles
        line += str(odo) + ","
        date = fake.date()
        line += date + ","
        amount = fake.pydecimal(positive=True)
        line += str(amount) + ","
        desc = fake.sentence(nb_words=5)
        line += desc + ","

        # Mechanic Table
        mechanic = fake.name()
        line += mechanic + ","
        location = fake.address().replace('\n', '').replace(",","|")
        line += location + ","
        phone = fake.phone_number()
        line += str(phone) + ","
        print(line, file=file)
