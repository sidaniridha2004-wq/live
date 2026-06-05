import json
import logging
from sys import exit
import datetime
import requests
import warnings
from . import __repo__

warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

now = datetime.datetime.now()


def get_excep(e):
    return e.args[1] if len(e.args) > 1 else str(e)


DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}


class Utils:
    import sqlite3

    conn = sqlite3.connect(":memory:")
    formats = ("html", "csv", "xlsx", "markdown", "xml", "json")
    chosen_format = "json"
    chosen_output = "livescore"

    @staticmethod
    def error_handler(resp=None, exit_on_error=False, log=True):
        def decorator(func):
            def main(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if log:
                        logging.debug(f"Function ({func.__name__}) : {get_excep(e)}")
                        logging.error(get_excep(e))
                    if exit_on_error:
                        exit(1)
                    return resp

            return main

        return decorator

    @staticmethod
    def read_json(fnm):
        with open(fnm, encoding="utf-8") as fh:
            return json.load(fh)

    @staticmethod
    def dump_json(*args, **kwargs):
        return json.dumps(*args, **kwargs)

    @staticmethod
    def write_json(fnm, data, *args, **kwargs):
        with open(fnm, "w", encoding="utf-8") as fh:
            json.dump(data, fh, *args, **kwargs)

    @staticmethod
    def DataFrame(data, format_name):
        import pandas as pd

        df = pd.DataFrame(data)
        mapper = {
            "dict": df.to_dict,
            "csv": df.to_csv,
            "json": df.to_json,
            "xlsx": df.to_excel,
            "html": df.to_html,
            "xml": df.to_xml,
            "markdown": df.to_markdown,
        }
        return mapper[format_name]

    @classmethod
    def filter(cls, data: list, country=None, league=None, name=None, status=None):
        import pandas as pd

        if not data:
            return []
        pd.DataFrame(data).to_sql("Livescore", cls.conn, if_exists="replace", index=False)
        queries = ["Home IS NOT NULL"]
        if name:
            queries.append(f"(Home LIKE '%{name}%' OR Away LIKE '%{name}%')")
        if league:
            queries.append(f"League LIKE '%{league}%'")
        if country:
            queries.append(f"Country LIKE '%{country}%'")
        if status:
            queries.append(f"Status LIKE '%{status}%'")
        sql = f"SELECT * FROM Livescore WHERE {' AND '.join(queries)};"
        logging.debug(f"Executing sql : {sql}")
        df = pd.read_sql(sql, cls.conn)
        resp = cls.format(df)
        if cls.chosen_format in ("xlsx", "json"):
            resp = cls.reformat_json(json.loads(resp))
        return resp

    @classmethod
    def format(cls, df):
        if cls.chosen_format == "xlsx":
            df.to_excel(cls.chosen_output + ".xlsx", index=False)
            return df.to_json()
        mapper = {
            "csv": df.to_csv,
            "html": df.to_html,
            "markdown": df.to_markdown,
            "xml": df.to_xml,
            "json": df.to_json,
            "dict": df.to_dict,
        }
        return mapper[cls.chosen_format]()

    @classmethod
    def reformat_json(cls, reformatted):
        resp = []
        if not isinstance(reformatted, dict):
            reformatted = json.loads(reformatted)
        if "index" not in reformatted:
            for x in reformatted.get("serial_id", {}).keys():
                hunted = {key: reformatted[key].get(x) for key in reformatted.keys()}
                resp.append(hunted)
            return resp
        for x in list(reformatted["index"].keys()):
            hunted = {val: reformatted[val].get(x) for val in reformatted.keys() if val != "index"}
            resp.append(hunted)
        return resp


class JsonFormatter:
    def __init__(self, data: dict | str, update: bool = False, config_file: str = None):
        if not isinstance(data, dict):
            data = json.loads(data)
        self.data = data
        self.mappers = {"Stages": "Stages", "Events": "Events", "T1": "T1", "T2": "T2"}
        self.targets = {
            "serial_id": "Sid",
            "league": "Snm",
            "country": "Cnm",
            "match_id": "Eid",
            "home_scores": "Tr1",
            "away_scores": "Tr2",
            "kickoff": "Esd",
            "status": "Eps",
            "home": "Nm",
            "away": "Nm",
            "home_id": "ID",
            "away_id": "ID",
        }
        if update:
            self.update_keys()
        if config_file:
            new_config = Utils.read_json(config_file)
            self.mappers.update(new_config.get("mappers", {}))
            self.targets.update(new_config.get("targets", {}))

    def __call__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    @Utils.error_handler()
    def update_keys(self) -> None:
        link = f"{__repo__}/raw/main/assets/config.json"
        resp = requests.get(link, timeout=30)
        if resp.ok:
            data = resp.json()
            self.mappers.update(data.get("mappers", {}))
            self.targets.update(data.get("targets", {}))

    def __get_intro(self, data: dict) -> dict:
        return {
            "serial_id": data.get(self.targets["serial_id"]),
            "league": data.get(self.targets["league"]),
            "country": data.get(self.targets["country"]),
        }

    def __get_events(self, data: dict) -> dict:
        return {
            "match_id": data.get(self.targets["match_id"]),
            "home_scores": data.get(self.targets["home_scores"]),
            "away_scores": data.get(self.targets["away_scores"]),
            "kickoff": data.get(self.targets["kickoff"]),
            "status": data.get(self.targets["status"]),
        }

    def __get_team_info(self, data: dict) -> dict:
        resp = {}
        t1 = (data.get(self.mappers["T1"]) or [{}])[0]
        t2 = (data.get(self.mappers["T2"]) or [{}])[0]
        resp["home"] = t1.get(self.targets["home"])
        resp["home_id"] = t1.get(self.targets["home_id"])
        resp["away"] = t2.get(self.targets["away"])
        resp["away_id"] = t2.get(self.targets["away_id"])
        return resp

    @Utils.error_handler([])
    def main(self, max: int = 1000, filters: dict = None, output: str = None, format: str = "json"):
        filters = filters or {}
        response = []
        for x, entry in enumerate(self.data.get(self.mappers["Stages"], []), start=1):
            event = (entry.get(self.mappers["Events"]) or [{}])[0]
            resp = {}
            resp.update(self.__get_intro(entry))
            resp.update(self.__get_events(event))
            resp.update(self.__get_team_info(event))
            response.append(resp)
            if x >= max:
                break
        if filters or format != "json":
            Utils.chosen_output = output or Utils.chosen_output
            Utils.chosen_format = format
            return Utils.filter(response, **filters)
        return response


class Livescore:
    def __init__(self, date=now.day, month=now.month, year=now.year, country_code="KE", timeout=20):
        self.timeout = timeout
        self.country_code = country_code
        self.base_url = "https://prod-public-api.livescore.com/v1/api/app"
        self.url = f"{self.base_url}/date/soccer/{year}{str(month).zfill(2)}{str(date).zfill(2)}/3?MD=1&countryCode={country_code}"
        self.session = requests.Session()

    def __str__(self):
        return self.url

    def __call__(self, *args, **kwargs):
        return self.matches(*args, **kwargs)

    def _get(self, url, headers=None):
        reqs = self.session.get(url, timeout=self.timeout, headers=headers or DEFAULT_HEADERS)
        reqs.raise_for_status()
        ctype = reqs.headers.get("Content-Type", "")
        if "application/json" in ctype:
            return reqs.json()
        return reqs.text

    @Utils.error_handler([])
    def matches(self, max: int = 1000, filters: dict = None, output: str = None, format: str = "json", raw: bool = False, headers: dict = None):
        logging.info(f"Fetching matches from livescore with url - {self.url}")
        raw_content = self._get(self.url, headers=headers)
        if raw:
            return raw_content
        return JsonFormatter(data=raw_content).main(max, filters or {}, output, format)

    @Utils.error_handler({})
    def raw_match_data(self, match_id: str, headers: dict = None):
        url = f"{self.base_url}/match/detail?Eid={match_id}&countryCode={self.country_code}"
        return self._get(url, headers=headers)

    @Utils.error_handler("")
    def fetch_tv_guide_html(self):
        return self._get("https://www.livescore.com/en/tv-guide/football-on-tv/", headers=DEFAULT_HEADERS)
