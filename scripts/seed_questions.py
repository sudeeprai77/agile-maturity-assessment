from services.repository import execute

def add_question(sub_area_id, question, options):
    execute(
        "INSERT INTO questions (sub_area_id, question, option_type) VALUES (?, ?, 'SCALE_1_5')",
        (sub_area_id, question)
    )

    qid = execute("SELECT last_insert_rowid()")

    for level, text in options.items():
        execute(
            """
            INSERT INTO question_options (question_id, level, description)
            VALUES (?, ?, ?)
            """,
            (qid, level, text)
        )
