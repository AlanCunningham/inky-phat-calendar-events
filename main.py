import google_calendar
import settings
import pytz
from datetime import datetime, timedelta
from inky import InkyPHAT
from font_fredoka_one import FredokaOne
from PIL import Image, ImageDraw, ImageFont


def main():
    display = InkyPHAT("black")
    width = 212
    height = 104

    display.set_border(display.WHITE)

    image = Image.new(mode="RGB", size=display.resolution, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    chikarego_font = ImageFont.truetype("ChiKareGo.ttf", 16)

    now = datetime.now()
    day_of_week = datetime.strftime(now, "%A")
    day_of_month = datetime.strftime(now, "%d")

    # Remove zero-padding from day of month
    if day_of_month[0] == "0":
        day_of_month = day_of_month[1]

    # Add suffix to day of month
    if 4 <= int(day_of_month) <= 20 or 24 <= int(day_of_month) <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][int(day_of_month) % 10 - 1]

    # Draw a margin below the date
    draw.line((0, 15, width, 15), fill=5)

    month = datetime.strftime(now, "%B")
    date_title = f"{day_of_week} {day_of_month}{suffix} {month}"
    draw.text((0, 0), date_title, display.BLACK, font=chikarego_font)

    try:
        all_day_events, timed_events = google_calendar.get_todays_events()
    except Exception as exc:
        print(exc)
        draw.text(
            (width / 2, height / 2),
            "Token has expired",
            display.BLACK,
            anchor="mm",
            font=chikarego_font,
        )
        display.set_image(image)
        display.show()
        return

    if all_day_events or timed_events:
        starting_event_y_coords = 25
        max_summary_character_length = 26
        gap_between_events = 17

        # All day events
        for event in all_day_events:
            draw.text(
                (0, starting_event_y_coords),
                event,
                display.BLACK,
                font=chikarego_font,
            )
            starting_event_y_coords += gap_between_events

        # Timed events
        # Add a slight buffer from the all day events
        starting_event_y_coords += 3
        for event in timed_events:
            event_time, event_summary = event
            # Draw the event time
            draw.text(
                (0, starting_event_y_coords),
                f"{event_time}",
                display.BLACK,
                font=chikarego_font,
            )

            # Draw the event summary
            if len(event_summary) > max_summary_character_length:
                event_summary = event_summary[:max_summary_character_length] + "..."
            draw.text(
                (40, starting_event_y_coords),
                event_summary,
                display.BLACK,
                font=chikarego_font,
            )

            starting_event_y_coords += gap_between_events
    else:
        # No events
        draw.text(
            (width / 2, height / 2),
            "No events today",
            display.BLACK,
            anchor="mm",
            font=chikarego_font,
        )

    display.set_image(image)
    display.show()


if __name__ == "__main__":
    main()
