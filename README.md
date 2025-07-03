# report-vtb

A Python project for generating and managing reports with VTB integration.

## Features

- Secure environment variable management
- Integration with external APIs (e.g., Discord, Google)
- Automated report generation
- Configurable via `.env` file

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/report-vtb.git
   cd report-vtb
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```
   BUCKET_NAME=""            # Name of the cloud storage bucket for save daily or monthly transactions
   ICB_PUBLIC_KEY=""         # Public key for encryption or API authentication (multi-line, keep \n for line breaks)
   BASE_URL=""               # Base URL for the VTB API or service
   USER_NAME=""              # Username (Phonenumber) for authentication with the VTB service
   PASSWORD=""               # Password for authentication (keep this secure)
   CARD_NUMBER=""            # Card number or identifier used for report generation
   DISCORD_WEBHOOK_URL=""    # Discord webhook URL for sending notifications (error , etc... )
   GG_CREDS_PATH=""          # Path to Google credentials JSON file for Google API integration
   ```

### Usage

Run the main script:

```sh
python main.py
```

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
