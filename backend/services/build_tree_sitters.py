# build_tree_sitter.py

from tree_sitter import Language
import os

# Output path for compiled library
LIB_PATH = "/home/shubhk/sentinal-ai/backend/build/my-languages.so"

# List of grammar repositories
LANGUAGES = [
    "/home/shubhk/sentinal-ai/backend/language-support/tree-sitter-javascript",
    "/home/shubhk/sentinal-ai/backend/language-support/tree-sitter-python",
]

# Make sure build dir exists
os.makedirs("build", exist_ok=True)

# Build the shared library
Language.build_library(
    LIB_PATH,
    LANGUAGES
)

print(f"✅ Tree-sitter shared library built at: {LIB_PATH}")
