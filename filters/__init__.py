from .not_the_end import NotTheEnd
from loader import dp


if __name__ == "filters":
    dp.filters_factory.bind(NotTheEnd)
