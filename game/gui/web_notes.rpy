# Web adaptation notes
# Ren'Py web builds use browser storage for saves. Do not add local filesystem reads/writes.

init python:
    def chuimuo_web_storage_note():
        return "Web build uses browser storage through Ren'Py web runtime."
