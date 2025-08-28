import google_calendar
import settings
import pytz
from datetime import datetime, timedelta
from inky import InkyPHAT
from font_fredoka_one import FredokaOne
from PIL import Image, ImageDraw, ImageFont


def main():
    display = InkyPHAT("black")

    events = google_calendar.get_todays_events()

    image = Image.new(mode="RGB", size=display.resolution, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    chikarego_font = ImageFont.truetype("ChiKareGo.ttf", 16)
    leco_font = ImageFont.truetype("leco.ttf", 16)

    date_title = datetime.strftime(datetime.now(), "%A %d %B")
    draw.text((0, 0), date_title, display.BLACK, font=chikarego_font)

    starting_event_y_coords = 30
    max_summary_character_length = 23
    for event in events:
        event_time, event_summary = event
        # Draw the event time
        draw.text(
            (0, starting_event_y_coords),
            f"{event_time}:",
            display.BLACK,
            font=chikarego_font,
        )

        # Draw the event summary
        if len(event_summary) > max_summary_character_length:
            event_summary = event_summary[:max_summary_character_length] + "..."
        draw.text(
            (50, starting_event_y_coords),
            event_summary,
            display.BLACK,
            font=chikarego_font,
        )

        starting_event_y_coords += 20

    display.set_image(image)
    display.show()


if __name__ == "__main__":
    main()
