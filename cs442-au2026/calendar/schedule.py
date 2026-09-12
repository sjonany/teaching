"""
Course schedule data for CS 442. This is the file you edit week to week.

After changing anything here, rebuild the calendar page:

    python3 generate.py

To see every attachment id you can hang files off of:

    python3 generate.py --ids

Nothing in this file renders HTML. generate.py owns that.
"""

import datetime as dt

D = dt.date

# ------------------------------------------------------------- when and where

QUARTER_START = D(2026, 9, 21)   # Monday, week 1
QUARTER_END = D(2026, 12, 11)    # Friday, finals week

MW_TIME = "12:30-2:20pm"
MW_ROOM = "Snohomish 119"
FR_TIME = "12:30-1:20pm"
FR_ROOM = "Online (Zoom)"

HW_DUE_TIME = "11:00pm"

# ------------------------------------------------------------------- lectures

# Week number -> lecture topic. Weeks run Monday-Friday from QUARTER_START.
TOPICS = {
    1: "Divide and conquer",
    2: "Dynamic programming, 1D",
    3: "Dynamic programming, 2D",
    4: "Streaming algorithms, sliding window",
    5: "Greedy algorithms, optimality arguments",
    6: "Midterm recap",
    7: "Graph traversals, reducing problems to graphs",
    8: "Dynamic programming on graphs",
    9: "DP on graphs II, greedy on graphs",
    10: "P vs NP intro",
    11: "P vs NP, final review",
    12: None,  # finals week, no lectures
}

# Weeks whose Friday holds a lecture rather than a mock interview.
FRIDAY_LECTURE_WEEKS = [8, 11]

# ------------------------------------------------------------------- calendar

# Days with no class at all.
NO_CLASS = {
    D(2026, 10, 9): "Non-instructional day",
    D(2026, 10, 30): "Non-instructional day",
    D(2026, 11, 11): "Veterans Day",
    D(2026, 11, 25): "Thanksgiving break",
    D(2026, 11, 26): "Thanksgiving break",
    D(2026, 11, 27): "Thanksgiving break",
}

MIDTERM = D(2026, 10, 28)

# Set by the college's final exam schedule, which keys off the class start time
# and meeting days: a 12:30 MW class examines on the Wednesday of finals week
# in its usual time slot.  https://www.edmonds.edu/calendar/exams/fall.html
FINAL_EXAM = D(2026, 12, 9)
FINAL_EXAM_TIME = MW_TIME
FINAL_EXAM_ROOM = MW_ROOM

# --------------------------------------------------------------------- quizzes

# Quiz number, topic, and the week it is first administered.
# Attempts run Monday and Wednesday of that week, then the following Monday.
# Any attempt landing on a holiday, the midterm, or finals week is dropped
# rather than rescheduled, so a few quizzes end up with 2 attempts. generate.py
# prints which ones every time it runs.
QUIZZES = [
    (1, "Runtime", 1),
    (2, "Divide and conquer", 2),
    (3, "DP 1D", 3),
    (4, "DP 2D", 4),
    (5, "Streaming", 5),
    (6, "Greedy", 6),
    # week 7 has no new quiz
    (7, "Graph traversals", 8),
    (8, "DP on graphs I", 9),
    (9, "DP on graphs II", 10),
    (10, "P vs NP", 11),
]

# ------------------------------------------------------------------- homework

# Homework number, topic, and its week. Each one goes out on that week's Monday
# and is due the following Sunday, so it appears twice on the calendar.
HOMEWORK = [
    (1, "Divide and conquer", 1),
    (2, "DP 1D", 2),
    (3, "DP 2D", 3),
    (4, "Streaming", 4),
    (5, "Greedy", 5),
    # week 6 is midterm week, no homework
    (6, "Graph traversals", 7),
    (7, "DP on graphs I", 8),
    (8, "DP on graphs II", 9),
    (9, "P vs NP", 10),
    # week 11 has no homework
]

# ------------------------------------------------------- mock interviews, etc.

# Weeks whose Friday is a mock interview, in order.
MOCK_WEEKS = [1, 2, 4, 5, 7, 9]

# One-off entries: id -> (date, css class, summary, description).
# Valid classes: lecture, quiz, mock, hw, exam, other, holiday.
EXTRAS = {
    "withdraw": (D(2026, 11, 10), "other", "Last day to withdraw", ""),
}

# ----------------------------------------------------------------- attachments

# Files and links hung off individual calendar items.
#
#   ATTACHMENTS[item_id] = [(link text, target), ...]
#
# A target is either a filename in ../assets/ or a full URL starting with
# http. generate.py fails loudly if a filename does not exist in assets/, so a
# typo can never ship as a broken link.
#
# Item ids, all listed by `python3 generate.py --ids`:
#
#   lec-YYYY-MM-DD   a lecture on that date
#   hw<N>            homework N going out, on Monday -- put handouts here
#   hw<N>-due        the Friday reminder of homework N's Sunday deadline
#   quiz<N>          quiz N (renders on its first attempt)
#   mock<N>          mock interview N
#   midterm, finals  the exams
#   <extras key>     anything in EXTRAS above
#
# Example:
#
#   "lec-2026-09-21": [
#       ("slides", "01-divide-and-conquer.pdf"),
#       ("annotated", "01-divide-and-conquer-ink.pdf"),
#       ("reading", "https://www.algorithmsilluminated.org/"),
#   ],
#
ATTACHMENTS = {
    "lec-2026-09-21": [
        ("slides-intro", "slides-intro.pdf"),
        ("slides-div", "slides-div-conq.pdf"),
    ],
    "hw1": [
        ("handout", "hw1-div.pdf"),
    ],
}
