import requests

class Address(object):
    """This class provides the mechanism for working building stand U.S. addresses.

    It provides methods for geocoding standard U.S. addresses. Standard U.S. addresses 
    are defined to have the following formats:

        street, state, country, zipcode.

    Attributes:
        
    """
    def __init__(self, street="", city="", state="", country="", zipcode=""):
        """Creates a standard U.S address.

        Args:
            street: 
                String representing the street number. String will be UTF-8 encoded.
            city:
                String representing the city. String will be UTF-8 encoded.
            state:
                String representing the state. String will be UTF-8 encoded.
            country: 
                Optional; String representing the country. String will be UTF-8 encoded.
                Default: United States of America.
            zipcode:
                Integer representing the zipcode.
        """

        self.__street = street
        self.__city = city
        self.__state = state
        self.__country = country
        self.__zipcode = zipcode
        self.__latitude = float("NaN")
        self.__longitude = float("NaN")
        self.__info = {}
        
    @property
    def street(self) -> str:
        """Retrives the street of this address.

        Returns:
            String representing the street of this address.
        """

        return self.__street
    
    @property
    def city(self) -> str:
        """Retrives the city in which this address is located.

        Returns:
            String representing the city in which this address is located.
        """

        return self.__city
    
    @property
    def state(self) -> str:
        """Retrives the state in which this address is located.

        Returns:
            String representing the state in which this address is located.
        """

        return self.__state
    
    @property
    def country(self) -> str:
        """Retrives the country in which this address is located.

        Returns:
            String representing the country in which this address is located.
        """

        return self.__country
    
    @property
    def zipcode(self) -> str:
        """Retrives the zipcode in which this address is located.

        Returns:
            String representing the zipcode in which this address is located.
        """
        
        return self.__zipcode
    
    @property
    def latitude(self) -> float:
        """Retrives the latitude of this address.

        Returns:
            Floating point representing the latitude of this address.
        """

        return self.__latitude
    
    @property
    def longitude(self) -> float:
        """Retrives the longitude of this address.

        Returns:
            Floating point representing the longitude of this address.
        """

        return self.__longitude
    
    @property
    def info(self) -> dict:
        """Retrives additional geocoding information about this address.

        Returns:
            Dict of additional information about this address.
        """

        return self._info
    
    @property
    def coordinates(self) -> tuple:
        """Retrives latitude and longitude of this address.

        Returns:
            A pair representing the latitude and longitude of this address.
        """

        return (self.__latitude, self.__longitude)
    
    def __str__(self) -> str:
        """Retrieves a string representation of this address.

        Returns:
            String representing this address. The string is formatted as follows:
            "STREET, CITY, STATE, COUNTRY, ZIPCODE"
        """
        return '{street}, {city}, {state}, {country}, {zipcode}'.format(street=self.__street, city=self.__city, \
                                                               state=self.__state, country=self.__country,
                                                               zipcode=self.__zipcode)

    def geocode(self):
        """Set geocode coordinates of this address."""

        if not self.__info:
            self.__info = Address.Geocode.get_geocode(self).json()
            
            # print(self._info)

            longitude, latitude = tuple(self.__info['features'][0]['geometry']['coordinates'])
            
            if latitude < -90 or latitude > 90:
                raise Exception("Illegal argument, latitude must be between -90 and 90")

            if longitude < -180 or longitude > 180:
                raise Exception("Illegal argument, longitude must be between -180 and 180")

            self.__latitude = latitude
            self.__longitude = longitude
    
    @staticmethod
    def get_geocodes(addresses:list) -> list:
        """Retrieves geocode coordinates for a list of addresses.

        Args:
            addresses:
                List of addresses.

        Returns:
            List of geocodes representing the geocode coordinates of address passed as arguments.
        """
        geocodes = []
        for address in addresses:
            address.geocode()
            result = '{latitude}, {longitude}'.format(latitude = str(address.latitude), \
                                                    longitude = str(address.longitude))
            geocodes.append(result)
        return geocodes

    class Geocode():
        """This inner class provides the mechanism for geocoding a standard U.S. address."""

        # Define base url
        __api_urls = {
            "base": "https://nominatim.openstreetmap.org/",
            "search": "search/",
            "status": "status.php"
        }

        @staticmethod
        def get_geocode(address):
            '''
            Retrieves geocode of this address.
            '''
            parameters = {
                "street": address.street,
                "city": address.city,
                "state": address.state,
                "country": address.country,
                "postalcode": address.zipcode,
                "format": "geocodejson",
                "polygon_svg": 1
            }
            url = Address.Geocode.__api_urls['base'] + Address.Geocode.__api_urls['search']
            return requests.get(url=url, params=parameters)
        
        @staticmethod
        def connection():
            '''Check server availability'''
            url = "{base}{status}?format={format}".format(base=__api_urls["base"], status=__api_urls["status"], 
                                                          format="json")
            return requests.get(url=url)
    
        @staticmethod
        def json_response(obj, sort=False, indent=4):
            # Create a formatted string of JSON object
            return json.dumps(obj, sort_keys=sort, indent=indent)