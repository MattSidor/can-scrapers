import pandas as pd
import lxml.html
import requests

# import us

# from can_tools.scrapers import CMU

# from can_tools.scrapers.official.base import StateDashboard


class MichiganBase:

    source = "https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html"

    def get_excel_file(self, filename: str):
        """
        locate most recent data export, download excel file
        Returns
        -------
        xl: requests.models.Response
            An html response object containing the downloaded data
        """

        # get today's date for finding most recent file
        date = pd.to_datetime(pd.Timestamp.now())

        # query MI coronavirus webpage
        res = requests.get(self.source)
        if not res.ok:
            raise ValueError("Could not fetch source of MI page")

        # find COVID data download links for specified date
        tree = lxml.html.fromstring(res.content)
        xp = "//a[contains(@href,'{date:%Y-%m-%d}')]"
        links = tree.xpath(xp.format(date=date))

        if len(links) == 0:
            raise ValueError("No links returned for date: {date} on MI page")

        # search download links for link matching filename parameter
        xl_src = ""
        for link in links:
            if filename in link.attrib["href"]:
                xl_src = link.attrib["href"]
                break

        if xl_src == "":
            raise ValueError(
                "No links returned for filename parameter: {filename} on MI page"
            )

        # add domain name to download link if necessary
        if xl_src.startswith("https"):
            pass
        elif xl_src.startswith("/"):
            xl_src = "https://www.michigan.gov" + xl_src
        else:
            raise ValueError("Could not parse download link from MI page")

        print(xl_src)

        # download file from selected link
        xl = requests.get(xl_src)
        if not xl.ok:
            raise ValueError("Could not fetch download file from MI page")

        return xl  # return request response

    # def normalize(self, data):
    # df = self.arcgis_jsons_to_df(data)
    # df.columns = [x.lower() for x in list(df)]
    # df["location"] = (self.state_fips * 1000) + df["county"].astype(int)

    # # 12025 is the OLD (retired in 1997) fips code for Date county. It is now known
    # # as Miami-Dade county with fips code 12086
    # df.loc[:, "location"] = df["location"].replace(12025, 12086)

    # crename = {
    #     "casesall": CMU(category="cases", measurement="cumulative", unit="people"),
    #     "deaths": CMU(category="deaths", measurement="cumulative", unit="people"),
    #     "newpos": CMU(
    #         category="unspecified_tests_positive",
    #         measurement="new",
    #         unit="test_encounters",
    #     ),
    #     "newneg": CMU(
    #         category="unspecified_tests_negative",
    #         measurement="new",
    #         unit="test_encounters",
    #     ),
    #     "newtested": CMU(
    #         category="unspecified_tests_total",
    #         measurement="new",
    #         unit="test_encounters",
    #     ),
    # }
    # out = (
    #     df.melt(id_vars=["location"], value_vars=crename.keys())
    #     .assign(
    #         dt=self._retrieve_dt("US/Eastern"), vintage=self._retrieve_vintage()
    #     )
    #     .query("location not in (12998, 12999)")
    #     .dropna()
    # )
    # out.loc[:, "value"] = pd.to_numeric(out["value"])

    # # Extract category information and add other variable context
    # out = self.extract_CMU(out, crename)

    # cols_to_keep = [
    #     "vintage",
    #     "dt",
    #     "location",
    #     "category",
    #     "measurement",
    #     "unit",
    #     "age",
    #     "race",
    #     "ethnicity",
    #     "sex",
    #     "value",
    # ]

    # return out.loc[:, cols_to_keep]


# class MichiganStateDemographics(StateDashboard):

mi = MichiganBase()

test = mi.get_excel_file("Cases_and_Deaths_by_County")

print(test)