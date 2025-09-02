# Project Setup

This project requires Python 3.

To set up the project, follow these steps:

1. Download the installation script:
   ```bash
   wget https://raw.githubusercontent.com/your-repo/your-project/main/install.sh
   ```
   (Note: You'll need to replace `https://raw.githubusercontent.com/your-repo/your-project/main/install.sh` with the actual URL to your `install.sh` script.)

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