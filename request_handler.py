from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from moods import get_all_moods
from entries import get_all_entries, get_single_entries, delete_entry, search_all_entries
# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entries(id)}"
                else:
                    response = f"{get_all_entries()}"
            if resource == "moods":
                if id is not None:
                    response = f"{get_all_moods()}"
                else:
                    response = f"{get_all_moods()}"
            # elif resource == "customers":
            #     if id is not None:
            #         response = f"{get_single_customer(id)}"
            #     else:
            #         response = f"{get_customers()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`


        elif len(parsed) == 3:
            ( resource, key, value ) = parsed
            if resource == "entries":
                if key == "q":
                    response = search_all_entries(value)
            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            # if key == "email" and resource == "customers":
            #     response = get_customers_by_email(value)
            # elif key == "location_id" and resource == "animals":
            #     response = get_animal_by_location(value)
            # elif key == "location_id" and resource == "employees":
            #     response = find_employees_by_location(value)
            # elif key == "status" and resource == "animals":
            #     response = find_animals_by_status(value)

        self.wfile.write(f"{response}".encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_location = None
        new_employee = None
        new_customer2 = None
        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        # if resource == "animals":
        #     new_animal = ""
        #     self.wfile.write(f"{new_animal}".encode())
        # elif resource == "locations":
        #     new_location = create_location(post_body)
        #     self.wfile.write(f"{new_location}".encode())
        # elif resource == "employees":
        #     new_employee = create_employee(post_body)
        #     self.wfile.write(f"{new_employee}".encode())
        # elif resource == "customers":
        #     new_customer = create_customer(post_body)
        #     self.wfile.write(f"{new_customer}".encode())
        # Encode the new animal and send in response
        self.wfile.write(f"{new_animal}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)
        # elif resource == "customers":
        #     delete_customer(id)
        # elif resource == "employees":
        #     delete_employee(id)
        # elif resource == "locations":
        #     delete_location(id)
        # # Encode the new animal and send in response
        self.wfile.write("".encode())
    


    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        # if resource == "animals":
        #     pass
        # elif resource == "customers":
        #     update_customer(id, post_body)
        # elif resource == "employees":
        #     update_employee(id, post_body)
        # elif resource == "locations":
        #     update_location(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())



# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()