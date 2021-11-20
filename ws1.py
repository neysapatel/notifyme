import requests;
from bs4 import BeautifulSoup;

# Scrape content from classes.uwaterloo.ca (instead of uwflow.ca due to authentication barrier)

def url_to_text(url):
    page = requests.get(url).text;
    soup = BeautifulSoup(page, "lxml");
    text = [x.text for x in soup.find_all('td')];
    return text;

urls = ['https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1221&subject=CS&cournum=241',
        'https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1221&subject=CS&cournum=240',
        'https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1221&subject=CS&cournum=245',
        'https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1221&subject=CS&cournum=246']

table_data = [url_to_text(x) for x in urls];


# Clean and filter data, place in dictionary

alldata = dict();

for enum, data in enumerate(table_data):
        classname = data[0].strip() + data[1];
        sec_index = 1;
        time_index = 10;
        prof_index = 12;
        length = len(table_data[enum][7:]);

        lecture_data = [];
        while (table_data[enum][7+sec_index][0:3] == "LEC") and (length > prof_index) :
                lecture_data.append(table_data[enum][7+sec_index].strip());
                sec_index += 13;
                lecture_data.append(table_data[enum][7+time_index].strip());
                time_index += 13;
                lecture_data.append(table_data[enum][7+prof_index].strip());
                prof_index += 13;

                # filters out "Reserved: ... " messages

                if table_data[enum][7+sec_index][0:3] not in ('LEC', 'TUT', 'LAB', 'TST') :
                        sec_index += 7;
                        time_index += 7;
                        prof_index += 7;


        tutorial_data = [];
        while (table_data[enum][7+sec_index][0:3] == "TUT") and (length > time_index) :
                tutorial_data.append(table_data[enum][7+sec_index].strip());
                sec_index += 12;
                tutorial_data.append(table_data[enum][7+time_index].strip());
                time_index += 12;

        alldata.update({classname: [lecture_data, tutorial_data]});

