import datetime
import logging
import time
import pytz
import aiohttp
from aiogram import html


# Define global text variables
ERROR_MESSAGE = f"⚠️ {html.bold('щось не так з сервером')}\nприйдеться виходити на балкон дивитися погоду"
FEELS_LIKE_EMOJI = html.code("\U0001faac")


# A funcion to get a response from API
async def make_async_request(url):
    # Get the start time
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        # Try getting the URL
        try:
            async with session.get(url) as response:
                # Get the end time
                end_time = time.time()

                # Print the execution time
                execution_time = end_time - start_time
                logging.info(f"Execution time: {execution_time} seconds")

                # Check the response status
                # If it's 200 -> return json
                if response.status == 200:
                    response_json = await response.json()
                    return response_json

                # Else return None
                else:
                    logging.error(f"Received non-200 response: {response.status}")
                    return None

        # If there is an exception -> log it and return None
        except Exception as e:
            logging.error(f"An error occurred during the request: {e}")
            return None


async def weather_now(
    API_KEY,
    lat=49.8252088,
    lon=24.0780526,  # Lviv LNU Dorm 3 coordinates
):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang=uk&units=metric"  # OWM endpoint
    response = await make_async_request(url)

    # If response is not None - proceed
    if not response:
        logging.error("Something is wrong with the weather_now response.")
        return ERROR_MESSAGE

    weather_text = (
        f"{html.bold('погода зараз:')}\n"
        f"🌡 {round(response['main']['temp'])}°C ({FEELS_LIKE_EMOJI} {round(response['main']['feels_like'])}°C), {response['weather'][0]['description']}"
    )

    return weather_text


# A weather forecast for the day
async def weather_forecast(
    API_KEY,
    lat=49.8252088,
    lon=24.0780526,  # Lviv LNU Dorm 3 coordinates
):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&lang=uk&units=metric"  # OWM endpoint
    response = await make_async_request(url)

    # Catching response errors
    if not response:
        logging.error("Something is wrong with the weather_now response.")
        return ERROR_MESSAGE

    # Get the data for only today
    today_list = response["list"][:8]

    # Initialize a forecast string and get "feels like" emoji
    forecast_string = html.bold("прогноз на сьогодні:\n")

    # For each forecast
    for i, forecast in enumerate(today_list):
        # Get the time from the 'dt_text' property
        time_str = forecast["dt_txt"][11:16]

        # Convert it to time object
        dt = datetime.datetime.strptime(time_str, "%H:%M").time()

        kyiv_timezone = pytz.timezone("Europe/Kiev")
        localized_time = datetime.datetime.now(kyiv_timezone).time()

        # If the time is greater than current -> add to the forecast
        if dt > localized_time:
            # Add an icon
            forecast_string += "🔸🔹"[i % 2]

            # Round the temperature
            temp = round(forecast["main"]["temp"])

            # Description
            description = forecast["weather"][0]["description"]

            # Round the "feels like" temperature
            feels_like = round(forecast["main"]["feels_like"])

            # Create a forecast entry
            txt = f"{html.bold(time_str)}: {temp}°C ({FEELS_LIKE_EMOJI} {feels_like}°C), {description}\n"
            forecast_string += txt

    if forecast_string == html.bold("прогноз на сьогодні:\n"):
        forecast_string += "🙄 нема вже шо прогрозувати, ви час бачили? до завтра!!"

    return forecast_string
