
# GS-Spy

GS-Spy is a Python script designed for logging activities of a group of targets on Discord. It provides the ability to log various events such as typing, message deletion, message edits, Spotify activity, game status, and custom status text for the specified targets. This project can be useful for monitoring and tracking specific user activities within a Discord server.

## Installation

To get started with GS-Spy, follow these steps:

1.  Clone the repository to your local machine:
    
    bashCopy code
    
    `https://github.com/GSstarGamer/GS-Spy.git` 
    
2.  Navigate to the project directory:
    
    bashCopy code
    
    `cd GS-Spy` 
    
3.  Install the required Python packages by running:
    
    bashCopy code
    
    `pip install -r requirements.txt` 
    

## Configuration

Before running the script, you need to configure your Discord bot token, webhook URL, and targets:

### Discord Bot Token

1.  Create a `.env` file in the project directory if it doesn't already exist.
    
2.  Open the `.env` file and add your Discord bot token in the following format:
    
    envCopy code
    
    `TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE` 
    

### Webhook and Targets

1.  Open the `config.json` file in the project directory.
    
2.  Set your webhook URL and target IDs. You can add multiple target IDs separated by commas if you want to monitor more than one person. Additionally, you can customize other options such as the command prefix and the initial enabled status:
    
    jsonCopy code
    
    ```json
    {
        "webhookURL": "YOUR_WEBHOOK_URL_HERE",
        "targets": ["TARGET_USER_ID_1", "TARGET_USER_ID_2"],
        "prefix": "!",
        "enabled": true
    }
    ```
    
    -   `webhookURL`: Replace with the URL of your Discord webhook.
    -   `targets`: Replace with the user IDs of the targets you want to log.
    -   `prefix`: Set the prefix for the command (default is "!").
    -   `enabled`: Set to `true` if you want the script to start logging automatically when run.

## Usage

To run the GS-Spy script, execute the following command in your terminal:

bashCopy code

`py main.py` 

Save to grepper

Once the script is running, it will begin logging activities of the specified targets. The primary command available is:

-   `!toggle`: This command toggles the logging status. When set to `false`, nothing will be logged.

## Contributing

If you would like to contribute to GS-Spy or report issues, please feel free to create a pull request or submit an issue on the [GitHub repository](https://github.com/GSstarGamer/GS-Spy).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/GSstarGamer/GS-Spy/blob/main/LICENSE) file for details.

----------

**Note**: Logging deleted messeges is **AGAINST** TOS ⚠️
