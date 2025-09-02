# Project Setup

This project requires Python 3.

To set up the project, follow these steps:

1. Download and extract the latest release:
   ```bash
   wget https://github.com/gaashvik/sentinal-ai/archive/refs/tags/v1.0.3.tar.gz
   tar -xzf v1.0.3.tar.gz
   cd NeoCLI-1.0.3 # Adjust directory name if different
   ```

2. Run the installation script:
   ```bash
   source install.sh
   ```

The `install.sh` script will perform the following actions:
- Create a Python virtual environment.
- Install necessary Python dependencies from `requirements.txt`.
- Prompt you to enter the following API keys and paths:
  - HuggingFace API Key
  - Gemini API Key
  - GitHub App Token
  - GitHub Installation Token
  - GitHub Private Key Path
- Add a source line for `neocli.sh` to your `~/.bashrc` file.

After running `source install.sh`, the changes to your `.bashrc` will be applied in new terminal sessions.
