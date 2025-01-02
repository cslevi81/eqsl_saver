""" Save QSLs from eqsl.cc Archive directory """

import os
import re
import sys
import shutil
import time
import getpass
import requests
from bs4 import BeautifulSoup

MAIN_URL = "https://www.eqsl.cc/qslcard/"
URLS = {
    "LOGIN": MAIN_URL + "Login.cfm",
    "LOGIN_FORM": MAIN_URL + "LoginFinish.cfm",
    "COOKIETEST": MAIN_URL + "CookieTest.cfm?sw=1280&sh=1024",
    "QSLLIST": MAIN_URL + "Inbox.cfm?Archive=1&Reject=0"
}
if len(sys.argv) != 2:
    if sys.platform == "win32":
        print("Usage: python eqsl_saver.py username")
    elif sys.platform == "linux":
        print("Usage: python3 eqsl_saver.py username")
    sys.exit()

pw = getpass.getpass()
LOGIN_FIELDS = {
    "Callsign": sys.argv[1],
    "EnteredPassword": pw,
    "ZeroType": "Slash"
}

if not os.path.exists("cards"):
    print("Create directory")
    os.makedirs("cards")

req = requests.Session()
print("Load login page...", end=" ")
login_resp = req.get(URLS[
    "LOGIN"],
    timeout=100
)
if login_resp.status_code == 200:
    print("...success!")
    print("Wait 1 second...")
    time.sleep(1)
    print("Send login datas...", end=" ")
    login_form_resp = req.post(
        URLS["LOGIN_FORM"],
        data=LOGIN_FIELDS,
        timeout=100
    )
    if login_form_resp.status_code == 200:
        print("...success!")
        print("Wait 3 seconds...")
        time.sleep(3)
        print("Load cookietest page...", end=" ")
        cookietest_resp = req.get(
            URLS["COOKIETEST"],
            timeout=100
        )
        if cookietest_resp.status_code == 200:
            print("...success!")
            print("Wait 1 second...")
            time.sleep(1)
            print("Load archive page...", end=" ")
            archive_resp = req.get(
                URLS["QSLLIST"],
                timeout=100
            )
            if archive_resp.status_code == 200:
                print("...success!")
                archive_soup = BeautifulSoup(
                    archive_resp.text,
                    'html.parser'
                )
                table_rows = archive_soup.find(id="MainForm").find("table").find_all("tr")
                rownum = len(table_rows)
                for i in range(2, rownum-1):
                    display_eqsl_cols = table_rows[i].find_all("td")
                    display_eqsl_href = display_eqsl_cols[0].find("a")["href"]
                    display_eqsl_callsign = display_eqsl_cols[1].find("a").text
                    display_eqsl_datetime = display_eqsl_cols[2].contents
                    display_eqsl_url = MAIN_URL + re.sub(
                        r"Javascript:popupPrintPage\('(.[^']*)'.*",
                        r"\1",
                        display_eqsl_href
                    )
                    fname = display_eqsl_callsign + "_"
                    fname += display_eqsl_datetime[0].strip() + "_"
                    fname += display_eqsl_datetime[2].strip().replace(":", "-")
                    fname += ".jpg"
                    if os.path.isfile(
                        os.path.join("cards", fname)
                    ):
                        print(
                            "#" + str(i - 1) + ": " +
                            "eQSL card page from " +
                            display_eqsl_callsign +
                            " QSO at " +
                            display_eqsl_datetime[0].strip() +
                            " " +
                            display_eqsl_datetime[2].strip() +
                            " exists - omit."
                        )
                    else:
                        print("Wait 10 seconds...")
                        time.sleep(10)
                        print(
                            "#" + str(i - 1) + ": " +
                            "Load eQSL card page from " +
                            display_eqsl_callsign +
                            " QSO at " +
                            display_eqsl_datetime[0].strip() +
                            " " +
                            display_eqsl_datetime[2].strip() +
                            "...",
                            end=""
                        )
                        display_eqsl_resp = req.get(
                            display_eqsl_url,
                            timeout=100
                        )
                        if display_eqsl_resp.status_code == 200:
                            print("...success!")
                            display_eqsl_img_soup = BeautifulSoup(
                                display_eqsl_resp.text,
                                'html.parser'
                            )
                            try:
                                display_eqsl_img_src = display_eqsl_img_soup.find("img")["src"]
                            except TypeError:
                                print("ERROR: Image not found in QSL!")
                            else:
                                print("Wait 3 seconds...")
                                time.sleep(3)
                                print(
                                    "#" + str(i - 1) + ": " +
                                    "Save image...",
                                    end=" "
                                )
                                display_eqsl_img_resp = requests.get(
                                    "https://www.eqsl.cc/" + display_eqsl_img_src,
                                    timeout=100,
                                    stream=True
                                )
                                if display_eqsl_img_resp.status_code == 200:
                                    print("...success!")
                                    with open(
                                        os.path.join("cards", fname),
                                        'wb'
                                    ) as f:
                                        display_eqsl_img_resp.raw.decode_content = True
                                        shutil.copyfileobj(display_eqsl_img_resp.raw, f)
            else:
                print("...archive ERROR")
        else:
            print("...cookietest ERROR")
    else:
        print("...login Form ERROR")
else:
    print("...login page ERROR")
