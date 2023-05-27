import pandas as pd

class Hotel:
    def __init__(self, hotel_chosen):
        self.hotel_id = hotel_chosen

    def available(self):
        value = list_hotels[list_hotels['id'] == self.hotel_id]['available'].squeeze()
        if value.strip() == 'yes':
            print('available!')
            return True
        else:
            return False

    def book(self):
        list_hotels.loc[list_hotels['id'] == self.hotel_id, 'available'] = 'no'
        list_hotels.to_csv('hotels.csv', index=False)

        
class Confo:
    def __init__(self, name, hotel_chosen):
        self.name = name
        self.hotel_id = hotel_chosen

    def generate(self):
        hotel_name = list_hotels.loc[list_hotels['id'] == self.hotel_id, 'name'].squeeze()
        city = list_hotels.loc[list_hotels['id'] == self.hotel_id, 'city'].squeeze()
        capacity = list_hotels.loc[list_hotels['id'] == self.hotel_id, 'capacity'].squeeze()
        print(f"""
        dear {name}, 
        you have booked {hotel_name} in the city of {city}
        with a capacity of {capacity} pax""")



class Payment:
    def __init__(self, ccard):
        self.ccard = ccard

    def validate(self):
        if any(cards['number'].isin([self.ccard])):
            return True
        else:
            print("number doesn't exist")
            return False

    def prompt(self):
        i = cards[cards['number'] == self.ccard].index
        expiration = input('enter expiration date (mm/yy):').strip()
        cvv = input('enter cvv number:').strip()
        cardholder = input('enter cardholder name:').strip().upper()
        expirationX = cards['expiration'][i].squeeze().replace('"', '').strip()
        cvvX = cards['cvc'][i].squeeze().replace('"', '').strip()
        cardholderX = cards['holder'][i].squeeze().replace('"', '').strip()

        if all([expiration == expirationX,
                cardholder == cardholderX,
                cvv == cvvX]):
            return True
        else:
            print('credit card not validated')
            return False


cards = pd.read_csv('cards.csv', sep=",")
#cards.astype('string').dtypes
list_hotels = pd.read_csv('hotels.csv')
print(list_hotels)
hotel_chosen = int(input('enter id of hotel: '))
hotel = Hotel(hotel_chosen)

#note addition of .values to panda series
if hotel_chosen in list_hotels['id'].values:
    if hotel.available():
        #check if cc exists
        ccard = int(input('input credit card number, no spaces: ').strip())

        payment = Payment(ccard)
        if payment.validate():
            if payment.prompt():
                #change avail status of hotel
                hotel.book()
                name = input('enter your name: ')
                confo = Confo(name, hotel_chosen)
                #generate confo
                confo.generate()
        else:
            print('credit card details incorrect')
    else:
        print('hotel not available. pls choose another hotel')
else:
    print("hotel doesn't exist. pls try again")
