from PasswordManager import *


def main():
    pm = PasswordManager("Student", "FINAL")
    pm.add_password("www.gmail.com", "a_student")
    pm.add_password("www.wm.edu", "WMStudent", criteria={"max_spec": 2, "min_upper": 2})
    pm.change_password("www.gmail.com", "FINAL", "update1235")
    pm.get_site_info("www.wm.edu")
    print(pm)


if __name__ == "__main__":
    main()
