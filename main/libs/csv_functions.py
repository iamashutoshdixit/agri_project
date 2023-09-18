from users.models import User


def csv_handler(f):
    for row in f.readlines():
        entry = row.decode().strip().split(",")
        username, password, first_name, last_name, is_staff = entry
        is_staff = True if is_staff.lower() == "true" else False
        User.objects.create(
            username=username,
            password=password,
            is_staff=is_staff,
        )
