class ChapterInfo(object):
    def __init__(self, manga_name, chapter_title, chapter_num, href):
        self.manga_name = manga_name
        self.chapter_title = chapter_title
        self.chapter_num = chapter_num
        self.href = href

    def __str__(self):
        return self.href + self.chapter_title + self.chapter_num

class UpdateInfo(object):
    def __init__(self, manga_name, new_chapters):
        self.manga_name = manga_name
        self.new_chapters = new_chapters

    def __str__(self):
        info_str = self.manga_name
        for chapter in self.new_chapters:
            info_str += str(chapter)

        return info_str

    def __html__(self):
        html = ''
        html += '<table border=0>'
        html += '<tr>'
        html += '<td>'
        html += '<b>' + self.manga_name + '</b>'
        for chapter in self.new_chapters:
            html += '<td>'
            html += str(chapter)
            html += '</td>'
        html += '</td>'
        html += '</tr>'
        html += '</table'
        return html
