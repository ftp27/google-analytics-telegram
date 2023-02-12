## Google Analytics to Telegram Bot

This app retrieves data from Google Analytics and sends it to a Telegram chat. This is mainly an example of how to work with Google Analytics. It is better to be customised for production use.

### Prerequisites

Before you start, you'll need the following:

- A Google Analytics account and access to a Google Analytics property. [Docs](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries#python)
- A Telegram bot, with the bot token [@BotFather](https://telegram.me/BotFather)
- A Telegram chat ID for the chat where you want to receive the Google Analytics data

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/ftp27/google-analytics-telegram.git
```

Navigate to the project directory:

```bash
cd google-analytics-telegram
```

Create a virtual environment and activate it:

```bash
python -m venv env
source env/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `config.yml` file in the `data` directory of the project, and enter the following details:

```yaml
server:
  host: 127.0.0.1 # Server host
  port: 8080 # Server port
analytics:
  property_id: <your_google_analytics_view_id>
telegram:
  token: <your_telegram_bot_token>
  chat_id: <your_telegram_chat_id>
propertirs:
  - 
    title: <property_title_for_a_message>
    dimension: <dimension_id>
    limit: <result_limit>
    endpoint: <enpoint for the server>
  - # Example
    title: 'Popular categories'
    dimension: 'category_name'
    limit: 15
    endpoint: 'top_categories'
```

Create a service account for your Google Analytics property and download the private key file in JSON format. Rename the file to service_account.json and place it in the `data` directory of the project.

### Usage

Activate the virtual environment:

```bash
source env/bin/activate
```

Run the script:

```bash
python app.py
```

The script will retrieve data from Google Analytics and send it to the Telegram chat. The data is sent once per day.

### Docker Usage

This project can also be run in a Docker container.

Build the Docker image:

```bash
docker build -t google-analytics-telegram .
```

Run a container from the image:

```bash
docker run -p 8080:8080 -v ./data:/app/data google-analytics-telegram
```

The container will run in the background and send data from Google Analytics to the Telegram chat once per day.

### Docker Compose Usage

You can also use Docker Compose to manage the container.

Create a docker-compose.yml file with the following contents:

```yaml
version: '3'
services:
  google-analytics-telegram:
    build: .
    volumes:
      - ./data:/app/data
```

Run the container using Docker Compose:

```bash
docker-compose up -d
```

This will run the container in the background, and mount the config.yml and service_account.json files as volumes.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.