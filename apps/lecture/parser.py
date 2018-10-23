from openpyxl import load_workbook

from .models import Lecture, LectureTime, Department


def parse_lecture_data():
    """
    Parse the lecture.xlsx file and create a lecture database.
    """
    wb = load_workbook('lectures.xlsx', read_only=True)
    ws = wb['강의시간표(schedule)']

    first_row = False
    for row in ws.rows:
        # Skip the first row
        if not first_row:
            first_row = True
            continue

        title = row[4].value            # column E
        uuid = row[2].value             # column C
        division = row[3].value         # column D
        grade = int(row[7].value)       # column H
        point = float(row[8].value)     # column I

        # column F
        type = Lecture.LECTURE_TYPE.get(row[5].value)

        # column G
        field = Lecture.FIELD_TYPE.get(row[6].value)

        # column S
        language = Lecture.LANGUAGE_TYPE.get(row[18].value)

        # column B
        department, created = Department.objects.get_or_create(title=row[1].value)

        # column O
        origin_dept, created = Department.objects.get_or_create(title=row[14].value)

        classroom = row[12].value       # column M
        professor = row[13].value       # column N

        # Create a corresponding object for an input.
        lecture = Lecture.objects.create(
            title=title, uuid=uuid, division=division, grade=grade, point=point,
            type=type, field=field, language=language,
            department=department, origin_department=origin_dept,
            classroom=classroom, professor=professor,
        )

        # column L
        rawtimes = row[11].value

        # if value is None, skip the current row
        if rawtimes is None:
            continue

        # split rawtime with comma
        rawtimes = rawtimes.split(',')
        for rawtime in rawtimes:
            rawtime = rawtime.split()
            days_cache = []
            for token in rawtime:
                # add all days before timerange into days_cache
                if token in LectureTime.TIME_DAYS:
                    days_cache.append(LectureTime.TIME_DAYS[token])
                # create time range with days
                elif len(token) > 2:
                    times = token.split('~')
                    for days in days_cache:
                        LectureTime.objects.get_or_create(
                            lecture=lecture, start_time=times[0], end_time=times[1], day=days)
                    days_cache.clear()
