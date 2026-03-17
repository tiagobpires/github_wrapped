from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
BASE_IMAGE_PATH = IMAGES_DIR / "github_wrapped_base.png"


def get_total_stars(repositories):
    return sum(repo.stars for repo in repositories)


def get_most_used_language(repositories):
    languages = []

    for repo in repositories:
        if repo.language != "Unknown":
            languages.append(repo.language)

    if not languages:
        return "Unknown"

    language_counter = Counter(languages)
    return language_counter.most_common(1)[0][0]


def get_top_repositories(repositories, limit=3):
    sorted_repositories = sorted(
        repositories, key=lambda repo: repo.stars, reverse=True
    )
    return sorted_repositories[:limit]


def _truncate_text(text, max_chars):
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def _draw_centered_text(draw, text, font, fill, center_x, y):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text((center_x - text_width / 2, y), text, font=font, fill=fill)


def _get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def generate_wrapped_image(user, total_stars, most_used_language, top_repositories):
    image = Image.open(BASE_IMAGE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(image)

    color_text = "#111B4D"
    username_font = _get_font(48)
    name_font = _get_font(56)
    bio_font = _get_font(40)
    card_font = _get_font(52)
    repo_font = _get_font(46)
    repo_description_font = _get_font(28)
    star_font = _get_font(40)

    username = f"@{user.login}"
    name = user.name

    max_chars_por_linha = 45
    bio = _truncate_text(user.bio, max_chars_por_linha * 2)
    bio_line_1 = bio[:max_chars_por_linha].strip()
    bio_line_2 = bio[max_chars_por_linha:].strip()
    language = _truncate_text(most_used_language, 18)

    _draw_centered_text(draw, username, username_font, color_text, center_x=540, y=225)
    _draw_centered_text(draw, name, name_font, color_text, center_x=540, y=540)
    _draw_centered_text(draw, bio_line_1, bio_font, color_text, center_x=540, y=635)
    if bio_line_2:
        _draw_centered_text(draw, bio_line_2, bio_font, color_text, center_x=540, y=685)

    _draw_centered_text(
        draw, str(user.followers), card_font, color_text, center_x=340, y=835
    )
    _draw_centered_text(
        draw, str(user.public_repos), card_font, color_text, center_x=805, y=835
    )
    _draw_centered_text(draw, language, card_font, color_text, center_x=375, y=1050)
    _draw_centered_text(
        draw, str(total_stars), card_font, color_text, center_x=810, y=1050
    )

    row_y_positions = [1340, 1511, 1690]
    for index, y in enumerate(row_y_positions):
        if index < len(top_repositories):
            repo = top_repositories[index]
            repo_name = _truncate_text(repo.name, max_chars=30)
            repo_description = _truncate_text(repo.description or "", max_chars=55)

            draw.text((250, y), repo_name, font=repo_font, fill=color_text)
            draw.text(
                (250, y + 62),
                repo_description,
                font=repo_description_font,
                fill=color_text,
            )
            draw.text((895, y), str(repo.stars), font=star_font, fill=color_text)

    IMAGES_DIR.mkdir(exist_ok=True)
    output_path = IMAGES_DIR / f"github_wrapped_{user.login}.png"
    image.save(output_path)
    return str(output_path)
