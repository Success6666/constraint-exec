def accept_upload(filename):
    return not filename.lower().endswith((".exe", ".sh"))
