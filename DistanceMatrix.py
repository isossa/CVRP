import requests
import json

class DistanceMatrix(object):
    """
    This class defines the mechanics for requesting a distance/duration matrix 
    from a set of locations.

    This implementation relies on Microsoft Bing Maps DistanceMatrix API. A 
    distance/duration can be requested by simply running the following line:

        Typical usage example:

        matrix = DistanceMatrix.get_matrix(geocodes, 'travelDistance', 'driving')

    Attributes:
        None.        

    More information about the Bing Maps DistanceMatrix API can be found here:
    """

    # Defines API urls
    __api_urls = {
        "base" : "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?"
    }
    
    # Distance matrix between pair of locations
    __distance_matrix = []

    # HTTP response
    __response = {}

    # Store list of last locations whose distance matrix has been requested
    __last_requested = []

    # Count of number of unnecessary requests. These are saved!
    __number_of_requests_saved = 0

    # Total number of requests made.
    __number_of_requests_made = 0

    @staticmethod
    def get_matrix(geocodes:list, api_key:str, key='travelDistance', travelMode='driving') -> list:
        """Gets distance or duration matrix.

        Retrieves duration or duration matrix between pairs of a list of locations 
        representing by their geocodes.

        Args:
            geocodes: 
                A list of geocodes representing locations.
            api_key:
                Bing Maps Developer's API key.
            key:
                Type of matrix to retrieve. Can be either 'travelDistance' or 
                      'travelDuration'.
            travelMode: 
                Optional; Specifies the means of transportation. Default value is
                        'driving'.

        Returns:
            A matrix whose cells represent the travel distance/duration between pairs of 
            locations.

            When an inappropriate key is passed, an empty list is returned.

            The unit of these numbers depends on the type (distance or duration) is specified 
            by Microsoft Bing Maps Distance Matrix API.
        """

        if key not in ["travelDistance", "travelDuration"]:
            return []

        # Make API request
        response = DistanceMatrix.__request_matrix(geocodes=geocodes, api_key=api_key, travelMode=travelMode)

        # Build distance and time matrix between pair of geocodes
        grid = DistanceMatrix.__build_matrix(geocodes=geocodes, response=response)
        matrix = []
        for row in grid:
            result = [x[key] for x in row]
            matrix.append(result)
        return (matrix)
        
    def __identical_list(list1: list, list2: list) -> bool:
        """Checks if two list are equals.

        Args:
            list1:
                List of geocodes represented as string.
            list2:
                List of geocodes representes as string.

        Returns:
            True if the list arguments contains exactly the same elements.
        """

        return (len(set(list1) - set(list2)) == 0 and len(set(list2) - set(list1)) == 0)

    def __build_matrix(geocodes:list, response:requests.Response) -> list:
        """Creates a matrix, distance and duration between pairs of locations.

        Args:
            geocodes:
                Location geocodes specified as a list of longitude and latitude coordinates.
            response:
                HTTP request response. Only '200 OK' will result in matrix.

        Returns:
            Matrix of distance and duration between pairs of locations.
        """
        matrix = []

        if response['statusCode'] == 200:
            row = []

            for counter, item in enumerate(response["resourceSets"][0]['resources'][0]['results']):
                keys_of_interest = ["travelDistance", "travelDuration"]
                result = {key : item[key] for key in keys_of_interest}
                row.append(result)
                if (counter + 1) % len(geocodes) == 0:
                    matrix.append(row)
                    row = []
        else:
            print(f"Execution stopped with HTTP code {response['statusCode']} {response['statusDescription']}")

        return matrix
    
    def __request_matrix(geocodes:list, api_key:str, travelMode:str) -> requests.Response:
        """Initializes an HTTP request to Bing Maps Distance Matrix API.

            Args:
                geocodes:
                    Location geocodes specified as a list of longitude and latitude coordinates.
                api_key:
                    Bing Maps Developer's API key.
                travelMode:
                    String represented the travel mode between locations.

            Returns:
                HTTP response.
        """
        DistanceMatrix.__number_of_requests_made += 1
        condition1 = len(DistanceMatrix.__response) == 0 or DistanceMatrix.__response['statusCode'] != 200
        condition2 = not(DistanceMatrix.__identical_list(DistanceMatrix.__last_requested, geocodes))

        if condition1 or condition2:
            DistanceMatrix.__last_requested = geocodes
            parameters = {
                "origins": '; '.join(geocodes),
                "destinations" : '; '.join(geocodes),
                "travelMode" : travelMode,
                "key" : api_key
            }
            url = DistanceMatrix.__api_urls['base']
            DistanceMatrix.__response = requests.get(url, params=parameters).json()
        else:
            DistanceMatrix.__number_of_requests_saved += 1
        return DistanceMatrix.__response