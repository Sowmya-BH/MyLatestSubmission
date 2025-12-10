from crewai.tools.base_tool import BaseTool

from pydantic import BaseModel, Field
from typing import Type

import subprocess
import json

import shutil # Required for moving the file
from pathlib import Path

from typing import Dict, Any, List
import pymupdf as fitz
import os
from agentops.sdk.decorators import tool


class DoclingToolInput(BaseModel):
    pdf_file_name: str = Field(..., description="Path of the PDF file")
    # output_dir: str = Field(..., description="The desired absolute directory path where the resulting JSON file should be saved.")

# @tool("Docling")
class DoclingTool(BaseTool):
    name: str = "Docling"
    description: str = "Tool used to parse input PDF file and convert it into a JSON file"
    args_schema: Type[BaseModel] = DoclingToolInput

    def _run(self, pdf_file_name: str) -> str:
        """Uses Docling to process a PDF file and convert it to a JSON file."""
        try:
            cmd = f"docling --to json --force-ocr {pdf_file_name}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                # temp_json_file = os.path.splitext(pdf_file_name)[0] + ".json"

                # 3. Calculate the final destination path
                # final_json_file_name = Path(pdf_file_name).stem + ".json"
                # final_json_path = Path(output_dir) / final_json_file_name
                #
                # # 4. Move the file to the final destination directory
                # shutil.move(temp_json_file, final_json_path)
                #
                # print("Document processed successfully! Output moved to:", str(final_json_path))
                # return str(final_json_path)

                json_file = os.path.splitext(pdf_file_name)[0] + ".json"
                print("Document processed successfully! Output saved to file:", json_file)
                return json_file
            else:
                return f"Error processing document: {result.stderr}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"
