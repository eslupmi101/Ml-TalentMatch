
import os
import asyncio

from dotenv import find_dotenv, load_dotenv
from client.templates import template
from io import BytesIO

import reflex as rx
import requests

load_dotenv(find_dotenv())

HOST_WITH_SCHEMA = os.getenv('HOST_WITH_SCHEMA')


class FormInputState(rx.State):
    # Table
    score: str
    resume_id: str
    first_name: str
    last_name: str
    middle_name: str
    birth_date: str
    birth_date_year_only: str
    country: str
    city: str
    about: str
    key_skills: str
    salary_expectations_amount: str
    salary_expectations_currency: str
    photo_path: str
    gender: str
    language: str
    resume_name: str
    source_link: str
    contactItems: str
    educationItems: str
    experienceItems: str
    languageItems: str
    # ==============

    result: str
    uploading: bool = False
    progress: int = 0
    total_bytes: int = 0
    api_key: str
    waiting_result: str = ""
    waiting_color: str = "black"
    good_result: dict = {}
    answer: str

    async def handle_upload(
        self,
        files: list[rx.UploadFile]
    ):
        file = files[-1]
        # Отправляем запрос на бэкэнд при загрузке файла
        self.waiting_result = "Ожидаем ответ от AI"
        self.waiting_color = "blue"
        asyncio.create_task(self.send_request_to_backend(file))

    async def send_request_to_backend(self, file):
        #  Формируем URL для отправки запроса на бэкэнд
        backend_url = f"{HOST_WITH_SCHEMA}:8001/api/v1/resumes/"

        await file.seek(0)
        file_content = await file.read()

        # Формируем данные для отправки вместе с файлом
        files = {"file": (file.filename, BytesIO(file_content), file.content_type)}
        data = {"api_key": self.api_key}

        # Отправляем POST-запрос на бэкэнд
        try:
            response = requests.post(backend_url, files=files, data=data)
        except Exception as e:
            self.answer = "Ответ"
            self.waiting_result = "Ошибка"
            self.waiting_color = "red"
            self.result = f"Ошибка {response.status_code} при отправке файла на сервер. {e}"
            
        # Проверяем код ответа
        if response.status_code == 201:
            self.result = str(response.json()['resume'])
            self.answer = "Ответ"
            self.waiting_result = "Ответ получен"
            self.waiting_color = "green"
            self.score = str(response.json()['score'])

            # Table
            for key, value in response.json()['resume'].items():
                setattr(self, key, str(value))

        else:
            self.answer = "Ответ"
            self.waiting_result = "Ошибка"
            self.waiting_color = "red"
            self.result = f"Ошибка {response.status_code} при отправке файла на сервер. {str(response.text)}"

        self.uploading = False
        self.progress = 0
        self.total_bytes = 0

    def handle_upload_progress(self, progress: dict):
        self.uploading = True
        self.progress = round(progress["progress"] * 100)
        if self.progress >= 100:
            self.uploading = False

    def cancel_upload(self):
        self.uploading = False

        return rx.cancel_upload("upload3")


@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """

    # Render initial UI with instructions
    return rx.chakra.vstack(
        rx.heading(
            "AI ResParse парсинг резюме",
            font_size="3em",
            margin_top="3em",
            margin_bottom="1em",
        ),

        rx.text(
            FormInputState.waiting_result,
            color=FormInputState.waiting_color,
            font_size="2em",
        ),

        rx.chakra.vstack(
            rx.chakra.text(
                "Token",
                font_size="2em"
            ),
            rx.input(
                placeholder="Введите token ChatGPT",
                value=FormInputState.api_key,
                type="password",
                on_change=FormInputState.set_api_key,
                width="700px",
                height="50px",
                required=True
            ),
            rx.chakra.text(
                "Загрузите одно резюме в форматах pdf, doc, docx",
                font_size="2em"
            ),
            rx.upload(
                rx.text(
                    "Перетащите файл сюда или нажмите, чтобы выбрать файл"
                ),
                id="upload3",
                border="2px dotted rgb(107,99,246)",
                padding="3em",
                required=True
            ),
            rx.vstack(
                rx.foreach(
                    rx.selected_files("upload3"), rx.text
                )
            ),
            rx.cond(
                ~FormInputState.uploading,
                rx.button(
                    "Отправить",
                    on_click=FormInputState.handle_upload(
                        rx.upload_files(
                            upload_id="upload3",
                            on_upload_progress=FormInputState.handle_upload_progress,
                        ),
                    ),
                    size="3"
                ),
                rx.button(
                    "Cancel",
                    on_click=FormInputState.cancel_upload,
                ),
            ),
            align="center",
        ),
        rx.divider(width="100%"),

        rx.heading(
            FormInputState.answer,
            font_size="3em",
            padding="1em",
            margin_top="1em",
            margin_bottom="1em",
        ),

        rx.table.root(
            rx.table.body(
                rx.table.row(
                    rx.table.row_header_cell("score"),
                    rx.table.cell(FormInputState.score),
                ),
                rx.table.row(
                    rx.table.row_header_cell("resume_id"),
                    rx.table.cell(FormInputState.resume_id),
                ),
                rx.table.row(
                    rx.table.row_header_cell("first_name"),
                    rx.table.cell(FormInputState.first_name),
                ),
                rx.table.row(
                    rx.table.row_header_cell("middle_name"),
                    rx.table.cell(FormInputState.middle_name),
                ),
                rx.table.row(
                    rx.table.row_header_cell("birth_date"),
                    rx.table.cell(FormInputState.birth_date),
                ),
                rx.table.row(
                    rx.table.row_header_cell("birth_date_year_only"),
                    rx.table.cell(FormInputState.birth_date_year_only),
                ),
                rx.table.row(
                    rx.table.row_header_cell("country"),
                    rx.table.cell(FormInputState.country),
                ),
                rx.table.row(
                    rx.table.row_header_cell("city"),
                    rx.table.cell(FormInputState.city),
                ),
                rx.table.row(
                    rx.table.row_header_cell("about"),
                    rx.table.cell(FormInputState.about),
                ),
                rx.table.row(
                    rx.table.row_header_cell("key_skills"),
                    rx.table.cell(FormInputState.key_skills),
                ),
                rx.table.row(
                    rx.table.row_header_cell("salary_expectations_amount"),
                    rx.table.cell(FormInputState.salary_expectations_amount),
                ),
                rx.table.row(
                    rx.table.row_header_cell("salary_expectations_currency"),
                    rx.table.cell(FormInputState.salary_expectations_currency),
                ),
                rx.table.row(
                    rx.table.row_header_cell("photo_path"),
                    rx.table.cell(FormInputState.photo_path),
                ),
                rx.table.row(
                    rx.table.row_header_cell("gender"),
                    rx.table.cell(FormInputState.gender),
                ),
                rx.table.row(
                    rx.table.row_header_cell("language"),
                    rx.table.cell(FormInputState.language),
                ),
                rx.table.row(
                    rx.table.row_header_cell("resume_name"),
                    rx.table.cell(FormInputState.resume_name),
                ),
                rx.table.row(
                    rx.table.row_header_cell("source_link"),
                    rx.table.cell(FormInputState.source_link),
                ),
                rx.table.row(
                    rx.table.row_header_cell("contactItems"),
                    rx.table.cell(FormInputState.contactItems),
                ),
                rx.table.row(
                    rx.table.row_header_cell("educationItems"),
                    rx.table.cell(FormInputState.educationItems),
                ),
                rx.table.row(
                    rx.table.row_header_cell("languageItems"),
                    rx.table.cell(FormInputState.languageItems),
                ),
            ),
            align="center",
        ),
        rx.text(
            FormInputState.result,
            width="100%",
        ),

    )
