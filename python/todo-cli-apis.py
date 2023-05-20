import os
import sys
import argparse
import requests
import json
import random
from tabulate import tabulate

def get_all(format):
    """
    Retrieve all TO-DO items from the API.
    
    Args:
        format (str): Output format for the TO-DO items.
    
    Returns:
        Print the list of TO-DO items in the specified format.
    """
    url = api_url + "/api/todos"
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            data = response.json()
            match format:
                case "txt":
                    for item in data:
                        print(item['text'])
                case "json":
                    print(json.dumps(data, indent=4))
                case "table":
                    print(tabulate(data, headers="keys", tablefmt="grid"))
                case _:
                    return data
        else:
            print(f"Error retrieving TO-DOs with HTTP ERROR {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving TO-DOs: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing response: {e}")
        sys.exit(1)

def create(description):
    """
    Create a new TO-DO item with the given description.
    
    Args:
        description (str): Description of the TO-DO item.
    """
    url = api_url + "/api/todos"
    todo = {"text": description}
    try:
        response = requests.post(url, json=todo)
        if response.status_code == requests.codes.ok:
            print(f"TO-DO with description '{description}' created correctly.")
        else:
            print(f"Error creating TO-DO with HTTP ERROR {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating TO-DO: {e}")
        sys.exit(1)

def delete(description):
    """
    Delete a TO-DO item with the given description.
    
    Args:
        description (str): Description of the TO-DO item to delete.
    """
    try:
        # Filter the JSON data based on the 'text' field to get the ID
        filtered_json = [item for item in get_all("") if item['text'] == description]
        # If the TO-DO is not found, exit 0.
        if len(filtered_json) == 0:
            print(f"TO-DO with description {description} not found.")
            sys.exit(0)
        for item in filtered_json:
            id = item["_id"]
            url = api_url + "/api/todos/" + id
            response = requests.delete(url)
            if response.status_code == requests.codes.ok:
                print(f"TO-DO with description '{description}' and ID {id} deleted correctly.")
            else:
                print(f"Error deleting TO-DO with HTTP ERROR {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting TO-DO: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing response: {e}")
        sys.exit(1)

def test():
    """
    Execute the test workflow for TO-DOs.
    """
    try:
        # Loop in range between 10 and 100
        for i in range(0, random.randint(10, 100)):
            create(f"dummy_{i}")
        print("Get all TO-DOs in JSON format:")
        get_all("json")
        print("Get all TO-DOs in TXT format:")
        get_all("txt")
        print("Get all TO-DOs in TABLE format:")
        get_all("table")
        print("Deleting all the TO-DOs")
        for item in get_all(""):
            delete(item["text"])
    except Exception as e:
        print(f"Error during test workflow: {e}")
        sys.exit(1)

def main():
    """
    Main entry point of the CLI program.
    """
    # Read and verify connection string env variable
    global api_url
    api_url = os.environ.get('API_URL')
    if api_url is None:
        print("Environment variable API_URL is not defined. You must define it before starting the CLI. Check README.md.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="TO-DO Console Client")

    # Add Help support and customize error message if invalid action is passed.
    def error_message(message):
        print(f"Error: {message}\n")
        parser.print_help()
        exit(1)

    # Print the custom error message
    parser.error = error_message

    # Parse the different actions supported
    subparsers = parser.add_subparsers(title="Actions")

    # Get All Action.
    parser_get_all = subparsers.add_parser("get_all", help="Get all TO-DOs. Accepted Parameters: --format")
    parser_get_all.add_argument("--format", choices=["txt", "table", "json"], type=str, help="Output format")
    parser_get_all.set_defaults(func=get_all)

    # Create 1 TO-DO
    parser_create = subparsers.add_parser("create", help="Create 1 TO-DO. Accepted Parameters: --description")
    parser_create.add_argument("--description", type=str, help="TO-DO description to create")
    parser_create.set_defaults(func=create)

    # Delete 1 TO-DO
    parser_delete = subparsers.add_parser("delete", help="Delete 1 TO-DO. Accepted Parameters: --description")
    parser_delete.add_argument("--description", type=str, help="TO-DO description to delete")
    parser_delete.set_defaults(func=delete)

    # Test workflow
    parser_test = subparsers.add_parser("test", help="Execute TO-DO test workflow. No parameters needed.")
    parser_test.set_defaults(func=test)

    # Parse arguments and verify action and arguments
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.error("Please specify a valid action.")
    elif args.func == get_all and args.format is None:
        parser.error("Please specify the --format parameter for the get_all action.")
    elif args.func == create and args.description is None:
        parser.error("Please specify the --description parameter for the create action.")
    elif args.func == delete and args.description is None:
        parser.error("Please specify the --description parameter for the delete action.")
    args_dict = vars(args)
    function = args_dict.pop("func")
    function(**args_dict)

# Run the main method if the script is called directly
if __name__ == "__main__":
    main()
