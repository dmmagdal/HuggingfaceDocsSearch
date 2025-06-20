# downloader.py
# Download the documents from huggingface via the repo in huggingface datasets.
# Python 3.11
# Windows/MacOS/Linux


import os
import shutil
import zipfile

from huggingface_hub import list_repo_files, hf_hub_download


def main():
    # CONFIGURATION.
    repo_id = "hf-doc-build/doc-build"
    revision = "main"
    cache_dir = "hf_zips-tmp"
    output_dir = "huggingface_docs"

    # Make sure local directory exists.
    os.makedirs(output_dir, exist_ok=True)

    # 1. List all files in the repo.
    files = list_repo_files(
        repo_id, repo_type="dataset", revision=revision
    )

    # 2. Filter all paths ending in `main.zip`.
    main_zip_paths = [f for f in files if f.endswith("main.zip")]
    print(f"Found {len(main_zip_paths)} main.zip files.")

    # 3. Download each `main.zip` file.
    for zip_path in main_zip_paths:
        local_path = hf_hub_download(
            repo_id=repo_id,
            repo_type="dataset",
            revision=revision,
            filename=zip_path,
            local_dir=cache_dir,
            local_dir_use_symlinks=False  # Set to True if you're okay with symlinks
        )
        print(f"Downloaded: {zip_path} -> {local_path}")

    # 4. Remove .cache folder.
    shutil.rmtree(os.path.join(cache_dir, ".cache"))

    # 5. unzip all main.zip files.
    downloaded_zip_paths = sorted([
        os.path.join(cache_dir, zip_path) 
        for zip_path in main_zip_paths
    ])
    os.makedirs(output_dir, exist_ok=True)
    for zip_path in downloaded_zip_paths:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            print(f"✅ Unzipped: {zip_path} → {output_dir}")
        except zipfile.BadZipFile:
            print(f"❌ Failed to unzip (corrupt?): {zip_path}")
    
    # 6. Remove cache directory and all other superfluous files (i.e. 
    # non-English entries).
    shutil.rmtree(cache_dir)

    non_english_paths = list()
    modules = os.listdir(output_dir)
    for module in modules:
        module_path = os.path.join(output_dir, module, "main")
        non_english_paths.extend([
            os.path.join(module_path, language)
            for language in os.listdir(module_path)
            if language != "en"
        ])

    for path in non_english_paths:
        shutil.rmtree(path)

    print("Removed all non-english variants of the documentation.")

    # Exit the program.
    exit(0)


if __name__ == '__main__':
    main()