import random
import string
from random import randint, shuffle
import pandas as pd


class PasswordManager:

    def __init__(self, name, master_pw):
        self.__passwords = pd.DataFrame(columns=["Username", "Password"])
        self.__name = name
        self.__master_pw = master_pw

    @staticmethod
    def __password_specs(length=14, min_spec=0, max_spec=0, min_num=0, min_upper=0):
        num_sc = randint(min_spec, min(length - min_num - min_upper, max_spec))
        num_num = randint(min_num, length - num_sc - min_upper)
        num_upper = randint(min_upper, length - num_sc - num_num)
        num_lower = length - (num_sc + num_num + num_upper)
        return [num_sc, num_num, num_upper, num_lower]

    def __password_gen(self, criteria=None, length=14, spec_char="@!&", repeat=True, min_spec=0, max_spec=0, min_num=0, min_upper=0):
        if criteria is not None:
            return self.__password_gen(length=criteria.get("length", length),
                                       spec_char=criteria.get("spec_char", spec_char),
                                       repeat=criteria.get("repeat", repeat),
                                       min_spec=criteria.get("min_spec", min_spec),
                                       max_spec=criteria.get("max_spec", max_spec),
                                       min_num=criteria.get("min_num", min_num),
                                       min_upper=criteria.get("min_upper", min_upper))
        if max_spec < min_spec:
            max_spec = min_spec
        required = sum([min_spec, min_num, min_upper])
        if required <= length and (repeat or len(spec_char) >= min_spec):
            specs = self.__password_specs(length, min_spec, max_spec, min_num, min_upper)
            if repeat:
                password = random.choices(string.ascii_lowercase, k=specs[3]) + random.choices(string.ascii_uppercase, k=specs[2]) + random.choices(string.digits, k=specs[1]) + random.choices(spec_char, k=specs[0])
            else:
                while specs[0] > len(spec_char) or specs[1] > len(string.digits) or specs[2] > len(string.ascii_uppercase) or specs[3] > len(string.ascii_lowercase):
                    specs = self.__password_specs(length, min_spec, max_spec, min_num, min_upper)
                password = random.sample(string.ascii_lowercase, k=specs[3]) + random.sample(string.ascii_uppercase, k=specs[2]) + random.sample(string.digits, k=specs[1]) + random.sample(spec_char, k=specs[0])
            shuffle(password)
            return "".join(password)

    def add_password(self, site, username, criteria=None):
        if site not in self.__passwords.index:
            if (password := self.__password_gen(criteria)) is not None:
                self.__passwords = self.__passwords.append(pd.DataFrame([[username, password]], columns=["Username", "Password"], index=[site]))
            else:
                print("Invalid specifications.")

    def validate(self, mp):
        return mp == self.__master_pw

    def change_password(self, site, master_pass, new_pass=None, criteria=None):
        if not self.validate(master_pass):
            print("Incorrect password.")
            return False
        if site not in self.__passwords.index:
            print("Site does not exist.")
            return False
        if (password := self.__password_gen(criteria) if new_pass is None else new_pass) is None:
            print("Invalid specifications.")
            return False
        self.__passwords.at[site, "Password"] = password

    def remove_site(self, site):
        if site in self.__passwords.index:
            self.__passwords.drop(site, inplace=True)

    def get_site_info(self, site):
        if site in self.__passwords.index:
            return self.__passwords.loc[site].values

    def get_name(self):
        return self.__name

    def get_site_list(self):
        return self.__passwords.index.values

    def __str__(self):
        return "\n".join(["Sites stored for username:", *self.get_site_list()])
