from mimesis import Text, Address, Person
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender


class GetFakeData:
    '''
        API for generation fake data
    '''
    def get_fake_content(self, loc, count):
        text = Text(loc)
        content = text.text(quantity=count)
        return content

    def get_fake_address(self, loc):
        address = Address(loc)
        city = address.city()
        kind_street = address.street_suffix()
        street = address.street_name()
        house = address.street_number()
        area = address.state()
        zip = address.zip_code()
        country = address.country()
        return zip, city, kind_street, street, house, area, country

    def make_full_name(self, loc, value):
        global sex
        per = Person(loc)
        rsp = RussiaSpecProvider()

        if value == 'male':
            sex = Gender.MALE
        elif value == 'famale':
            sex = Gender.FEMALE
        name = per.name(sex)
        surname = per.surname(sex)
        patron = rsp.patronymic(sex)
        age = per.age(16, 66)
        occup = per.occupation()
        return name, surname, patron, age, occup

    def make_phone_number(self, loc):
        per = Person(loc)
        full_phone = per.telephone(mask='', placeholder='#')
        return full_phone

    def get_fake_user(self, loc, sex):
        user_name = self.make_full_name(loc, sex)[0]
        surname = self.make_full_name(loc, sex)[1]
        if loc == 'ru' or loc == 'uk':
            patronymic = self.make_full_name(loc, sex)[2]
        else:
            patronymic = ''
        age = self.make_full_name(loc, sex)[3]
        phone = self.make_phone_number(loc)
        occupation = self.make_full_name(loc, sex)[4]
        return surname, user_name, patronymic, age, phone, occupation

    def get_fake_authentication(self, loc):
        per = Person(loc)
        nickname = per.username(template=None)
        email = per.email(domains=None)
        password = per.password(8)
        return nickname, email, password
