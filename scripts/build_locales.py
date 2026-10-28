"""Build uk/pl Django locale catalogs without system gettext."""

from __future__ import annotations

from pathlib import Path

from babel.messages.catalog import Catalog
from babel.messages.mofile import write_mo
from babel.messages.pofile import write_po

ROOT = Path(__file__).resolve().parents[1]
LOCALE = ROOT / "locale"

TRANSLATIONS = {
    "uk": {
        "Language": "Мова",
        "Theme": "Тема",
        "Light": "Світла",
        "Dark": "Темна",
        "Open menu": "Відкрити меню",
        "Menu": "Меню",
        "Sign in": "Увійти",
        "Sign out": "Вийти",
        "Close": "Закрити",
        "Collapse sidebar": "Згорнути меню",
        "Expand sidebar": "Розгорнути меню",
        "Signed in as": "Ви увійшли як",
        "Workspace": "Робочий простір",
        "Catalog": "Каталог",
        "Manage": "Керування",
        "Dashboard": "Дашборд",
        "Tasks": "Задачі",
        "My tasks": "Мої задачі",
        "Projects": "Проєкти",
        "Teams": "Команди",
        "Workers": "Працівники",
        "Tags": "Теги",
        "Task types": "Типи задач",
        "Admin": "Адмін",
        "Create team": "Створити команду",
        "Create tag": "Створити тег",
        "Create type": "Створити тип",
        "Complex work. Clear rhythm.": "Складна робота. Зрозумілий ритм.",
        "Sign in to plan, assign and finish work with your team.": (
            "Увійдіть, щоб планувати, призначати та завершувати роботу з командою."
        ),
        "Could not sign in. Check your username and password, then try again.": (
            "Не вдалося увійти. Перевірте ім’я користувача та пароль і спробуйте ще раз."
        ),
        "Username": "Ім’я користувача",
        "Password": "Пароль",
        "Demo:": "Демо:",
        "One place for people, projects and the next step in your work.": (
            "Одне місце для людей, проєктів і наступного кроку у вашій роботі."
        ),
        "New task": "Нова задача",
        "Your workload": "Ваше навантаження",
        "Open tasks": "Відкриті задачі",
        "Completed": "Завершені",
        "View open": "Переглянути відкриті",
        "View done": "Переглянути завершені",
        "Browse, filter and prioritize team work.": (
            "Переглядайте, фільтруйте та пріоритезуйте роботу команди."
        ),
        "Status filters": "Фільтри статусу",
        "All": "Усі",
        "Open": "Відкриті",
        "Done": "Готово",
        "Filter": "Фільтр",
        "Work assigned to you — next steps first.": (
            "Робота, призначена вам — спочатку наступні кроки."
        ),
        "Name": "Назва",
        "Project": "Проєкт",
        "Type": "Тип",
        "Priority": "Пріоритет",
        "Deadline": "Термін",
        "Status": "Статус",
        "No deadline": "Без терміну",
        "No tasks here yet": "Тут ще немає задач",
        "Create the first task to get the team moving — or adjust filters.": (
            "Створіть першу задачу, щоб запустити роботу команди — або змініть фільтри."
        ),
        "Edit": "Редагувати",
        "Delete": "Видалити",
        "Mark open": "Позначити відкритою",
        "Mark done": "Позначити готовою",
        "Creator": "Автор",
        "Team": "Команда",
        "Assignees": "Виконавці",
        "Description": "Опис",
        "Nobody assigned": "Нікого не призначено",
        "Task form": "Форма задачі",
        "Edit task": "Редагувати задачу",
        "Update details and keep ownership clear.": (
            "Оновіть деталі та залиште відповідальність зрозумілою."
        ),
        "Capture the next step so the team can move.": (
            "Зафіксуйте наступний крок, щоб команда могла рухатися далі."
        ),
        "Save": "Зберегти",
        "Cancel": "Скасувати",
        "Delete task": "Видалити задачу",
        "This action cannot be undone.": "Цю дію неможливо скасувати.",
        "Delete <strong>%(name)s</strong>? You will not be able to restore it.": (
            "Видалити <strong>%(name)s</strong>? Відновити буде неможливо."
        ),
        "Initiatives owned by teams.": "Ініціативи, якими володіють команди.",
        "New project": "Новий проєкт",
        "No projects yet": "Проєктів ще немає",
        "Create a project to group related tasks.": (
            "Створіть проєкт, щоб згрупувати пов’язані задачі."
        ),
        "Team:": "Команда:",
        "Project form": "Форма проєкту",
        "Edit project": "Редагувати проєкт",
        "Define the space where related work lives.": (
            "Визначте простір, де живе пов’язана робота."
        ),
        "Groups collaborating on projects.": (
            "Групи, що співпрацюють над проєктами."
        ),
        "New team": "Нова команда",
        "Members": "Учасники",
        "No teams yet": "Команд ще немає",
        "Create a team to start organizing people and projects.": (
            "Створіть команду, щоб почати організовувати людей і проєкти."
        ),
        "No members yet": "Учасників ще немає",
        "Team form": "Форма команди",
        "Edit team": "Редагувати команду",
        "Bring people together around shared work.": (
            "Об’єднайте людей навколо спільної роботи."
        ),
        "People across positions and teams.": (
            "Люди за посадами та командами."
        ),
        "Search": "Пошук",
        "Position": "Посада",
        "No workers found": "Працівників не знайдено",
        "Try another username or clear the search.": (
            "Спробуйте інше ім’я користувача або очистіть пошук."
        ),
        "No full name": "Немає повного імені",
        "No position": "Немає посади",
        "Not in any team": "Не входить до жодної команди",
        "No open tasks": "Немає відкритих задач",
        "No completed tasks": "Немає завершених задач",
        "Labels used across tasks.": "Мітки, що використовуються в задачах.",
        "New tag": "Новий тег",
        "No tags yet": "Тегів ще немає",
        "Create a tag so the team can label related work.": (
            "Створіть тег, щоб команда могла позначати пов’язану роботу."
        ),
        "Tag form": "Форма тега",
        "Add a label the team can reuse on tasks.": (
            "Додайте мітку, яку команда зможе повторно використовувати."
        ),
        "Categories for planning and reporting.": (
            "Категорії для планування та звітності."
        ),
        "New type": "Новий тип",
        "No task types yet": "Типів задач ще немає",
        "Create types so planning stays consistent across teams.": (
            "Створіть типи, щоб планування залишалося узгодженим між командами."
        ),
        "Task type form": "Форма типу задачі",
        "New task type": "Новий тип задачі",
        "Define a category the team can plan against.": (
            "Визначте категорію, за якою команда зможе планувати."
        ),
        "Page navigation": "Навігація сторінками",
        "Previous": "Назад",
        "Next": "Далі",
        "Page %(page)s of %(pages)s": "Сторінка %(page)s з %(pages)s",
        "Urgent": "Терміновий",
        "High": "Високий",
        "Medium": "Середній",
        "Low": "Низький",
        "name": "назва",
        "description": "опис",
        "deadline": "термін",
        "completed": "завершено",
        "priority": "пріоритет",
        "task type": "тип задачі",
        "task types": "типи задач",
        "project": "проєкт",
        "creator": "автор",
        "assignees": "виконавці",
        "tags": "теги",
        "task": "задача",
        "tasks": "задачі",
        "team": "команда",
        "teams": "команди",
        "members": "учасники",
        "projects": "проєкти",
        "position": "посада",
        "positions": "посади",
        "worker": "працівник",
        "workers": "працівники",
        "tag": "тег",
        "New tags": "Нові теги",
        "Comma-separated new tags (e.g. python-refactoring)": (
            "Нові теги через кому (напр. python-refactoring)"
        ),
        "Invalid tags: %(tags)s. Use lowercase letters, digits and hyphens only.": (
            "Некоректні теги: %(tags)s. Лише малі літери, цифри та дефіси."
        ),
        "You cannot create tasks in this project.": (
            "Ви не можете створювати задачі в цьому проєкті."
        ),
        "Search by name": "Пошук за назвою",
        "All statuses": "Усі статуси",
        "All priorities": "Усі пріоритети",
        "All projects": "Усі проєкти",
        "All tags": "Усі теги",
        "All teams": "Усі команди",
        "You cannot manage projects for this team.": (
            "Ви не можете керувати проєктами цієї команди."
        ),
        "Search by username": "Пошук за ім’ям користувача",
        "Use lowercase letters, digits and hyphens only.": (
            "Використовуйте лише малі літери, цифри та дефіси."
        ),
    },
    "pl": {
        "Language": "Język",
        "Theme": "Motyw",
        "Light": "Jasny",
        "Dark": "Ciemny",
        "Open menu": "Otwórz menu",
        "Menu": "Menu",
        "Sign in": "Zaloguj się",
        "Sign out": "Wyloguj się",
        "Close": "Zamknij",
        "Collapse sidebar": "Zwiń menu",
        "Expand sidebar": "Rozwiń menu",
        "Signed in as": "Zalogowano jako",
        "Workspace": "Przestrzeń robocza",
        "Catalog": "Katalog",
        "Manage": "Zarządzanie",
        "Dashboard": "Pulpit",
        "Tasks": "Zadania",
        "My tasks": "Moje zadania",
        "Projects": "Projekty",
        "Teams": "Zespoły",
        "Workers": "Pracownicy",
        "Tags": "Tagi",
        "Task types": "Typy zadań",
        "Admin": "Admin",
        "Create team": "Utwórz zespół",
        "Create tag": "Utwórz tag",
        "Create type": "Utwórz typ",
        "Complex work. Clear rhythm.": "Złożona praca. Jasny rytm.",
        "Sign in to plan, assign and finish work with your team.": (
            "Zaloguj się, aby planować, przydzielać i kończyć pracę z zespołem."
        ),
        "Could not sign in. Check your username and password, then try again.": (
            "Nie udało się zalogować. Sprawdź nazwę użytkownika i hasło, a następnie spróbuj ponownie."
        ),
        "Username": "Nazwa użytkownika",
        "Password": "Hasło",
        "Demo:": "Demo:",
        "One place for people, projects and the next step in your work.": (
            "Jedno miejsce na ludzi, projekty i kolejny krok w Twojej pracy."
        ),
        "New task": "Nowe zadanie",
        "Your workload": "Twoje obciążenie",
        "Open tasks": "Otwarte zadania",
        "Completed": "Ukończone",
        "View open": "Zobacz otwarte",
        "View done": "Zobacz ukończone",
        "Browse, filter and prioritize team work.": (
            "Przeglądaj, filtruj i ustalaj priorytety pracy zespołu."
        ),
        "Status filters": "Filtry statusu",
        "All": "Wszystkie",
        "Open": "Otwarte",
        "Done": "Gotowe",
        "Filter": "Filtruj",
        "Work assigned to you — next steps first.": (
            "Praca przypisana do Ciebie — najpierw kolejne kroki."
        ),
        "Name": "Nazwa",
        "Project": "Projekt",
        "Type": "Typ",
        "Priority": "Priorytet",
        "Deadline": "Termin",
        "Status": "Status",
        "No deadline": "Brak terminu",
        "No tasks here yet": "Nie ma tu jeszcze zadań",
        "Create the first task to get the team moving — or adjust filters.": (
            "Utwórz pierwsze zadanie, aby ruszyć pracę zespołu — albo zmień filtry."
        ),
        "Edit": "Edytuj",
        "Delete": "Usuń",
        "Mark open": "Oznacz jako otwarte",
        "Mark done": "Oznacz jako gotowe",
        "Creator": "Autor",
        "Team": "Zespół",
        "Assignees": "Wykonawcy",
        "Description": "Opis",
        "Nobody assigned": "Nikt nieprzypisany",
        "Task form": "Formularz zadania",
        "Edit task": "Edytuj zadanie",
        "Update details and keep ownership clear.": (
            "Zaktualizuj szczegóły i utrzymaj jasną odpowiedzialność."
        ),
        "Capture the next step so the team can move.": (
            "Zapisz kolejny krok, aby zespół mógł iść dalej."
        ),
        "Save": "Zapisz",
        "Cancel": "Anuluj",
        "Delete task": "Usuń zadanie",
        "This action cannot be undone.": "Tej czynności nie można cofnąć.",
        "Delete <strong>%(name)s</strong>? You will not be able to restore it.": (
            "Usunąć <strong>%(name)s</strong>? Nie będzie można tego przywrócić."
        ),
        "Initiatives owned by teams.": "Inicjatywy należące do zespołów.",
        "New project": "Nowy projekt",
        "No projects yet": "Nie ma jeszcze projektów",
        "Create a project to group related tasks.": (
            "Utwórz projekt, aby pogrupować powiązane zadania."
        ),
        "Team:": "Zespół:",
        "Project form": "Formularz projektu",
        "Edit project": "Edytuj projekt",
        "Define the space where related work lives.": (
            "Zdefiniuj przestrzeń, w której żyje powiązana praca."
        ),
        "Groups collaborating on projects.": (
            "Grupy współpracujące przy projektach."
        ),
        "New team": "Nowy zespół",
        "Members": "Członkowie",
        "No teams yet": "Nie ma jeszcze zespołów",
        "Create a team to start organizing people and projects.": (
            "Utwórz zespół, aby zacząć organizować ludzi i projekty."
        ),
        "No members yet": "Nie ma jeszcze członków",
        "Team form": "Formularz zespołu",
        "Edit team": "Edytuj zespół",
        "Bring people together around shared work.": (
            "Połącz ludzi wokół wspólnej pracy."
        ),
        "People across positions and teams.": (
            "Ludzie na stanowiskach i w zespołach."
        ),
        "Search": "Szukaj",
        "Position": "Stanowisko",
        "No workers found": "Nie znaleziono pracowników",
        "Try another username or clear the search.": (
            "Spróbuj innej nazwy użytkownika albo wyczyść wyszukiwanie."
        ),
        "No full name": "Brak pełnego imienia i nazwiska",
        "No position": "Brak stanowiska",
        "Not in any team": "Nie należy do żadnego zespołu",
        "No open tasks": "Brak otwartych zadań",
        "No completed tasks": "Brak ukończonych zadań",
        "Labels used across tasks.": "Etykiety używane w zadaniach.",
        "New tag": "Nowy tag",
        "No tags yet": "Nie ma jeszcze tagów",
        "Create a tag so the team can label related work.": (
            "Utwórz tag, aby zespół mógł oznaczać powiązaną pracę."
        ),
        "Tag form": "Formularz tagu",
        "Add a label the team can reuse on tasks.": (
            "Dodaj etykietę, którą zespół może ponownie używać w zadaniach."
        ),
        "Categories for planning and reporting.": (
            "Kategorie do planowania i raportowania."
        ),
        "New type": "Nowy typ",
        "No task types yet": "Nie ma jeszcze typów zadań",
        "Create types so planning stays consistent across teams.": (
            "Utwórz typy, aby planowanie było spójne między zespołami."
        ),
        "Task type form": "Formularz typu zadania",
        "New task type": "Nowy typ zadania",
        "Define a category the team can plan against.": (
            "Zdefiniuj kategorię, względem której zespół może planować."
        ),
        "Page navigation": "Nawigacja stron",
        "Previous": "Poprzednia",
        "Next": "Następna",
        "Page %(page)s of %(pages)s": "Strona %(page)s z %(pages)s",
        "Urgent": "Pilny",
        "High": "Wysoki",
        "Medium": "Średni",
        "Low": "Niski",
        "name": "nazwa",
        "description": "opis",
        "deadline": "termin",
        "completed": "ukończone",
        "priority": "priorytet",
        "task type": "typ zadania",
        "task types": "typy zadań",
        "project": "projekt",
        "creator": "autor",
        "assignees": "wykonawcy",
        "tags": "tagi",
        "task": "zadanie",
        "tasks": "zadania",
        "team": "zespół",
        "teams": "zespoły",
        "members": "członkowie",
        "projects": "projekty",
        "position": "stanowisko",
        "positions": "stanowiska",
        "worker": "pracownik",
        "workers": "pracownicy",
        "tag": "tag",
        "New tags": "Nowe tagi",
        "Comma-separated new tags (e.g. python-refactoring)": (
            "Nowe tagi oddzielone przecinkami (np. python-refactoring)"
        ),
        "Invalid tags: %(tags)s. Use lowercase letters, digits and hyphens only.": (
            "Nieprawidłowe tagi: %(tags)s. Używaj tylko małych liter, cyfr i myślników."
        ),
        "You cannot create tasks in this project.": (
            "Nie możesz tworzyć zadań w tym projekcie."
        ),
        "Search by name": "Szukaj po nazwie",
        "All statuses": "Wszystkie statusy",
        "All priorities": "Wszystkie priorytety",
        "All projects": "Wszystkie projekty",
        "All tags": "Wszystkie tagi",
        "All teams": "Wszystkie zespoły",
        "You cannot manage projects for this team.": (
            "Nie możesz zarządzać projektami tego zespołu."
        ),
        "Search by username": "Szukaj po nazwie użytkownika",
        "Use lowercase letters, digits and hyphens only.": (
            "Używaj tylko małych liter, cyfr i myślników."
        ),
    },
}


def build_locale(lang: str, mapping: dict[str, str]) -> None:
    catalog = Catalog(locale=lang, domain="django", fuzzy=False)
    for msgid, msgstr in mapping.items():
        catalog.add(msgid, msgstr)

    out_dir = LOCALE / lang / "LC_MESSAGES"
    out_dir.mkdir(parents=True, exist_ok=True)
    po_path = out_dir / "django.po"
    mo_path = out_dir / "django.mo"
    with po_path.open("wb") as fh:
        write_po(fh, catalog, width=88)
    with mo_path.open("wb") as fh:
        write_mo(fh, catalog)
    print(f"Wrote {po_path.relative_to(ROOT)} and {mo_path.name}")


def main() -> None:
    for lang, mapping in TRANSLATIONS.items():
        build_locale(lang, mapping)


if __name__ == "__main__":
    main()
