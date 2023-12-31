from typing import Dict, List

from sqlalchemy.orm import Session

from hangman import app, db
from hangman.models.word import Word

with app.app_context():
    db.create_all()


def has_data_in_database(db: Session) -> bool:
    return db.query(Word).count() > 0


def add_word(
    db: Session,
    word: Word,
) -> Word:
    db_word = Word(
        word=word.word,
        word_length=word.word_length,
        category=word.category,
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def create_words_db(words: Dict[str, List[str]]) -> None:
    with app.app_context():
        session = Session(bind=db.engine)
        if not has_data_in_database(session):
            for category, word_list in words.items():
                for word in word_list:
                    word_data = Word(
                        word=word,
                        word_length=len(word),
                        category=category,
                        times_called=0,
                        times_answered=0,
                        times_lost=0,
                    )
                    add_word(session, word_data)


if __name__ == "__main__":
    words = {
        "animals": [
            "DOG",
            "CAT",
            "ELEPHANT",
            "LION",
            "TIGER",
            "GIRAFFE",
            "ZEBRA",
            "MONKEY",
            "GORILLA",
            "KANGAROO",
            "KOALA",
            "PANDA",
            "BEAR",
            "CHEETAH",
            "LEOPARD",
            "RHINO",
            "HIPPO",
            "CAMEL",
            "HORSE",
            "COW",
            "PIG",
            "SHEEP",
            "GOAT",
            "RABBIT",
            "SQUIRREL",
            "BAT",
            "DOLPHIN",
            "WHALE",
            "SHARK",
            "OCTOPUS",
            "SQUID",
            "JELLYFISH",
            "SEAHORSE",
            "LOBSTER",
            "CRAB",
            "PENGUIN",
            "OSTRICH",
            "FLAMINGO",
            "TOUCAN",
            "PARROT",
            "EAGLE",
            "HAWK",
            "FALCON",
            "OWL",
            "SPARROW",
            "PEACOCK",
            "PELICAN",
            "HUMMINGBIRD",
            "SWAN",
            "GOOSE",
            "DUCK",
            "PIGEON",
            "CROW",
            "RACCOON",
            "FOX",
            "WOLF",
            "COYOTE",
            "HYENA",
            "JACKAL",
            "OTTER",
            "BEAVER",
            "PLATYPUS",
            "ARMADILLO",
            "HEDGEHOG",
            "SLOTH",
            "TAPIR",
            "ANTEATER",
            "MEERKAT",
            "CHIMPANZEE",
            "ORANGUTAN",
            "LEMUR",
            "LLAMA",
            "ALPACA",
            "BISON",
            "YAK",
            "MUSKOX",
            "OCELOT",
            "LYNX",
            "WOLVERINE",
            "CAVY",
            "CHINCHILLA",
            "HAMSTER",
            "GERBIL",
            "RAT",
            "MOLE",
            "SHREW",
            "DEVIL",
            "WOMBAT",
            "ECHIDNA",
            "ALLIGATOR",
            "CROCODILE",
            "IGUANA",
            "CHAMELEON",
            "TURTLE",
            "TORTOISE",
            "PYTHON",
            "COBRA",
            "JAGUAR",
            "PANTHER",
            "DINGO",
        ],
        "home": [
            "CHAIR",
            "TABLE",
            "SOFA",
            "BED",
            "LAMP",
            "RUG",
            "CLOCK",
            "MIRROR",
            "SHELF",
            "PILLOW",
            "BLANKET",
            "CURTAIN",
            "TOWEL",
            "DISH",
            "FORK",
            "KNIFE",
            "SPOON",
            "PLATE",
            "BOWL",
            "GLASS",
            "POT",
            "MONITOR",
            "FRIDGE",
            "OVEN",
            "SINK",
            "MICROWAVE",
            "TOASTER",
            "BLENDER",
            "MIXER",
            "KETTLE",
            "DISHWASHER",
            "WASHER",
            "DRYER",
            "IRON",
            "VACUUM",
            "BROOM",
            "TRASHCAN",
            "DUSTPAN",
            "BUCKET",
            "HAMPER",
            "HANGER",
            "DRAWER",
            "CLOSET",
            "CABINET",
            "BOOKCASE",
            "ALARM",
            "SPEAKER",
            "TELEVISION",
            "REMOTE",
            "CHARGER",
            "LAPTOP",
            "TABLET",
            "PHONE",
            "TISSUE",
            "SOAP",
            "SHAMPOO",
            "CONDITIONER",
            "TOOTHBRUSH",
            "TOOTHPASTE",
            "SPONGE",
            "DETERGENT",
            "BRUSH",
            "COMB",
            "RAZOR",
            "DEODORANT",
            "PERFUME",
            "LOTION",
            "TRASHBAG",
            "WINDEX",
            "CANDLE",
            "MATCHES",
            "LIGHTER",
            "BATTERY",
            "FLASHLIGHT",
            "FIRSTAID",
            "EXTENSIONCORD",
            "ADHESIVE",
            "SCISSORS",
            "TAPE",
            "GLUE",
            "STAPLER",
            "PEN",
            "PAPER",
            "NOTEPAD",
            "FOLDER",
            "ERASER",
            "CLIPBOARD",
            "PENCIL",
            "CALENDAR",
            "KEYCHAIN",
            "SCREWDRIVER",
            "PLIERS",
            "HAMMER",
            "NAIL",
            "SAW",
            "LEVEL",
            "LADDER",
            "WRENCH",
            "GLOVES",
            "MASK",
        ],
        "jobs": [
            "DOCTOR",
            "CHEF",
            "TEACHER",
            "ENGINEER",
            "ARTIST",
            "WRITER",
            "ACTOR",
            "DESIGNER",
            "CARPENTER",
            "PLUMBER",
            "PAINTER",
            "PILOT",
            "DRIVER",
            "NURSE",
            "DENTIST",
            "WAITER",
            "SINGER",
            "PHOTOGRAPHER",
            "MECHANIC",
            "LAWYER",
            "GARDENER",
            "FARMER",
            "MUSICIAN",
            "SCIENTIST",
            "DETECTIVE",
            "ELECTRICIAN",
            "BARBER",
            "STYLIST",
            "TAILOR",
            "CASHIER",
            "JANITOR",
            "LIBRARIAN",
            "THERAPIST",
            "COACH",
            "EDITOR",
            "COUNSELOR",
            "VETERINARIAN",
            "ACCOUNTANT",
            "SURGEON",
            "PARAMEDIC",
            "POLICE",
            "FIREFIREFIGHTER",
            "BAKER",
            "JEWELER",
            "MINER",
            "FOREMAN",
            "COURIER",
            "JOCKEY",
            "SCULPTOR",
            "BUTCHER",
            "POTTER",
            "CARTOONIST",
            "BARTENDER",
            "BREWER",
            "CURATOR",
            "DIVER",
            "ENTERTAINER",
            "FLORIST",
            "GEOLOGIST",
            "HAIRSTYLIST",
            "INSPECTOR",
            "JUDGE",
            "LECTURER",
            "MATHEMATICIAN",
            "NANNY",
            "OPTOMETRIST",
            "QUIZMASTER",
            "REFEREE",
            "TAXI",
            "VENDOR",
            "YOGA",
            "ZOOKEEPER",
            "ASTRONOMER",
            "BROKER",
            "CAMERAMAN",
            "DECORATOR",
            "EMBROIDERER",
            "FRAMER",
            "GEMOLOGIST",
            "HATTER",
            "ILLUSTRATOR",
            "JAILER",
            "KNITTER",
            "LINGUIST",
            "MASON",
            "NAUTICAL",
            "ORNITHOLOGIST",
            "PSYCHOLOGIST",
            "QUARRIER",
            "RADIOLOGIST",
            "STUNTMAN",
            "TATTOO",
            "VENTRILOQUIST",
            "WEAVER",
            "YODELER",
            "XYLOPHONIST",
            "YOGURTier",
            "ZIPLINER",
            "QUILTER",
            "BIOLOGIST",
        ],
        "food": [
            "PIZZA",
            "BURGER",
            "SUSHI",
            "PASTA",
            "STEAK",
            "SALAD",
            "TACO",
            "SOUP",
            "RICE",
            "FRIES",
            "CAKE",
            "COOKIE",
            "BREAD",
            "CHEESE",
            "PANCAKE",
            "WAFFLE",
            "MUFFIN",
            "NOODLE",
            "BACON",
            "EGG",
            "DONUT",
            "SANDWICH",
            "MILK",
            "TEA",
            "COFFEE",
            "JUICE",
            "SMOOTHIE",
            "YOGURT",
            "CHEESECAKE",
            "NAPOLEON",
            "SHRIMP",
            "SALMON",
            "CHICKEN",
            "TURKEY",
            "RAMEN",
            "PINEAPPLE",
            "GRAPES",
            "CHERRY",
            "APPLE",
            "ORANGE",
            "BANANA",
            "PEAR",
            "KIWI",
            "MANGO",
            "STRAWBERRY",
            "BLUEBERRY",
            "RASPBERRY",
            "CUCUMBER",
            "CARROT",
            "SPINACH",
            "LETTUCE",
            "TOMATO",
            "POTATO",
            "ONION",
            "BROCCOLI",
            "CAULIFLOWER",
            "ZUCCHINI",
            "PEPPER",
            "GINGER",
            "GARLIC",
            "CABBAGE",
            "AVOCADO",
            "PEAS",
            "CORN",
            "BEANS",
            "MUSHROOM",
            "WATERMELON",
            "HONEYDEW",
            "CANTALOUPE",
            "POMEGRANATE",
            "COCONUT",
            "MELON",
            "FIG",
            "PAPAYA",
            "PASSIONFRUIT",
            "LYCHEE",
            "GUAVA",
            "DRAGONFRUIT",
            "DURIAN",
            "QUINCE",
            "PERSIMMON",
            "APRICOT",
            "PLUM",
            "LIME",
            "LEMON",
            "CRANBERRY",
            "BLACKBERRY",
            "CURRANT",
            "BOYSENBERRY",
            "RHUBARB",
            "ACAI",
            "STARFRUIT",
            "LINGONBERRY",
            "CEPPELINE",
            "WATERCRESS",
            "HAZELNUT",
            "PECAN",
            "TANGERINE",
            "ARTICHOKE",
            "PAPRIKA",
        ],
        "clothes": [
            "SWEATER",
            "JEANS",
            "DRESS",
            "T-SHIRT",
            "JACKET",
            "SKIRT",
            "SHORTS",
            "BLOUSE",
            "PANTS",
            "COAT",
            "SHIRT",
            "SUIT",
            "HAT",
            "SOCKS",
            "HELMET",
            "SCARF",
            "BELT",
            "SHOES",
            "BOOTS",
            "SANDALS",
            "SNEAKERS",
            "HEELS",
            "SLIPPERS",
            "PAJAMAS",
            "HOODIE",
            "BLAZER",
            "TUNIC",
            "OVERALLS",
            "VEST",
            "RAINCOAT",
            "CARDIGAN",
            "POLO",
            "PARKA",
            "PONCHO",
            "TANKTOP",
            "ROMPER",
            "JUMPSUIT",
            "BODYSUIT",
            "PULLOVER",
            "CHINOS",
            "TIGHTS",
            "CAP",
            "TURBAN",
            "CLOAK",
            "CAPE",
            "KIMONO",
            "TOGA",
            "JERSEY",
            "BRA",
            "BOXERS",
            "BRIEFS",
            "THONG",
            "GOWN",
            "SARONG",
            "MUUMUU",
            "CAFTAN",
            "JERKIN",
            "DUNGAREES",
            "JODHPURS",
            "ANORAK",
            "BIKINI",
            "BOLERO",
            "DOLMAN",
            "FROCK",
            "HALTER",
            "PEACOAT",
            "TRENCHCOAT",
            "SHAWL",
            "STOLE",
            "TRUNKS",
            "JEGGINGS",
            "SWEATPANTS",
            "LEGGINGS",
            "BANDANA",
            "ASCOT",
            "KILT",
            "SHRUG",
            "CAMISOLE",
            "MANTLE",
            "CULOTTES",
            "CHEMISE",
            "PINAFORE",
            "TIPPET",
            "JABOT",
            "GAUNTLET",
            "GAITERS",
            "PASHMINA",
            "HIJAB",
            "JOGGERS",
            "UNDERWEAR",
            "CROCS",
            "STATSON",
            "СAMELOT",
        ],
        "countries": [
            "AFGHANISTAN",
            "ALBANIA",
            "ALGERIA",
            "ANDORRA",
            "ANGOLA",
            "ANTIGUA AND BARBUDA",
            "ARGENTINA",
            "ARMENIA",
            "AUSTRALIA",
            "AUSTRIA",
            "AZERBAIJAN",
            "BAHAMAS",
            "BAHRAIN",
            "BANGLADESH",
            "BARBADOS",
            "BELARUS",
            "BELGIUM",
            "BELIZE",
            "BENIN",
            "BHUTAN",
            "BOLIVIA",
            "BOSNIA AND HERZEGOVINA",
            "BOTSWANA",
            "BRAZIL",
            "BRUNEI",
            "BULGARIA",
            "BURKINA FASO",
            "BURUNDI",
            "CABO VERDE",
            "CAMBODIA",
            "CAMEROON",
            "CANADA",
            "CENTRAL AFRICAN REPUBLIC",
            "CHAD",
            "CHILE",
            "CHINA",
            "COLOMBIA",
            "COMOROS",
            "CONGO",
            "COSTA RICA",
            "CROATIA",
            "CUBA",
            "CYPRUS",
            "CZECH REPUBLIC",
            "DENMARK",
            "DJIBOUTI",
            "DOMINICA",
            "DOMINICAN REPUBLIC",
            "ECUADOR",
            "EGYPT",
            "EL SALVADOR",
            "EQUATORIAL GUINEA",
            "ERITREA",
            "ESTONIA",
            "ESWATINI",
            "ETHIOPIA",
            "FIJI",
            "FINLAND",
            "FRANCE",
            "GABON",
            "GAMBIA",
            "GEORGIA",
            "GERMANY",
            "GHANA",
            "GREECE",
            "GRENADA",
            "GUATEMALA",
            "GUINEA",
            "GUINEA-BISSAU",
            "GUYANA",
            "HAITI",
            "HONDURAS",
            "HUNGARY",
            "ICELAND",
            "INDIA",
            "INDONESIA",
            "IRAN",
            "IRAQ",
            "IRELAND",
            "ISRAEL",
            "ITALY",
            "JAMAICA",
            "JAPAN",
            "JORDAN",
            "KAZAKHSTAN",
            "KENYA",
            "KIRIBATI",
            "KOREA",
            "KOSOVO",
            "KUWAIT",
            "KYRGYZSTAN",
            "LAOS",
            "LATVIA",
            "LEBANON",
            "LESOTHO",
            "LIBERIA",
            "LIBYA",
            "LIECHTENSTEIN",
            "LITHUANIA",
            "LUXEMBOURG",
        ],
        "cities": [
            "ADELAIDE",
            "ALGIERS",
            "ALYTUS",
            "AMSTERDAM",
            "ANKARA",
            "ANTWERP",
            "ASUNCION",
            "ATHENS",
            "AUSTIN",
            "BAMAKO",
            "BANGKOK",
            "BARCELONA",
            "BEIJING",
            "BEIRUT",
            "BELGRADE",
            "BERLIN",
            "BOGOTA",
            "BOSTON",
            "BRASILIA",
            "BRATISLAVA",
            "BRIDGETOWN",
            "BRUSSELS",
            "BUCHAREST",
            "BUDAPEST",
            "CAIRO",
            "CASABLANCA",
            "CHICAGO",
            "COLOGNE",
            "COPENHAGEN",
            "DAKAR",
            "DALLAS",
            "DELHI",
            "DENVER",
            "DETROIT",
            "DUBAI",
            "DUBLIN",
            "EDINBURGH",
            "FLORENCE",
            "FRANKFURT",
            "GENEVA",
            "GLASGOW",
            "GUANGZHOU",
            "HAMBURG",
            "HAVANA",
            "HELSINKI",
            "HOUSTON",
            "INCHEON",
            "ISTANBUL",
            "JAKARTA",
            "JERUSALEM",
            "KARACHI",
            "KAUNAS",
            "KIEV",
            "KINGSTON",
            "KOKTEBEL",
            "RIGA",
            "LIMA",
            "LISBON",
            "LONDON",
            "MADRID",
            "MANILA",
            "MELBOURNE",
            "MIAMI",
            "MILAN",
            "MOSCOW",
            "MUNICH",
            "MURMANSK",
            "NAIROBI",
            "NAPLES",
            "NORILSK",
            "OSLO",
            "OTTAWA",
            "PARIS",
            "PERTH",
            "PRAGUE",
            "QUEBEC",
            "REYKJAVIK",
            "RIYADH",
            "RIO",
            "ROME",
            "SALEM",
            "SARTAVALA",
            "SEATTLE",
            "SEOUL",
            "SYDNEY",
            "SINGAPORE",
            "SOFIA",
            "STOCKHOLM",
            "TAIPEI",
            "TEHRAN",
            "TERIBERKA",
            "TOKYO",
            "TORONTO",
            "VANCOUVER",
            "VENICE",
            "VIENNA",
            "VILNIUS",
            "WARSAW",
            "WELLINGTON",
            "ZURICH",
        ],
        "space": [
            "ADAM",
            "ADAMS",
            "AOIDA",
            "ANANKE",
            "APOLLO",
            "ARES",
            "ATLAS",
            "CALYPSO",
            "CALLIOPE",
            "CALLISTO",
            "CERES",
            "CLIO",
            "DEMETETER",
            "DIONE",
            "EARTH",
            "EIRENE",
            "ELPIDA",
            "ENCELADUS",
            "EPIMETHEUS",
            "EROS",
            "EUROPA",
            "EUPHEMIA",
            "EUTERPE",
            "FLORA",
            "GAIA",
            "GALATEA",
            "GANymede",
            "GIGEIA",
            "GRIGORY",
            "GRUBA",
            "HARMONIA",
            "HELENE",
            "HELIKE",
            "HELIOS",
            "HERA",
            "HERMES",
            "HESTIA",
            "HYPERION",
            "HYGIEIA",
            "IAPETUS",
            "ICARUS",
            "IO",
            "IRIS",
            "JANUS",
            "JUNO",
            "JUPITER",
            "KALLIOPE",
            "KALLISTO",
            "KALYPSO",
            "KARME",
            "LEDDA",
            "LUNA",
            "MARS",
            "MASSALIA",
            "MERCURY",
            "METIS",
            "MIMIS",
            "MNEME",
            "MNEMOSYNE",
            "NEPTUNE",
            "PALLAS",
            "PAN",
            "PASIPHAE",
            "PHOEBE",
            "PHOLUS",
            "PLUTO",
            "POLIA",
            "POLYCHORDIA",
            "PRAISEDIKA",
            "PROMETHEUS",
            "PROTEUS",
            "PSYCHE",
            "RHEA",
            "REYNOLD",
            "SATURN",
            "SCHMIDT",
            "SCHWABE",
            "SELENE",
            "SMITH",
            "SVIRSKIY",
            "TANTALUS",
            "TARA",
            "TEFIA",
            "TELESTO",
            "TERPSICHORE",
            "TETIS",
            "THEBE",
            "THEMIS",
            "THETIS",
            "TITANIA",
            "TRITON",
            "URANUS",
            "VENUS",
            "VESTA",
            "VOLVA",
            "YAPET",
            "ZEPHYRUS",
            "ZOE",
            "ZUBENELGENUBI",
        ],
        "mountains": [
            "ACONCAGUA",
            "MANASLU",
            "ANETO",
            "ANNAPURNA",
            "APO",
            "ARAGATS",
            "ARARAT",
            "ARBER",
            "ARGENTERA",
            "BELUKHA",
            "BLACKBURN",
            "BOISING",
            "BONA",
            "BROCKEN",
            "CARMEL",
            "CITLALTEPETL",
            "CHIMBORAZO",
            "COOK",
            "CORCOVADO",
            "CORNO",
            "DEMAVEND",
            "DENALI",
            "DHAULAGIRI",
            "EIGER",
            "ELBERT",
            "ELBRUS",
            "EREBUS",
            "ESTRELLA",
            "ETNA",
            "EVEREST",
            "FAIRWEATHER",
            "FINSTERAARHORN",
            "FUJI",
            "GERLACHOVKA",
            "HELICON",
            "HELVELLYN",
            "HERMON",
            "HYMETTUS",
            "IDA",
            "ILLIMANI",
            "ISTO",
            "JUNGFRAU",
            "KAMET",
            "KANGCHENJUNGA",
            "KILIMANJARO",
            "KINABALU",
            "KLYUCHEVSKAYA",
            "LEONE",
            "LOGAN",
            "MANSFIELD",
            "MARCY",
            "MARGHERITA",
            "MARKHAM",
            "MARMOLADA",
            "MASHARBRUM",
            "MATTERHORN",
            "MITCHELL",
            "MUSALA",
            "NARODNAYA",
            "NEBO",
            "NEGOIU",
            "OSSA",
            "PALOMAR",
            "PARNASSUS",
            "PELION",
            "PENTELIKON",
            "PERDIDO",
            "PILATUS",
            "RAINIER",
            "RANTEMARIO",
            "RIGI",
            "ROBSON",
            "ROSA",
            "RUSHMORE",
            "SCHNEEOPPE",
            "SCOPUS",
            "SINAI",
            "SIPLE",
            "SKALITSY",
            "SNOWDON",
            "SORATA",
            "STANLEY",
            "TABOR",
            "TAJUMULCO",
            "TEIDE",
            "TIMPANOGOS",
            "TOUBKAL",
            "TROGLAV",
            "VENUSBERG",
            "VICTORIA",
            "VISO",
            "WADDINGTON",
            "WASHINGTON",
            "WEISSHORN",
            "WHITNEY",
            "WRANGELL",
            "ZUGSPITZE",
            "PUTORANA",
        ],
    }

    create_words_db(words=words)
