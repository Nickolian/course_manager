from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from .models import Group


def add_to_group(product, user):
    groups = Group.objects.filter(product=product).annotate(num_students=Count("students")).order_by("num_students")
    # groups_info = ", ".join([f"{group.title}: {group.num_students} students" for group in groups])

    need_new_group = False

    if groups:
        smallest_group = groups[0]
        total_groups = len(groups)
        if can_rebuild_groups(product):
            students = get_students(product)
            if user not in students:
                students.append(user)
            rebuild_groups(groups, students)
            return "Students in groups were reassembled."

        else:
            if smallest_group.num_students < product.max_students:
                if user not in smallest_group.students.all():
                    smallest_group.students.add(user)
                    return f"User added to {smallest_group.title}"
                else:
                    return "You already subscribed"
            else:
                need_new_group = True

    else:
        need_new_group = True

    if need_new_group:
        title = f"Group {total_groups + 1}" if groups else "Group 1"
        new_group = Group.objects.create(title=title, product=product)
        new_group.students.add(user)
        return f"New group created {new_group.title}\nUser added to {new_group.title}"
    else:
        return f"Cannot create new group!"


def can_rebuild_groups(product):
    return timezone.now() < product.start_date


def get_students(product):
    students = User.objects.filter(groups__product=product).distinct()
    return list(students)


def rebuild_groups(groups, students):
    for group in groups:
        group.students.clear()

    for index, student in enumerate(students):
        group = groups[index % len(groups)]
        group.students.add(student)
