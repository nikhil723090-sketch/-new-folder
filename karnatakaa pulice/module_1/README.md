# Generative AI-Based Cloud Removal for LISS-IV Imagery

This project builds a preprocessing and deep learning workflow for removing clouds
from LISS-IV satellite imagery.

My assigned work is the preprocessing stage:

1. Create cloud and shadow masks
2. Register cloudy images, masks, and cloud-free reference images
3. Extract aligned training patches
4. Normalize the dataset for model training

## Folder Structure

```text
NEW FOLDER/
  data/
    raw/
      cloudy/
      cloudfree/
    masks/
    registered/
    patches/
    normalized/

  preprocessing/
    create_masks.py
    register_images.py
    registert_images.py
    extract_patches.py
    normalize_data.py
    io.py
    masks.py
    preview.py
    register.py

  models/
  training/
  inference/
  evaluation/
  dashboard/
  result/

  requirements.txt
  README.md
```

## Where To Put Dataset Files

Put cloudy LISS-IV images here:

```text
data/raw/cloudy/
```

Put matching cloud-free/reference images here:

```text
data/raw/cloudfree/
```

Recommended image format:

```text
.tif or .tiff GeoTIFF files
```

## Install Libraries

Run this from the main project folder:

```bash
pip install -r requirements.txt
```

## Step 1: Create Cloud Masks

```bash
python preprocessing/create_masks.py --input-dir data/raw/cloudy --output-dir data/masks --preview-dir result/mask_previews
```

Output:

```text
data/masks/
result/mask_previews/
```

Mask values:

```text
0   = clear area
1   = cloud
2   = cloud shadow
255 = nodata
```

## Step 2: Register Images

Replace `scene_001.tif` with your actual cloud-free reference image name.

```bash
python preprocessing/register_images.py --reference data/raw/cloudfree/scene_001.tif --input-dir data/raw/cloudy --mask-dir data/masks --output-dir data/registered
```

Output:

```text
data/registered/images/
data/registered/masks/
```

## Step 3: Extract Patches

```bash
python preprocessing/extract_patches.py --cloudy-dir data/registered/images --target-dir data/raw/cloudfree --mask-dir data/registered/masks --output-dir data/patches --patch-size 256 --stride 128
```

Output:

```text
data/patches/
```

Each patch contains:

```text
cloudy image patch
cloud-free target patch
cloud mask patch
CRS and transform metadata
```

## Step 4: Normalize Data

```bash
python preprocessing/normalize_data.py --patch-dir data/patches --output-dir data/normalized --stats-json result/normalization_stats.json
```

Output:

```text
data/normalized/
result/normalization_stats.json
```

## My Contribution Summary

The preprocessing module prepares LISS-IV imagery for cloud removal model training.
It produces cloud masks, aligns images to a common grid, extracts training-ready
patches, and normalizes the dataset using reusable statistics.

## SCRB Conversational AI Platform - Module 1

The first module for the Karnataka SCRB conversational AI platform is available
in `crime_database/`.

It includes:

- PostgreSQL/PostGIS schema
- MySQL schema
- structured `crime_records` table
- sample seed records
- SQLAlchemy model, validation schema, and repository helpers

See `crime_database/README.md` for setup and usage.

## SCRB Conversational AI Platform - Module 2

The AI chatbot module is available in `karnatakaa pulice/module_2_ai_chatbot/`.

It converts investigator questions into safe SQL, runs them against the
`crime_records` table, and returns human-readable answers. It supports an
offline rule-based planner and optional OpenAI, Gemini, or Ollama SQL generation.

## SCRB Conversational AI Platform - Modules 3 to 5

The next modules are also available in `karnatakaa pulice/`:

- `module_3_context_chat/` remembers previous chat turns and resolves follow-up
  questions.
- `module_4_voice_support/` adds speech-to-text and text-to-speech support.
- `module_5_crime_pattern_detection/` uses pandas, Matplotlib, and Plotly for
  crime pattern analytics and Power BI-ready CSV outputs.
