

def test_email(email):
    return True if email else False


def test_spreadsheet_id(spreadsheet_id: str):
    return spreadsheet_id if spreadsheet_id.lower().strip() != 'нет' else None
