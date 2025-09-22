import flet as ft
from db_connection import connect_db
import mysql.connector

def main(page: ft.Page):
    # Page setup
    page.title = "User Login"
    page.window_width = 400
    page.window_height = 350
    page.bgcolor = ft.Colors.AMBER_ACCENT
    page.window_frameless = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Title
    title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.CENTER
    )

    # Username field with person icon
    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=250,
        autofocus=True,
        bgcolor=ft.Colors.CYAN,
        text_style=ft.TextStyle(color=ft.Colors.BLACK)
    )
    username_row = ft.Row(
        controls=[
            ft.Icon(ft.Icons.PERSON, size=30, color=ft.Colors.BLACK),
            username_field
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    # Password field with PASSWORD icon
    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=250,
        password=True,
        can_reveal_password=True,
        bgcolor=ft.Colors.CYAN,
        text_style=ft.TextStyle(color=ft.Colors.BLACK)
    )
    password_row = ft.Row(
        controls=[
            ft.Icon(ft.Icons.PASSWORD, size=30, color=ft.Colors.BLACK),
            password_field
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    # Function to show dialogs
    def show_dialog(dialog):
        if dialog not in page.controls:       # Ensure the dialog is added to page
            page.controls.append(dialog)
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    # Dialogs
    success_dialog = ft.AlertDialog(
        title=ft.Text("Login Successful"),
        content=ft.Text("Welcome!", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(success_dialog))],
        modal=True
    )

    failure_dialog = ft.AlertDialog(
        title=ft.Text("Login Failed"),
        content=ft.Text("Invalid username or password", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(failure_dialog))],
        modal=True
    )

    invalid_input_dialog = ft.AlertDialog(
        title=ft.Text("Input Error"),
        content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(invalid_input_dialog))],
        modal=True
    )

    database_error_dialog = ft.AlertDialog(
        title=ft.Text("Database Error"),
        content=ft.Text("An error occurred while connecting to the database"),
        actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(database_error_dialog))],
        modal=True
    )

    # Login button logic
    def login_click(e):
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not username or not password:
            show_dialog(invalid_input_dialog)
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                show_dialog(success_dialog)
            else:
                show_dialog(failure_dialog)

        except mysql.connector.Error:
            show_dialog(database_error_dialog)

    # Login button
    login_btn = ft.ElevatedButton(
        text="Login",
        width=100,
        on_click=login_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.WHITE,
            color="#2596be"
        )
    )

    # Add controls to page
    page.add(
        title,
        ft.Column([username_row, password_row], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(login_btn, alignment=ft.alignment.top_right, margin=ft.Margin(0, 20, 40, 0))
    )

ft.app(target=main)
