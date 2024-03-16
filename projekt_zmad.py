import csv
from math import floor


class Dataset:
    """
        Klasa zawiera atrybuty i metody
        potrzebne do realizacji projektu
    """

    def __init__(self):
        self.__headers = []
        self.__data = []
        self.__train = []
        self.__test = []
        self.__validate = []
        self.__slice = []
        self.__class_data = []

    def read_file(self, path: str, delim: str = ',', is_header: int = 0):
        """
        Funkcja odczytująca dane z pliku o podanej ścieżce.
        :param path: ścieżka do pliku
        :param delim: rozdzielnik w pliku csv
        :param is_header: parametr okreslający czy w pliku jest nagłówek. 1 - Tak,
        w przeciwnym wypadku brak nagłówków
        """
        if type(path) is str:
            try:
                with open(path, 'r', encoding='utf-8', newline='') as file_reader:
                    reader = csv.reader(file_reader, delimiter=delim)
                    self.__data = list(reader)
                if type(is_header) is int and is_header == 1 and len(self.__data):
                    self.__headers = self.__data[0]
                    self.__data = self.__data[1:]
                print("Udało się wczytać plik: '" + path + "'")
            except FileNotFoundError:
                print("Nie znaleziono pliku '" + path + "'")
            except PermissionError:
                print("Brak dostępu do pliku '" + path + "'")
            except OSError:
                print("Nie udało się otworzyć pliku '" + path + "'")
            except Exception as exc:
                print(f"Wystąpił błąd: {type(exc)}: {exc}")
        else:
            print("Nieprawidłowa ścieżka.")

    def save_data(self, path: str, data_list):
        """
        Funkcja zapisuje przekazane dane do pliku o podanej ścieżce.
        :param path: ścieżka do pliku
        :param data_list: dane do zapisania
        """
        try:
            with open(path, 'w', newline="") as file_writer:
                writer = csv.writer(file_writer)
                writer.writerows(*data_list)
            print("Poprawnie zapisano plik.\n")
        except PermissionError:
            print("Nie udało się zapisać pliku.'" + path + "' Brak dostępu.")
        except OSError:
            print("Nie udało się zapisać pliku '" + path + "'")
        except Exception as exc:
            print(f"Wystąpił błąd: {type(exc)}: {exc}")

    def save_question(self, input_string: str, yes_value: str, *data_list):
        """
            Funkcja pomocnicza. Pyta czy zapisać dane. Jeżeli odpowiedź brzmi yes_value, to
            zapisuje dane do pliku.
        :param input_string: Treść pytania o zapis pliku.
        :param yes_value: Odpowiedź wywołująca zapisanie pliku.
        :param data_list: dane do zapisu
        :return:
        """
        if input(input_string) == yes_value:
            filepath = input("Proszę podać nazwę pliku by zapisać.\n")
            self.save_data(filepath, data_list)

    def print_headers(self):
        """
        Funkcja wypisuje nagłówki wczytanych danych, o ile te zostały wczytane.
        """
        print(self.__headers) if len(self.__headers) else print('Brak nagłówków.')

    def dataset_slice(self, arg: list):
        """
        Funkcja wypisuje dane z wczytanego pliku na wzór konstrukcji 'slice'.
        :param arg: lista argumentów określających początek, koniec i krok wypisywanego zakresu.
        Brane pod uwagę są 0-3 argumenty, wszystkie kolejne są ignorowane.
        Jeżeli przynajmniej jeden argument wśród pierwszych trzech ma inny typ niż int, to
        komunikat o błędzie.
        Jeżeli krok == 0, to również komunikat o błędzie.
        """
        self.__slice = []
        if_ints = [1 if len(arg) >= i+1 and not type(arg[i]) is int else 0 for i in range(3)]
        # if_ints = [0 jeżeli arg[i] istnieje oraz jest intem, inaczej 0]
        # cel: do sprawdzania poprawności argumentów.
        params = [arg[i] if len(arg) >= i+1 else None for i in range(3)]
        # params = [arg[i] jeżeli arg[i] istnieje, inaczej None]
        # cel: aby potem wykorzystać konstrukcję slice(arg1, arg2, arg3)
        if sum(if_ints) > 0 or params[2] == 0:
            print("Podano niepoprawne argumenty.")
        else:
            self.__slice = [self.__headers] + self.__data[params[0]:params[1]:params[2]]
            print(*self.__slice, sep='\n')
            self.save_question("Czy zapisać wybrany wycinek? (Tak/Nie)\n", "Tak",  self.__slice)

    def divide_dataset(self, ratios: list):
        """
        Funkcja dzieląca zbiór danych na zbiory: testowy, treningowy oraz walidacyjny
        :param ratios: procentowe udziały danych w zbiorach treningowym i testowym.
                       Reszta - zbiór walidacyjny.
        :return:
        """
        self.__train = []
        self.__test = []
        self.__validate = []
        if len(self.__data) < 3:
            print("Wczytano zbyt mało danych aby móc je podzielić.")
        else:
            if len(ratios) >= 2 and type(ratios[0]) is int and type(ratios[1]) is int:
                if min(ratios[0], ratios[1]) <= 0 or ratios[0] + ratios[1] >= 100:
                    print("Podano niepoprawne argumenty.")
                else:
                    # treningowy = początkowy procent (ratios[0] % - po zaokrągleniu do całkowitych) zbioru danych
                    # testowy = kolejny procent (ratios [0] % -  po zaokrągleniu do całkowitych)
                    # reszta danych - zbiór walidacyjny
                    train_ratio = max(floor(ratios[0]*len(self.__data)/100), 1)
                    test_ratio = max(floor(ratios[1]*len(self.__data)/100), 1)
                    self.__train = self.__data[0:train_ratio + 1]
                    self.__test = self.__data[train_ratio+1:train_ratio + test_ratio + 1]
                    self.__validate = self.__data[train_ratio + test_ratio + 1:]
                    print("Udało się podzielić dane.")
                    self.save_question("Czy zapisać dane treningowe? (Tak/Nie)\n",
                                        "Tak", [self.__headers] + self.__train)
                    self.save_question("Czy zapisać dane testowe? (Tak/Nie)\n",
                                        "Tak", [self.__headers] + self.__test)
                    self.save_question("Czy zapisać dane walidacyjne? (Tak/Nie)\n",
                                        "Tak", [self.__validate] + self.__train)
            else:
                print("Podano niepoprawne argumenty.")

    def dec_classes(self):
        """
        Wartości i liczebności klas decyzyjnych
        Przy założeniu, że są w ostatniej kolumnie
        :return:
        """
        if self.__data:
            hd = len(self.__data[0]) - 1
            classes = [self.__data[i][hd] for i in range(len(self.__data))]
            set_classes = set(classes)
            return [(i, classes.count(i)) for i in set_classes]

    def data_for_given_class(self, class_value):
        """
        Funkcja wyświetla dane dla zadanej wartości klasy decyzyjnej.
        :param class_value:
        :return:
        """
        self.__class_data = []
        if self.__headers:
            self.__class_data += [self.__headers]
        if self.__data:
            hd = len(self.__data[0]) - 1
            self.__class_data += [i for i in self.__data if i[hd] == class_value]

    def str_to_int(self, string: str):
        """
        Funkcja pomocnicza. Jeżeli string jest intem to funkcja konwertuje go na inta
         w przeciwnym wypadku pozostawia go stringiem.
        :param string:
        :return: typ stringa, bez względu na to czy się zmienił czy nie.
        """
        try:
            string = int(string)
        finally:
            return string

    def main(self, path: str, delim: str = ',', is_header: int = 0):
        """
        Funkcja główna, pozwalająca używać zdefiniowanych w klasie funkcjonalności.
        :param path:
        :param delim:
        :param is_header:
        :return:
        """
        self.read_file(path, delim, is_header)
        while True:
            print("""\nCo chcesz zrobić? Wybierz odpowiednią opcję:
                1 - wypisanie nagłówków,
                2 - wypisanie danych z pliku,
                3 - wypisanie wycinka danych,
                4 - podział danych na zbiory: treningowy, testowy, walidacyjny,
                5 - wypisanie klas decyzyjnych (nazwa & liczność),
                6 - wypisanie danych zawierających daną klasę dezycyjną.""")
            function = input("Proszę wybrać opcję: \n")
            if function == "0":
                break
            elif function == "1":
                self.print_headers()
            elif function == "2":
                print(*([self.__headers] + self.__data), sep='\n')
            elif function == "3":
                params_slice = input("""Proszę podać 0-3 parametry całkowite (początek, koniec, krok).
                                    \r Brak parametrów = całość danych.\n""").strip().split(' ')
                params = [self.str_to_int(i) if i != '' else 0 for i in params_slice]
                self.dataset_slice(params)
            elif function == "4":
                params_divide = list(input("""Proszę podać 2 parametry naturalne o sumie mniejszej niż 100.
                                Pierwszy - % udział zbioru treningowego.
                                Drugi - % udział zbioru testowego.
                                Reszta - % udział zbioru walidacyjnego.\n""").split(' '))
                ratios = [self.str_to_int(i) for i in params_divide]
                self.divide_dataset(ratios)
            elif function == "5":
                print(self.dec_classes())
            elif function == "6":
                self.data_for_given_class(input("Proszę podać nazwę klasy decyzyjnej.\n"))
                if self.__class_data:
                    print(self.__class_data)
                    self.save_question("Czy zapisać dane? (Tak/Nie)\n", "Tak", self.__class_data)


if __name__ == "__main__":
    d = Dataset()
    d.main('iris.csv', ',', 1)
