import csv
import os


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.name = self
        self.brand = str(brand)
        self.photo_file_name = str(photo_file_name)
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        ext = os.path.splitext(self.photo_file_name)
        if ext[1] == '.jpg' or '.jpeg' or '.png' or '.gif':
            return ext[1]
        else:
            print('Неверный формат фото')


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        self.car_type = 'truck'
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl
        if self.body_whl != '' and len(self.body_whl.split('x')) == 3:
            self.body_length = float(self.body_whl.split('x')[0])
            self.body_width = float(self.body_whl.split('x')[1])
            self.body_height = float(self.body_whl.split('x')[2])
        else:
            self.body_length = float()
            self.body_width = float()
            self.body_height = float()

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        try:
            for row in reader:
                if row[0] == 'car' and row[1] != '' and row[3] != '' and row[5] != '' and row[2] != '' \
                        and (row[3].split('.')[1] == '.jpg' or '.jpeg' or '.png' or '.gif'):
                    try:
                        car = Car(row[1], row[3], row[5], row[2])
                        car_list.append(car)
                    except ValueError as err:
                        pass
                elif row[0] == 'truck' and row[1] != '' and row[3] != '' and row[5] != '' \
                        and (row[3].split('.')[1] == '.jpg' or '.jpeg' or '.png' or '.gif'):
                    try:
                        car = Truck(row[1], row[3], row[5], row[4])
                        car_list.append(car)
                    except ValueError as err:
                        pass
                elif row[0] == 'spec_machine' and row[1] != '' and row[3] != '' and row[5] != '' and row[6] != '' \
                        and (row[3].split('.')[1] == '.jpg' or '.jpeg' or '.png' or '.gif'):
                    try:
                        car = SpecMachine(row[1], row[3], row[5], row[6])
                        car_list.append(car)
                    except ValueError as err:
                        pass
            return car_list
        except IndexError as err:
            pass
    return car_list

# with open('coursera_week3_cars.csv') as csv_fd:
#     car_list2 = []
#     reader = csv.reader(csv_fd, delimiter=';')
#     next(reader)  # пропускаем заголовок
#     for row in reader:
#         # if row[0] == 'car':
#         car_list2.append(row)
# print(car_list2)
#
# cars = get_car_list('coursera_week3_cars.csv')
# print(cars[1].brand)
# print(len(cars))
# for car in cars:
#     print(type(car))
# print(cars[0].passenger_seats_count)
# cars[1].get_body_volume()
# truck = Truck('Nissan', 't1.jpg', '2.5', '')
# print(truck.carrying)
# print(isinstance(truck.carrying, float))
# print(truck.get_body_volume())