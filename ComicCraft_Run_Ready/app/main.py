
import os
import json
import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()


# Project paths
BASE = Path(__file__).resolve().parent.parent

STATIC = BASE / "static"
EXPORTS = STATIC / "exports"
PANELS = STATIC / "panels"

EXPORTS.mkdir(parents=True, exist_ok=True)
PANELS.mkdir(parents=True, exist_ok=True)


# Create FastAPI application
app = FastAPI(
    title="ComicCraft - AI Comic Story Creator"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC)),
    name="static"
)


# Jinja2 templates
templates = Jinja2Templates(
    directory=str(BASE / "templates")
)


# --------------------------------------------------
# DEMO COMIC GENERATOR
# --------------------------------------------------

def make_demo_comic(
    prompt,
    character,
    setting,
    tone,
    art_style
):

    panels = []

    for i in range(1, 6):

        panel = {
            "number": i,

            "title": f"Panel {i}",

            "scene": (
                f"{character} explores {setting} "
                f"in a {tone} {art_style} adventure."
            ),

            "caption": (
                f"Scene {i}: "
                f"The story continues..."
            ),

            "narration": (
                f"{character} faces a new moment "
                f"in the story inspired by: {prompt}"
            ),

            "image_prompt": (
                f"{art_style} comic panel of "
                f"{character} in {setting}, "
                f"{tone} mood"
            )
        }

        panels.append(panel)

    return panels


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )


# --------------------------------------------------
# GENERATE COMIC
# --------------------------------------------------

@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    layout = make_demo_comic(
        story_prompt,
        character_name,
        setting,
        tone,
        art_style
    )

    panels_html = ""

    for panel in layout:
        panels_html += f"""
        <div class="panel">
            <h2>{panel["title"]}</h2>

            <div class="image-placeholder">
                🎨
                <br>
                <span>AI Illustration Placeholder</span>
            </div>

            <p><strong>Scene:</strong> {panel["scene"]}</p>

            <p><strong>Caption:</strong> {panel["caption"]}</p>

            <p><strong>Narration:</strong> {panel["narration"]}</p>

            <p><strong>Image Prompt:</strong> {panel["image_prompt"]}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>ComicCraft - Comic Preview</title>

        <link rel="stylesheet" href="/static/style.css">

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4efe8;
                color: #29231f;
                margin: 0;
                padding: 20px;
            }}

            .preview {{
                max-width: 850px;
                margin: 30px auto;
                padding: 30px;
                background: white;
                border-radius: 18px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }}

            .panel {{
                border: 2px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
            }}

            .image-placeholder {{
                height: 220px;
                background: #eeeeee;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                font-size: 45px;
                color: #777;
                text-align: center;
            }}

            .image-placeholder span {{
                font-size: 16px;
            }}

            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 14px 22px;
                background: #29231f;
                color: white;
                text-decoration: none;
                border-radius: 10px;
            }}

            .back {{
                display: block;
                margin-top: 20px;
            }}
        </style>
    </head>

    <body>

        <div class="preview">

            <h1>📖 Comic Preview</h1>

            <p>
                Your ComicCraft story has been generated successfully!
            </p>

            {panels_html}

            <a class="button" href="/export-success">
                📄 Download Your Comic as PDF
            </a>

            <a class="back" href="/">
                ← Create Another Comic
            </a>

        </div>

    </body>
    </html>
    """

    return HTMLResponse(content=html)

@app.get("/export-success")
async def export_success():

    pdf_path = EXPORTS / "ComicCraft_Comic.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.set_font("Arial", "B", 22)
    pdf.cell(0, 15, "ComicCraft - AI Comic Story", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", "", 14)
    pdf.multi_cell(
        0,
        10,
        "Your ComicCraft comic has been generated successfully."
    )

    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(
        0,
        8,
        "ComicCraft generated comic preview."
    )

    pdf.output(str(pdf_path))

    return FileResponse(
        path=str(pdf_path),
        filename="ComicCraft_Comic.pdf",
        media_type="application/pdf"
    )