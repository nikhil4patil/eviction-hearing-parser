import pytest

import hearing


class TestSearchFilingsPage:
    def test_get_filings_numbers(self):
        soup = hearing.get_test_filings_search_page()
        filings, need_splitting = hearing.get_filing_case_nums(soup)
        assert "J1-CV-20-001773" in filings
        assert need_splitting is False

    def test_split_date_range(self):
        afterdate = "1-1-2020"
        beforedate = "1-20-2020"
        end_first, start_second = hearing.split_date_range(afterdate, beforedate)
        assert end_first == "1-10-2020"
        assert start_second == "1-11-2020"


class TestSearchPage:
    @pytest.mark.parametrize(
        "index, expected",
        [(0, "Final Status"), (1, "Final Status"), (2, "Trial/Hearing Set"),],
    )
    def test_get_case_status(self, index, expected):
        soup = hearing.get_test_search_page(index)
        status, type = hearing.get_status_and_type(soup)
        assert expected in status

    @pytest.mark.parametrize(
        "index, expected",
        [
            (
                0,
                "https://odysseypa.traviscountytx.gov/JPPublicAccess/CaseDetail.aspx?CaseID=2286743",
            ),
            (
                1,
                "https://odysseypa.traviscountytx.gov/JPPublicAccess/CaseDetail.aspx?CaseID=2286703",
            ),
            (
                2,
                "https://odysseypa.traviscountytx.gov/JPPublicAccess/CaseDetail.aspx?CaseID=2270305",
            ),
        ],
    )
    def test_get_url_to_register_of_actions(self, index, expected):
        soup = hearing.get_test_search_page(index)
        url = hearing.get_register_url(soup)
        assert expected == url
