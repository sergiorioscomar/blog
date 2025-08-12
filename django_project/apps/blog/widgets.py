from django_summernote.widgets import SummernoteWidget

class SimpleSummernoteWidget(SummernoteWidget):
    def summernote_settings(self):
        return {
            'width': '100%',
            'height': '200px',
            'toolbar': [
                ['font', ['bold', 'italic']],
                ['para', ['ul', 'ol']],
            ],
            'lang': 'es-ES',
        }