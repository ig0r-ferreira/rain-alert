import smtplib
from email.mime.text import MIMEText
from typing import Any, Optional

import requests
from dotenv import dotenv_values

ENV_VARS: dict[str, Optional[str]] = dotenv_values()


def get_data_from_api() -> dict[str, Any]:
    weather_params: dict[str, str | float] = {
        "lat": float(ENV_VARS["LAT"]),
        "lon": float(ENV_VARS["LON"]),
        "appid": ENV_VARS["API_KEY"]
    }
    response = requests.get(url=ENV_VARS["API_URL"], params=weather_params)
    response.raise_for_status()

    return response.json()


def send_email() -> None:
    with smtplib.SMTP(
        ENV_VARS["SMTP_SERVER_ADDRESS"], int(ENV_VARS["SMTP_SERVER_PORT"])
    ) as server:
        server.starttls()
        server.login(ENV_VARS["EMAIL_USERNAME"], ENV_VARS["EMAIL_PASSWORD"])

        msg = MIMEText("It's going to rain today, take an umbrella. ☔")
        msg["From"] = ENV_VARS["SENDER_EMAIL"]
        msg["To"] = ENV_VARS["RECIPIENT_EMAILS"]
        msg["Subject"] = "Rain alert 🌧️"

        server.sendmail(
            from_addr=ENV_VARS["SENDER_EMAIL"],
            to_addrs=ENV_VARS["RECIPIENT_EMAILS"].split(","),
            msg=msg.as_string()
        )


def main() -> None:
    data = get_data_from_api()
    will_rain = any(
        int(info["weather"][0]["id"]) < 600 for info in data["list"][:4]
    )

    if will_rain:
        send_email()


if __name__ == "__main__":
    main()
