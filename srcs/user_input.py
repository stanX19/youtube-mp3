def get_song_range_from_response(response: str, song_count: int) -> list:
    song_range = []
    error_messages = []

    if response == "all":
        return list(range(song_count))

    parts = response.split(",")
    for part in parts:
        part = part.strip()

        if "-" in part:
            range_parts = part.split("-")

            if len(range_parts) != 2:
                error_messages.append(f"Invalid song range format: {part}. Please provide a valid range.")
                continue

            start = range_parts[0].strip()
            end = range_parts[1].strip()

            if not start.isdigit() or not end.isdigit():
                error_messages.append(f"Invalid song range format: {part}. song numbers must be integers.")
                continue

            start = int(start) - 1
            end = int(end) - 1

            if start < 0 or end >= song_count:
                error_messages.append(f"Invalid song range: {part}. songs are out of range")
                continue

            if start > end:
                error_messages.append(f"Invalid song range: {part}. songs are in incorrect order.")
                continue

            song_range.extend(range(start, end + 1))

        else:
            if not part.isdigit():
                error_messages.append(f"Invalid song number format: {part}. song number must be an integer.")
                continue

            song_number = int(part) - 1

            if song_number < 0 or song_number >= song_count:
                error_messages.append(f"Invalid song number: {part}. song is out of range.")
                continue

            song_range.append(song_number)

    if error_messages:
        raise ValueError("\n".join(error_messages))

    song_range = sorted(list(set(song_range)))
    return song_range


def get_songs_to_download(song_count) -> list[int]:
    print(f"{song_count} songs found. Do you want to download all songs? [Y/n]")

    response = input(": ").lower()
    while response not in ["y", "yes", "n", "no"]:
        print("Please input [Y] for yes or [N] for no.")
        response = input(": ").lower()
    if response in ["yes", "y"]:
        return list(range(song_count))
    if song_count <= 1:
        return []
    print("Enter the range of songs you want to download, inclusive, separated by commas.")
    print(f"Note: The first song is indexed as 1.")
    print(f"Example: 1-5, 11, 13-{song_count}")

    while True:
        try:
            response = ""
            while not response:
                response = input(": ").strip().lower()
            song_range = get_song_range_from_response(response, song_count)
            break
        except ValueError as exc:
            print(exc)

    return song_range


if __name__ == '__main__':
    result = get_songs_to_download(100)
    print(f"\nFinal result: {result}")
    import time
    time.sleep(1000)
