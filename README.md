# APRA Regulatory Landscape

## Introduction

One way to learn about APRA reagulatory landscape is to look at the list of [APRA regulted industries](https://www.apra.gov.au/industries) and browse related Prudential and Reporting Standards pages (for example, [Prudential and Reporting Standards for Authorised deposit-taking institutions](https://www.apra.gov.au/industries/1/standards)). Summaries are available for some industries, such as this [Authorised deposit-taking institutions: guide for directors](https://www.apra.gov.au/information-paper-authorised-deposit-taking-institutions-guide-for-directors) information paper, but for others you'd need to build it yourself.

## Scraper

This is a simple BeautifulSoup-based scraper that creates a single CSV file with the following columns:

| Column      | Example                                |
| ----------- | -------------------------------------- |
| Industry    | Authorised deposit-taking institutions |
| Section     | Governance                             |
| Series      | 310                                    |
| Standard    | Audit and Related Matters              |
| Status      | In Force                               |
| Status Date |                                        |
| Type        | CPS, CPG                               |
| Title       | APS 310 Audit and related matters      |
| Description |                                        |
| Link        |                                        |

## Attribution and Disclaimer

All material on the [Australian Prudential Regulation Authority (APRA)](https://www.apra.gov.au/) website is provided under [Creative Commons Attribution 3.0 Australia Licence (CCBY 3.0)](www.creativecommons.org/licenses/by/3.0/au/).

APRA do not endorse this work or its author.