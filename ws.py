import requests;
from bs4 import BeautifulSoup;

# Scrape the web for course codes for each subject

subjects_avail = ['CS', 'MATH', 'AFM', 'AHS', 'AMATH', 'ANTH', 'APPLS', 'ARABIC', 'ARBUS'];
course_codes = {};
base_subject_url = 'https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1221&subject=';
subject_urls = [];

def subject_url_generator(subjects):
        for s in subjects:
                new_url = base_subject_url + s;
                subject_urls.append(new_url);


# Scrape content from general course webpages on classes.uwaterloo.ca
def url_to_text(url):
    page = requests.get(url).text;
    soup = BeautifulSoup(page, "lxml");
    text = [x.text for x in soup.find_all('td')];
    return text;

subject_url_generator(subjects_avail);
general_table_data = [url_to_text(x) for x in subject_urls];

#sort through data and find all course codes:

for index1, course in enumerate(general_table_data):
        for index2, item in enumerate(general_table_data[index1]):
                len_of_items = len(general_table_data[index1]);
                if (subjects_avail[index1] == item.strip()) and (len_of_items > index2 + 1) :
                        if subjects_avail[index1] in course_codes:
                                course_codes[subjects_avail[index1]].append(int(general_table_data[index1][index2+1][0:3]));
                        else:
                                course_codes.update({subjects_avail[index1] : [int(general_table_data[index1][index2+1][0:3])]});


# generate urls to specific course pages on classes.uwaterloo.ca to view specific sections, times, profs

urls = [];
base_url = 'https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1221&subject=&cournum='

def course_url_generator(subject):
        for code in course_codes.get(subject):
                new_url = base_url[:94] + subject + base_url[94:] + str(code);
                urls.append(new_url);


for i in subjects_avail:
        course_url_generator(i);

# Scrape content from specific course pages on classes.uwaterloo.ca (instead of uwflow due to authentication barrier)

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
        while (length > prof_index) and (table_data[enum][7+sec_index][0:3] == "LEC") :
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
        while (length > time_index) and (table_data[enum][7+sec_index][0:3] == "TUT") :
                tutorial_data.append(table_data[enum][7+sec_index].strip());
                sec_index += 12;
                tutorial_data.append(table_data[enum][7+time_index].strip());
                time_index += 12;

        alldata.update({classname: [lecture_data, tutorial_data]});