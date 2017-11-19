from server import Server


if __name__ == '__main__':
    def choose():
        choice = input(
            '''Are you sure you want to start the web server? : '''
        )
        if choice == 'y' or choice == 'yes':
            Server()
        if choice == 'n' or choice == 'no':
            exit()
        else:
            print('Invalid choice. Try again.')
            choose()
    choose()
