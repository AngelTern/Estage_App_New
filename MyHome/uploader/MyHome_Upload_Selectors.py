class MyHomeUploadSelectors:
    NAV_BUTTONS = {
        "PARAMETERS": "#root > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > ul li:nth-of-type(2)",
        "PRICE": "#root > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > ul li:nth-of-type(3) a",
        "CONTACT": "#root > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > ul li:nth-of-type(4) a",
        "DESCRIPTION": "#root > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > ul li:nth-of-type(5) a",
        "SERVICIES": "#root > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > ul li:nth-of-type(6) a"
    }


    AUTHENTICATION_BUTTON = "#root > section > article > button"
    EMAIL_INPUT_FIELD = "div.wrapper > div > div > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div > form > div.forms-group div:nth-of-type(1) > div > input"
    PASSWORD_INPUT_FIELD = "div.wrapper > div > div > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div > form > div:nth-of-type(1) div:nth-of-type(2) > div > input"
    CONFIRM_AUTHENTICATION_BUTTON = "div.wrapper > div > div > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div > form > div:nth-of-type(3) > button"
    PROPERTY_TYPE_BUTTONS = "#root > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div > div > div > div"
    PROPERTY_TYPE_TEXT = "label > div > div > span:nth-of-type(1)"
    TRANSACTION_TYPE_BUTTONS = "#root > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(3) > div > div > div >div"
    TRANSACTION_TYPE_TEXT = "label > div > div > span:nth-of-type(1)"
    INPUT_CITY = "#root > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(6) > div > div > div > div > input"
    SELECT_CITY = "#root > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(6) > div > div > div > div:nth-of-type(2) > ul > li"
    INPUT_STREET = "#root > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(7) > div > div:nth-of-type(1) > div:nth-of-type(2) > label > input"
    SELECT_STREET = "#root > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(7) > div > div:nth-of-type(1) > div:nth-of-type(2) > div > ul > li"
    STREET_INNER_DISTRICT = "span:nth-of-type(2)"
    INPUT_STREET_NUMBER = "#root > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(7) > div > div:nth-of-type(2) > div > label > input"
    ROOM_SELECTION = "#\\31  > div:nth-child(2) > div > div:nth-child(2) > div > div > div"
    ROOM_SELECTION_INNER_TEXT = "label > div > div > span:nth-child(1)"
    BEDROOM_SELECTION = "#\\31  > div:nth-child(2) > div > div:nth-child(4) > div > div > div"
    BEDROOM_SELECTION_INNER_TEXT = "label > div > div > span:nth-child(1)"
    WASHROOM_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(6) > div > div > div"
    WASHROOM_DROPDOWN_SELECTION = "#\\31  > div:nth-child(2) > div > div:nth-child(6) > div > div > div:nth-of-type(2) ul > li"
    FLOOR_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(8) > div:nth-child(1) > div > label > input"
    TOTAL_FLOOR_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(8) > div:nth-child(2) > div > label > input"
    STATUS_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(10) > div > div > div:nth-of-type(1)"
    STATUS_SELECT = "#\\31  > div:nth-child(2) > div > div:nth-child(10) > div > div > div:nth-of-type(2) > ul > li"
    BUILD_DATE_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(12) > div > div > div"
    BUILD_DATE_SELECT = "#\\31  > div:nth-child(2) > div > div:nth-child(12) > div > div > div:nth-of-type(2) > ul > li"
    STATE_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(14) > div > div > div:nth-of-type(1)"
    STATE_SELECT = "#\\31  > div:nth-child(2) > div > div:nth-child(14) > div > div > div:nth-of-type(2) > ul > li"
    PROJECT_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(16) > div > div > div:nth-of-type(1)"
    PROJECT_SELECT = "#\\31  > div:nth-child(2) > div > div:nth-child(16) > div > div > div:nth-of-type(2) > ul > li"
    CEILING_HEIGHT_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(18) > div > div > label > input"
    HEATING_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(20) > div > div > div:nth-of-type(1)"
    HEATING_SELECT = "#\\31  > div:nth-child(2) > div > div:nth-child(20) > div > div > div:nth-of-type(2) > ul > li"
    PARKING_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(22) > div > div > div:nth-of-type(1)"
    PARKING_SELECTION = "#\\31  > div:nth-child(2) > div > div:nth-child(22) > div > div > div:nth-of-type(2) > ul > li"
    HOT_WATER_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(24) > div > div > div:nth-of-type(1)"
    HOT_WATER_SELECTION = "#\\31  > div:nth-child(2) > div > div:nth-child(24) > div > div > div:nth-of-type(2) > ul > li"
    BALCONY_COUNT_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(28) > div:nth-of-type(1) > div > label > input"
    BALCONY_AREA_INPUT = "#\\31  > div:nth-child(2) > div > div:nth-child(28) > div:nth-of-type(2) > div > label > input"



