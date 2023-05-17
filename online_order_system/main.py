
from user import User, Role, Permissions
from verifications import RequestFilter, DataSanitizer, CacheManager
from data import Data
from order_manager import OrderManager
from request import Request

def main():
    # Create roles and permissions
    permisos_admin = [Permissions("crear"), Permissions("editar"), Permissions("eliminar")]
    permisos_usuario = [Permissions("leer")]

    rol_admin = Role("Admin")
    rol_usuario = Role("Usuario")

    # Set permissions to roles
    roles_permisos = {
        rol_admin: permisos_admin,
        rol_usuario: permisos_usuario
    }

    print("Welcome to the Order online!")
    username = input("Please write your username: ")
    cantidad_fallas = 1

    ip_address = "127.0.0.3"

    # Authentication of the user.
    try:
        for i in range(1):
            if username == "johnwick" or username == "janesmith":
                break
            else:
                print("Invalid username")
                username = input("Please write your username: ")
                cantidad_fallas += 1
        if cantidad_fallas == 2:
            with open("blacklist.txt", "a") as file:
                file.write(ip_address + "\n")
            raise ValueError
    except ValueError:
        print("You have exceeded the number of attempts")
        exit()

    # Crear usuarios con sus respectivos roles
    if username == "johnwick":
        user = User("John Wick", "johnwick", "password123", rol_admin)
    else:
        user = User("Jane Smith", "janesmith", "password456", rol_usuario)

    if user.role == rol_admin:
        print("Welcome, Admin!")
        choice = input("What do you want to do: 1. View orders, 2. Delete order, 0. To exit ")
    else:
        print("Welcome, User!")
        choice = input("What do you want to do: 1. Create order, 2. View orders, 0. To exit ")

    order_number = ""
    lines = []
    match choice:
        case "1":
            if user.role == rol_admin:
                print("Viewing orders...")
                with open("orders.txt", "r") as file:
                    for line in file:
                        print(line.strip())
            else:
                order_number = input("Please write the order number: ")
        case "2":
            if user.role == rol_admin:
                print("Deleting order...")
                order_number = input("Please write the order number: ")

                # Open the file for reading and create an empty list to store the lines
                with open("orders.txt", "r") as file:
                    for line in file:
                        if line.strip() != order_number:
                            lines.append(line)

                # Open the file for writing and write the lines we didn't read from the original file
                with open("orders.txt", "w") as file:
                    for line in lines:
                        file.write(line)
            else:
                print("Viewing orders...")
        case "0":
            print("Exiting...")
        case _:
            print("Invalid option")

        # Crear una solicitud
    credentials = user
    data = Data("1", order_number)
    request = Request(credentials, data, ip_address)

    # Create instances of each handler in the chain
    filter_handler = RequestFilter(role_permissions=rol_admin, ip_address=ip_address)
    sanitizer_handler = DataSanitizer(json_data={"id":request.data.id,"order":request.data.order})
    cache_handler = CacheManager()

    # Connect the handlers in the chain
    filter_handler.successor = sanitizer_handler
    sanitizer_handler.successor = cache_handler

    # Crear una instancia de OrderManager con el manejador de solicitud configurado
    order_manager = OrderManager(filter_handler)

    # Procesar la solicitud
    order_manager.processRequest(request)

if __name__ == '__main__':
    main()
