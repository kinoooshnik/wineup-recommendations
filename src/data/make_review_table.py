import click
import pandas as pd
from tqdm import tqdm

COINCIDENCES = [
    [
        'Вино ООО "Кубань - вино" Мадера Кубанская Chateau Tamagne',
        "Вино Madera Chateau Tamagne Reserve  Мадера Кубанская Шато Тамань Резерв",
    ],
    [
        "Вино Шато Тамань сухое белое Fleurs du Sud",
        "Вино Rose de Tamagne Fleurs du Sud  Роза Тамани Шато Тамань",
    ],
    [
        'Вино Concha y Toro "Casillero Del Diablo Cabernet Sauvignon" (Казильеро Дель Дьябло Каберне Савиньон) алк. 13,5% красное сухое 0,75л ',
        "Вино Casillero del Diablo Cabernet Sauvignon Reserva  Казильеро дель Дьябло Каберне Совиньон Резерва",
    ],
    [
        "Вино Массандра Портвейн красный крымский",
        "Вино Crimsky Red Port Massandra  Портвейн Красный Крымский Массандра",
    ],
    [
        "Вино  Cusumano Nero D'Avola",
        "Вино Cusumano Nero d'Avola Terre Siciliane  Кузумано Неро д'Авола Терре Сичилиане",
    ],
    [
        'Вино ООО "Кубань - вино"  столовое полусухое розовое Роза Тамани. Шато Тамань',
        "Вино Rose de Tamagne Fleurs du Sud  Роза Тамани Шато Тамань",
    ],
    [
        "Вино Plantaze Vranac Pro Corde",
        "Вино Plantaze Vranac Pro Corde  Плантаже Вранац Про Корде",
    ],
    [
        "Вино Мадера дионис крымская Старый Крым",
        "Вино Madera Stary Crym Dionis  Мадера Дионис Крымская Старый Крым",
    ],
    [
        "Вино Freixenet Carta Nevada Dulce Фрешенед Кава Карта Невада Дульче игристое белое сладкое",
        "Вино Freixenet Cava Carta Nevada Semi Seco  Фрешенет Кава Карта Невада",
    ],
    [
        "Вино Concha y Toro  VCT Casillero del Diablo Shiraz",
        "Вино Casillero del Diablo Shiraz Reserva  Казильеро дель Дьябло Шираз Резерва",
    ],
    [
        "Вино Casa Vitivinicola Tinazzi POGGIO AI SANTI Rosato",
        "Вино Poggio ai Santi Sangiovese  Поджио ай Санти Санджовезе",
    ],
    [
        'Вино ООО "Кубань - вино" Chateau Tamagne DUO Rose (Шато Тамань Дуо Розовое)',
        "Вино Cabernet Merlot Chateau Tamagne Duo  Каберне Мерло Шато Тамань Дуо",
    ],
    [
        "Вино   Jerez Fino Romate (Херес Фино Ромате)",
        "Вино Osborne Sherry Fino  Осборн Херес Фино",
    ],
    [
        "Вино   Friuli Venezia Giulia - Villa Dragoni Friuli Grave Refosco dal peduncolo rosso -Emmegio тм",
        "Вино Moletto Refosco dal Peduncolo Rosso  Молетто Рефоско даль Педунколо Россо",
    ],
    [
        "Вино Bodegas Penalba Lopez / Бодегас Пеньялба Лопез Monte Castrillo Tinto\Монте Кастрильо",
        "Вино Penalba Lopez Cava Brut Nature  Пеньялба Лопез Кава Брют Натур",
    ],
    [
        "Вино Concha y Toro Casillero del Diablo Carmenere Reserva, 2010",
        "Вино Casillero del Diablo Carmenere Reserva  Казильеро дель Дьябло Карменер Резерва",
    ],
    [
        "Вино   SICILIA - Cusumano Nadaria Nero d'Avola I.G.T.",
        "Вино Cusumano Nero d'Avola Terre Siciliane  Кузумано Неро д'Авола Терре Сичилиане",
    ],
    [
        "Вино Pago de Tharsys Cava Brut Rosado  Паго де Тарсис Кава Брют Розовое",
        "вино игристое КАВА ДОМИНИО ДЕ ТАРСИС БРЮТ НАТЮР 11.5% 0.75",
    ],
    [
        "Вино Burgo Viejo Garnacha  Бурго Вьехо Гарнача",
        "вино БУРГО ВЬЕХО ГАРНАЧА 13.5% 0.75",
    ],
    [
        "Вино Burgo Viejo Graciano  Бурго Вьехо Грасиано",
        "вино БУРГО ВЬЕХО ГРАСИАНО 14% 0.75",
    ],
    [
        "Вино Morande Pinot Noir Gran Reserva  Моранде Пино Нуар Гран Резерва",
        "вино МОРАНДЕ ГРАН РЕЗЕРВА ПИНО НУАР 13.5-14% 0.75",
    ],
    [
        "Вино Pago de Tharsys Cava Brut Nature  Паго де Тарсис Кава Брют Натюр",
        "вино игристое КАВА ДОМИНИО ДЕ ТАРСИС БРЮТ НАТЮР 11.5% 0.75",
    ],
    [
        "Вино Luigi Leonardo Pinot Grigio  Луиджи Леонардо Пино Гриджио",
        "вино ЛУИДЖИ ЛЕОНАРДО ПИНО ГРИДЖИО 12% 0,75",
    ],
    [
        "Вино Eidosela Seleccion Albarino  Эйдосела Селексьон Альбариньо",
        "вино ЭЙДОСЕЛА СЕЛЕКСЬОН АЛЬБАРИНЬО 12-15% 0.75",
    ],
    [
        "Вино Luigi Leonardo Montepulciano d'Abruzzo  Луиджи Леонардо Монтепульчано д'Абруццо",
        "вино ЛУИДЖИ ЛЕОНАРДО МОНТЕПУЛЬЧАНО Д АБРУЦЦО 13% 0,75",
    ],
    [
        "Вино Burgo Viejo Rosado  Бурго Вьехо Росадо",
        "вино БУРГО ВЬЕХО РОСАДО 12-14% 0,75",
    ],
    [
        "Вино Corte Olivi Valpolicella Classico  Корте Оливи Вальполичелла Классико",
        "вино КОРТЕ ОЛИВИ ВАЛЬПОЛИЧЕЛЛА КЛАССИКО 12.5-13% 0.75",
    ],
    [
        "Вино Corte Olivi Chiaretto Bardolino Classico  Корте Оливи Кьяретто Бардолино Классико",
        "вино КЬЯРЕТТО БАРДОЛИНО КЛАССИКО КОРТЕ ОЛИВИ 12% 0,75",
    ],
    [
        "Вино LFE Pinot Noir Family Selection Gran Reserva  ЛФЭ Пино Нуар Фэмили Селекшн Гран Резерва",
        "вино МОРАНДЕ ГРАН РЕЗЕРВА ПИНО НУАР 13.5-14% 0.75",
    ],
    [
        "Вино Zonin Pinot Grigio Delle Venezie  Зонин Пино Гриджо Делле Венецие",
        "вино ПИНО ГРИДЖИО ДЕЛЛЕ ВЕНЕЦИЕ 12% 0,75",
    ],
    [
        "Вино Chateau Maison Blanche Cru Bourgeous  Шато Мезон Бланш Крю Буржуа",
        "вино ШАТО ПЛАНТЕ КРЮ БУРЖУА 13% 0,75",
    ],
    [
        "Вино Les Dorees Bourgogne Pinot Noir  Ле Доре Бургонь Пино Нуар",
        "Вино БУРГОНЬ ПИНО НУАР ПРЕСТИЖ 2017 12.5% 0.75",
    ],
    [
        "Вино Leyenda Pedro Ximenez Sherry  Леенда Педро Хименес Херес",
        "херес ЛЕЕНДА ПЕДРО ХИМЕНЕС 17% 0,75",
    ],
    [
        "Вино Chateau Preuillac Cru Bourgeous  Шато Прюйяк Крю Буржуа",
        "вино ШАТО ПЛАНТЕ КРЮ БУРЖУА 13% 0,75",
    ],
    ["Вино Leyenda Fino Sherry  Леенда Фино Херес", "херес ЛЕЕНДА ФИНО 15% 0,75"],
    ["Вино Leyenda Cream Sherry  Леенда Крим Херес", "херес ЛЕЕНДА КРИМ 17,5% 0,75"],
    [
        "Вино Chateau Le Monteil d'Arsac Cru Bourgeois  Шато Ле Монтей д'Арсак Крю Буржуа ",
        "вино ШАТО ПЛАНТЕ КРЮ БУРЖУА 13% 0,75",
    ],
]

COLUMNS = [
    "wine_name",
    "wine_id",
    "user_name",
    "user_id",
    "rating",
    "variants",
    "other_wine_names",
]


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def make_table(irecommend_path, vinofan_path, somelie_path):
    irecommend = pd.read_csv(irecommend_path)
    vinofan = pd.read_csv(vinofan_path)
    somelie = pd.read_csv(somelie_path)
    concat = pd.concat([irecommend, vinofan, somelie])
    concat["wine_name"] = concat["wine_name"].map(
        lambda x: x.replace(" ", " ")
    )  # пробелы разные

    # удаление строк, где оценка - не число
    concat = concat.drop(concat[concat["rating"].apply(lambda x: not isfloat(x))].index)

    for wine in concat["wine_name"]:
        for wine_list in COINCIDENCES:
            if wine in wine_list:
                break
        else:
            COINCIDENCES.append([wine])
    id_coincidences = dict(zip(range(len(COINCIDENCES)), COINCIDENCES))
    id_username = dict(
        zip(
            concat["username"].drop_duplicates(),
            range(len(set(concat["username"].drop_duplicates()))),
        )
    )

    def search_in_coincidences(id_coincidences, wine):
        for idx, wines in id_coincidences.items():
            if wine in wines:
                return idx, wines[0], wines
        raise Exception("Can't find wine in coincidences list")

    result = []
    for _, row in tqdm(concat.iterrows(), total=len(concat)):
        idx, wine_name, other_wine_names = search_in_coincidences(
            id_coincidences, row["wine_name"]
        )

        result_row = [
            wine_name,
            idx,
            row["username"],
            id_username[row["username"]],
            row["rating"],
            row["variants_number"],
            "|".join(other_wine_names),
        ]

        result.append(result_row)

    return pd.DataFrame(result, columns=COLUMNS)


@click.command()
@click.argument("irecommend_path", type=click.Path(exists=True))
@click.argument("vinofan_path", type=click.Path(exists=True))
@click.argument("somelie_path", type=click.Path(exists=True))
@click.argument("output_reviews_path", type=click.Path())
def main(irecommend_path, vinofan_path, somelie_path, output_reviews_path):
    df = make_table(irecommend_path, vinofan_path, somelie_path)
    df.to_csv(output_reviews_path, index=False)


if __name__ == "__main__":
    main()
