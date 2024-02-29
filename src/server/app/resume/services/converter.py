import io
import os

import aiohttp
import docx
import docx2txt
from PyPDF2 import PdfReader

from core.exceptions import FileConverterServiceError


class FileConverterService:
    def __init__(self):
        self.converting_functions: dict = {
            'pdf': self._convert_pdf_to_text,
            'docx': self._convert_docx_to_text,
            'doc': self._convert_doc_to_text
        }

    async def convert_file(self, file_identifier):
        if self._is_url(file_identifier):
            return await self._convert_from_url(file_identifier)
        else:
            return await self._convert_from_local(file_identifier)

    async def _convert_conten_to_text(self, file_format, file_content) -> str:
        converting_function = self.converting_functions.get(file_format)
        if converting_function is None:
            raise FileConverterServiceError(f"Error unsupported file format to convert: {file_format}")

        return await converting_function(file_content)

    async def _convert_from_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_content = await response.read()
                file_format = await self._get_file_format(url)

                return await self._convert_conten_to_text(file_format, file_content)

    async def _convert_from_local(self, file_path):
        if not os.path.isfile(file_path):
            raise FileConverterServiceError("File for converting not found")

        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_format = await self._get_file_format(file_path)
            return await self._convert_conten_to_text(file_format, file_content)

    async def _convert_pdf_to_text(self, file_content):
        try:
            with io.BytesIO(file_content) as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
                return text
        except Exception as e:
            raise FileConverterServiceError(f"Error converting PDF to text: {str(e)}")

    async def _convert_docx_to_text(self, file_content):
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            for para in doc.paragraphs:
                text += para.text + '\n'
            return text
        except Exception as e:
            raise FileConverterServiceError(f"Error converting DOCX to text: {str(e)}")

    async def _convert_doc_to_text(self, file_content):
        try:
            text = docx2txt.process(io.BytesIO(file_content))
            return text
        except Exception as e:
            raise FileConverterServiceError(f"Error converting DOC to text: {str(e)}")

    # Utils
    def _is_url(self, file_identifier):
        return file_identifier.startswith('http')

    async def _get_file_format(self, filename: str):
        return filename.split('.')[-1]


async def convert_resume(file_path: str) -> str:
    converter = FileConverterService()
    return await converter.convert_file(file_path)
