# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
#
# Image Service – ATRA (Photorealistic Flat-Lay Edition v4.2 – Compatibility Fix)

import base64
import os
import random
from datetime import datetime
from io import BytesIO

import requests
from openai import OpenAI
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageStat

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Image model version (upgrade target)
IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1.5")
IMAGE_EDIT_MODEL = os.getenv("OPENAI_IMAGE_EDIT_MODEL", IMAGE_MODEL)
USE_IMAGE_EDIT = os.getenv("ATRA_USE_IMAGE_EDIT", "1").strip() not in {"0", "false", "False"}

# Exact Cloudinary cover asset
JOURNAL_COVER_URL = "https://res.cloudinary.com/dssvwcrqh/image/upload/v1754278923/1_pobsxq.jpg"
COVER_CACHE_PATH = "output/_journal_cover_cache.png"

DAY_ITEMS = {
    "monday": "iced coffee, laptop corner, work badge, receipts, tangled charger cable, sticky notes, highlighter cap",
    "tuesday": "iced coffee, highlighters, headphones, tote bag corner, sticky notes, open planner page, marker smudge",
    "wednesday": "water bottle, pens, keys, clean notepad sheet, lip balm, hand cream tube, crumpled sticky note",
    "thursday": "beer bottle or beer can (subtle), keys, earbuds, scattered receipts, coasters, bottle opener, napkin",
    "friday": "cocktail glass with garnish, lipstick, jewelry tray, sunglasses, camera, hair clip, glittery receipt",
    "saturday": "cocktail glass, makeup items, film camera, snack wrapper, tote bag, earrings, half-open compact",
    "sunday": "iced coffee, cozy candle, soft blanket texture, gentle clutter, to-do list scrap, TV remote, pen cap",
}

EXTRA_CHAOS_ITEMS = [
    "crumpled receipt",
    "random business card",
    "post-it with messy handwriting",
    "loose bobby pins",
    "ring or bracelet",
    "opened gum or mint pack",
    "USB cable",
    "phone face down",
    "small perfume roller",
    "chapstick cap",
    "tea bag wrapper",
    "takeout sauce packet",
    "ticket stub",
    "tampon wrapper (subtle, not gross)",
    "mini hand sanitizer",
]

MOOD_OBJECTS = {
    "corporate_burnout": """
        Items: laptop corner, dried highlighter, work badge, cold coffee,
        half-used sticky notes. Lighting: warm desk-lamp cinematic glow.
    """,
    "adhd_spiral": """
        Items: tangled earbuds, scattered pens, lipstick half open,
        slightly chaotic key placement. Lighting: energetic but warm.
    """,
    "delusional_romantic": """
        Items: soft lipstick, flower petal, warm coffee, heart doodle.
        Lighting: dreamy warm highlights.
    """,
    "existentially_exhausted": """
        Items: water bottle, minimal clutter, clean pen, blank note.
        Lighting: soft cool-but-warm-balanced cinematics.
    """,
    "sunday_scaries": """
        Items: iced coffee, crumpled receipt, keys, tote bag corner.
        Lighting: warm side lighting, slight vignette.
    """
}


def _get_day_items() -> str:
    day = datetime.now().strftime("%A").lower()
    base_items = DAY_ITEMS.get(day, DAY_ITEMS["monday"])
    extras = ", ".join(random.sample(EXTRA_CHAOS_ITEMS, k=5))
    return f"{base_items}, {extras}"


def _load_cover_asset() -> Image.Image:
    """
    Retrieve the canonical journal cover image from Cloudinary.
    Cached locally to avoid repeated downloads.
    """
    try:
        os.makedirs("output", exist_ok=True)

        if os.path.isfile(COVER_CACHE_PATH):
            return Image.open(COVER_CACHE_PATH).convert("RGBA")

        response = requests.get(JOURNAL_COVER_URL, timeout=20)
        response.raise_for_status()
        cover_image = Image.open(BytesIO(response.content)).convert("RGBA")
        cover_image.save(COVER_CACHE_PATH, format="PNG")
        return cover_image
    except Exception as exc:
        raise RuntimeError(f"Failed to load canonical journal cover: {exc}") from exc


def _place_cover_on_image(base: Image.Image, cover: Image.Image) -> Image.Image:
    """
    Integrate the canonical cover onto the generated flat-lay so it reads as
    the actual printed cover (matched size + lighting), not a pasted sticker.
    """
    base_rgba = base.convert("RGBA")

    # This must match the prompt instructions for notebook size/position.
    target_width = int(base_rgba.width * 0.35)
    aspect_ratio = cover.height / cover.width
    target_height = int(target_width * aspect_ratio)
    cover_resized = cover.resize((target_width, target_height), Image.LANCZOS)

    def _apply_matte_finish(cover_rgba: Image.Image) -> Image.Image:
        cover_rgb = cover_rgba.convert("RGB")
        cover_rgb = ImageEnhance.Color(cover_rgb).enhance(0.92)
        cover_rgb = ImageEnhance.Contrast(cover_rgb).enhance(0.96)
        cover_rgb = ImageEnhance.Brightness(cover_rgb).enhance(0.98)
        cover_rgb = cover_rgb.filter(ImageFilter.GaussianBlur(radius=0.25))

        noise = Image.effect_noise(cover_rgb.size, 8).convert("L")
        noise_rgb = Image.merge("RGB", (noise, noise, noise))
        cover_rgb = Image.blend(cover_rgb, noise_rgb, alpha=0.03)

        return cover_rgb.convert("RGBA")

    def _match_lighting(cover_rgba: Image.Image, under_rgb: Image.Image) -> Image.Image:
        """
        Use the luminance of the underlying notebook area as a soft shading map
        so the cover inherits the same light falloff/shadows as the "book".
        """
        under_l = under_rgb.convert("L")
        under_l = ImageEnhance.Contrast(under_l).enhance(1.15)
        under_l = under_l.filter(ImageFilter.GaussianBlur(radius=max(2, target_width // 180)))

        mean = ImageStat.Stat(under_l).mean[0] or 128.0
        normalized = under_l.point(lambda p: int(max(0, min(255, (p * 128.0) / mean))))

        # Convert normalized luminance into a multiplier map for ImageChops.multiply.
        # 180..255 ~= 0.70..1.00 multiplier range.
        shading = normalized.point(lambda p: int(180 + (p / 255.0) * 75))
        shading_rgb = Image.merge("RGB", (shading, shading, shading))

        cover_rgb = cover_rgba.convert("RGB")
        lit_rgb = ImageChops.multiply(cover_rgb, shading_rgb)
        return lit_rgb.convert("RGBA")

    # The cover footprint should match the notebook exactly (no padding)
    cover_resized = _apply_matte_finish(cover_resized)
    book_w, book_h = cover_resized.size

    x = (base_rgba.width - book_w) // 2
    y = (base_rgba.height - book_h) // 2

    under_region = base_rgba.convert("RGB").crop((x, y, x + book_w, y + book_h))
    cover_lit = _match_lighting(cover_resized, under_region)

    # Slight edge feathering so the cover prints "into" the notebook surface.
    feather_radius = max(1, target_width // 220)
    alpha = Image.new("L", (book_w, book_h), 255).filter(ImageFilter.GaussianBlur(radius=feather_radius))
    cover_lit.putalpha(alpha)

    base_rgba.paste(cover_lit, (x, y), cover_lit)
    return base_rgba.convert("RGB")


def _create_center_cover_mask(canvas_size: tuple[int, int], cover_aspect_ratio: float) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """
    Create a mask for the centered notebook cover region.

    Mask format: RGBA PNG where transparent pixels are the editable region.
    Returns (mask_image, (x0,y0,x1,y1)).
    """
    width, height = canvas_size
    target_width = int(width * 0.35)
    target_height = int(target_width * cover_aspect_ratio)
    x0 = (width - target_width) // 2
    y0 = (height - target_height) // 2
    x1 = x0 + target_width
    y1 = y0 + target_height

    mask = Image.new("RGBA", (width, height), (0, 0, 0, 255))  # keep everything by default
    draw = ImageDraw.Draw(mask)
    corner_radius = max(8, target_width // 28)
    draw.rounded_rectangle((x0, y0, x1, y1), radius=corner_radius, fill=(0, 0, 0, 0))  # edit region
    return mask, (x0, y0, x1, y1)


def _edit_in_cover(base_image: Image.Image, cover_image: Image.Image, mode: str, day_items: str) -> Image.Image:
    """
    Use the OpenAI image edit endpoint to apply the cover naturally (lighting/texture)
    into the notebook area, instead of a hard pixel overlay.
    """
    os.makedirs("output", exist_ok=True)
    base_path = "output/_base_flatlay.png"
    mask_path = "output/_mask.png"
    cover_path = "output/_cover.png"

    base_image.convert("RGBA").save(base_path, format="PNG")
    cover_image.convert("RGBA").save(cover_path, format="PNG")

    cover_aspect_ratio = cover_image.height / cover_image.width
    mask, _ = _create_center_cover_mask(base_image.size, cover_aspect_ratio)
    mask.save(mask_path, format="PNG")

    edit_prompt = f"""
    You are editing a photorealistic top-down flat-lay photo.

    Goal: replace ONLY the masked notebook cover area with the provided cover artwork image.
    - The artwork MUST be placed with NO resizing mismatch: it must perfectly fill the notebook cover.
    - Preserve the same angle/perspective (aligned to frame), and match lighting/shadows/reflections so it looks printed.
    - Apply a subtle matte paperback print finish (slightly reduced glare, realistic paper texture).
    - Do NOT change anything outside the mask.

    Context (do not add new objects here, preserve the scene):
    - Mood: {mode}
    - Surrounding clutter: {day_items}
    """

    with open(base_path, "rb") as base_f, open(cover_path, "rb") as cover_f, open(mask_path, "rb") as mask_f:
        try:
            # Prefer passing both the base image and the cover image as inputs so the model can
            # directly reference the exact artwork while editing the masked region.
            result = client.images.edit(
                model=IMAGE_EDIT_MODEL,
                image=[base_f, cover_f],
                mask=mask_f,
                prompt=edit_prompt.strip(),
                size="1024x1024",
                n=1,
            )
        except Exception as exc:
            # Fallback: some backends only accept a single input image for edits.
            print(f"⚠️ images.edit with 2 images failed; retrying with base only. Error: {exc}")
            base_f.seek(0)
            mask_f.seek(0)
            result = client.images.edit(
                model=IMAGE_EDIT_MODEL,
                image=base_f,
                mask=mask_f,
                prompt=edit_prompt.strip() + f"\n\nThe cover artwork reference is at: {JOURNAL_COVER_URL}",
                size="1024x1024",
                n=1,
            )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    return Image.open(BytesIO(image_bytes)).convert("RGB")


def generate_image(prompt: str, mode: str) -> str:
    print(f"🎨 Generating grounded flat-lay Joanie image ({mode}) – prompt: {prompt}")

    mood_influence = MOOD_OBJECTS.get(mode, "")
    day_items = _get_day_items()

    # ----------------------------------------------------------
    # PROMPT-BASED GROUNDING (since reference-image parameter is unsupported)
    # ----------------------------------------------------------
    visual_prompt = f"""
    Create a *photorealistic editorial-quality flat-lay photograph* shot perfectly from above.
    Warm, cinematic, textured, lived-in chaos — but not depressing.

    ## NOTEBOOK (COVER WILL BE APPLIED VIA IMAGE EDIT)
    - A physical matte-black paperback notebook centered in frame.
    - The notebook cover is BLANK (no text, no art, no logo).
    - Notebook occupies ~35% of image width and is perfectly aligned to the frame (no rotation).
    - Full notebook visible, no cropping, nothing on top of it.
    - Natural shadows/reflections and paper thickness visible.

    ## REQUIRED OBJECTS
    - A pen beside the journal.
    - Everyday clutter items for the day of week:
      {day_items}
    - Increase clutter density: MANY small objects, slightly overlapping, messy but photogenic.
    - Some items can be partially cropped by the frame edges for a more chaotic look.

    ## SURFACE & LIGHTING
    - Dark wood desk with visible grain.
    - Cinematic directional warm lighting, defined shadows.

    ## STYLE
    - 100% camera-real. No illustrations, digital UI, or stickers.
    - Preserve wood grain, metal shine, paper texture.

    ## MOOD INFLUENCE
    {mood_influence}

    Respond ONLY with the generated image.
    """

    # ----------------------------------------------------------
    # Image generation (NO image= parameter — fully compatible)
    # ----------------------------------------------------------
    try:
        result = client.images.generate(
            model=IMAGE_MODEL,
            prompt=visual_prompt,
            size="1024x1024",
            n=1,
        )
    except Exception as exc:
        if IMAGE_MODEL != "gpt-image-1":
            print(f"⚠️ Image generation failed with {IMAGE_MODEL}; falling back to gpt-image-1. Error: {exc}")
            result = client.images.generate(
                model="gpt-image-1",
                prompt=visual_prompt,
                size="1024x1024",
                n=1,
            )
        else:
            raise

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")

    cover_image = _load_cover_asset()
    if USE_IMAGE_EDIT:
        try:
            print("🧩 Applying cover via OpenAI image edit (mask-based) for natural integration.")
            pil_image = _edit_in_cover(pil_image, cover_image, mode=mode, day_items=day_items)
        except Exception as exc:
            print(f"⚠️ Image edit integration failed; falling back to local overlay. Error: {exc}")
            print("📚 Overlaying canonical journal cover onto generated frame.")
            pil_image = _place_cover_on_image(pil_image, cover_image)
    else:
        print("📚 Overlaying canonical journal cover onto generated frame.")
        pil_image = _place_cover_on_image(pil_image, cover_image)

    os.makedirs("output", exist_ok=True)
    path = "output/generated_image.jpg"

    pil_image.save(
        path,
        format="JPEG",
        quality=90,
        subsampling=0,
        optimize=True,
    )

    print(f"✅ Grounded image generated at: {path}")
    return path
