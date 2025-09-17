# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600

    db_conn = init_db()

    # --- Original input fields ---
    name_input = ft.TextField(label="Name", width=350)
    phone_input = ft.TextField(label="Phone", width=350)
    email_input = ft.TextField(label="Email", width=350)
    inputs = (name_input, phone_input, email_input)

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn)
    )

    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    # --- Extras: search field and dark mode ---
    search_input = ft.TextField(
        label="Search",
        width=250,
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, search_input.value)
    )

    theme_switch = ft.Switch(label="Dark Mode")

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT
        page.update()

    theme_switch.on_change = toggle_theme

    # --- Layout ---
    page.add(
        ft.Column(
            [
                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(),
                # Row with "Contacts" label, search field, and dark mode switch
                ft.Row(
                    [
                        ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=1),
                        search_input,
                        theme_switch,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                contacts_list_view,
            ]
        )
    )

    # --- Initial display ---
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)