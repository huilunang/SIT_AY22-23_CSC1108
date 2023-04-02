def decode_polyline(polyline_str):
    """
    Decodes a polyline string into a list of latitude/longitude coordinates.
    """
    index = 0
    coordinates = []
    lat = 0
    lng = 0

    while index < len(polyline_str):
        # calculate the latitude
        shift = 0
        result = 0
        while True:
            b = ord(polyline_str[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1
            if not b >= 0x20:
                break
        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat

        # calculate the longitude
        shift = 0
        result = 0
        while True:
            b = ord(polyline_str[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1
            if not b >= 0x20:
                break
        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng

        # add the coordinate to the list
        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates
